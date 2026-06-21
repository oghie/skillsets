# Reliability, Operations, And Monitoring

## DBRE Principles
- Protect the data.
- Build self-service guardrails for scale.
- Eliminate toil through automation.
- Treat database infrastructure as software, while treating data as valuable and recoverable.
- Remove barriers between application engineering, operations, security, and data ownership.

## SLO And SLI
Define SLIs for:
- Availability: successful requests/queries/jobs.
- Latency: p50/p95/p99 by operation and user path.
- Throughput: reads/writes/events/rows/files per second.
- Durability: acknowledged writes, backup success, restore success, data loss window.
- Freshness: replication lag, CDC lag, warehouse lag, search/vector index lag.
- Correctness: failed constraints, reconciliation diffs, data-quality failures.
- Cost/efficiency: compute, storage, IOPS, cache memory, query cost, egress.

## Operational Visibility
Collect:
- Application: query names, request IDs, tenant, latency, errors, retries, pool wait.
- Database: query stats, waits, locks, deadlocks, buffer/cache hit, checkpoint/journal/redo, transactions, connections, replication, compaction, index usage.
- Host: CPU, memory, disk utilization, IOPS, latency, queue depth, filesystem, network, kernel errors, time sync.
- Pipeline: lag, retries, dead-letter counts, schema failures, job duration, small files, compaction.
- Security: logins, failed auth, privilege changes, sensitive reads, export, deletion, admin actions.

## Backup And Recovery
Backup types:
- Physical vs logical.
- Online vs offline.
- Full, incremental, differential, WAL/binlog/archive log.
- Snapshots, object storage copies, and export dumps.

Recovery design:
- RPO and RTO per data class.
- Detection mechanism for deletion, corruption, and ransomware.
- Restore target environment.
- Point-in-time recovery when needed.
- Verification after restore: counts, checksums, invariants, sample queries, app smoke tests.
- Access controls for backup and restore.

Backup without restore proof is an assumption, not a control.

## Release And Migration Operations
Database releases need:
- Schema versioning.
- Backward/forward-compatible app code.
- Full dataset tests for risky migrations.
- Operational tests: backup, restore, failover, load, lock duration, replication lag.
- Online DDL or low-lock migration strategy.
- Rollout phases and abort criteria.
- Observability during cutover.

## Incident Troubleshooting
Use layered diagnosis:
1. What changed?
2. Which SLI is breached?
3. Which layer saturates: app, pool, DB, storage, network, cache, replica, pipeline?
4. Is the data safe?
5. Is the service up?
6. Are users or consumers in pain?
7. What mitigation reduces harm without corrupting data?

## Reliability Red Flags
- No RPO/RTO.
- Backup success is monitored but restore is never tested.
- Replica lag is unmonitored.
- Schema migrations run directly in peak traffic with no lock analysis.
- Manual failover steps known by one person.
- No runbook for corruption or accidental delete.
- Observability only at host level, no query-level or operation-level metrics.
- Database credentials or infra are managed outside version control and review.
