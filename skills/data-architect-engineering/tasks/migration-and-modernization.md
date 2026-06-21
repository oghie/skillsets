# Migration And Modernization

## Step
1. Inventory source system: schema, data volume, constraints, procedures, triggers, jobs, reports, integrations, users, privileges, backup, and operational runbooks.
2. Classify source-of-truth vs derived data.
3. Identify legacy semantics: collation, timezone, decimal precision, nulls, identity keys, isolation, locking, batch windows, and stored logic.
4. Profile migration dimensions beyond TPS/QPS: top query plans, data shape, skew, locks, WAL/binlog/logical replication, storage latency, network, memory, CPU, backup/restore, consumers, and operational history.
5. Design target model and compatibility layer.
6. Choose migration method: dump/load, CDC/Debezium, dual write, event replay, backfill, strangler, or parallel run.
7. Build validation: row counts, checksums, referential integrity, sampled business invariants, query parity, CDC replay, delete propagation, and performance.
8. Plan cutover: freeze, sync, shadow reads, traffic switch, rollback, and decommission.

## Check
- Is the target actually better for the workload?
- Are old reports and downstream users included?
- Are stored procedures/triggers translated or retired deliberately?
- Are data types and precision safe?
- Are backup/restore and audit requirements preserved?
- Is rollback possible after writes start on the target?
- Are CDC offsets, schema history, source log retention, and sink idempotency safe if Debezium or another CDC tool is used?

## Validate
- Rehearse migration on a production-like dataset.
- Compare source and target with deterministic checks.
- Run top workload on target.
- Test failure in the middle of migration.
- Test rollback or roll-forward.
- Test restore of target after cutover.
- Test CDC lag, replay, duplicate handling, deletes, and schema changes if CDC is in scope.

## Ship
Deliver:
- Migration runbook.
- Compatibility and cutover plan.
- Data validation report.
- Risk register.
- Decommission checklist.
