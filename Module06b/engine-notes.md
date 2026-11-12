# Module 06b — Engine notes and evidence

## Bench 1 — JSON metadata
Paste json_bench.py output, including both EXPLAIN QUERY PLAN results. Why does the expression index not serve the ->> query? What schema flexibility did JSON buy, and what typing/joins did it make harder?

## Bench 2 — key-value session state
Paste all four kv_compare.py timings. State which store you would ship for this access pattern and why. Name one cross-session query SQLite can answer that shelve cannot answer directly.

## Bench 3 — server contrast
Complete only after the actual instructor PostgreSQL demo or your own authorized server session.
- What became easier?
- What became harder?
- What server/network failure did you observe?
- What happened with a second writer?
- Three actual observations:

## Bench 4 — decision record and peer defence
- Paste your completed decision-record.md.
- Which row had no measurement behind it?
- What did the neighbouring pod challenge?
- What changed after the defence, and why?
- Which single engine would you keep if forced, and what breaks first?
