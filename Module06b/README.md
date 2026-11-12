# Module 06b — Polyglot Persistence and the Decision

This module implements the professor's four benches: JSON metadata in SQLite with an expression index; key-value session storage compared with SQLite; observations from the instructor's PostgreSQL server; and a one-page engine decision record.

## Run
- uv run python Module06b/json_bench.py
- uv run python Module06b/kv_compare.py

The scripts create local databases/files under Module06b. They report actual plans and timings; results vary by machine and shelve backend. Do not commit generated .db files or the sessions* files.

Read concepts.md for the ACID/BASE/CAP distinctions. Complete engine-notes.md with the PostgreSQL observations from the real instructor demo or your actual server session. Fill decision-record.md using measured Module 06a and 6b evidence, then record your nearest-pod defence and any change to your decision.

Key lesson: flexible JSON is still a schema. CHECK(json_valid(meta)) enforces valid JSON, and an expression index only helps when the query uses the matching expression. ACID concerns transaction guarantees; BASE describes relaxed consistency in distributed systems. CAP is a distributed-systems trade-off, not a rule that every local database must explain itself against.


Reusable scripts and reference notes in this folder were imported from [Michael’s Module 06b work](https://github.com/MichaelKonsduAmpadu/michael-sql.portfolio/tree/main/Module06b). Fill in the evidence documents only with observations from my runs and the instructor’s actual server demonstration.
