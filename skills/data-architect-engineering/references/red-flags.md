# Data Architecture Red Flags

## Design
- Technology chosen before workload and access patterns.
- "Use NoSQL for scale" without partition key and query matrix.
- "Use vector DB" without recall evaluation, embedding versioning, tenant filters, and stale-vector plan.
- "Use graph DB" for ordinary relational joins.
- "Use search as database" without source-of-truth and rebuild plan.
- "Use data lake" without catalog, schema evolution, quality gates, and ownership.
- Multi-model database chosen to avoid modeling decisions.

## SQL And Modeling
- No primary keys.
- No foreign keys for data that requires referential integrity.
- Nullable columns with no semantic distinction.
- Comma-separated lists in a column.
- EAV used for core business facts.
- Polymorphic foreign keys.
- Money stored in floating point.
- Every column indexed or no indexes at all.
- `SELECT *` in stable API/reporting paths.
- ORM-generated queries never reviewed.

## Distributed Systems
- Active-active writes with no conflict model.
- Cross-region synchronous writes without latency budget.
- Shard key chosen from convenience, not distribution and query patterns.
- Hot partitions ignored.
- Dual writes without outbox, idempotency, reconciliation, or repair.
- CDC pipeline has no ordering, replay, or poison-message plan.
- Read replicas used for consistency-sensitive reads without read-after-write strategy.

## Security
- Shared admin credentials.
- Plaintext passwords or secrets in DB/logs.
- No TLS for networked database access.
- No tenant filter in search/vector/cache/warehouse copies.
- Backups not encrypted or access-controlled.
- Data deletion does not propagate to derived stores.
- Audit logs absent for admin actions and sensitive reads.

## Reliability
- Backup success assumed; restore never tested.
- RPO/RTO unknown.
- No corruption recovery plan.
- Migrations have no rollback or rehearsal.
- Schema changes may lock large tables during peak traffic.
- Monitoring lacks query latency, lock waits, replication lag, and disk I/O.
- Manual failover known by one operator.

## Performance
- Query tuning without `EXPLAIN`/actual plan evidence.
- Index added without write-cost analysis.
- Cache added before fixing access pattern.
- Benchmark uses tiny clean data with no skew.
- p99 ignored.
- Warehouse/lake jobs produce small-file explosion.
- Time-series tags include unbounded identifiers by default.

## Operations
- Database config not versioned.
- No owner for each data product/table/index/topic.
- No service catalog or runbook.
- Direct production data access for ad hoc analysis without audit.
- No license/cost/managed-service limit review.
- No exit/export strategy for proprietary systems.
