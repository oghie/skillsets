# Database Internals, Storage, Query, And Recovery Review

Use this playbook when a design, incident, migration, or stack choice depends on DBMS internals.

1. Define the path.
   - Trace one read, one write, one analytical scan, one index lookup, and one recovery path.
   - Verify: each path names logical object, physical page/key/segment, buffer/cache behavior, WAL/log behavior, and returned result.

2. Review storage engine fit.
   - Choose row/column/PAX, tuple/log/index-organized, B+Tree/LSM/hash/search/vector, compression, and large-value policy by workload.
   - Verify: workload has point/range/scan/write/compaction/GC evidence, not only TPS/QPS.

3. Review memory and I/O.
   - Profile working set, buffer pool, page cache, dirty pages, prefetch, replacement policy, scan bypass, temp spills, and storage queue.
   - Verify: p95/p99 read/write latency, cache hit, eviction, dirty flush, fsync/WAL, and temp I/O metrics exist.

4. Review execution path.
   - Inspect logical plan, physical plan, access methods, join strategy, pipeline breakers, parallelism, and optimizer statistics.
   - Verify: estimated vs actual rows, spill metrics, join skew, sort/hash memory, and index selectivity are documented.

5. Review concurrency.
   - Identify locks, latches, isolation level, deadlock behavior, MVCC version storage, GC/vacuum, and phantom/write-skew risk.
   - Verify: lock wait, deadlock, long transaction, vacuum/compaction lag, and retry behavior are observable.

6. Review recovery and CDC.
   - Map WAL/binlog/logical stream, checkpoint, backup, restore, PITR, CDC, outbox, and replay.
   - Verify: crash tests, restore tests, CDC replay, delete propagation, schema change handling, and reconciliation pass.

7. Review distributed boundary.
   - Identify partitioning, routing, replication, coordinator, commit protocol, consensus, distributed joins, and failover.
   - Verify: single-partition ratio, cross-partition transaction rate, replica lag, quorum/failover behavior, and rebalancing drill.

8. Ship the recommendation.
   - Output: `Facts`, `Assumptions`, `Risks`, `Decision`, `Rejected Options`, `Validation Plan`, `Rollback Plan`, `Operational Runbook`.
   - Verify: the recommendation can be falsified by concrete benchmark, plan, consistency, or restore evidence.
