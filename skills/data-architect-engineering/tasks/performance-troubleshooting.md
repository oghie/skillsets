# Performance Troubleshooting

## Step
1. State symptom and blast radius.
2. Confirm data safety before aggressive mitigation.
3. Gather evidence: top queries, plans, wait events, locks/latches, buffer pool/cache hit ratio, dirty pages, WAL/checkpoint pressure, compaction/vacuum lag, replication lag, disk I/O, CPU, memory, network, queue lag, and recent changes.
4. Locate bottleneck layer.
5. Form one or more hypotheses.
6. Test the least risky mitigation first.
7. Verify improvement and watch for regression.

## Check
- Is p99 or p95 affected, not only average?
- Is the query plan actual, not only estimated?
- Are statistics stale?
- Are estimated rows close to actual rows?
- Is a sequential scan, index scan, multi-index scan, join, sort, or aggregation spilling or reading far more pages than expected?
- Is there lock contention or deadlock?
- Is there latch contention on hot index/page/buffer structures?
- Is MVCC cleanup, vacuum, or compaction falling behind?
- Is replication lag making reads stale or slow?
- Is storage saturated, or is the buffer/page/cache policy causing avoidable I/O?
- Are checkpoints, WAL fsync, or dirty-page flushes aligned with latency spikes?
- Is cache masking a primary DB issue?
- Is a recent migration/index/deploy causing the regression?

## Validate
- Capture before/after metrics.
- Run `EXPLAIN` or equivalent.
- Test with representative parameters and tenant sizes.
- Confirm write impact of new indexes.
- Confirm index/storage changes do not increase write amplification, vacuum/compaction debt, or recovery time beyond SLO.
- Confirm cache invalidation if cache changes.
- Confirm rollback path.

## Ship
Report:
- Root cause confidence.
- Evidence.
- Mitigation applied or proposed.
- Residual risk.
- Follow-up preventive action.
