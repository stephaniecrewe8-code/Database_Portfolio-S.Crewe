# Recommendation to Yasmin Kaya

Use the Module 5 measurements from [my notes](normalization-notes.md) and [the benchmark scripts](benchmark.py). Replace every prompt with results from my own run.

I recommend **[3NF only / 3NF plus a reporting copy]** for the operational workload. The normalized report query measured [median] ms, compared with [median] ms for the report table, a [ratio]× difference on this dataset. The site update touched [row count] source row(s) and [row count] report row(s); measured table storage was [size] bytes and [size] bytes. These numbers support [explain the decision], but they describe the tested synthetic workload and local machine.

If a denormalized reporting copy is used, keep it derived from the normalized source and update it transactionally. Add a rebuild and reconciliation path, and show the dashboard’s last successful refresh time. If the observed query improvement is not meaningful for the real workload, keep the simpler normalized query.

## What would change my recommendation?

[Describe the expected workload, freshness needs, and failure mode that would make you change the decision.]
