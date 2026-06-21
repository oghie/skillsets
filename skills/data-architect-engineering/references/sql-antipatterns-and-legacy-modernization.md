# SQL Antipatterns And Legacy Modernization

## Traditional Database Knowledge Still Matters
Legacy migration requires understanding older patterns:
- Navigational access paths, COBOL/mainframe-style record traversal, and application-coupled storage layouts.
- Stored procedures as business logic and deployment units.
- Trigger-heavy side effects.
- Denormalized reporting tables.
- Implicit constraints enforced only in application code.
- Weak typing, nullable everything, natural-key drift, and duplicated reference data.
- Manual DBA processes, undocumented jobs, and backup scripts outside version control.

Do not call a legacy system "bad" before identifying which constraints it was optimized for: hardware limits, batch windows, vendor tooling, reporting needs, regulatory retention, or operational familiarity.

## Logical Design Antipatterns
- Comma-separated lists in one column: replace with an intersection/dependent table.
- EAV/generic attribute tables for core domain facts: model subtypes or bounded extension points.
- Polymorphic foreign keys: replace with explicit relationships, supertype/subtype tables, or separate association tables.
- One-size-fits-all primary key: choose keys based on identity, distribution, locality, and reference needs.
- Missing constraints: add primary, foreign, unique, check, and not-null constraints where safe.
- Cloned tables or columns for categories/time: use partitioning, type columns, or normalized related tables.
- Naive hierarchy modeling: choose adjacency list, path enumeration, nested sets, closure table, graph DB, or recursive CTE based on query shape.

## Physical Design Antipatterns
- Floating-point for money: use integer minor units or exact numeric.
- Indexing every column: indexes speed reads but cost writes, storage, memory, and maintenance.
- No index plan: every index must map to a query, constraint, or ordering requirement.
- Large opaque blobs in the wrong place: decide between DB BLOB, object storage, filesystem, and metadata references based on transactionality, backup, access, and cost.
- Engine mismatch: verify storage engine supports required foreign keys, transactions, crash recovery, row locks, and replication behavior.

## Query Antipatterns
- `SELECT *` in production paths: fetch explicit columns to reduce I/O and contract drift.
- Random sort at scale: avoid full randomization over large sets; use precomputed sampling or indexed random keys.
- Pattern matching for full-text search: use search indexes when relevance, tokenization, stemming, or scale matters.
- One huge query that hides multiple concerns: split into understandable steps, CTEs, materialized views, or precomputed read models when justified.
- Non-grouped columns with aggregates: return deterministic grouped data.
- NULL confusion: define semantics for unknown, not applicable, absent, deleted, and default.

## Application/Data Boundary Antipatterns
- Plaintext passwords or reversible password storage: use password hashing outside ordinary database encryption.
- Unparameterized SQL: never execute untrusted input as SQL code.
- ORM hides N+1 queries, missing transactions, or implicit lazy loads.
- Foreign keys disabled for speed and never revalidated.
- Data migrations shipped without full dataset tests and rollback.
- SQL treated as a second-class artifact with no review, linting, or versioning.

## Legacy Modernization Steps
1. Inventory: tables, procedures, triggers, jobs, reports, integrations, backup scripts, permissions, data volume, and owners.
2. Classify system-of-record tables vs derived/reporting tables.
3. Extract invariants currently enforced by code, triggers, batch jobs, or human procedure.
4. Build read/write access pattern matrix from logs, code, and reports.
5. Add observability around query latency, locks, deadlocks, replication, disk, backup duration, and job windows.
6. Create compatibility layer or strangler facade if consumers cannot move at once.
7. Migrate in phases: schema compatibility, dual-read/shadow-read, backfill, validation, cutover, rollback, and decommission.
8. Retire legacy only after downstream consumers, backups, audit retention, and legal hold obligations are closed.

## Legacy Migration Red Flags
- "We can just dump and import" for a system with active writes.
- No owner for stored procedures, triggers, or scheduled jobs.
- No way to compare source and target record counts/checksums.
- No rollback because "the old system will be turned off."
- Character set, collation, timezone, precision, or NULL semantics are not tested.
- Primary keys change without consumer contract review.
- Reporting users query production tables directly and are not inventoried.
