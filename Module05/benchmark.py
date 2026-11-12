"""Warm, interleave and compare the normalized and denormalized reports."""
import sqlite3
import statistics
import time
from pathlib import Path

DB=Path(__file__).resolve().parent/"normalize.db"
NORMALIZED="""SELECT m.machine_id,m.site,j.technician,SUM(p.part_price) AS cost
FROM job j JOIN machine m ON m.machine_id=j.machine_id
JOIN job_part jp ON jp.job_id=j.job_id
JOIN part p ON p.part_no=jp.part_no
WHERE j.done_on>=date('2026-03-01')
GROUP BY m.machine_id,j.technician"""
DENORMALIZED="""SELECT machine_id,site,technician,SUM(part_price) AS cost
FROM report_jobpart
WHERE done_on>=date('2026-03-01')
GROUP BY machine_id,technician"""


def plan(con,sql):
    return [r[3] for r in con.execute("EXPLAIN QUERY PLAN "+sql)]


def timed(con,sql):
    start=time.perf_counter()
    rows=con.execute(sql).fetchall()
    return (time.perf_counter()-start)*1000,rows


def main():
    if not DB.exists():
        raise SystemExit("Run Module05/build.py first.")
    con=sqlite3.connect(DB)
    # Warm both query paths, discard first timings.
    _,a=timed(con,NORMALIZED)
    _,b=timed(con,DENORMALIZED)
    assert sorted(a)==sorted(b), "The normalized and denormalized queries differ."
    nt,dt=[],[]
    for i in range(5):
        if i % 2 == 0:
            n,_=timed(con,NORMALIZED)
            d,_=timed(con,DENORMALIZED)
        else:
            d,_=timed(con,DENORMALIZED)
            n,_=timed(con,NORMALIZED)
        nt.append(n); dt.append(d)
    print(f"normalized median ms: {statistics.median(nt):.3f}; samples={nt}")
    print(f"denormalized median ms: {statistics.median(dt):.3f}; samples={dt}")
    print(f"normalized/denormalized ratio: {statistics.median(nt)/statistics.median(dt):.2f}x")
    print("normalized plan:")
    print("\n".join(plan(con,NORMALIZED)))
    print("denormalized plan:")
    print("\n".join(plan(con,DENORMALIZED)))
    print("equal output rows:",len(a))
    print("\n--- Report index experiment ---")
    con.execute("DROP INDEX IF EXISTS ix_report_machine")
    no_index_samples=[timed(con,DENORMALIZED)[0] for _ in range(5)]
    no_index=statistics.median(no_index_samples)
    print(f"report query without ix_report_machine median: {no_index:.3f} ms; samples={no_index_samples}")
    print("plan without report index:")
    print("\n".join(plan(con,DENORMALIZED)))
    con.close()


if __name__=="__main__":
    main()
