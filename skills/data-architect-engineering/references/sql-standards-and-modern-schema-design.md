# SQL Standards And Modern Schema Design

## ISO/IEC 9075-* Alignment
Treat ISO/IEC 9075 as the reference vocabulary and portability baseline, not as proof that any engine behaves identically.

The SQL standard family includes a framework/foundation plus optional parts and features such as:
- SQL/Foundation: core language, data definition, queries, constraints, transactions.
- SQL/CLI and language bindings.
- SQL/PSM stored modules.
- SQL/MED external data.
- SQL/Schemata information and definition schemas.
- SQL/XML, SQL/JSON, SQL/MDA, and SQL/PGQ property graph queries.

Modern engines implement different subsets and dialect extensions. Therefore:
- Label each SQL construct as standard core, standard optional, or dialect-specific.
- Verify engine conformance documentation before relying on portability.
- Prefer standard constructs in portable migrations.
- Use dialect-specific features deliberately when they buy safety, performance, or maintainability.
- Capture compatibility risk in ADRs and migration plans.

This needs verification for the current target engine and version.

## SQL Compatibility Checklist
- Data types: exact numeric, decimal, timestamp/timezone, boolean, JSON, arrays, UUID, spatial, vector, domain/custom types.
- DDL: generated identity, computed/generated columns, default expressions, check constraints, deferrable constraints, exclusion constraints, partitions.
- DML: `MERGE`, `RETURNING`, upsert syntax, common table expressions, recursive CTEs, window functions.
- Query semantics: NULL behavior, collation, grouping, `ORDER BY`, set operations, date arithmetic, string functions.
- Transactions: isolation levels, savepoints, advisory locks, locking reads, deadlock behavior.
- Information schema/catalog: introspection portability.
- Procedural SQL: stored procedures, functions, triggers, exception handling.
- JSON/XML/graph: standard syntax vs engine-specific JSON operators, SQL/PGQ, graph extensions, or document APIs.
- Replication/migration: sequences/identity, auto-increment, generated columns, triggers, and computed values across source/target.

## Modern Schema Design
Use modern features to make invariants explicit:
- Primary, foreign, unique, check, and not-null constraints.
- Generated identity instead of ad hoc sequences where portable enough.
- Generated/computed columns for derived values that must stay consistent.
- Partial/filtered indexes for skewed predicates.
- Expression indexes for stable computed predicates.
- Declarative partitioning for retention, pruning, and maintenance.
- Row-level security or security views where DB-level authorization is required.
- JSON columns only for bounded flexible attributes, not to avoid modeling.
- Temporal fields and bitemporal patterns when audit/history matters.
- Event/outbox tables for durable publication.
- Soft delete only with retention, uniqueness, and derived-store deletion policy.
- Schema comments/metadata for ownership and data classification when supported.

## Schema Evolution Pattern
Prefer expand-contract:
1. Add nullable/new column or new table.
2. Deploy code that writes both old and new when needed.
3. Backfill in batches.
4. Validate counts, checksums, constraints, and query parity.
5. Switch reads.
6. Enforce constraints.
7. Remove old column/table after compatibility window.

## Standardization Red Flags
- SQL described as portable while using engine-specific syntax.
- JSON/graph/vector extensions used without fallback or migration path.
- NULL/collation/timezone behavior not tested.
- `MERGE`/upsert semantics assumed identical across engines.
- Stored procedures migrated without language/runtime compatibility review.
