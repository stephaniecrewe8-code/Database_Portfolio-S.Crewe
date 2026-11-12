"""Final-project ingestion starter.

Replace the TODO section once the team selects and documents its real data source.
The finished script must be reproducible and idempotent: running it twice must not
duplicate source records. Use sqlite3 placeholders and executemany/UPSERT.
"""
from pathlib import Path

ROOT=Path(__file__).resolve().parent
SCHEMA=ROOT/"schema.sql"
DB=ROOT/"project.db"


def main():
    if not SCHEMA.exists():
        raise SystemExit("schema.sql is missing.")
    raise SystemExit(
        "Project ingestion is not implemented yet. First complete docs/team.md "
        "with the real stakeholder story and data source, then implement the "
        "documented CSV/JSON/API ingestion with bound parameters and UPSERT."
    )


if __name__=="__main__":
    main()
