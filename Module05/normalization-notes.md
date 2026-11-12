# Module 05 — Normalization notes and evidence

Official sequence: [seven rounds in the course workbook](https://github.com/iotempire/iotempire-teaching/blob/main/full-classes/hsbi-databases-10d/modules/05-normalization-vs-denormalization.md).

## Round 1 — Functional dependencies

For the supplied flat job-part relation, the intended dependencies under the stated business assumptions are:

| Dependency | Basis |
|---|---|
| `job_id → machine_id, technician, done_on` | One machine, responsible technician, and completion date per job |
| `machine_id → site` | One current site per machine |
| `part_no → part_price` | One current catalogue price per part; historical transaction prices would require a different model |
| `(job_id, part_no)` | Candidate key for a job-part line |

The five sample rows only *happen* to associate some technicians and machines. They do not establish dependencies such as `technician → machine_id` or `machine_id → technician`.

### ER sketches

Draw the supplied flat relation and the decomposed model here (or attach a diagram):

- Flat model: [add your ER sketch]
- 3NF model: `Machine 1—N Job`, `Job 1—N JobPart`, `Part 1—N JobPart`

## Round 2 — Anomalies

See and run [anomalies.py](anomalies.py) and [anomalies.sql](anomalies.sql). Record your own terminal output and what fact was duplicated or lost:

- Update anomaly:
- Insert anomaly:
- Delete anomaly:

## Round 3 — Build and normalize

Run `uv run python Module05/build.py`.

The generator is designed to make 20,000 jobs × 10 job-part rows. Record your actual terminal output:

```text
[Paste output from your run here]
```

Explain why the decomposition has separate `machine`, `part`, `job`, and `job_part` tables, and why the join-back row counts match:

[Write your explanation after checking the output.]

## Round 4 — Compare queries

Run `uv run python Module05/benchmark.py`. Save the actual plans, timing samples, medians, and result comparison:

```text
[Paste output from your run here]
```

- Which plan did SQLite choose?
- Did the two report queries return the same result?
- What was the measured ratio, and what are the limits of this small synthetic dataset?

## Round 5 — Measure write and storage costs

Run `uv run python Module05/update_cost.py` and paste the actual output:

```text
[Paste output from your run here]
```

Explain how much write fan-out the design creates, and which storage objects are included in the reported total.

## Round 6 — Decision

Use your measured results in [decision-memo.md](decision-memo.md). Explain when the denormalized report path is worth its maintenance cost and what safeguards keep it consistent.

## Round 7 — Harvest and pod check

Do not invent a discussion or a gate result.

- One question or curiosity from my run:
- What my pod partner noticed:
- Neighbouring-pod gate question and actual response:
