# Module 06a — DuckDB notes and evidence

This file separates explanations (which can be completed before running the experiments) from measured evidence. **Do not replace the evidence placeholders with guessed numbers.** Paste the actual terminal output after running each script.

## Round 1 — Build

### Terminal evidence
```text
[PASTE THE COMPLETE OUTPUT OF: uv run python Module06a/prepare.py]
```

### Explanation
The source table `Module05/normalize.db → report_jobpart` contains 200,000 rows. The script creates ten copies (quarter offsets `k = 0…9`), so the expected history size is:

`10 × 200,000 = 2,000,000 rows`.

Each copy receives a distinct `job_id` offset (`k × 1,000,000`) so the generated identifiers do not collide. The date is shifted by `k × 91` days; 91 days represents a 13-week quarter. Ten quarter-sized periods span 910 days, approximately 2.5 years.

If the offset were 90 days instead of 91, each copy would start one day earlier relative to the 91-day schedule. Since the source data covers 90 calendar days, 90-day shifts make consecutive date ranges meet without the one-day gap left by a 91-day shift. The row count and prices would stay the same; only the generated dates would change. Calendar months are not fixed 90- or 91-day periods, so this is a controlled synthetic timeline, not a calendar-quarter model.

## Round 2 — Convert

### Terminal evidence
```text
[PASTE THE COMPLETE OUTPUT OF: uv run python Module06a/to_parquet.py]
```

Also record the actual file sizes after both files exist:

```text
history.db bytes: [PASTE ACTUAL SIZE]
report_history.parquet bytes: [PASTE ACTUAL SIZE]
report_history.parquet MB: [PASTE ACTUAL SIZE]
```

### Explanation
The Parquet file is produced from the 200,000-row base CSV by expanding it ten times, matching the ten-copy history table in SQLite. I check that the Parquet and SQLite copies have the same row count (2,000,000) and the same rounded `SUM(part_price)`. Matching both values is useful evidence that the conversion preserved the dataset's size and aggregate price total.

These checks do **not** prove every row is identical: two different datasets can have the same row count and total if row-level differences compensate. A cryptographic hash or a row-by-row comparison would provide stronger evidence. Parquet is columnar and compressed; for analytical queries it can read only the required columns, while a row-oriented SQLite table generally reads complete rows. The actual size comparison must come from the files generated on this machine.

## Round 3 — Race

### Terminal evidence
```text
[PASTE THE COMPLETE OUTPUT OF: uv run python Module06a/race.py]
```

| Query | SQLite samples (ms) | SQLite median (ms) | DuckDB samples (ms) | DuckDB median (ms) | SQLite / DuckDB |
|---|---|---:|---|---:|---:|
| Dashboard | [actual samples] | [actual] | [actual samples] | [actual] | [actual]× |
| Monthly | [actual samples] | [actual] | [actual samples] | [actual] | [actual]× |

### Explanation
The script warms both engines before timing and interleaves the runs to reduce bias from always running one engine first. The median is more robust than the mean when one run is unusually slow because of operating-system activity or cache effects. The ratio is calculated as SQLite median divided by DuckDB median; a ratio above 1 means DuckDB was faster for that query on this machine.

DuckDB is expected to perform well on full-table analytical scans and aggregations because its columnar execution can reduce the amount of data read and process values in batches. The exact result depends on hardware, cache state, data layout and software versions. I should report my measured values, not assume the professor's reference timings.

SQLite could win for a selective point lookup or a small indexed range query, because it is designed for transactional access to individual records. A full scan over millions of rows is a different workload from retrieving one record by primary key.

## Round 4 — Plan

### Terminal evidence
```text
[PASTE THE COMPLETE OUTPUT OF: uv run python Module06a/plan.py]
```

### What to identify in the output
- **Scan:** DuckDB's `TABLE_SCAN` / `READ_PARQUET` operator reads the Parquet data.
- **Projections:** the dashboard aggregate needs `machine_id`, `site`, `technician` and `part_price`; it does not need every column in the file.
- **Rows:** identify the actual number of rows read by the scan (expected to be up to 2,000,000 for this workload) and the number of groups produced.
- **Grouping:** identify the `HASH_GROUP_BY` (or equivalent grouping operator) that computes `SUM(part_price)`.
- **SQLite comparison:** `SCAN report_history` indicates a table scan; `USE TEMP B-TREE FOR GROUP BY`, if shown, indicates temporary sorting/grouping work.

The scan is likely to dominate because it processes the large input; the grouped output is much smaller. DuckDB's `EXPLAIN ANALYZE` executes the query and reports actual operator timings and row counts. SQLite's `EXPLAIN QUERY PLAN` describes the chosen access strategy but does not provide comparable actual operator timings. I must mark the operator and row count from my own output rather than copy illustrative numbers.

## Round 5 — Boundary

### Terminal evidence
```text
[PASTE THE COMPLETE OUTPUT OF: uv run python Module06a/boundary.py]
```

| Workload | SQLite (ms) | DuckDB (ms) | Faster engine on this run |
|---|---:|---:|---|
| 1,000 row-by-row inserts | [actual] | [actual] | [actual] |
| 1,000 batched inserts (`executemany`) | [actual] | [actual] | [actual] |
| 1,000 point lookups | [actual] | [actual] | [actual] |

### Explanation and numeric boundary
This experiment represents an OLTP-style workload: many small writes and individual lookups. SQLite is designed for embedded transactional workloads and is expected to be the better fit here. DuckDB is designed primarily for analytical, scan-heavy OLAP workloads; repeated individual statements add overhead that batching can reduce but not necessarily eliminate.

**My measured boundary:** DuckDB is the wrong choice for this tested application pattern when it must perform 1,000 individual inserts and 1,000 individual point lookups: SQLite took [actual SQLite time] ms versus DuckDB's [actual DuckDB time] ms for [name the measured operation]. I will fill in the values after running the benchmark. This is a boundary demonstrated by this benchmark, not a universal performance threshold.

## Round 6 — Decision

### Decision memo
The operational source of truth should remain in SQLite. It handles job ingestion, small transactional updates and point lookups. The two-year-plus historical reporting copy should be exported to Parquet and queried with DuckDB, because the dashboard and monthly reports scan and aggregate many rows. On this machine, the dashboard query took [SQLite median] ms in SQLite and [DuckDB median] ms in DuckDB; the monthly query took [SQLite median] ms and [DuckDB median] ms, respectively. The Parquet copy occupied [actual bytes] bytes, compared with [actual bytes] bytes for the SQLite database.

I recommend rebuilding the analytical copy after the operational shift closes each night (or after a successful ingestion batch), with an automated scheduled job owned by the data/application operations role. The refresh process should write a new temporary Parquet file, verify it, and only then replace the previous published copy. The dashboard should display the last successful refresh timestamp and flag the report as stale if the expected refresh window is missed. A stale report can mislead management even when it runs quickly, so freshness must be visible. Frequent single-row updates and transactional ingestion should not move to Parquet because it is an analytical snapshot, not the operational source of truth.

Replace every bracketed measurement above with the values from your own runs before treating this memo as final.

## Homework / intense track — Refresh verification

### First check run
```text
[PASTE OUTPUT OF: uv run python Module06a/refresh.py --check]
```

### Second consecutive check run
```text
[PASTE OUTPUT OF THE SECOND: uv run python Module06a/refresh.py --check]
```

### Explanation
Matching row counts and rounded `SUM(part_price)` values show that the Parquet copy agrees with SQLite on these two aggregate checks. They can detect missing/extra rows and many accidental changes to prices. They do **not** constitute a cryptographic checksum and cannot detect every row-level change: for example, one price could increase while another decreases by the same amount, leaving the total unchanged. The check also cannot prove that the SQLite source itself contains the latest expected business data. The refresh should therefore record its successful timestamp and be monitored for missed runs. Repeated runs should produce matching logical row counts and sums; Parquet bytes may differ because file metadata or row-group layout can vary.

## Core homework — ZSTD compression (S3)

The professor lists the ZSTD size comparison as core homework for everyone. Run the script and paste its actual output here.

- **S3 — ZSTD size comparison:** [PASTE actual Snappy and ZSTD byte sizes. Calculate the percentage saved: `(snappy_bytes - zstd_bytes) / snappy_bytes × 100`. Explain the storage-versus-compression trade-off.]

## Optional stretchers

Only complete S1 and S2 if you actually run them. Paste the real output and add a short observation.

- **S1 — JSON read / join:** [PASTE OUTPUT OF `uv run python Module06a/stretchers.py` and explain what the JSON-to-Parquet join demonstrates.]
- **S2 — Sorted Parquet row-group statistics:** [PASTE the original and sorted `done_on` row-group statistics. Explain whether sorting narrows each row group's date range and can help date-filtered scans.]
## Final verification checklist

- [ ] Module 5 prerequisite exists: `Module05/normalize.db`.
- [ ] Build output confirms 2,000,000 history rows.
- [ ] Parquet and SQLite row counts and rounded price totals match.
- [ ] Database and Parquet file sizes are recorded.
- [ ] Dashboard and monthly benchmarks are recorded with samples, medians and ratios.
- [ ] Actual DuckDB and SQLite plans are pasted and annotated.
- [ ] Row-by-row, batched insert and point-lookup timings are recorded.
- [ ] Decision memo contains actual measurements and a refresh/ownership plan.
- [ ] Two consecutive `refresh.py --check` outputs are pasted.
- [ ] Required S3 ZSTD size comparison is recorded; optional S1/S2 are documented only if completed.
