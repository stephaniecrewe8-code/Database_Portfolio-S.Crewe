"""Show DuckDB EXPLAIN ANALYZE and SQLite EXPLAIN QUERY PLAN for the same query."""
import sqlite3
from pathlib import Path
import duckdb

HERE=Path(__file__).resolve().parent
PQ=HERE/"report_history.parquet"
DB=HERE/"history.db"


def main():
    if not PQ.exists() or not DB.exists():
        raise SystemExit("Run prepare.py and to_parquet.py first.")
    p=str(PQ).replace("'","''")
    query=f"""SELECT machine_id,site,technician,SUM(part_price) AS cost
    FROM read_parquet('{p}') WHERE done_on>='2026-01-01'
    GROUP BY machine_id,site,technician"""
    con=duckdb.connect()
    print("DUCKDB EXPLAIN ANALYZE")
    print(con.execute("EXPLAIN ANALYZE "+query).fetchone()[1])
    con.close()
    sq=sqlite3.connect(DB)
    print("SQLITE EXPLAIN QUERY PLAN")
    for row in sq.execute("""EXPLAIN QUERY PLAN SELECT machine_id,site,technician,
      SUM(part_price) FROM report_history WHERE done_on>='2026-01-01'
      GROUP BY machine_id,site,technician"""):
        print(row)
    sq.close()


if __name__=="__main__":
    main()
