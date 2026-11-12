"""Final-project interface starter.

Implement a CLI, Datasette instance or small app after the project schema and
headline query are agreed. All external inputs must use bound SQL parameters.
The finished interface must handle a missing database and missing rows clearly.
"""
from pathlib import Path

ROOT=Path(__file__).resolve().parent
DB=ROOT/"project.db"


def main():
    if not DB.exists():
        raise SystemExit("Project database not found. Run the documented ingestion command first.")
    raise SystemExit(
        "Interface not implemented yet. Add the stakeholder's headline query "
        "using sqlite3 placeholders; never interpolate user input into SQL."
    )


if __name__=="__main__":
    main()
