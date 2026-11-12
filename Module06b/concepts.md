# Module 06b — Concepts to defend

## ACID and BASE

- **Atomicity:** a transaction happens completely or not at all.
- **Consistency:** committed transactions preserve declared database rules.
- **Isolation:** concurrent transactions do not expose invalid intermediate states.
- **Durability:** committed data survives the failures covered by the storage system.

SQLite provides ACID transactions for its local database file. This matters for the edge gateway: a batch of readings should not be half-written after a crash.

BASE is a loose design philosophy for distributed, highly available systems: Basically Available, Soft state, Eventual consistency. It accepts that replicas or derived copies may temporarily disagree and converge later. The Parquet report in Module 6a is a deliberately stale-able analytical copy; the SQLite operational database remains the source of truth.

## CAP theorem

For a distributed system experiencing a network partition, a design cannot guarantee both linearizable Consistency and Availability for every request. A CP choice may reject or delay requests until consistency can be maintained; an AP choice may answer using stale data and reconcile later. CAP is about distributed systems under partition, not a rule that every standalone SQLite file must satisfy.

An embedded database avoids a network hop and distributed replica coordination for the local workload. A PostgreSQL server adds shared multi-client access, roles and centralized administration, but clients depend on network connectivity and server availability.

## Apply the concepts to the benches

- SQLite sensor ingestion: ACID transactions and local durability are valuable.
- Parquet/DuckDB reporting: the report is a derived copy; refresh lag is an explicit eventual-consistency trade-off.
- JSON metadata: schema flexibility does not mean no schema; json_valid and expression indexes still enforce and optimize a known contract.
- shelve key-value state: simple get/set access can be fast, but it lacks SQL joins, filtering and aggregation across values.
- PostgreSQL: server-side roles and concurrent clients become easier; connection management, network failure and server operations become additional concerns.
