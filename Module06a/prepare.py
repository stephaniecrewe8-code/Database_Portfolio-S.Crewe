"""Stretch Module 05's report table to ten quarters (2,000,000 rows)."""
import csv
import sqlite3
from pathlib import Path

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/"Module05"/"normalize.db"
DB=HERE/"history.db"
CSV=HERE/"report_jobpart.csv"
QUARTERS=10


def main():
    if not SOURCE.exists():
        raise SystemExit("Module05/normalize.db missing; run Module05/build.py first.")
    DB.unlink(missing_ok=True)
    con=sqlite3.connect(DB)
    con.execute("ATTACH DATABASE ? AS m5",(str(SOURCE),))
    con.execute("""CREATE TABLE report_history(
      job_id INTEGER,machine_id TEXT,site TEXT,technician TEXT,
      part_no TEXT,part_price REAL,done_on TEXT)""")
    con.execute(f"""
      WITH RECURSIVE q(k) AS (SELECT 0 UNION ALL SELECT k+1 FROM q WHERE k<{QUARTERS-1})
      INSERT INTO report_history
      SELECT r.job_id+k*1000000,r.machine_id,r.site,r.technician,
             r.part_no,r.part_price,date(r.done_on,'+'||(k*91)||' days')
      FROM m5.report_jobpart r CROSS JOIN q
    """)
    con.commit()
    count,total=con.execute("SELECT COUNT(*),ROUND(SUM(part_price),2) FROM report_history").fetchone()
    with CSV.open("w",newline="",encoding="utf-8") as handle:
        writer=csv.writer(handle)
        writer.writerow(["job_id","machine_id","site","technician","part_no","part_price","done_on"])
        writer.writerows(con.execute("SELECT * FROM m5.report_jobpart"))
    print("history rows:",count)
    print("history SUM(part_price):",total)
    print("base CSV rows:",sum(1 for _ in CSV.open(encoding="utf-8"))-1)
    print("CSV bytes:",CSV.stat().st_size)
    assert count==2_000_000
    con.close()


if __name__=="__main__":
    main()
