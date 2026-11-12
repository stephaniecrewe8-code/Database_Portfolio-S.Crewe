
# Decision memo to Lea Winter and Yasmin Kaya

Keep job ingestion, transactional changes, and point lookups in SQLite. In the recorded run, 1,000 row-by-row inserts took 1.78 ms in SQLite and 1,127.72 ms in DuckDB; 1,000 point lookups took 2.23 ms and 819.84 ms, respectively. Batched inserts took 0.98 ms in SQLite and 705.48 ms in DuckDB.

Move the broad historical reporting copy to Parquet and query it with DuckDB. On the two-million-row dataset, the dashboard median was 3,270.58 ms in SQLite and 36.47 ms in DuckDB (89.68×); the monthly query was 3,902.31 ms and 78.59 ms (49.65×). The Parquet file occupied 2,325,330 bytes, compared with 112,685,056 bytes for the SQLite history database.

Rebuild the Parquet snapshot after the operational shift closes. Write to a temporary file, check row count and rounded `SUM(part_price)`, then publish it only after those checks pass. Show the last successful refresh time and flag stale reports when the expected refresh window is missed. Two consecutive refresh checks matched at 2,000,000 rows and a sum of 21,000,000.0. These aggregate checks can miss compensating row-level changes, so they are not a cryptographic checksum.

Evidence was generated on 2026-11-12 in a Windows-hosted environment with Python 3.14.9, SQLite 3.53.1, and DuckDB 2.0.0. Rerun on the intended laptop before relying on these machine-specific timings.
