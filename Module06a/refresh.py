"""Rebuild Parquet from history.db; --check verifies rows and sum."""
import argparse
import csv
import sqlite3
import time
from pathlib import Path
import duckdb

HERE=Path(__file__).resolve().parent
DB=HERE/"history.db"
PARQUET=HERE/"report_history.parquet"
CSV=HERE/"refresh_source.csv"


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--check",action="store_true")
    args=parser.parse_args()
    if not DB.exists():
        raise SystemExit("history.db missing; run prepare.py first.")
    start=time.perf_counter()
    with sqlite3.connect(DB) as sq:
        expected=sq.execute("SELECT COUNT(*),ROUND(SUM(part_price),2) FROM report_history").fetchone()
        if not args.check:
            with CSV.open("w",newline="",encoding="utf-8") as f:
                writer=csv.writer(f)
                writer.writerow(["job_id","machine_id","site","technician","part_no","part_price","done_on"])
                writer.writerows(sq.execute("SELECT * FROM report_history"))
    if not args.check:
        temp=HERE/"report_history.tmp.parquet"
        temp.unlink(missing_ok=True)
        path=str(CSV).replace("'","''")
        target=str(temp).replace("'","''")
        con=duckdb.connect()
        con.execute(f"COPY (SELECT * FROM read_csv_auto('{path}',header=true)) TO '{target}' (FORMAT PARQUET,COMPRESSION SNAPPY)")
        con.close()
        temp.replace(PARQUET)
        CSV.unlink(missing_ok=True)
    if not PARQUET.exists():
        raise SystemExit("Parquet missing; run refresh.py without --check first.")
    pq=str(PARQUET).replace("'","''")
    con=duckdb.connect()
    actual=con.execute(f"SELECT COUNT(*),ROUND(SUM(part_price),2) FROM read_parquet('{pq}')").fetchone()
    con.close()
    elapsed=(time.perf_counter()-start)*1000
    print("SQLite rows,sum:",expected)
    print("Parquet rows,sum:",actual)
    print(f"rows={actual[0]} checksum_sum={actual[1]} parquet_bytes={PARQUET.stat().st_size} elapsed_ms={elapsed:.2f}")
    matches=actual[0]==expected[0] and round(float(actual[1]),2)==round(float(expected[1]),2)
    print("row-count and rounded-sum check:", "PASS" if matches else "FAIL")
    if not matches:
        raise SystemExit(1)


if __name__=="__main__":
    main()
