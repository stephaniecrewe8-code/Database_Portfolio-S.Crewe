"""Expand the 200k CSV to a 2M-row Parquet file with DuckDB."""
from pathlib import Path
import sqlite3
import duckdb

HERE=Path(__file__).resolve().parent
CSV=HERE/"report_jobpart.csv"
PARQUET=HERE/"report_history.parquet"
SQLITE=HERE/"history.db"


def sql_path(path):
    return str(path).replace("'","''")


def main():
    if not CSV.exists() or not SQLITE.exists():
        raise SystemExit("Run Module06a/prepare.py first.")
    PARQUET.unlink(missing_ok=True)
    con=duckdb.connect()
    source=sql_path(CSV)
    target=sql_path(PARQUET)
    con.execute(f"""
      COPY (
        SELECT r.job_id+k*1000000 AS job_id,r.machine_id,r.site,r.technician,
               r.part_no,r.part_price,
               CAST(r.done_on AS DATE)+CAST(k*91 AS INTEGER) AS done_on
        FROM read_csv_auto('{source}',header=true) r
        CROSS JOIN range(0,10) t(k)
      ) TO '{target}' (FORMAT PARQUET,COMPRESSION SNAPPY)
    """)
    rows,total=con.execute(
      f"SELECT COUNT(*),ROUND(SUM(part_price),2) FROM read_parquet('{target}')"
    ).fetchone()
    print("Parquet rows:",rows)
    print("Parquet SUM(part_price):",total)
    print("Parquet bytes:",PARQUET.stat().st_size)
    print("Parquet MB:",round(PARQUET.stat().st_size/1e6,3))
    with sqlite3.connect(SQLITE) as sq:
        expected=sq.execute("SELECT COUNT(*),ROUND(SUM(part_price),2) FROM report_history").fetchone()
    print("SQLite rows and sum:",expected)
    print("SQLite database bytes:",SQLITE.stat().st_size)
    print("SQLite database MB:",round(SQLITE.stat().st_size/1e6,3))
    assert rows==expected[0] and round(float(total),2)==round(float(expected[1]),2)
    con.close()


if __name__=="__main__":
    main()
