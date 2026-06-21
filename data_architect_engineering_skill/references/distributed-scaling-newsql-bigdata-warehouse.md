# Distributed Scaling, NewSQL, Big Data, And Warehouses

## Scaling Patterns
- Vertical scaling: add CPU, memory, IOPS, cache, or better storage to one node.
- Horizontal scaling: add nodes/replicas/shards/partitions.
- Functional partitioning: split workloads by bounded domain or service.
- Sharding: split the same logical dataset by key/range/hash.
- Read scaling: replicas, materialized views, caches, search indexes, and read models.
- Write scaling: partitioning, queueing, batching, distributed consensus, or eventual consistency.

Do not scale prematurely, but design for known growth by avoiding choices that make future partitioning impossible.

## Distributed SQL / NewSQL Choice
Use when SQL and transactions remain valuable but data/availability exceeds single-node comfort.

Decision checks:
- Required consistency and isolation level.
- Cross-region latency budget.
- Transaction size and cross-key/cross-range frequency.
- Hot row/range risk.
- SQL compatibility gaps.
- Operational maturity: backup, restore, upgrades, node replacement, monitoring, and incident response.
- Migration path from existing SQL dialect.

Candidate framing:
- TiDB: consider for MySQL-compatible distributed SQL with horizontal scaling, strong consistency, high availability, and mixed OLTP/real-time analytics needs.
- Vitess: consider for scaling MySQL through routing, sharding, online DDL, and operational patterns while preserving MySQL ecosystem investment.
- CockroachDB/YugabyteDB/Spanner-like systems: consider for strongly consistent distributed SQL with multi-region or cloud-native deployment needs.

This needs verification for current feature support, version behavior, license, and managed-service limits.

## Wide-Column Distributed Stores
Use when availability, write throughput, partition-key access, and large scale dominate.

Design around:
- Partition key and clustering order.
- Replication factor and consistency level.
- Compaction strategy.
- Repair/read-repair behavior.
- Tombstones and TTL.
- Multi-datacenter topology.

Avoid when:
- Queries require ad hoc joins.
- Foreign keys and cross-partition transactions are central.
- Users need flexible reporting directly from the operational store.

## Stream And Event Systems
Use Kafka, Pulsar, Kinesis, Redpanda, or similar when data movement and replay are core.

Design:
- Topic/event schema and compatibility.
- Partition key and ordering requirement.
- Producer idempotency and retries.
- Consumer groups, offset commits, dead-letter handling.
- Retention and replay.
- Exactly-once claims should be treated as end-to-end design problems, not broker magic.

## Big Data Processing
Batch frameworks fit large offline jobs, backfills, and model/data preparation. Stream frameworks fit continuous low-latency processing.

Common layers:
- Ingestion: CDC, event streams, batch files, API extracts.
- Storage: file, object, block, memory-centric, warehouse, or lakehouse.
- Processing: Spark, Flink, Beam, Trino/Presto, Hadoop lineage where present.
- Serving: warehouse, OLAP DB, search index, vector DB, feature store, API DB.
- Monitoring: job latency, lag, data quality, schema drift, small files, compaction, and cost.

## Lakehouse And Warehouse Design
Warehouse:
- Curated analytical system with governed schemas, BI, semantic models, and predictable query performance.

Lakehouse:
- Object storage plus table format and query engines, supporting open data files, schema evolution, snapshots, and multi-engine access.

Design checks:
- File format: Parquet/ORC/Avro/JSON/CSV; prefer columnar for analytics.
- Table format: Iceberg/Delta/Hudi where snapshot evolution, compaction, and time travel are needed.
- Catalog and governance.
- Partitioning and clustering.
- Small-file management.
- Data quality gates.
- Lineage and ownership.
- Cost and retention.

## HTAP
HTAP combines transactional and analytical needs but is not free.

Check:
- Resource isolation between OLTP and OLAP.
- Freshness requirement.
- Query complexity.
- Impact of analytical scans on transaction latency.
- Storage overhead and replica topology.

## Multi-Region
Before recommending multi-region writes, define:
- Data residency.
- Latency budget.
- Conflict model.
- Consistency requirement.
- Failover automation.
- Split-brain prevention.
- RPO/RTO.
- Operational playbook.

Red flag: "active-active" without conflict semantics.
