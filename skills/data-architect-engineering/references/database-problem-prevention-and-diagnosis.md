# Database Problem Prevention And Diagnosis

Use this before shipping a database design, schema change, query change, migration, or traffic growth plan. The goal is to predict failure modes early and define evidence, guardrails, and recovery actions.

## Critical View
Do not reduce every database problem to "add an index" or "scale the server". Locking, blocking, deadlocks, slow queries, connection exhaustion, high I/O wait, bad queries, full table scans, and data-growth regressions are often coupled. A query can be slow because the plan changed, because the working set no longer fits memory, because statistics are stale, because it waits on locks, because a checkpoint is flushing dirty pages, or because the app exhausted the connection pool and amplified retries.

## Preventive Baseline
Before production:
- Define top read/write paths and expected cardinality.
- Capture expected p50/p95/p99 and timeout budget.
- Capture table/partition growth and tenant/key skew.
- Require actual plan review for hot queries.
- Require index and constraint review for each access path.
- Set connection pool limits lower than database capacity.
- Add lock wait, deadlock, slow query, buffer/cache hit, I/O latency, checkpoint/WAL, replication lag, and pool wait metrics.
- Test with realistic data volume and skew, not only empty or tiny data.
- Test cold cache, warm cache, long transactions, DDL, backfill, and failover where relevant.
- Define rollback and kill-session policy before incidents happen.

## Problem Matrix
| Problem | Definition | Typical evidence | Prevention | First response |
| --- | --- | --- | --- | --- |
| Locking | Transactions hold locks that protect rows/pages/tables/metadata. | Lock wait metrics, blocked sessions, long transactions, DDL waiting. | Short transactions, stable lock order, correct isolation, online DDL, explicit `FOR UPDATE` only when needed. | Identify blocker, protect data safety, cancel/kill only after understanding transaction role. |
| Blocking | One session prevents others from progressing. | Wait graph, many sessions waiting on one PID/query, pool saturation. | Timeouts, bounded transactions, lock-aware migrations, background job throttling. | Stop new load, resolve blocker, lower concurrency, retry idempotently. |
| Deadlocks | Transactions wait on each other in a cycle. | Deadlock logs, aborted victim transactions, retry spikes. | Consistent access order, smaller transactions, proper indexes for update/delete predicates, avoid user interaction inside txn. | Ensure app retries safe transactions; inspect deadlock graph; change access order or predicates. |
| Slow query | Query exceeds latency/error budget. | Slow query log, actual plan, wait events, p99 increase. | Plan review, statistics maintenance, bounded result sets, indexes, partition pruning, query budgets. | Compare estimated vs actual rows, check waits, check recent stats/schema/data growth/deploy. |
| Connection exhaustion | Clients use or wait for more DB connections than available. | Pool wait, max connections reached, idle-in-transaction, many idle sessions, app timeouts. | Pool sizing, backpressure, timeouts, transaction hygiene, worker concurrency limits. | Stop retry storm, reduce concurrency, terminate idle-in-transaction if safe, fix leak. |
| High I/O wait | CPU waits on storage reads/writes/fsync. | Host iowait, disk queue depth, p99 storage latency, low cache hit, WAL fsync spikes. | Working-set sizing, indexes, partitioning, direct I/O/page-cache policy, checkpoint tuning, storage headroom. | Identify read vs write vs fsync vs temp spill; reduce scan/spill load; add IOPS only if access path is sane. |
| Bad queries | Query shape is logically or operationally harmful. | `SELECT *`, unbounded result, non-sargable predicate, N+1, leading wildcard, implicit cast, Cartesian join. | Query review, linting, ORM safeguards, pagination, parameterization, safe defaults. | Patch query shape; add guardrails; only index after query semantics are correct. |
| Full table scan | Plan reads whole table or partition. | Sequential scan, high rows read vs returned, buffer churn, I/O spike. | Proper predicates, indexes, partition pruning, zone maps/BRIN, bounded analytics path. | Determine if scan is expected; if not, fix predicate/index/stats/cast/partitioning. |
| Data-growth regression | Query was fast at small scale but degrades as rows, tenants, or partitions grow. | Latency grows with table size, plan flip, cache miss increase, index bloat, skewed tenant. | Model cardinality early, load-test at projected size, use composite indexes, archive/partition, monitor bloat. | Reproduce with production-sized data; compare plan over time; fix access path or data layout. |

## Locking And Blocking
Prevent:
- Keep transactions short and avoid remote calls, file I/O, UI pauses, or user prompts inside transactions.
- Access shared resources in a consistent order.
- Add indexes for `UPDATE`, `DELETE`, and `SELECT ... FOR UPDATE` predicates so locks target fewer rows.
- Use lock timeouts and statement timeouts with application-level idempotency.
- Use online schema changes or phased migrations for DDL.

Diagnose:
- Find blocker and blocked sessions.
- Capture transaction age, query text, lock mode, relation/object, wait event, application name, and client.
- Separate lock waits from latch/internal waits.
- Check whether the blocker is doing useful work, stuck, idle in transaction, or waiting on I/O.

Solutions:
- Commit/rollback stuck application transaction.
- Cancel a statement before killing a session when possible.
- Reduce batch size or concurrency.
- Add missing index for lock-targeting predicate.
- Reorder writes or split transaction boundaries.

## Deadlocks
Prevent:
- Use one resource acquisition order across code paths.
- Keep write sets small.
- Avoid read-modify-write patterns without clear lock semantics.
- Add uniqueness and foreign-key indexes where the engine needs them for efficient checks.
- Ensure retries are idempotent and bounded.

Diagnose:
- Read the deadlock graph.
- Identify both transactions, statements, lock types, objects, and access order.
- Check if one query scans too many rows before updating.

Solutions:
- Change access order.
- Narrow predicates with indexes.
- Reduce transaction size.
- Move unrelated writes out of the same transaction.
- Add safe retry with jitter for retryable deadlock victims.

## Slow Query
Prevent:
- Require actual plan review for hot queries.
- Keep statistics fresh.
- Avoid non-sargable predicates: functions on indexed columns, implicit casts, leading wildcard patterns, mismatched collations.
- Avoid unbounded sort, offset pagination at large offsets, and `SELECT *` on wide rows.
- Use query budgets in CI or staging for critical paths when feasible.

Diagnose:
- Compare current actual plan with historical plan.
- Compare estimated vs actual rows.
- Inspect waits: CPU, I/O, lock, network, temp spill, WAL/fsync.
- Check parameter sensitivity and tenant skew.
- Check whether a prepared statement uses a generic plan that is bad for skewed parameters.

Solutions:
- Rewrite predicate or join.
- Add/adjust composite, covering, partial, BRIN/zone-map-like, or specialized index where justified.
- Refresh statistics or increase statistics target for skewed columns where engine supports it.
- Partition/archive when pruning or retention is the real issue.
- Materialize or pre-aggregate when repeated expensive computation is legitimate.

## Connection Exhaustion
Prevent:
- Size app pools from database capacity, not from app worker count.
- Use one pool per process/service with clear max, idle timeout, acquisition timeout, and transaction timeout.
- Avoid connection-per-request patterns in high-concurrency apps.
- Add backpressure before the database is saturated.
- Monitor idle-in-transaction, active sessions, pool wait, and rejected acquisitions.

Diagnose:
- Count active, idle, idle-in-transaction, waiting, and long-running sessions.
- Check retry storms and app autoscaling events.
- Check leaked transactions and code paths missing release/close.

Solutions:
- Reduce app concurrency and retry rate.
- Fix connection leaks.
- Terminate idle-in-transaction sessions if safe.
- Add pooling proxy only when it matches transaction/session semantics.
- Split read/write workloads only after primary bottleneck is understood.

## High I/O Wait
Prevent:
- Keep hot working set in memory where expected.
- Avoid plans that read many more rows/pages than returned.
- Bound sort/hash temp spills.
- Reserve disk headroom for WAL, checkpoints, vacuum/compaction, index builds, and restore.
- Use storage with p99 latency appropriate to workload.

Diagnose:
- Separate data reads, index reads, temp reads/writes, WAL fsync, checkpoint flush, swap, and backup I/O.
- Check buffer/cache hit ratio and eviction churn.
- Check checkpoint timing vs latency spikes.
- Check full table scans and temp spills.

Solutions:
- Fix access path before buying hardware.
- Add memory only when working-set evidence supports it.
- Add or adjust indexes/partitioning when scans are accidental.
- Tune checkpoint/writeback carefully and verify recovery impact.
- Move analytical scans away from OLTP primary when isolation is required.

## Full Table Scan
Full table scans are not always bad. They can be correct for small tables, low-selectivity predicates, columnar analytics, or maintenance. They are bad when they surprise an OLTP path or read far more data than the result requires.

Prevent:
- Query matrix includes predicate and expected cardinality.
- Indexes match equality/range/sort pattern.
- Partition keys align with retention and query windows.
- Type/collation/cast compatibility is tested.

Diagnose:
- Is the scan table small, or has it grown?
- Is selectivity low enough that scan is rational?
- Did stats go stale?
- Did an implicit cast or function disable index use?
- Is partition pruning failing?

Solutions:
- Fix predicate shape.
- Add correct index or partitioning.
- Refresh stats.
- Rewrite query to become sargable.
- Route analytics to OLAP/read model when full scans are legitimate but harmful to OLTP.

## Data-Growth Regression
Prevent:
- Test with projected 10x and 100x data where growth is plausible.
- Include skew: one large tenant, hot key, heavy time range, popular status.
- Track rows read vs rows returned.
- Track index/table bloat and stats drift.
- Define archival, partitioning, rollup, or lifecycle policy before tables become unbounded.

Diagnose:
- Compare plan at small vs current data size.
- Compare cardinality estimate error.
- Check whether old index order no longer matches dominant queries.
- Check if offset pagination, sorting, grouping, or joins grow superlinearly.

Solutions:
- Change access path and index order.
- Use keyset pagination instead of deep offset pagination.
- Partition by time/tenant only if it supports pruning and operations.
- Add summary tables/materialized views for repeated aggregations.
- Move historical/cold data to cheaper analytical storage when OLTP no longer needs it.

## Preventive Output Standard
For each predicted problem, output:
- `Risk`: concise failure mode.
- `Trigger`: condition that makes it likely.
- `Evidence to collect`: metric/log/plan/query needed.
- `Prevention`: design or guardrail before release.
- `Mitigation`: safe immediate response.
- `Fix`: durable schema/query/app/infra change.
- `Rollback`: how to undo if the fix is wrong.
- `Owner`: app, DBA/DBRE, platform, data, or security.
