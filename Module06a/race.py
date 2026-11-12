"""Same analytical queries in SQLite and DuckDB; warm and interleave five runs."""
import sqlite3
import statistics
import time
from pathlib import Path
import duckdb

HERE=Path(__file__).resolve().parent
SQLITE=HERE/"history.db"
PARQUET=HERE/"report_history.parquet"
RUNS=5
DASH="""SELECT machine_id,site,technician,SUM(part_price) AS cost
FROM {source} WHERE done_on>='2026-01-01'
GROUP BY machine_id,site,technician"""
MONTH="""SELECT strftime('%Y-%m',done_on) AS month,machine_id,
COUNT(*) AS rows_n,SUM(part_price) AS cost
FROM {source} GROUP BY month,machine_id ORDER BY month,machine_id"""


def ms(fn):
    start=time.perf_counter()
    result=fn()
    return (time.perf_counter()-start)*1000,result


def canonical(rows):
    return sorted(tuple(row[:-1])+(round(float(row[-1]),2),) for row in rows)


def main():
    if not SQLITE.exists() or not PARQUET.exists():
        raise SystemExit("Run prepare.py and to_parquet.py first.")
    sq=sqlite3.connect(SQLITE)
    du=duckdb.connect()
    pq=str(PARQUET).replace("'","''")
    for label,template in (("dashboard",DASH),("monthly",MONTH)):
        qsql=template.format(source="report_history")
        qduck=template.format(source=f"read_parquet('{pq}')")
        _,sr=ms(lambda:sq.execute(qsql).fetchall())
        _,dr=ms(lambda:du.execute(qduck).fetchall())
        assert canonical(sr)==canonical(dr),f"{label}: SQLite and DuckDB aggregate results differ"
        st,dt=[],[]
        for i in range(RUNS):
            # Alternate execution order to reduce systematic order/cache bias.
            if i % 2 == 0:
                a,_=ms(lambda:sq.execute(qsql).fetchall())
                b,_=ms(lambda:du.execute(qduck).fetchall())
            else:
                b,_=ms(lambda:du.execute(qduck).fetchall())
                a,_=ms(lambda:sq.execute(qsql).fetchall())
            st.append(a);dt.append(b)
        sm,dm=statistics.median(st),statistics.median(dt)
        print(f"{label}: SQLite median={sm:.2f} ms {st}")
        print(f"{label}: DuckDB median={dm:.2f} ms {dt}")
        print(f"{label}: SQLite/DuckDB ratio={sm/dm:.2f}x")
    sq.close();du.close()


if __name__=="__main__":
    main()
