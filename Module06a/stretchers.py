"""Module 06a stretchers: JSON join, sorted Parquet statistics and ZSTD."""
import json
from pathlib import Path
import duckdb

HERE=Path(__file__).resolve().parent
PARQUET=HERE/"report_history.parquet"
SORTED=HERE/"report_history_sorted.parquet"
ZSTD=HERE/"report_history_zstd.parquet"
DEVICES=HERE/"devices.json"


def qpath(path):
    return str(path).replace("'","''")


def main():
    if not PARQUET.exists():
        raise SystemExit("Run prepare.py and to_parquet.py first.")
    devices=[
      {"machine_id":"cnc-01","vendor":"Siemens","firmware":"4.2"},
      {"machine_id":"cnc-02","vendor":"Fanuc","firmware":"3.9"},
      {"machine_id":"cnc-03","vendor":"Siemens","firmware":"4.0"}
    ]
    DEVICES.write_text(json.dumps(devices),encoding="utf-8")
    p=qpath(PARQUET);d=qpath(DEVICES);s=qpath(SORTED);z=qpath(ZSTD)
    SORTED.unlink(missing_ok=True)
    ZSTD.unlink(missing_ok=True)
    con=duckdb.connect()
    print("S1 — JSON metadata joined to Parquet:")
    print(con.execute(f"""
      SELECT d.vendor,r.machine_id,ROUND(SUM(r.part_price),2) AS cost
      FROM read_json_auto('{d}') d
      JOIN read_parquet('{p}') r USING(machine_id)
      GROUP BY d.vendor,r.machine_id ORDER BY cost DESC
    """).fetchall())

    print("\nS2 — original Parquet row-group date statistics:")
    print(con.execute(f"""
      SELECT row_group_id,stats_min,stats_max
      FROM parquet_metadata('{p}')
      WHERE path_in_schema='done_on' ORDER BY row_group_id LIMIT 5
    """).fetchall())
    con.execute(f"COPY (SELECT * FROM read_parquet('{p}') ORDER BY done_on) TO '{s}' (FORMAT PARQUET)")
    print("sorted Parquet row-group date statistics:")
    print(con.execute(f"""
      SELECT row_group_id,stats_min,stats_max
      FROM parquet_metadata('{s}')
      WHERE path_in_schema='done_on' ORDER BY row_group_id LIMIT 5
    """).fetchall())

    con.execute(f"COPY (SELECT * FROM read_parquet('{p}')) TO '{z}' (FORMAT PARQUET,COMPRESSION ZSTD)")
    print("\nS3 file sizes:")
    print(f"snappy={PARQUET.stat().st_size} bytes")
    print(f"zstd={ZSTD.stat().st_size} bytes")
    print("ZSTD smaller:",ZSTD.stat().st_size<PARQUET.stat().st_size)
    con.close()


if __name__=="__main__":
    main()
