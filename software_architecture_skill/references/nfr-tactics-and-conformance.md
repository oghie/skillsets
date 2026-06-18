# NFR Tactics And Conformance

Non-functional requirements must become measurable scenarios, architecture tactics, impacted views, and verification evidence.

## NFR Scenario Template

```markdown
| ID | Quality Attribute | Stimulus | Environment | Response | Target | Priority | Source |
|---|---|---|---|---|---|---|---|
```

Good NFRs have a trigger, context, response, and measurable target. "Fast", "secure", "scalable", and "reliable" are not requirements until quantified.

## Facts, Policies, Criteria, Tactics

Use this chain:

```text
Fact or policy
  -> desirable criterion
  -> candidate tactics
  -> selected tactics
  -> impacted architecture views
  -> verification evidence
```

Examples:
- Fact: users include external partners. Criterion: partner access is controlled and auditable. Tactics: OAuth/OIDC, scoped tokens, audit logging, rate limits, tenant isolation.
- Policy: customer data must be retained for a limited time. Criterion: data lifecycle is enforceable. Tactics: retention jobs, deletion API, archival tiers, audit trail.
- Fact: checkout flow is revenue critical. Criterion: payment failures are recoverable. Tactics: idempotency keys, retries with budgets, outbox, compensation, operator alerting.

## Tactic Catalog

| Attribute | Candidate Tactics |
|---|---|
| Performance | Profiling, indexing, caching, batching, pooling, async processing, compression, pagination, load shedding, backpressure |
| Scalability | Stateless services, horizontal scaling, partitioning, sharding, read replicas, queueing, autoscaling, CDN/edge, bounded contexts |
| Availability | Redundancy, failover, health checks, circuit breakers, graceful degradation, multi-zone deployment, backup/restore, disaster recovery |
| Reliability | Idempotency, retries with budgets, timeouts, sagas, outbox pattern, dead-letter queues, reconciliation jobs, invariant checks |
| Security | Least privilege, authentication, authorization, MFA/step-up, session revocation, token rotation, input validation, encryption, secrets management, audit logs, threat modeling |
| Privacy | Data minimization, consent, purpose limitation, retention/deletion, pseudonymization, residency controls, access review |
| Observability | Structured logs, metrics, traces, correlation IDs, service-level indicators, alerts, dashboards, runbooks |
| Modifiability | Cohesion, dependency inversion, adapters, stable interfaces, feature flags, plugin boundaries, automated regression tests |
| Deployability | CI/CD, infrastructure as code, immutable artifacts, canary, blue/green, rollback, migration automation, environment parity |
| Usability | Task flow simplification, clear feedback, accessibility, responsive behavior, error recovery, usage analytics |
| Interoperability | Versioned APIs, schema registry, protocol adapters, contract tests, backwards compatibility, gateway mediation |
| Cost | Right-sizing, autoscaling limits, storage lifecycle, queue buffering, sampling, reserved capacity, cost observability |

## Conformance Map

Use this map to prove that quality concerns changed the design:

```markdown
| NFR | Facts/Policies | Criteria | Selected Tactics | Functional Impact | Information Impact | Behavior Impact | Deployment Impact | Verification |
|---|---|---|---|---|---|---|---|---|
```

Fill all impacted views. A tactic that has no impact is usually not a tactic; it is an intention.

## Tactic Evaluation

Evaluate each candidate tactic against:
- Effectiveness for the target scenario.
- Side effects on other NFRs.
- Implementation complexity.
- Operational burden.
- Cost.
- Team capability.
- Migration and rollback risk.
- Testability.

## Common NFR Findings

- Performance target without workload model.
- Availability target without dependency failure analysis.
- Security claim without trust boundaries and authorization model.
- IAM design without token/session expiry, revocation, MFA recovery, admin authorization, and audit events.
- Scalability claim with shared mutable state and no partition strategy.
- Event-driven reliability claim without idempotency and replay policy.
- Cache tactic without invalidation and consistency rules.
- Compliance claim without retention, access, audit, or evidence plan.
- Observability plan limited to logs with no metrics, traces, or alerts.

## Verification Examples

| Attribute | Evidence |
|---|---|
| Performance | Benchmark, trace, profiling result, load test, query plan |
| Availability | Failure injection, failover exercise, backup restore, SLO/error budget |
| Security | Threat model, security test, access review, audit log sample |
| Privacy | Data inventory, retention test, deletion proof, access trace |
| Modifiability | Dependency check, module boundary test, refactor spike |
| Deployability | Canary result, rollback test, migration dry run |
| Observability | Dashboard, alert firing test, trace sample, incident drill |
