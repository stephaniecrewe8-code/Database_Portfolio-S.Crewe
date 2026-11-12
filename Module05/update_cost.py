"""Measure update fan-out and per-table storage for the two designs."""
import sqlite3
import time
from pathlib import Path

DB=Path(__file__).resolve().parent/"normalize.db"


def main():
    if not DB.exists():
        raise SystemExit("Run Module05/build.py first.")
    con=sqlite3.connect(DB)
    machine="cnc-02"
    normalized_rows=con.execute("SELECT COUNT(*) FROM machine WHERE machine_id=?",(machine,)).fetchone()[0]
    report_rows=con.execute("SELECT COUNT(*) FROM report_jobpart WHERE machine_id=?",(machine,)).fetchone()[0]
    print("rows updated in normalized machine table:",normalized_rows)
    print("rows updated in denormalized report table:",report_rows)
    for label,sql in [
        ("3NF machine update","UPDATE machine SET site='Bielefeld' WHERE machine_id=?"),
        ("report table update","UPDATE report_jobpart SET site='Bielefeld' WHERE machine_id=?")
    ]:
        start=time.perf_counter()
        con.execute(sql,(machine,))
        con.commit()
        print(f"{label}: {(time.perf_counter()-start)*1000:.3f} ms")
    try:
        rows=con.execute("""
          SELECT name,SUM(pgsize) AS bytes FROM dbstat
          WHERE name IN ('machine','part','job','job_part','report_jobpart')
          GROUP BY name ORDER BY name
        """).fetchall()
        print("dbstat bytes by object:",rows)
        print("normalized bytes:",sum(x[1] for x in rows if x[0] in {"machine","part","job","job_part"}))
        print("denormalized bytes:",sum(x[1] for x in rows if x[0]=="report_jobpart"))
    except sqlite3.OperationalError as exc:
        print("dbstat unavailable in this SQLite build:",exc)
    con.close()


if __name__=="__main__":
    main()
