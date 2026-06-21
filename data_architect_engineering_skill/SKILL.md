---
name: data-architect-engineering
description: Use when designing, reviewing, modifying, migrating, optimizing, securing, operating, troubleshooting, or decommissioning data architectures across SQL, ISO SQL conformance, NoSQL, vector, graph, document, time-series, NewSQL, search, in-memory, SQLite, CDC/Debezium, hardware acceleration, cache, big-data, lakehouse, and warehouse systems.
---

# Data Architect Engineering

## Core Rule
Treat data architecture as a safety-critical engineering system: define workload, data model, access pattern, consistency, security, reliability, operational ownership, and validation before choosing a database, schema, index, shard key, cache, warehouse, or migration path.

## First Pass
1. Classify the task: database necessity assessment, greenfield design, new datastore creation, data model change, enhancement, migration, legacy modernization, decommissioning, performance tuning, security review, reliability review, incident troubleshooting, stack selection, hardware/storage sizing, monitoring, CDC/data movement, or orchestration.
2. Identify workload shape: OLTP, OLAP, HTAP, stream, event log, search, vector retrieval/RAG, graph traversal, document CRUD, time-series ingest/query, key-value/session/cache, queue-like, ML feature store, data lake, data warehouse, or hybrid.
3. Ask whether the application needs a database at all, a local embedded database, a file/object store, a cache, an event log, a search/vector index, or a full client/server DBMS.
4. Capture non-negotiables: data criticality, RPO/RTO, SLO/SLI, latency percentiles, throughput, data volume/growth, write/read ratio, retention, tenant isolation, compliance, confidentiality, integrity, availability, and recovery evidence.
5. Name the data model and query path before naming technology: entities, relationships, aggregates, documents, keys, partitions, series, embeddings, graph edges, search fields, analytical facts/dimensions, lineage, and access patterns.
6. Decide validation before recommendation: schema review, ISO SQL/dialect compatibility check, EXPLAIN/plan analysis, benchmark, load test, migration rehearsal, CDC replay test, restore drill, failover test, consistency check, threat model, data-quality test, or rollback simulation.

## Required Reads By Task
- Intake, decision forces, unknowns, or task classification: `references/data-system-intake-and-decision-forces.md`.
- Choosing among SQL, NoSQL, vector, graph, document, time-series, NewSQL, search, in-memory, columnar, key-value, object-oriented, multi-model, cache, big-data, lakehouse, or warehouse systems: `references/datastore-taxonomy-and-selection.md`.
- Deciding whether an app needs a DBMS, SQLite, a local file, object storage, static data, event log, cache-only design, or a client/server database for millions of users: `references/database-necessity-sqlite-and-scale.md`.
- SQL standard alignment, ISO/IEC 9075-* conformance, SQL dialect portability, SQL/JSON, SQL/PGQ, information schema, temporal/schema features, or modern schema design: `references/sql-standards-and-modern-schema-design.md`.
- Data modeling, schema design, ERD/document/graph/time-series/vector models, query-language fit, SQL vs non-SQL access patterns, or example queries: `references/modeling-and-query-patterns.md` and `references/query-examples-sql-nosql-vector-graph.md`.
- Traditional RDBMS, SQL correctness, normalization, referential integrity, indexing discipline, SQL antipatterns, legacy database constraints, or navigational/mainframe migration: `references/sql-antipatterns-and-legacy-modernization.md`.
- Query performance, indexing, partitioning, sharding, cardinality, plan review, caching, buffer/I/O, hot partitions, or database internals: `references/performance-indexing-and-query-optimization.md`.
- Migration profiling beyond TPS/QPS, workload capture, query plan inventory, data-shape profiling, lock/log/WAL/binlog metrics, storage/network/CPU/memory profiling, or migration readiness: `references/migration-profiling-dimensions.md`.
- CDC, Debezium, logical replication, binlog, outbox, schema-change streams, event ordering, replays, dual writes, and sink propagation: `references/cdc-debezium-and-data-movement.md`.
- Distributed SQL, NewSQL, TiDB, Vitess, Cassandra/Scylla-style wide-column systems, big-data processing, stream/batch, lakehouse, data warehouse, or HTAP: `references/distributed-scaling-newsql-bigdata-warehouse.md`.
- Security, privacy, IAM-to-data boundaries, roles, privileges, TLS, encryption, hashing, masking, row/column/table-level access, audit logs, injection risk, CIA, or governance: `references/security-governance-and-cia.md`.
- Reliability, SLO/SLI, backup/restore, replication, failover, observability, release management, operational visibility, runbooks, or incident response: `references/reliability-operations-monitoring.md`.
- Hardware, OS, filesystem, RAID, NVMe/SSD/HDD, SAN/NAS/object storage, network, RDMA, CPU/GPU/FPGA, virtualization, containers, cloud DBaaS, or Kubernetes operators: `references/infrastructure-storage-os-and-hardware.md`.
- FPGA/GPU/CPU-FPGA database acceleration, SIMD/vectorized execution, HBM, CXL, DPU/SmartNIC, GPUDirect/RDMA/NVMe-oF, PMEM, chipset-aware DB design, or accelerator fit checks: `references/hardware-acceleration-and-chipset-aware-db.md`.
- Red-flag review or pre-ship checklist: `references/red-flags.md`.

## Task Playbooks
- Design a new data architecture: `tasks/design-new-data-architecture.md`.
- Decide whether a database is needed and how much DBMS is enough: `tasks/database-necessity-and-scale-assessment.md`.
- Select a datastore or data platform and define next steps: `tasks/stack-selection-and-next-steps.md`.
- Modify, enhance, remove, or decommission a data component: `tasks/modify-enhance-or-remove-data-system.md`.
- Migrate or modernize legacy data systems: `tasks/migration-and-modernization.md`.
- Troubleshoot performance, availability, consistency, or operational incidents: `tasks/performance-troubleshooting.md`.
- Review data security, privacy, governance, reliability, and CIA risk: `tasks/security-reliability-review.md`.

## Templates
- Decision matrix: `templates/datastore-decision-matrix.md`.
- Capacity, SLO, RPO, and RTO sheet: `templates/capacity-slo-rpo-rto-sheet.md`.
- Migration runbook: `templates/migration-runbook.md`.
- Data model review checklist: `templates/data-model-review-checklist.md`.
- Data architecture view starters: `templates/mermaid-data-architecture-views.mmd`.

## Decision Discipline
- Separate `Fact`, `Inference`, `Assumption`, and `Question` when evidence is incomplete.
- If a product capability, version, service limit, pricing, license, CVE, compliance rule, or managed-service behavior affects the decision, say exactly: `This needs verification.`
- Do not recommend "NoSQL", "vector DB", "distributed SQL", "data lake", "warehouse", "cache", or "microservice database per service" without access patterns and operational constraints.
- Do not claim ISO/IEC 9075 conformance. State which SQL features are standard, optional, dialect-specific, or require live verification.
- Do not introduce Debezium/CDC as a generic migration fix without WAL/binlog/logical-replication readiness, schema-change handling, ordering, idempotency, offset storage, replay, and sink validation.
- Prefer boring, well-understood stores when they satisfy the workload and team can operate them. Add distribution, multi-model abstraction, global replication, or exotic storage only when the forces justify the operational cost.
- Prefer no database, a local file, SQLite, or object storage when the application only needs immutable/static/local data, low-write embedded state, or a portable application file.
- Treat caches, search indexes, vector stores, materialized views, and replicas as derived data unless explicitly designed as systems of record with durability, recovery, and reconciliation.
- Make reversibility explicit: backup, restore, rollback, dual-write reconciliation, compatibility window, data validation, and decommission criteria.

## Architecture Heuristics
- OLTP wants correctness, constraints, transactions, predictable p99 latency, and recoverability before raw throughput.
- OLAP and warehouses want scan efficiency, columnar layout, partitioning, materialization, compression, and governance before row-level mutation convenience.
- Search systems optimize relevance and text/filter retrieval; they are risky as the only source of truth unless writes, durability, transactions, and recovery are intentionally designed.
- Vector systems optimize semantic retrieval; require embedding versioning, recall evaluation, metadata filters, tenant isolation, reindex strategy, and stale-vector handling.
- Graph systems fit deep or variable relationship traversal; do not use them only because data has relationships.
- Time-series systems fit high-ingest timestamped data with retention/downsampling; do not store high-cardinality tags casually.
- Wide-column/key-value systems fit partition-key-oriented access at scale; cross-partition joins, foreign keys, and ad hoc querying are red flags.
- NewSQL/distributed SQL fits strong consistency with horizontal scale, but demands explicit latency, region, transaction, hotspot, and operational trade-off analysis.
- Big-data/lakehouse/warehouse designs need lineage, schema evolution, partition strategy, compaction, quality gates, cost controls, and consumer contracts.
- Accelerator-aware DB design only helps after profiling proves the bottleneck matches the accelerator: scan, join, aggregation, decompression, encryption, vector search, ML-adjacent retrieval, or memory bandwidth.

## Visual And Diagram Standards
- Use diagrams to clarify system of record, derived stores, ingestion, query paths, replication, consistency boundaries, migration phases, failure domains, backup/restore, and security enforcement points.
- Prefer ERD/data model diagrams for relational design, document shape examples for document stores, key/partition diagrams for wide-column/key-value stores, node-edge diagrams for graph systems, timeline diagrams for time-series, embedding/index lifecycle diagrams for vector systems, and pipeline diagrams for big-data/warehouse flows.
- Every diagram must state ownership, consistency boundary, durability path, and failure mode; decorative diagrams are not useful.

## Script Helper
- Run `scripts/data_architecture_static_audit.py <file-or-dir>` to scan Markdown design docs, ADRs, migration notes, or schema proposals for missing workload, access pattern, consistency, security, recovery, observability, migration, and validation coverage.

## Output Standard
Lead with the data architecture judgment or proposed path. State workload, data model, selected/avoided datastore classes, access patterns, consistency and transaction model, scaling path, security controls, reliability plan, monitoring, migration or rollback plan, validation checks, and residual uncertainty. For code or schema changes, include exact files/tables/queries affected and the verification run.
