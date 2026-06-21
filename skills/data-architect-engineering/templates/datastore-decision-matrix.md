# Datastore Decision Matrix

| Dimension | Requirement | Candidate A | Candidate B | Candidate C | Notes |
| --- | --- | --- | --- | --- | --- |
| Workload | OLTP/OLAP/HTAP/search/vector/graph/time-series/cache | | | | |
| System of record | Yes/no/derived | | | | |
| Data model fit | Relational/document/key/graph/vector/etc. | | | | |
| Top reads | Query shapes and p99 target | | | | |
| Top writes | Commands, rate, idempotency | | | | |
| Consistency | Isolation/staleness/conflict model | | | | |
| Transactions | Scope and limits | | | | |
| Scale path | Vertical/horizontal/shard/partition | | | | |
| Security | Roles, tenant isolation, encryption, audit | | | | |
| Reliability | RPO/RTO, HA, backup/restore | | | | |
| Operations | Team skill, tooling, upgrades, runbooks | | | | |
| Migration | Import/export, compatibility, rollback | | | | |
| Cost | Compute, storage, replicas, egress, labor | | | | |
| Lock-in | Exit path and data portability | | | | |
| Verification needed | Current limits/licensing/versions | | | | |

## Decision
- Selected:
- Rejected alternatives:
- Main trade-off:
- Validation plan:
- Rollback/exit plan:
