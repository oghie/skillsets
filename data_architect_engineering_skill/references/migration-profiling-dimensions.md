# Migration Profiling Dimensions

TPS and QPS are insufficient. Profile the system as data, workload, engine, infrastructure, operations, and consumers.

## Workload Profile
- Read/write ratio by endpoint/job.
- Top queries by total time, p95/p99, calls, rows read, rows returned, temp spill, and lock wait.
- Query shape: point lookup, range scan, join, aggregate, search, vector, graph, batch scan.
- Parameter skew and tenant skew.
- Burst pattern, peak windows, batch jobs, cron jobs.
- Connection concurrency and pool wait.
- Transaction duration and statements per transaction.
- Error and retry rates.

## Data Shape Profile
- Table/collection sizes.
- Row/document size distribution.
- Index size and bloat.
- Cardinality and histograms for predicates.
- Null/default distribution.
- Largest tenant/key/partition.
- Growth rate and retention.
- LOB/BLOB/object references.
- Compression ratio.
- Data quality errors and orphan records.

## Engine Profile
- Query plans and estimate error.
- Buffer/cache hit ratio.
- Checkpoint, redo/WAL/binlog volume, fsync latency.
- Lock waits, deadlocks, MVCC bloat, vacuum/compaction debt.
- Replication lag and apply rate.
- Isolation level usage.
- Stored procedures, triggers, functions, sequences, generated columns.
- DDL lock behavior.

## Infrastructure Profile
- CPU utilization, run queue, IPC, cache miss, SIMD/vectorization where available.
- Memory working set, page faults, NUMA locality, swap.
- Disk IOPS, throughput, queue depth, p99 latency, write amplification.
- Filesystem, RAID, volume type, snapshot behavior.
- Network RTT, packet loss, bandwidth, TLS overhead.
- VM/container noisy neighbor and cgroup limits.
- Kernel logs, device SMART/NVMe health, thermal throttling.

## Operational Profile
- Backup duration, restore duration, and restore success.
- Maintenance windows.
- Failover time and operator steps.
- Monitoring coverage.
- On-call incident history.
- Upgrade cadence.
- Security grants and audit.
- Cost by compute, storage, IOPS, egress, licenses, and labor.

## Consumer Profile
- Apps, reports, analysts, pipelines, exports, search indexes, caches, vector stores, warehouses.
- Direct database readers.
- SLA per consumer.
- Compatibility with target dialect/schema.
- Cutover and rollback tolerance.

## Migration Readiness Output
Produce:
- Baseline dashboard.
- Top workload matrix.
- Data risk register.
- Compatibility gap list.
- Backfill and CDC capacity estimate.
- Cutover window estimate.
- Rollback constraints.
- Validation plan.
