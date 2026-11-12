
# Module 05 — Normalization vs. Denormalization

[Official task specification](https://github.com/iotempire/iotempire-teaching/blob/main/full-classes/hsbi-databases-10d/modules/05-normalization-vs-denormalization.md)

This module covers functional dependencies, candidate keys, 1NF–3NF, anomalies, and measured read/write/storage trade-offs. The exercises use the course's maintenance-job dataset.

## Run

From the repository root:

- `uv run python Module05/anomalies.py` — demonstrate update, insert, and delete anomalies.
- `uv run python Module05/build.py` — build the deterministic 200,000-row flat table, 3NF tables, and reporting table.
- `uv run python Module05/benchmark.py` — compare the report query plans and timings.
- `uv run python Module05/update_cost.py` — measure update fan-out and table storage.

Reusable scripts were imported from [Michael's Module 05 portfolio](https://github.com/MichaelKonsduAmpadu/michael-sql.portfolio/tree/main/Module05). The benchmark reopens its SQLite connection after dropping the report index so the no-index plan is freshly compiled.

## Run evidence

The completed run and interpretation are in [normalization-notes.md](normalization-notes.md), with the recommendation in [decision-memo.md](decision-memo.md). Results were captured on 2026-11-12 in a Windows-hosted environment with Python 3.14.9 and SQLite 3.53.1. They are machine-dependent and should be rerun on the laptop used for the course if a local result is required.

The measured no-index and indexed plans are distinct; benchmark evidence records both. The build output verifies matching normalized and denormalized row counts and a clean foreign-key check.

## Evidence integrity

The deterministic build and benchmark are reproducible. A neighbour gate and harvest discussion are not claimed here; add them only after the actual pod activity.
