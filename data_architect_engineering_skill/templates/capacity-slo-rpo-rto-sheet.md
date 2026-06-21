# Capacity, SLO, RPO, And RTO Sheet

## Workload
- Service/data product:
- System of record:
- Critical users/consumers:
- Data classification:

## Current And Projected Data
- Current rows/documents/events/vectors:
- Current raw data size:
- Current index size:
- Daily/monthly growth:
- Retention:
- Largest tenant/partition/key:
- Cardinality risks:

## Traffic
- Reads/sec:
- Writes/sec:
- Peak concurrency:
- Active users:
- Concurrent users:
- Write-active users:
- Batch/stream ingest:
- Top queries/jobs:
- p50/p95/p99 target:
- Largest tenant/key/partition:
- Cache hit ratio:

## Reliability
- Availability SLO:
- RPO:
- RTO:
- Backup type/frequency:
- Last restore test:
- Failover mode:
- Corruption detection:

## Infrastructure
- Deployment:
- CPU/memory:
- Storage type and IOPS:
- Filesystem:
- RAID/replication:
- Network:
- Regions/AZs:

## Headroom And Limits
- CPU headroom:
- CPU cache/SIMD/NUMA concerns:
- Memory headroom:
- Working set in pages:
- Buffer pool/cache hit target:
- Disk headroom:
- IOPS headroom:
- Connection pool:
- WAL/binlog/logical replication headroom:
- Dirty page/checkpoint headroom:
- Temp spill headroom:
- Vacuum/compaction debt:
- Replication lag threshold:
- Restore/recovery time evidence:
- Cost threshold:

## Validation
- Load test:
- Restore drill:
- Failover test:
- Query plan review:
- Security review:
