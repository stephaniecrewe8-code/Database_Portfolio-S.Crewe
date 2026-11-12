##Observations 

When running the following in the terminal:
```SQL
CREATE TABLE t(sensor_id INTEGER, metric TEXT, value REAL);
INSERT INTO t VALUES (1, 'temp_c', 9000);
INSERT INTO t VALUES (1, 'temp_c', 'hot');
INSERT INTO t VALUES (2, 'bogus', -500);
SELECT * FROM t;
```

The output was given:
```
╭───────────┬────────┬────────╮
│ sensor_id │ metric │ value  │
╞═══════════╪════════╪════════╡
│         1 │ temp_c │ 9000.0 │
│         1 │ temp_c │ hot    │
│         2 │ bogus  │ -500.0 │
╰───────────┴────────┴────────╯
```
All three rows should be accepted. That’s the problem this module addresses: without rules, the database can store values that are impossible or nonsensical.



Impossible value, rejected by CHECK:
sqlite3 .\Module04\edge.db "INSERT INTO reading(sensor_id, ts, value, interval_s) VALUES (1, '2026-03-01 08:00:01', 9000, 1);"

RESULT:
Error in 2nd command line argument: CHECK constraint failed: value >= -273.15 AND value <= 5000



Text where a real number is required, rejected by STRICT:
sqlite3 .\Module04\edge.db "INSERT INTO reading(sensor_id, ts, value, interval_s) VALUES (1, '2026-03-01 08:00:02', 'hot', 1);"

RESULT:
Error in 2nd command line argument: cannot store TEXT value in REAL column reading.value



A sensor ID that doesn't exist, rejected by FOREIGN KEY:
sqlite3 .\Module04\edge.db "PRAGMA foreign_keys=ON; INSERT INTO reading(sensor_id, ts, value, interval_s) VALUES (99, '2026-03-01 08:00:03', 40, 1);"

RESULT:
Error in 2nd command line argument: FOREIGN KEY constraint failed




A second temperature sensor for the same machine, rejected by UNIQUE:
sqlite3 .\Module04\edge.db "INSERT INTO sensor VALUES (3, 'cnc-01', 'temp_c', 'degC');"

RESULT:
Error in 2nd command line argument: UNIQUE constraint failed: sensor.machine_id, sensor.metric



The error wording can vary slightly:
sqlite3 .\Module04\edge.db "SELECT sensor_id, value, interval_s, energy_j FROM reading;"

RESULT:
╭───────────┬───────┬────────────┬──────────╮
│ sensor_id │ value │ interval_s │ energy_j │
╞═══════════╪═══════╪════════════╪══════════╡
│         1 │  41.5 │          1 │     41.5 │
╰───────────┴───────┴────────────┴──────────╯
For the valid row, energy_j should be 41.5, calculated automatically from 41.5 x 1 .

Result with a corrected value:
╭───────────┬─────────────────────┬───────╮
│ sensor_id │         ts          │ value │
╞═══════════╪═════════════════════╪═══════╡
│         1 │ 2026-03-01 08:00:00 │  41.7 │
╰───────────┴─────────────────────┴───────╯


##UPSERT evidence
When running the python script it stated it processed 3 readings.
The timestamp still shows 3 rows, as followed:
╭──────────╮
│ COUNT(*) │
╞══════════╡
│        3 │
╰──────────╯

The alarm automatically created from the alarm trigger:
╭────────┬─────────┬───────────────────┬─────┬──────────────────╮
│alarm_id│sensor_id│        ts         │value│      reason      │
╞════════╪═════════╪═══════════════════╪═════╪══════════════════╡
│       1│        2│2026-03-01 09:00:00│  2.7│vibration over 2.0│
│        │         │                   │     │mm/s              │
╰────────┴─────────┴───────────────────┴─────┴──────────────────╯
Reading changed:
╭────────┬──────────┬─────────┬─────────┬───────────────────╮
│audit_id│reading_id│old_value│new_value│    changed_at     │
╞════════╪══════════╪═════════╪═════════╪═══════════════════╡
│       1│         5│      2.7│      1.4│2026-11-05 01:25:44│
╰────────┴──────────┴─────────┴─────────┴───────────────────╯

Result for read only access:
╭──────────╮
│ COUNT(*) │
╞══════════╡
│        5 │
╰──────────╯


╭────────────┬─────────┬──────┬───╮
│ machine_id │ metric  │ peak │ n │
╞════════════╪═════════╪══════╪═══╡
│ cnc-01     │ temp_c  │ 42.2 │ 3 │
│ cnc-01     │ vib_rms │  1.8 │ 2 │
╰────────────┴─────────┴──────┴───╯
