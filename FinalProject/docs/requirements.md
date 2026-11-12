# Module 8 requirements-to-deliverables map

Fill in the deliverable paths and status from the actual project. A checked box means the evidence exists and has been tested, not merely planned.

| Must-have | Required deliverable | Status | Evidence / commit |
|---|---|---|---|
| Embedded DB, documented schema, enforced relationship | schema.sql, docs/schema.md, ER diagram | [Not started] | |
| Reproducible real-world ingestion, idempotent rerun | ingest.py + source data/download script | [Not started] | |
| Measured index proof | benchmark + EXPLAIN QUERY PLAN before/after | [Not started] | |
| Parameterized, injection-safe external input | app.py + malicious-input self-test | [Not started] | |
| Constraint plus trigger/generated column | schema.sql + live rejection/firing evidence | [Not started] | |
| Evaluation evidence | timings, plans, storage size, load time | [Not started] | |
| Reachable interface and graceful recovery | Datasette/CLI/app + failure test | [Not started] | |

## Architecture context
- What does the system remove compared with a classic multi-tier stack?
- What does it trade away?
- What does it gain?
- Which Module 8 must-have is harder in this architecture, and how will we satisfy it?

## Definition of done
The README rebuild instructions work on a clean checkout in three commands; the database is generated from scripts, not committed; all external inputs use bound parameters; and each member can explain their own component.
