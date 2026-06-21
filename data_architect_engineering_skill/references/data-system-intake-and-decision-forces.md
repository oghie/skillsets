# Data System Intake And Decision Forces

## Intake Order
1. Business and failure impact: money movement, identity, health/safety, customer-facing latency, compliance, analytics, internal reporting, ML/RAG, observability, or archival.
2. System of record: which store owns each invariant and which stores are derived.
3. Workload shape: OLTP, OLAP, HTAP, stream, search, graph, vector, document, time-series, cache, queue-like, lakehouse, or warehouse.
4. Access patterns: exact lookup, range scan, join, aggregation, full-text search, semantic search, traversal, time-window query, append-only ingest, batch scan, feature lookup, or low-latency session lookup.
5. Write path: single writer, multiple writers, CDC, event sourcing, dual write, idempotent retry, transactional outbox, bulk import, streaming ingest, or offline compaction.
6. Read path: synchronous user request, asynchronous worker, analytics, dashboard, search endpoint, model retrieval, audit, export, or replication consumer.
7. Consistency model: strict serializable, serializable, snapshot isolation, read committed, read-your-writes, monotonic reads, bounded staleness, eventual, or best-effort.
8. Reliability: SLO/SLI, p50/p95/p99, RPO, RTO, restore proof, failover mode, corruption detection, and capacity headroom.
9. Security and governance: data classification, tenant boundaries, PII/secrets, roles, privileges, encryption, masking, retention, deletion, audit, and legal hold.
10. Operations: team skill, on-call burden, managed vs self-hosted, orchestration, observability, upgrade path, backup tooling, license, cost, and vendor exit.

## Decision Forces
- Correctness: constraints, transactions, idempotency, validation, ordering, and reconciliation.
- Performance: query shape, selectivity, cardinality, index structure, memory, I/O, network, CPU, compaction, and query planner behavior.
- Scale: vertical headroom, horizontal partitioning, functional partitioning, sharding, replication, data movement, and rebalancing.
- Availability: replication topology, failover, recovery time, blast radius, failure domains, quorum, and operational runbooks.
- Confidentiality: least privilege, encryption, TLS, secret handling, row/column/table controls, and data minimization.
- Integrity: normalization, referential integrity, check constraints, transactions, locks, audit trails, hashes, checksums, and immutable logs.
- Maintainability: schema evolution, migrations, local development, test fixtures, self-service operations, and developer ergonomics.
- Cost: hardware, storage tier, network egress, index bloat, replica count, compaction, cloud service limits, backup retention, and operational labor.

## Minimum Evidence Before A Recommendation
- Current schema or proposed model.
- Top 5-10 read and write queries or API access patterns.
- Data volume now, expected growth, retention, and cardinality.
- p95/p99 latency and throughput target, or the admission that they are unknown.
- RPO/RTO and recovery evidence.
- Security classification and tenant model.
- Operational ownership and deployment environment.

## Fact, Inference, Assumption, Question
Use this structure when the user has incomplete context:

```text
Fact:
- The orders table currently has a tenant_id column and 1.2B rows.

Inference:
- Tenant-scoped range queries likely need a composite partition/index strategy.

Assumption:
- Writes are append-heavy and tenants are not evenly distributed.

Question:
- What is the largest tenant and the p99 query latency target?
```

If the answer materially changes technology choice, do not pretend certainty. Name the risk and give a safe default.
