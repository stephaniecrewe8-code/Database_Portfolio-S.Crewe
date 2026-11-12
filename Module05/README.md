# Module 05 — Normalization vs. Denormalization

[Official task specification](https://github.com/iotempire/iotempire-teaching/blob/main/full-classes/hsbi-databases-10d/modules/05-normalization-vs-denormalization.md)

This module covers functional dependencies, candidate keys, 1NF–3NF, anomalies, and measured read/write/storage trade-offs. The exercises use the course’s maintenance-job dataset.

## Run

From the repository root:

- `uv run python Module05/anomalies.py` — demonstrate update, insert, and delete anomalies.
- `uv run python Module05/build.py` — build the deterministic 200,000-row flat table, 3NF tables, and reporting table.
- `uv run python Module05/benchmark.py` — compare the report query plans and timings.
- `uv run python Module05/update_cost.py` — measure update fan-out and table storage.

Scripts are reusable study tools imported from [Michael’s Module 05 portfolio](https://github.com/MichaelKonsduAmpadu/michael-sql.portfolio/tree/main/Module05). They create local files that are ignored by Git. The scripts are not proof that I have personally run or defended the exercises.

## Portfolio evidence

- [Normalization notes](normalization-notes.md): functional-dependency reasoning, anomalies, schema explanation, and spaces to record actual output.
- [Decision memo](decision-memo.md): recommendation to Yasmin based on measurements from my run.

Do not substitute another student’s measurements for your own. Query timing and database size depend on the local environment.
