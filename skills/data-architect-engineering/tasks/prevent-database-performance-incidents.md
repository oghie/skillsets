# Prevent Database Performance Incidents

Use this playbook before schema releases, query releases, traffic growth, migrations, new background jobs, or datastore changes.

1. Inventory high-risk operations.
   - List hot reads, writes, updates, deletes, DDL, background jobs, analytics scans, queue consumers, and API endpoints.
   - Verify: each operation has expected cardinality, frequency, concurrency, timeout, and data growth assumption.

2. Predict failure modes.
   - Evaluate locking, blocking, deadlocks, slow query, connection exhaustion, high I/O wait, bad queries, full table scans, and data-growth regression.
   - Verify: each risk has trigger, evidence, prevention, mitigation, durable fix, rollback, and owner.

3. Review physical evidence.
   - Check actual plans, indexes, stats, row estimates, buffer/cache behavior, lock waits, WAL/checkpoint behavior, temp spills, and I/O latency.
   - Verify: no recommendation relies on TPS/QPS alone.

4. Add guardrails.
   - Add statement timeout, lock timeout, pool limits, backpressure, query review, migration lock analysis, slow-query logging, and retry/idempotency rules.
   - Verify: guardrails fail safely and do not corrupt data.

5. Test with realistic data.
   - Use production-like volume, skew, tenant distribution, cold/warm cache, concurrent writes, long transactions, and migration/backfill load.
   - Verify: p95/p99, rows read/returned, waits, I/O, pool wait, and error rate are captured.

6. Ship with rollback.
   - Define rollout phases, abort thresholds, dashboards, responder actions, rollback script/path, and communication owner.
   - Verify: rollback was tested or its constraints are explicitly accepted.
