# Infrastructure, Storage, OS, And Hardware

## Deployment Options
- Embedded/local DB: lowest operational overhead, limited concurrency/distribution; good for local apps and edge cases.
- Single-node server: simple operations, strong local performance, vertical scaling.
- Primary/replica: read scaling and failover, but replication lag and split-brain must be handled.
- Sharded cluster: scale and isolation, but rebalancing and cross-shard operations are harder.
- Distributed consensus DB: strong replication semantics, but write latency and operational complexity increase.
- DBaaS: reduced toil, but service limits, cost, networking, backup, support, and lock-in must be verified.
- Kubernetes/operator: repeatable orchestration, but stateful workloads still need storage, backup, upgrade, and failure-domain discipline.

## OS And Host
Check:
- Linux distribution and kernel support.
- Filesystem choice and mount options.
- Time synchronization.
- ulimit, file descriptors, process limits.
- Transparent huge pages, swappiness, NUMA, CPU governor where relevant.
- I/O scheduler and block device settings.
- Network sysctls and connection tracking for high concurrency.
- Container limits vs actual DB memory needs.

This needs verification for engine-specific recommendations.

## Storage
Match storage to workload:
- HDD: cheap capacity, poor random I/O.
- SSD/NVMe: low latency and high IOPS for OLTP, compaction, and random reads.
- SAN/NAS: central manageability, but latency, noisy neighbors, and failure domains need evidence.
- Object storage: durable and cheap for lakehouse/backups, not a POSIX database disk.
- NVM/PMEM: specialized low-latency designs; validate engine support.

## RAID And Redundancy
- RAID is not a backup.
- RAID 1/10: common for latency and rebuild behavior.
- RAID 5/6: capacity efficient but rebuild and write penalty can hurt database workloads.
- Cloud disks use provider-level replication; still test snapshots and restore.
- Database-level replication may make local RAID choices different.

State:
- Failure domain covered by RAID.
- Failure domain covered by replication.
- Failure domain covered by backup.
- Restore path for accidental delete/corruption.

## Network
Check:
- Latency between app and DB.
- Latency between replication/consensus nodes.
- Bandwidth for backup, restore, rebalancing, compaction, and analytics export.
- TLS overhead and termination.
- MTU and packet loss.
- Load balancers, connection pooling, keepalive.
- RDMA/RoCE/InfiniBand only when engine and workload are designed to use them.

## Accelerators
- GPU/FPGA/ASIC can accelerate analytics, vector search, compression, or ML-adjacent pipelines.
- Do not add accelerators without profiling bottlenecks and confirming engine support.
- Include fallback, scheduling, driver, observability, and cost.

## Capacity Planning
Track:
- Data size now and growth rate.
- Index size.
- Write amplification.
- Compression ratio.
- Replication factor.
- Backup retention.
- Working set in memory.
- Peak concurrent queries.
- Maintenance windows.
- Rebuild/rebalance time.

## Infrastructure Red Flags
- Database on ephemeral disk without explicit durability.
- Object storage mounted as a normal DB data directory.
- Single AZ/region claimed as highly available.
- No storage latency metrics.
- No disk-space headroom for compaction, index builds, or restore.
- Kubernetes StatefulSet used without tested backup/restore and node failure drills.
- RAID used as a substitute for backup.
