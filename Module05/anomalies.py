"""Reproduce update, insert and delete anomalies in the five-row flat relation."""
import sqlite3

ROWS=[
 (1,"cnc-01","Gütersloh","tech-0","P-0001","6.00"),
 (1,"cnc-01","Gütersloh","tech-0","P-0002","7.00"),
 (2,"cnc-02","Gütersloh","tech-1","P-0001","6.00"),
 (2,"cnc-02","Gütersloh","tech-1","P-0003","8.50"),
 (3,"cnc-01","Gütersloh","tech-0","P-0003","8.50"),
]

def reset(con):
    con.execute("DROP TABLE IF EXISTS flat5")
    con.execute("""CREATE TABLE flat5(job_id INTEGER,machine_id TEXT,site TEXT,technician TEXT,part_no TEXT,part_price TEXT)""")
    con.executemany("INSERT INTO flat5 VALUES(?,?,?,?,?,?)",ROWS)

def main():
    con=sqlite3.connect(":memory:")
    reset(con)
    print("INITIAL:",con.execute("SELECT * FROM flat5 ORDER BY job_id,part_no").fetchall())
    print("\nUPDATE ANOMALY")
    changed=con.execute("UPDATE flat5 SET site='Bielefeld' WHERE machine_id='cnc-01'").rowcount
    print("rows changed:",changed)
    print("cnc-01 facts:",con.execute("SELECT DISTINCT machine_id,site FROM flat5 WHERE machine_id='cnc-01'").fetchall())
    reset(con)
    print("\nINSERT ANOMALY")
    con.execute("INSERT INTO flat5 VALUES(NULL,NULL,NULL,NULL,'P-9999','99.00')")
    print("part-only row:",con.execute("SELECT * FROM flat5 WHERE part_no='P-9999'").fetchall())
    reset(con)
    print("\nDELETE ANOMALY")
    con.execute("DELETE FROM flat5 WHERE job_id=1 AND part_no='P-0002'")
    print("remaining P-0002 rows:",con.execute("SELECT * FROM flat5 WHERE part_no='P-0002'").fetchall())
    print("The part fact vanished with its only job occurrence.")
    con.close()

if __name__=="__main__":
    main()
