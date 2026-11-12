
# Module 06b — Engine notes and evidence

Official task: [Polyglot Persistence](https://github.com/iotempire/iotempire-teaching/blob/main/full-classes/hsbi-databases-10d/modules/06b-polyglot-persistence.md).

Run date: 2026-11-12. Python 3.14.9 and SQLite 3.53.1 in a Windows-hosted environment. Timings below depend on the host and the selected shelve backend.

## Bench 1 — JSON metadata

`uv run python Module06b/json_bench.py`:

- `json_extract` returned the supplied Siemens, Fanuc, and Arburg device rows.
- Invalid JSON was rejected by `CHECK(json_valid(meta))`.
- The matching expression query used `ix_device_vendor`: `SEARCH device USING INDEX ix_device_vendor (<expr>=?)`.
- The alternate `->>` expression returned the same matching device but used `SCAN device`.

This demonstrates that flexible JSON still needs validation and that an expression index helps only when the query matches the indexed expression.

## Bench 2 — Key-value operations

`uv run python Module06b/kv_compare.py` ran 50,000 set and get operations:

| Store | Set | Get |
|---|---:|---:|
| shelve | 69.637 s | 0.734 s |
| SQLite | 0.175 s | 18.653 s |

In this specific implementation, shelve read much faster while SQLite wrote much faster and supports relational queries. Choose based on the real access mix; these numbers are not a general comparison of all key-value systems.

SQLite cross-session query result: 12,500.

## Bench 3 — PostgreSQL server

Not recorded. Add observations only after the actual instructor server demonstration or a real server session. Do not infer server results from the SQLite and DuckDB benchmarks.

## Decision record

See [decision-record.md](decision-record.md). The one-engine answer is explicitly limited to the measured workload.
