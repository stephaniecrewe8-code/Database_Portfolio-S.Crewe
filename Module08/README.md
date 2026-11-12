# Module 08 — Final Project Specification

The final project is worth 5 points (25% of the course). The syllabus is the source of truth if any detail conflicts.

Build a story-driven, local-first embedded database application for a real mechatronics, IoT or industrial-automation problem and a real named stakeholder. Project Teams contain 4–6 people; each member must own a defensible part.

## Seven must-have criteria
1. Embedded database with documented schema and at least one enforced FOREIGN KEY relationship.
2. Reproducible real-world ingestion that can be rerun without duplicates.
3. At least one index with EXPLAIN QUERY PLAN and before/after timing on a non-trivial dataset.
4. All external inputs use bound parameters; demonstrate why the string-built equivalent is injectable.
5. At least one database constraint and one trigger or generated column enforcing a domain rule.
6. Evaluation evidence: timings, plan output, storage size and/or load throughput.
7. Reachable human interface (Datasette, CLI, small app or dashboard) with graceful recovery from missing/corrupt data.

## Required project files
The FinalProject folder contains a scaffold for the project repository and the report. Complete it with the team's real story and actual implementation.

The concise report must follow the exact six-part structure in docs/report.md and stay within five pages:
1. Story and stakeholders (~½ page)
2. Schema and data model (~1 page)
3. Ingestion and pipeline (~¾ page)
4. Queries, indexes and evidence (~1¼ pages)
5. Security, integrity and evaluation (~1 page)
6. Project Team and contributions (~½ page)

## 15-minute demo
- 0–2 min: story, stakeholder and data source.
- 2–8 min: live raw-data → ingestion → database → headline query → interface.
- 8–10 min: query plan, timings and injection self-test.
- 10–12 min: constraint/trigger demonstration.
- 12–15 min: individual project discussion.

## Rubric (5 points)
- Story: 1
- Architecture: 1
- Plan: 1
- Demo and individual discussion: 2

The project plan must contain your own dates and evidence of following or revising it. Do not commit database files, DuckDB files, Parquet files, credentials, .env files or personal data. Commit scripts that rebuild the data instead.
