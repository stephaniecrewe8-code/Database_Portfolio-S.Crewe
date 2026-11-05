import csv
import sqlite3
from pathlib import Path

folder = Path(__file__).parent
database = folder / "edge.db"
csv_file = folder / "readings.csv"

connection = sqlite3.connect(database)
connection.execute("PRAGMA foreign_keys = ON")

with csv_file.open(newline="", encoding="utf-8") as file:
    rows = [
        (
            int(row["sensor_id"]),
            row["ts"],
            float(row["value"]),
            int(row["interval_s"]),
        )
        for row in csv.DictReader(file)
    ]

connection.executemany(
    """
    INSERT INTO reading(sensor_id, ts, value, interval_s)
    VALUES (?, ?, ?, ?)
    ON CONFLICT(sensor_id, ts)
    DO UPDATE SET
        value = excluded.value,
        interval_s = excluded.interval_s
    """,
    rows,
)
connection.commit()

print(f"Processed {len(rows)} readings from {csv_file.name}")
connection.close()