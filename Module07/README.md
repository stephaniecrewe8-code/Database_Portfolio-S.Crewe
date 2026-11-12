# Module 07 — Final Project Studio

Module 07 is the three-session studio for the final project specified in Module 08. The required work is a real stakeholder story, a 4–6-person Project Team charter, a requirement-to-deliverable map, a reproducible vertical slice, peer review, and a timed 15-minute rehearsal.

The planning artefacts are scaffolded in FinalProject/docs. They are intentionally not filled with invented team members, ownership, stakeholder conversations, dates, peer-review findings or demo results. Complete them with your actual Project Team.

## Read before kickoff
The professor asks teams to compare two single-binary/local-first systems: GoToSocial (SQLite by default, PostgreSQL optional) and Chatto (single executable with embedded NATS JetStream). For each, note what the architecture removes, what it trades away and what it gains. Decide which shape fits your project and which Module 8 must-have becomes harder. Record the team's conclusion in FinalProject/docs/requirements.md.

## Start here
1. Read [Module 08](../Module08/README.md) and the professor's Module 8 specification.
2. Complete [team.md](../FinalProject/docs/team.md) with the real story, all team members and individually owned components.
3. Complete [requirements.md](../FinalProject/docs/requirements.md) and [plan.md](../FinalProject/docs/plan.md).
4. Build one vertical slice: raw data → idempotent ingestion → embedded database → headline query → usable interface.
5. Complete peer review and rehearsal documents after the actual activities.

## Session gates
- Session 8: named stakeholder/story, team charter, engine choice and first vertical slice.
- Session 9: benchmark and hardening; bound parameters, injection self-test, integrity rule.
- Session 10: peer review, fixes and timed 15-minute rehearsal.

The project discussion is individual: be able to explain your own contribution and design decisions. The optional Module 7 stretcher is an upstream pull request to IoTempower, the course repository or a tool used by the project; only an accepted, verifiable contribution can be proposed as an Excellence Stretcher.
