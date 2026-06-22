# Task: Microservices Pattern Architecture Design

## Goal
Design, review, or modernize a microservice architecture with explicit pattern choices and coding-ready consequences.

## Required Inputs
- Business goal, stakeholder requirements, use cases, and sector/context.
- Current state: greenfield, modular monolith, monolith, distributed monolith, SOA, or existing microservices.
- Critical workflows, commands, queries, and external clients.
- Data ownership, consistency expectations, and transaction boundaries.
- Team topology, release pain, operations maturity, CI/CD, observability, and on-call ownership.
- NFR scenarios: availability, latency, throughput, auditability, security, privacy, modifiability, deployability, and cost with workload, p95/p99, RTO/RPO, WBS/PERT, or TCO assumptions where relevant.

## Steps
1. State the strongest reason not to use microservices.
2. Decide architecture path: modular monolith, service-oriented design, microservices, or incremental strangler migration.
3. Identify service boundaries using business capability/subdomain, system operations, data ownership, and team ownership.
4. Choose communication patterns: synchronous call, messaging, pub/sub, request/async response, service discovery, circuit breaker.
5. Choose data consistency patterns: local transaction, outbox, saga choreography/orchestration, event sourcing, or explicit rejection.
6. Choose query patterns: direct read, API composition, CQRS/materialized view, or query service, including projection rebuild, lag, freshness, and stale-read contract.
7. Choose external API pattern: direct API, API gateway, BFF, public API module, or protocol adapter.
8. Add development and operation views: repository/package/service boundaries, dependency constraints, architecture-as-code fitness functions, health/readiness, logs, metrics, traces, exception tracking, audit logs, external config, contract tests, runbooks, failure model, recovery, backup/restore, and alert ownership.
9. Choose deployment/release pattern: container/VM/serverless, service mesh/sidecar if justified, traffic shifting, rollback.
10. Translate to coding tasks: contracts, schemas, migrations, service skeleton, outbox/inbox, saga state, tests, observability, deployment manifests.

## Verification
- Service boundaries are not technical layers.
- Service boundaries preserve coupling/cohesion and avoid low-cohesion technical splits.
- Each service owns its write data.
- Cross-service transactions have a saga or are rejected.
- Every event/API has a schema, owner, versioning, compatibility rule, and contract test.
- Every async path has idempotency, ordering assumption, retry, DLQ, and observability.
- Every service has health/readiness, metrics, logs, traces, ownership, and rollback.
- Availability-sensitive services define dependencies, failure modes, recovery path, RTO/RPO, and backup/restore evidence.
- Migration plan includes coexistence, ACL/integration glue, data cutover, and rollback when modernizing.

## Output
Use `templates/microservices-pattern-decision-matrix.md` and, when useful, `templates/mermaid-microservices-pattern-map.mmd`.
