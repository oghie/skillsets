# Data Model Review Checklist

## Ownership
- [ ] System of record is explicit.
- [ ] Derived stores are labeled.
- [ ] Data owner and on-call owner are known.

## Modeling
- [ ] Entities/aggregates/documents/nodes/series/vectors are defined.
- [ ] Keys are stable and scoped correctly.
- [ ] Relationships and invariants are explicit.
- [ ] Null/default semantics are defined.
- [ ] Cardinality and growth are estimated.

## Queries
- [ ] Top reads are listed with predicates, sort, cardinality, and latency target.
- [ ] Top writes are listed with transaction/idempotency requirements.
- [ ] Indexes or partition keys map to queries.
- [ ] Ad hoc/reporting needs are accounted for.

## Correctness
- [ ] Constraints or equivalent validations exist.
- [ ] Transaction boundaries are explicit.
- [ ] Retry/conflict/reconciliation behavior is explicit.
- [ ] Data quality checks exist.

## Security
- [ ] Data classification is known.
- [ ] Tenant boundary is enforced in all stores.
- [ ] Least privilege roles/grants are defined.
- [ ] Encryption/TLS/secrets/audit are covered.
- [ ] Retention/deletion propagates to derived stores.

## Reliability
- [ ] RPO/RTO are defined.
- [ ] Backup and restore are tested.
- [ ] Failover behavior is understood.
- [ ] Monitoring covers query, storage, replication, locks, and data freshness.

## Migration
- [ ] Compatibility window is defined.
- [ ] Backfill and validation are defined.
- [ ] Rollback or roll-forward is defined.
- [ ] Decommission criteria are defined.
