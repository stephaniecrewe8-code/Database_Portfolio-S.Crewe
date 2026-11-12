"""JSON metadata in SQLite: validate, query, expand and index a JSON path."""
import sqlite3
from pathlib import Path

HERE=Path(__file__).resolve().parent
DB=HERE/"polyglot.db"


def main():
    DB.unlink(missing_ok=True)
    con=sqlite3.connect(DB)
    con.executescript("""
    CREATE TABLE device(
      device_id INTEGER PRIMARY KEY,
      name TEXT NOT NULL,
      meta TEXT NOT NULL CHECK(json_valid(meta))
    ) STRICT;
    INSERT INTO device(name,meta) VALUES
      ('cnc-01','{"vendor":"Siemens","firmware":"4.2","calibrated":"2026-01-10"}'),
      ('cnc-02','{"vendor":"Fanuc","firmware":"3.9"}'),
      ('molder-07','{"vendor":"Arburg","firmware":"8.1","calibrated":"2025-11-02","nozzle_mm":2.5}');
    """)
    print("SQLite version:",sqlite3.sqlite_version)
    print("json_extract:",con.execute("SELECT name,json_extract(meta,'$.vendor') FROM device ORDER BY device_id").fetchall())
    print("operator ->>:",con.execute("SELECT name,meta ->> '$.firmware' FROM device ORDER BY device_id").fetchall())
    print("json_each:",con.execute(
      "SELECT d.name,j.key,j.value FROM device d,json_each(d.meta) j WHERE d.name=? ORDER BY j.key",
      ("cnc-01",)).fetchall())
    try:
        con.execute("INSERT INTO device(name,meta) VALUES(?,?)",("broken","not-json"))
    except sqlite3.IntegrityError as exc:
        print("invalid JSON rejected:",exc)
    con.execute("CREATE INDEX ix_device_vendor ON device(json_extract(meta,'$.vendor'))")
    for label,sql in [
      ("indexed expression","SELECT name FROM device WHERE json_extract(meta,'$.vendor')='Fanuc'"),
      ("different ->> expression","SELECT name FROM device WHERE meta ->> '$.vendor'='Fanuc'")
    ]:
        print(label,"result:",con.execute(sql).fetchall())
        print(label,"plan:",con.execute("EXPLAIN QUERY PLAN "+sql).fetchall())
    con.close()


if __name__=="__main__":
    main()
