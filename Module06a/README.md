# Module 06a — DuckDB Analytical Engine

Move the 200,000-row Module 05 reporting table into a reproducible 2,000,000-row history dataset and Parquet analytical copy. Compare the same aggregate in SQLite and DuckDB, inspect plans, measure the OLTP boundary, and write a refresh decision.

Prerequisite: run `uv run python Module05/build.py` first. DuckDB is already declared in the repository dependencies.

## Run
- `uv run python Module06a/prepare.py`
- `uv run python Module06a/to_parquet.py`
- `uv run python Module06a/race.py`
- `uv run python Module06a/plan.py`
- `uv run python Module06a/boundary.py`
- `uv run python Module06a/refresh.py`
- `uv run python Module06a/refresh.py --check`
- `uv run python Module06a/stretchers.py`

The first script creates `history.db` (2 million rows) and a base CSV export. The second expands that CSV into Parquet, checks row count and `SUM(part_price)`, and reports both SQLite and Parquet file sizes. `race.py` warms both engines and interleaves five runs per query, reporting medians. `plan.py` prints DuckDB `EXPLAIN ANALYZE` and SQLite `EXPLAIN QUERY PLAN` for the same filtered aggregate. `boundary.py` compares row-at-a-time and batched writes plus point lookups. `refresh.py` rebuilds Parquet from `history.db` and supports a separate `--check` mode. `stretchers.py` runs the JSON join, sorted-Parquet statistics, and ZSTD compression comparison.

Generated database, CSV and Parquet files are local artefacts; do not commit them. Record actual measurements in `duckdb-notes.md`, complete `decision-memo.md` with your own values, and add your own learning reflection in `../Reflections/ref06a.md`. The ZSTD size comparison (S3) is part of the core homework; S1 and S2 are optional stretchers.


Reusable scripts and the evidence-note template in this folder were imported from [Michael’s Module 06a work](https://github.com/MichaelKonsduAmpadu/michael-sql.portfolio/tree/main/Module06a). Measurements and terminal output must be produced on my own machine.
