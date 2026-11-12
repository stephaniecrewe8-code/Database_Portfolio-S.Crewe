# Engine decision record — Kortmann plant

Use the measurements from Modules 6a and 6b. Replace every bracketed prompt; do not invent benchmark results or server observations.

| Workload | Engine | Why | Evidence from this course | Cost accepted | If a copy is stale |
|---|---|---|---|---|---|
| Sensor/job ingest, every 30 s; crash must not lose rows | [SQLite] | [transactional writes/local-first] | [Module 4 and 6a result] | [single-writer/concurrency limit] | [not applicable / recovery plan] |
| Month-end report over two years | [DuckDB over Parquet] | [columnar scan/aggregate] | [Module 6a timings and plans] | [refresh lag/duplicate copy] | [display last refresh and flag stale] |
| Vendor metadata that gains fields | [SQLite JSON] | [flexible shape with json_valid] | [Module 6b expression-index plan] | [weaker field-level typing] | [source remains in operational DB] |
| Dashboard session state | [SQLite or shelve] | [measured get/set workload] | [four kv_compare timings] | [queryability or simplicity] | [session expiry/recreate] |
| Optional concurrent network clients | [PostgreSQL] | [server roles/concurrency] | [actual server observations] | [network/server operations] | [connection/retry strategy] |

## One-engine constraint

If Kortmann could run only one engine, I would choose [engine] because [workload priority and measured evidence]. The first thing that would break or become materially worse is [specific workload], because [measured reason].

## Defence notes

- Challenge from neighbouring pod:
- My answer:
- What I changed after the defence:
- Why:
