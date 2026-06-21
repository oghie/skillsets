# Performance, Indexing, And Query Optimization

## Performance Triage Order
1. Reproduce the symptom: query, endpoint, job, dashboard, or incident.
2. Define the metric: p50/p95/p99 latency, throughput, lock wait, CPU, memory, disk I/O, network, cache hit, queue lag, compaction, replication lag, or error rate.
3. Isolate the layer: application, connection pool, query planner, locks, storage engine, buffer pool, filesystem, disk, network, replica, cache, or downstream system.
4. Capture evidence: `EXPLAIN`, actual plan, query stats, wait events, slow query logs, locks/deadlocks, top statements, index usage, row counts, histograms, and I/O stats.
5. Change one variable, benchmark, and keep rollback.

## Query Plan Review
Check:
- Is the plan using the expected index?
- Are estimated rows close to actual rows?
- Is the join order sensible?
- Are sorts/hashes spilling to disk?
- Are filters applied early or late?
- Is a function/cast preventing index usage?
- Are statistics stale?
- Are partitions pruned?
- Is the query reading far more rows than returned?

## Index Design
Good indexes follow query predicates, join keys, ordering, uniqueness, and selectivity.

Consider:
- Composite index order: equality columns first, then range/sort columns when engine behavior supports it.
- Covering indexes for hot read paths.
- Partial/filtered indexes for skewed data.
- Unique indexes for invariants.
- Full-text/search indexes for language queries.
- HNSW/IVF/vector indexes for similarity search after recall/latency evaluation.
- BRIN or zone-map-like indexes for naturally ordered large append tables.

Avoid:
- Indexing every column.
- Duplicate or overlapping indexes.
- Indexes unused by any query or constraint.
- Indexes that make write-heavy workloads miss SLOs.
- Indexes whose maintenance cost exceeds query value.

## Partitioning And Sharding
Partitioning helps manage pruning, retention, maintenance, and large table operations. It is not automatically faster.

Sharding helps distribute load and data, but introduces:
- Cross-shard query complexity.
- Rebalancing and hot shard risk.
- Global uniqueness challenges.
- Transaction coordination.
- Operational tooling and incident complexity.

Pick shard/partition keys from:
- Query predicate frequency.
- Cardinality and distribution.
- Tenant size skew.
- Time retention.
- Write locality.
- Rebalancing plan.

## Caching
Define the cache pattern:
- Cache-aside: app reads cache, misses to DB, then fills cache.
- Read-through: cache layer loads from source.
- Write-through: write cache and source synchronously.
- Write-behind: cache accepts write and later persists; dangerous without durable queue and replay.
- Refresh-ahead: preload hot data before expiry.

Mitigate:
- Stampede with request coalescing, jittered TTLs, and locks.
- Stale data with versioning, invalidation events, or bounded TTL.
- Hot keys with sharding, local cache, or pre-aggregation.
- Authorization leakage by including tenant/user/security context in cache key or cache value contract.

## Storage Engine Concerns
- B-tree-oriented engines favor indexed point/range access and transactional workloads.
- LSM/SSTable engines favor write throughput and sequential writes but need compaction management.
- Columnar engines favor scans, compression, vectorized execution, and aggregates.
- In-memory engines favor low latency but require explicit durability and memory pressure strategy.
- Search/vector engines need index build, merge/compaction, refresh, segment, and recall behavior understood.

## Benchmark Discipline
- Use realistic data volume and skew.
- Include warm and cold cache tests.
- Measure p95/p99, not only average.
- Include writes, reads, maintenance, compaction, backup, and failover where relevant.
- Validate correctness after load.
- State the hardware, OS, filesystem, DB config, schema, indexes, client concurrency, and dataset generator.

## Performance Red Flags
- Tuning without a query plan.
- A single metric presented as proof.
- Benchmark dataset has no skew or realistic cardinality.
- Hot partition/key ignored.
- Cache added before fixing bad access pattern.
- Read replicas used to hide primary write bottlenecks without understanding lag.
- Scale-out proposed before vertical headroom, schema, and index issues are measured.
