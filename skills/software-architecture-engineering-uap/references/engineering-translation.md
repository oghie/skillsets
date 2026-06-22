# Engineering Translation

Architecture is not done until it becomes implementable work with tests, operations, rollout, and ownership.

## ADR Template

```markdown
# ADR: <decision>

## Status
Proposed | Accepted | Superseded

## Context
- Facts:
- Constraints:
- Requirements/NFRs:
- Unknowns:

## Decision

## Alternatives Considered

## Consequences
- Positive:
- Negative:
- Follow-up work:

## Verification
```

## RFC Template

```markdown
# RFC: <title>

## Problem
## Goals
## Non-Goals
## Current State
## Proposed Architecture
## API/Event/Data Contracts
## Functional View Impact
## Information View Impact
## Behavior View Impact
## Deployment View Impact
## NFR Conformance
## Migration And Rollout
## Test Plan
## Observability And Operations
## Risks And Open Questions
```

## Repository Mapping

Map architecture to code:
- Components -> packages, modules, services, apps, libraries.
- Interfaces -> public APIs, ports/adapters, events, schemas, OpenAPI/GraphQL/protobuf contracts.
- Data components -> tables, collections, streams, stores, migrations, ownership docs.
- Behavior flows -> handlers, workflows, queues, jobs, state machines, orchestration/saga logic.
- Deployment view -> Dockerfiles, manifests, IaC, CI/CD, environment config, secrets, runbooks.
- NFR tactics -> tests, metrics, alerts, rate limits, auth policies, cache policies, resilience libraries.

For microservices, also map:
- service boundary -> business capability/subdomain owner and repository/package/deployable;
- local transaction -> database tables/collections and write authority;
- event/API contract -> schema/versioning, compatibility tests, and producer/consumer owners;
- saga/outbox/inbox -> state table, retry/DLQ/reconciliation jobs, idempotency keys, and observability;
- API gateway/BFF -> route ownership, composition code, auth/claims propagation, and backward compatibility;
- service readiness -> health/readiness, logs, metrics, traces, audit events, runbook, and alert owner.

## Implementation Plan Shape

```markdown
## Implementation Plan
1. Establish contracts and boundaries.
2. Add or refactor internal modules/components.
3. Add data migrations and compatibility layers.
4. Implement behavior flows and failure handling.
5. Add NFR tactics and observability.
6. Add tests and verification automation.
7. Roll out behind flags or staged deployment.
8. Monitor, validate, and clean up old paths.
```

## Test Strategy

| Concern | Test/Evidence |
|---|---|
| API contract | Contract tests, schema validation, backwards compatibility tests |
| Component logic | Unit and integration tests |
| Data migration | Migration dry run, rollback test, data validation |
| Behavior flow | Workflow tests, sequence scenario tests, failure injection |
| Event-driven behavior | Idempotency tests, replay tests, consumer contract tests |
| Performance | Benchmark, load test, query plan, trace |
| Security/privacy | Auth tests, authorization matrix, threat model, audit log check |
| Deployment | Smoke test, health checks, canary, rollback |
| Observability | Log/metric/trace assertions, alert firing test |

## Rollout And Migration

Always consider:
- Feature flags or compatibility mode.
- Data backfill and forward/backward-compatible migrations.
- Dual-write or read-switch strategy when needed.
- Canary or phased rollout.
- Rollback limits and irreversible steps.
- Monitoring windows and success metrics.
- Ownership for incident response.

## Definition Of Done

Architecture-to-engineering work is done when:
- Decisions are documented with rationale and alternatives.
- Components, data, behavior, and deployment impacts are clear.
- NFR tactics have measurable verification.
- Tests cover critical success and failure paths.
- Rollout, rollback, observability, and ownership are defined.
- Residual risks and revisit triggers are visible.
