# Final Project — Team implementation workspace

This folder is a starting workspace for the HSBI Databases final project. It is not yet a completed project: the stakeholder, story, data source, team membership and component ownership must be agreed by the actual Project Team.

## Rebuild in three commands (complete after choosing the stack)
1. Install the pinned dependencies from requirements.txt.
2. Run the project ingestion script to rebuild the local database from the committed sample data or documented source.
3. Start the interface and open the headline query.

Replace these commands with exact, tested commands once the schema and ingestion are implemented. The project is not ready for submission until the three commands work from a clean checkout.

## Structure
- schema.sql — embedded schema with FK and domain constraints.
- ingest.py — reproducible, idempotent ingestion.
- queries.sql — named headline query and supporting queries.
- app.py — parameterized interface/CLI with graceful error handling.
- docs/team.md — stakeholder story, team charter and ownership.
- docs/requirements.md — Module 8 must-have mapping.
- docs/schema.md — ER diagram and design decisions.
- docs/plan.md — dated delivery plan.
- docs/benchmarks/ — EXPLAIN QUERY PLAN and before/after timings.
- docs/injection-self-test.md — parameterization audit and malicious-input test.
- docs/peer-review.md — review evidence.
- docs/demo-plan.md — timed rehearsal.
- docs/report.md — concise final report, maximum five pages.

## Integrity of evidence
Do not claim team agreement, data collection, peer review, benchmark results, rehearsal or stakeholder feedback until it has actually happened. Keep raw personal data and credentials out of Git.


This project scaffold was imported from [Michael’s portfolio](https://github.com/MichaelKonsduAmpadu/michael-sql.portfolio/tree/main/FinalProject). It remains a starter: the team story, data source, schema, and implementation must follow the team's agreed project.
