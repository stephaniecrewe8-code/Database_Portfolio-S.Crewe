
# Module 06a — DuckDB notes and evidence

Official task: [The Analytical Engine (DuckDB)](https://github.com/iotempire/iotempire-teaching/blob/main/full-classes/hsbi-databases-10d/modules/06a-duckdb-analytical-engine.md).

## Environment

Run date: 2026-11-12. Windows-hosted environment, Python 3.14.9, SQLite 3.53.1, DuckDB 2.0.0. Timings are local to that environment, not claims about another laptop.

## Round 1 — Build the history

`uv run python Module06a/prepare.py` produced:

```text
history rows: 2000000
history SUM(part_price): 21000000.0
base CSV rows: 200000
CSV bytes: 10805002
```

Ten offsets of the 200,000-row source produced the two-million-row history. The synthetic 91-day increments create a controlled timeline, not calendar quarters.

## Round 2 — Convert to Parquet

`uv run python Module06a/to_parquet.py` produced:

```text
Parquet rows: 2000000
Parquet SUM(part_price): 21000000.0
Parquet bytes: 2325330
Parquet MB: 2.325
SQLite rows and sum: (2000000, 21000000.0)
SQLite database bytes: 112685056
SQLite database MB: 112.685
```

Both copies agree on row count and rounded total. They could still differ in individual rows while sharing those two aggregate checks, so this is a useful consistency check rather than a cryptographic checksum. The Parquet file was about 48.5 times smaller than the history database in this run.

## Round 3 — Inspect the plans

`uv run python Module06a/plan.py` ran DuckDB `EXPLAIN ANALYZE` over Parquet and SQLite `EXPLAIN QUERY PLAN` over the history database.

- DuckDB plan: Parquet table scan projected only `machine_id`, `site`, `technician`, and `part_price`; all 2,000,000 rows and 17/17 row groups were scanned. DuckDB reported 47.2 ms total plan time and 181.8 kB data read.
- SQLite plan: `SCAN report_history`, followed by `USE TEMP B-TREE FOR GROUP BY`.

The plan timings are diagnostic output, not the race benchmark's median.

## Round 4 — Race the analytical queries

`uv run python Module06a/race.py` warmed and interleaved five runs:

| Query | SQLite median | DuckDB median | SQLite / DuckDB |
|---|---:|---:|---:|
| Dashboard | 3,270.58 ms | 36.47 ms | 89.68× |
| Monthly | 3,902.31 ms | 78.59 ms | 49.65× |

For this two-million-row scan-and-aggregate workload, DuckDB over Parquet was much faster in this run. The result does not imply DuckDB is the better transactional engine.

## Round 5 — Find the OLTP boundary

`uv run python Module06a/boundary.py`:

| Workload | SQLite | DuckDB |
|---|---:|---:|
| 1,000 row-by-row inserts | 1.78 ms | 1,127.72 ms |
| 1,000 row-by-row point lookups | 2.23 ms | 819.84 ms |
| 1,000 batched inserts | 0.98 ms | 705.48 ms |
| 1,000 batched point lookups | 2.32 ms | 842.33 ms |

The measured boundary is workload-shaped: SQLite fits these small transactional operations better; DuckDB fits the broad analytical scans above. Exact numbers vary by host and by how the benchmark batches work.

## Round 6 — Decision memo

See [decision-memo.md](decision-memo.md). Keep operational writes and point lookups in SQLite; use a Parquet snapshot with DuckDB for broad historical analytics. The refresh age must be visible because the snapshot may lag behind source writes.

## Refresh verification homework

Two consecutive `uv run python Module06a/refresh.py --check` runs:

```text
Run 1: rows=2000000, sum=21000000.0, Parquet bytes=2325330, elapsed=446.48 ms — PASS
Run 2: rows=2000000, sum=21000000.0, Parquet bytes=2325330, elapsed=430.08 ms — PASS
```

This repeats the row-count/rounded-sum check; it does not prove every row matches.

## Core homework — ZSTD

`uv run python Module06a/stretchers.py` reported:

- Snappy Parquet: 2,325,330 bytes
- ZSTD Parquet: 1,384,158 bytes
- ZSTD saved **40.5%** in this run.

## Optional stretchers completed

- **JSON-to-Parquet join:** Siemens matched cnc-01 and cnc-03 (420,000.0 each); Fanuc matched cnc-02 (420,000.0).
- **Row-group statistics:** unsorted groups each spanned 2026-01-01 through 2028-06-27; sorted groups narrowed to roughly two-month date windows.
- The JSON metadata is a small supplied example; these figures are not production data.
