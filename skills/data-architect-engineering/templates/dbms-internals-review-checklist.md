# DBMS Internals Review Checklist

## Workload
- Read/write ratio:
- Point/range/scan/query mix:
- OLTP/OLAP/HTAP:
- Data size and working set:
- Hot keys/ranges/tenants:
- Latency SLO p50/p95/p99:
- RPO/RTO:

## Storage Engine
- Row/column/PAX:
- Tuple/log/index-organized:
- Page size and checksum:
- Page directory/free-space tracking:
- Slotted-page or equivalent layout:
- Large-value/overflow policy:
- Compression and encoding:
- Compaction/vacuum/rewrite policy:

## Buffer And I/O
- Buffer pool size:
- OS page cache/direct I/O policy:
- Replacement policy:
- Dirty page rate:
- Checkpoint/writeback policy:
- Prefetch/scan sharing/bypass:
- Temp spill location and limit:
- Storage p95/p99 latency:

## Indexes And Filters
- Primary/clustered index:
- Secondary indexes:
- Composite key order:
- Covering/include columns:
- Partial/filtered indexes:
- Bloom/filter/zone-map metadata:
- Vector/search index:
- Index maintenance cost:

## Query Execution
- Plan shape:
- Access methods:
- Join algorithm:
- Aggregation/sort strategy:
- Pipeline breakers:
- Vectorized/JIT execution:
- Parallelism/exchange:
- Estimated vs actual rows:

## Transactions
- Isolation level:
- Lock/latch hotspots:
- Deadlock policy:
- MVCC version storage:
- Vacuum/GC lag:
- Long transaction risk:
- Phantom/write-skew protection:

## Recovery
- WAL/binlog/logical log:
- Checkpoint policy:
- pageLSN/flushedLSN equivalent:
- Backup/PITR:
- Restore drill date:
- Crash test coverage:
- CDC/outbox replay:

## Distributed
- Partition key:
- Single-partition transaction ratio:
- Cross-partition joins:
- Replication mode:
- Commit/consensus protocol:
- Replica lag:
- Failover/fencing:
- Rebalancing plan:
