
# Engine decision record — Kortmann plant

| Workload | Engine | Why | Evidence from this course | Cost accepted | If a copy is stale |
|---|---|---|---|---|---|
| Job ingest, transactional updates, point lookups | SQLite | Best fit among measured engines for small operational reads and writes | 1,000 row-by-row insert: 1.78 ms SQLite vs 1,127.72 ms DuckDB; lookup: 2.23 ms vs 819.84 ms | Single-writer/concurrency limit | Operational DB remains source of truth |
| Month-end report over two years | DuckDB over Parquet | Columnar scan and aggregate workload | Dashboard 36.47 ms DuckDB vs 3,270.58 ms SQLite; monthly 78.59 ms vs 3,902.31 ms; Parquet 2,325,330 bytes | Refresh lag and duplicate analytical copy | Show last successful refresh and flag stale |
| Vendor metadata with optional fields | SQLite JSON | Validated JSON plus an expression index | Matching expression used `ix_device_vendor`; alternate expression scanned the table | Weaker field-level typing | Operational JSON remains source of truth |
| Dashboard session state | Depends on access mix; compare before choosing | In this run shelve reads were faster and SQLite writes were faster | 50,000 shelve set/get: 69.637 s / 0.734 s; SQLite: 0.175 s / 18.653 s | Backend and read/write mix affect the result | Recreate ephemeral sessions or expire them |
| Concurrent network clients | PostgreSQL comparison pending | Needs the instructor's actual server evidence | No server observation recorded | Server/network operations | Add retry/reconnect plan after the demo |

## One-engine constraint

If restricted to one measured engine for this project's operational source of truth, I would choose **SQLite**: its measured point writes and lookups fit the transactional workload, it supports the relational integrity rules, and it can store validated JSON. The broad two-million-row analytics would become materially slower than the measured DuckDB/Parquet route. This conclusion is specific to the tested workloads and is not a universal engine ranking.

## Defence notes

- Challenge from neighbouring pod: Not yet recorded.
- My answer:
- What I changed after the defence:
- Why:
