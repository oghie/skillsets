# Datastore Taxonomy And Selection

## Selection Rule
Pick the datastore class from the invariant and access pattern, then pick a product from operational fit. Vendor choice is the last step, not the first.

## Relational SQL
Best for systems of record, strong integrity, joins, transactions, constraints, ad hoc queries, and mature tooling.

Use when:
- Invariants matter more than write fan-out convenience.
- Relationships and constraints must be enforced by the database.
- Queries need joins, grouping, transactional updates, or reporting over normalized data.
- Team needs mature backup, restore, migration, and observability practices.

Watch:
- Overloaded single node, unbounded joins, missing constraints, migration lock risk, index bloat, and replica lag.

Typical candidates:
- PostgreSQL, MySQL/MariaDB, SQL Server, Oracle, SQLite for embedded/local use.

## Distributed SQL / NewSQL
Best for SQL semantics with horizontal scale or high availability beyond a single primary.

Use when:
- Relational model and transactions are required, but single-node vertical scaling is no longer credible.
- Strong consistency and high availability are explicit requirements.
- Sharding should be hidden or partly automated by the database.

Watch:
- Cross-region latency, transaction coordination, hot ranges/keys, operational complexity, compatibility gaps, and cost.

Typical candidates:
- TiDB, CockroachDB, YugabyteDB, Google Spanner, AlloyDB/Cloud SQL variants depending on platform.
- TiDB is a candidate when MySQL compatibility, horizontal scale, strong consistency, and HTAP-like row/column storage are central.
- Vitess is a candidate when the organization wants to scale a MySQL estate with sharding, routing, online DDL, and MySQL operational continuity.

## Document Stores
Best for aggregate-oriented objects with flexible schema and document-local reads/writes.

Use when:
- The common read returns a whole aggregate document.
- Schema evolves frequently but still needs validation discipline.
- Horizontal scale and developer-friendly JSON models matter.

Watch:
- Cross-document transactions, duplicate data drift, unbounded document growth, ad hoc reporting, and hidden relational needs.

Typical candidates:
- MongoDB, Couchbase, Firestore, Cosmos DB.

## Wide-Column / Partitioned Key-Oriented Stores
Best for massive partition-key-oriented workloads, high write throughput, global availability, and predictable query patterns.

Use when:
- Queries always include the partition key.
- Denormalized tables per query are acceptable.
- Availability and scale matter more than joins and foreign keys.

Watch:
- Hot partitions, cross-partition queries, secondary index misuse, tombstones, compaction, repair, consistency tuning, and missing referential integrity.

Typical candidates:
- Cassandra, ScyllaDB, HBase, Bigtable, DynamoDB-like systems.

## Key-Value Stores
Best for exact-key lookups, session state, feature flags, counters, rate limits, and simple low-latency data access.

Use when:
- Access is naturally by key.
- Data can be small, bounded, and TTL-friendly.
- Complex query semantics are unnecessary.

Watch:
- Treating KV as relational storage, no secondary access plan, hot keys, large values, poor TTL policy, and unclear durability.

Typical candidates:
- Redis, DynamoDB, FoundationDB key-value layer, RocksDB/LevelDB embedded, etcd/Consul for coordination only with strict caution.

## In-Memory Stores And Caches
Best for latency reduction and load shedding, not as a silent source of truth.

Use when:
- Cache miss path is acceptable and measurable.
- Invalidation, TTL, write-through/write-behind, and stampede control are designed.
- Data loss from cache is acceptable or persistence is explicitly configured.

Watch:
- Cache as accidental system of record, stale authorization data, unbounded keys, missing tenant isolation, stampedes, split-brain, and eviction surprises.

Typical candidates:
- Redis, Memcached, Hazelcast, Aerospike, in-process caches.

## Search Engines
Best for full-text, relevance ranking, faceting, autocomplete, logs, observability search, and semi-structured retrieval.

Use when:
- Users search text or filtered documents by relevance.
- Read model can be rebuilt from source of truth.
- Indexing lag and eventual consistency are acceptable or bounded.

Watch:
- Search cluster as primary database without transaction/recovery design, shard oversizing, mapping drift, high-cardinality aggregations, and costly reindexing.

Typical candidates:
- Elasticsearch, OpenSearch, Solr, Vespa, Typesense, Meilisearch.

## Vector Stores
Best for embedding similarity, semantic search, recommendations, multi-modal retrieval, and RAG retrieval layers.

Use when:
- Similarity is defined by embedding distance, not exact predicates alone.
- Recall, precision, latency, metadata filtering, and re-ranking can be measured.
- Embedding model versioning and reindexing are planned.

Watch:
- No offline evaluation set, no tenant filter, no stale-vector strategy, no embedding version, no delete propagation, overusing vector search for exact lookup, and ignoring hybrid lexical search.

Typical candidates:
- pgvector for Postgres-integrated vector search with relational joins and ACID features.
- Qdrant, Milvus, Weaviate, Pinecone, Vespa, Elasticsearch/OpenSearch vector search for dedicated or managed vector retrieval.
- FAISS/HNSW libraries for embedded/offline/local search where database operations are not required.

## Graph Databases
Best for relationship-heavy queries and variable-depth traversal.

Use when:
- The hard query is "how are these things connected?" not "find row by key."
- Path length varies and relationship types matter.
- Impact analysis, fraud rings, identity graph, permissions graph, recommendation graph, or dependency graph are central.

Watch:
- Using graph only because an ERD has relationships, unbounded traversals, missing direction/type semantics, and poor bulk analytics integration.

Typical candidates:
- Neo4j, JanusGraph, TigerGraph, Neptune, ArangoDB graph mode.

## Time-Series Databases
Best for timestamped measurements, metrics, IoT, telemetry, financial ticks, observability, and retention/downsampling.

Use when:
- Writes are append-heavy and queries are time-windowed.
- Retention policies, compression, downsampling, and tags are central.
- Dashboards and alerting need fast time-bucket aggregation.

Watch:
- High-cardinality tags, out-of-order writes, long retention without rollups, tenant leakage, and treating time-series as general OLTP.

Typical candidates:
- InfluxDB, TimescaleDB, Prometheus/Mimir/Thanos for metrics, ClickHouse for analytical time-series/logs, QuestDB.

## Columnar OLAP And Warehouses
Best for analytics over large datasets, aggregations, scans, BI, reporting, and event/log analysis.

Use when:
- Queries scan many rows and few columns.
- Compression, partition pruning, vectorized execution, materialized views, and batch/stream ingestion matter.
- Workload is analytical, not row-by-row transactional mutation.

Watch:
- OLTP writes, many small updates/deletes, too many tiny files/parts, bad partition keys, expensive joins, and missing cost controls.

Typical candidates:
- ClickHouse, Druid, Pinot, DuckDB for local analytics, BigQuery, Snowflake, Redshift, Synapse, Databricks SQL.

## Big Data, Lakehouse, And Object Storage
Best for large-scale raw/curated data, batch processing, ML features, archival, cross-engine analytics, and data products.

Use when:
- Object storage economics and open table formats matter.
- Data needs lineage, schema evolution, partition evolution, compaction, and time travel.
- Spark/Flink/Trino/Presto/Beam or similar engines process the data.

Watch:
- Small-file explosion, missing catalog, schema drift, no quality gates, unclear ownership, and "data lake" becoming ungoverned dumping.

Typical candidates:
- S3/GCS/Azure Blob plus Iceberg/Delta/Hudi, Hive metastore or catalog, Spark, Flink, Trino/Presto, Kafka/Pulsar for ingestion.

## Object-Oriented And Multi-Model Databases
Use carefully.

Object-oriented databases can fit object persistence and niche domain models, but are often risky for broad team adoption, reporting, integration, and migration. Multi-model databases can reduce system count but can also blur ownership and create lowest-common-denominator design.

Choose them only when:
- The specific model mix is central to the product.
- Operational maturity, query behavior, backup/restore, and team skill are proven.
- Exit strategy and data export are acceptable.
