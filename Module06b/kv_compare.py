"""Compare 50,000 get/set operations using shelve and SQLite."""
import shelve
import sqlite3
import time
from pathlib import Path

HERE=Path(__file__).resolve().parent
N=50_000


def timed(fn):
    start=time.perf_counter()
    fn()
    return time.perf_counter()-start


def main():
    shelf_path=str(HERE/"sessions")
    with shelve.open(shelf_path) as db:
        # Clear previous run so set timings are comparable.
        db.clear()
        shelf_set=timed(lambda:[db.__setitem__(f"session-{i}",f"user-{i%100}:filter=city:{i%4}") for i in range(N)])
        shelf_get=timed(lambda:[db.__getitem__(f"session-{i}") for i in range(N)])
    con=sqlite3.connect(HERE/"sessions.db")
    con.execute("CREATE TABLE IF NOT EXISTS session(k TEXT PRIMARY KEY,v TEXT)")
    con.execute("DELETE FROM session")
    values=((f"session-{i}",f"user-{i%100}:filter=city:{i%4}") for i in range(N))
    sqlite_set=timed(lambda:(con.executemany("INSERT OR REPLACE INTO session(k,v) VALUES(?,?)",values),con.commit()))
    sqlite_get=timed(lambda:[con.execute("SELECT v FROM session WHERE k=?",(f"session-{i}",)).fetchone() for i in range(N)])
    print(f"shelve set={shelf_set:.3f}s get={shelf_get:.3f}s")
    print(f"sqlite set={sqlite_set:.3f}s get={sqlite_get:.3f}s")
    print("SQLite cross-session query:",con.execute(
      "SELECT COUNT(*) FROM session WHERE v LIKE ?",("%filter=city:2",)).fetchone()[0])
    print("SQLite-only capability demonstrated: SQL aggregation/filtering across values without reading every key into application code.")
    con.close()


if __name__=="__main__":
    main()
