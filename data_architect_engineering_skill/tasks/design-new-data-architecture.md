# Design New Data Architecture

## Step
1. Define scope and data criticality.
2. Identify system of record, derived stores, and consumers.
3. Build workload matrix: reads, writes, analytics, search, graph, vector, stream, retention, and growth.
4. Build data model: conceptual, logical, and physical depth according to risk.
5. Select datastore class, then concrete candidate(s).
6. Define consistency, transaction, idempotency, and reconciliation rules.
7. Define security and governance controls.
8. Define reliability and operations: SLO/SLI, RPO/RTO, backup, restore, failover, monitoring, and runbooks.
9. Define infrastructure: deployment mode, OS/storage/network/hardware, scaling, orchestration.
10. Define validation: benchmark, failure test, restore drill, threat model, schema review, and migration if applicable.

## Check
- Does every query have a data owner, access path, and expected cardinality?
- Is each datastore either a source of truth or explicitly derived?
- Are transaction and consistency boundaries explicit?
- Are tenant/security boundaries enforced at every copy?
- Is there a restore-tested recovery plan?
- Is scale path vertical, horizontal, functional partitioning, sharding, or a deliberate combination?

## Validate
- Run representative queries with realistic data.
- Test backup and restore to RPO/RTO.
- Run failover or node-loss scenario if HA is claimed.
- Review threat model and privilege plan.
- Run capacity model with growth and retention.
- Use `scripts/data_architecture_static_audit.py` on the design doc.

## Ship
Deliver an ADR/RFC with:
- Decision and alternatives rejected.
- Workload and data model.
- Chosen datastore(s) and why.
- Consistency, security, reliability, monitoring, and scaling plan.
- Validation evidence and remaining risks.
