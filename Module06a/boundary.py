"""Compare 1,000 point writes/lookups in SQLite and DuckDB."""
import sqlite3
import time
import duckdb

N=1000
ROWS=[(i,f"k{i}",i*1.5) for i in range(N)]


def sqlite_run(batch):
    con=sqlite3.connect(":memory:")
    con.execute("CREATE TABLE s(id INTEGER PRIMARY KEY,k TEXT,v REAL)")
    start=time.perf_counter()
    if batch:
        con.executemany("INSERT INTO s VALUES(?,?,?)",ROWS)
    else:
        for row in ROWS:
            con.execute("INSERT INTO s VALUES(?,?,?)",row)
    con.commit()
    insert=(time.perf_counter()-start)*1000
    start=time.perf_counter()
    for i in range(N):
        con.execute("SELECT v FROM s WHERE id=?",(i,)).fetchone()
    lookup=(time.perf_counter()-start)*1000
    con.close()
    return insert,lookup


def duck_run(batch):
    con=duckdb.connect()
    con.execute("CREATE TABLE s(id INTEGER PRIMARY KEY,k TEXT,v DOUBLE)")
    start=time.perf_counter()
    if batch:
        con.executemany("INSERT INTO s VALUES(?,?,?)",ROWS)
    else:
        for row in ROWS:
            con.execute("INSERT INTO s VALUES(?,?,?)",row)
    insert=(time.perf_counter()-start)*1000
    start=time.perf_counter()
    for i in range(N):
        con.execute("SELECT v FROM s WHERE id=?",[i]).fetchone()
    lookup=(time.perf_counter()-start)*1000
    con.close()
    return insert,lookup


if __name__=="__main__":
    for label,batch in (("row-by-row",False),("executemany",True)):
        si,sl=sqlite_run(batch);di,dl=duck_run(batch)
        print(f"{label}: SQLite insert={si:.2f}ms lookup={sl:.2f}ms")
        print(f"{label}: DuckDB insert={di:.2f}ms lookup={dl:.2f}ms")
