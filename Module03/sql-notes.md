##Outputs received after queried

- **Query 1:** `EXPLAIN QUERY PLAN SELECT * FROM maint_job WHERE technician = 'Beier';`
- **RESPONSE:** 
 QUERY PLAN
`--SCAN maint_job

σ technician = 'Beier' (maint_job)
The symbol σ means “select rows that match this condition.


- **Query 2:** EXPLAIN QUERY PLAN SELECT * FROM machine WHERE machine_name = 'cnc-02';
- **Response:**
QUERY PLAN
`--SCAN machine


- **Query 3:** EXPLAIN QUERY PLAN SELECT * FROM maint_job WHERE technician LIKE '%ei%';
- **Response:** 
QUERY PLAN
`--SCAN maint_job

CREATE INDEX ix_job_tech ON maint_job(technician);


Looking at the plan:
QUERY PLAN
|--SCAN ol
|--SEARCH o USING INTEGER PRIMARY KEY (rowid=?)
|--SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
|--SEARCH p USING INTEGER PRIMARY KEY (rowid=?)
|--USE TEMP B-TREE FOR GROUP BY
|--USE TEMP B-TREE FOR count(DISTINCT)
`--USE TEMP B-TREE FOR ORDER BY



The Report:
╭───────────┬───────────┬────────────╮
│   city    │ customers │  revenue   │
╞═══════════╪═══════════╪════════════╡
│ Bielefeld │       500 │ 11242176.0 │
│ Gütersloh │       500 │  8422344.0 │
│ Münster   │       500 │  5493504.0 │
│ Paderborn │       500 │  2815656.0 │
╰───────────┴───────────┴────────────╯

After running the python script, the result were:
normal   : [(1, 'Customer 1')]
injected : [(1, 'Customer 1'), (2, 'Customer 2'), (3, 'Customer 3')] ...
safe     : []