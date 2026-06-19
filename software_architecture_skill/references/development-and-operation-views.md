# Development And Operation Views

Use these optional views when architecture decisions affect implementation organization or production operation. They complement functional, information, behavior, and deployment views.

## Development View

Development view describes the static implementation structure developers work in:
- repositories and deployables;
- modules, packages, namespaces, libraries, generated code, and shared components;
- dependency direction and allowed imports;
- build/test boundaries;
- ownership and review paths;
- architecture fitness functions.

Produce a development view when:
- multiple teams contribute to the same codebase;
- modular monolith or microservices boundaries must be enforced;
- source layout must align with domains/subdomains/components;
- generated code, SDKs, plugins, or shared libraries affect architecture;
- code-level metrics or constraints are part of governance.

Development view checklist:
- Logical components map to paths/packages/services.
- Dependency rules are explicit.
- Shared libraries have limited responsibility and owner.
- Test boundaries match architecture boundaries.
- CI checks enforce the highest-risk constraints.

## Operation View

Operation view describes how the system is run, observed, repaired, upgraded, and governed in production:
- startup/shutdown and readiness;
- backup, restore, archival, and data retention;
- deployment, migration, rollback, and upgrade procedures;
- monitoring, alerting, SLOs, runbooks, and incident response;
- key/secret/certificate rotation;
- tenant/customer operations;
- batch jobs, schedulers, maintenance windows, and operator workflows.

Produce an operation view when:
- availability, recovery, observability, compliance, or operational safety matters;
- architecture tactics introduce operational procedures;
- upgrades/migrations are risky;
- security controls require audit, key rotation, or incident response;
- managed services or external dependencies affect production behavior.

Operation view checklist:
- Each critical runtime component has health, metrics, logs, and traces.
- Each data store has backup/restore and retention behavior.
- Each deployment has rollback or forward-fix strategy.
- Each secret/key/certificate has rotation and ownership.
- Each alert has an owner and response path.
- Each operational control has verification evidence.

## View Integration

Connect development and operation views back to other views:

| Source Decision | Development View Impact | Operation View Impact |
|---|---|---|
| Modular monolith | Package/module boundaries, dependency tests | Release coordination, operational blast radius |
| Microservices | Repo/service boundaries, contract tests | Service ownership, observability, incident routing |
| Event-driven flow | Producer/consumer packages, schema ownership | Replay, DLQ handling, lag alerts |
| IAM/security | Policy modules, enforcement/audit code paths | Key rotation, audit retention, incident response |
| Performance tactic | Benchmark harness, hot-path ownership | Capacity planning, autoscaling, SLO alerts |
| Data resilience | Repository/storage modules | Backup, restore, failover, RPO/RTO exercises |

Do not create these views as separate paperwork if they duplicate deployment or implementation plans. Create them when they reveal decisions that would otherwise be invisible.
