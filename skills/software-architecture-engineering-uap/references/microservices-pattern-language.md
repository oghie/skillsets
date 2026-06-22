# Microservices Pattern Language

## Table Of Contents
- Core Rule
- Adoption Fit
- Existing-State Decision Matrix
- Sector And Business Forces
- Pattern Map
- Decomposition
- Communication And Reliability
- Data Consistency And Transactions
- Querying And Read Models
- External API
- Production-Ready Service Baseline
- Deployment And Release
- Refactoring From Monolith
- Coding Readiness
- Prompt Templates
- Red Flags

## Core Rule
Use microservices only when the business and operating forces justify distributed system cost. A microservice architecture is not a default upgrade from a monolith. It is a pattern language that must connect stakeholder requirements, business capability, use cases, data ownership, communication style, consistency model, deployment/release model, testing, observability, team ownership, cost estimation, and workload/performance evidence.

Do not recommend microservices because the user says "scalable", "modern", or "cloud native". First identify the real driver: independent delivery, team autonomy, scale isolation, fault isolation, technology diversity, regulatory isolation, or incremental legacy replacement.

For cost-sensitive or performance-sensitive decisions, require an estimate model: WBS or PERT-style delivery uncertainty, runtime TCO, resource usage, workload profile, queueing/load-test evidence, p95/p99 targets, and risk reserve.

## Adoption Fit
Prefer modular monolith or well-structured service-oriented design when:
- the domain is not understood yet;
- the team is small and one deployable gives faster learning;
- cross-service transactions would dominate normal workflows;
- operations, CI/CD, observability, and contract testing are immature;
- service boundaries would be based on technical layers instead of business capabilities;
- the current pain is poor modularity, not independent deployment.

Consider microservices when:
- different business capabilities need different delivery cadence, ownership, scaling, or reliability posture;
- multiple teams are blocked by one release train;
- a bounded context owns its data and can expose stable contracts;
- critical flows can tolerate local transactions plus sagas, outbox, compensation, or eventual consistency;
- production operation can support many deployables, service discovery, health checks, tracing, metrics, logs, versioned contracts, and rollback;
- legacy modernization can proceed incrementally using a strangler approach.

## Existing-State Decision Matrix
| Current condition | Safer architecture move | Why |
|---|---|---|
| Greenfield with unclear domain | Modular monolith first | Keep feedback fast until boundaries are proven. |
| Monolith with clear bounded contexts but slow release | Modularize then extract selected services | Avoid distributed monolith while proving boundaries. |
| Monolith with one high-value new feature | Strangler service around old system | Demonstrate value and reduce risk incrementally. |
| Shared database used as integration layer | Establish data ownership before extraction | Shared writes break service autonomy. |
| High-volume read model across domains | API composition or CQRS view | Avoid expensive joins across service APIs. |
| Cross-domain workflow with separate owners | Saga with local transactions | Avoid distributed transaction dependence. |
| Many client types with different needs | API gateway or BFF | Avoid forcing clients to compose many service calls. |
| Many services lack health, logs, metrics, traces | Production-readiness first | More services without observability amplify failure. |
| Tooling/platform immature | Build platform/chassis/golden path before broad extraction | Microservices require deployment and operations automation. |

## Sector And Business Forces
Map sector forces before selecting patterns:

| Sector/context | Architecture forces | Patterns to evaluate |
|---|---|---|
| Banking, fintech, insurance | auditability, idempotency, ledger integrity, regulatory evidence, fraud/risk isolation | saga, outbox, event sourcing where justified, audit logging, API gateway, contract tests, reconciliation |
| E-commerce/marketplace | order lifecycle, catalog/search/read volume, payment/inventory/shipping coordination, traffic spikes | decomposition by capability/subdomain, saga, CQRS, API composition, BFF, outbox, event-driven integration |
| Logistics/supply chain | long-running workflows, status events, external partners, geospatial/edge constraints | saga, domain events, anti-corruption layer, API gateway, event streaming, idempotent commands |
| Healthcare | privacy, audit trail, interoperability, critical workflow safety | bounded contexts, access token, audit logging, API gateway, contract tests, explicit data retention |
| Government/defense | sovereignty, procurement, audit, security classification, legacy integration | strangler, anti-corruption layer, API gateway, strict trust boundaries, deployment controls |
| Energy/manufacturing/OT | safety, latency, offline/edge operation, operational continuity | edge/service partitioning, async messaging, circuit breaker, local autonomy, observability, rollback |
| SaaS/B2B platform | tenant isolation, public API compatibility, customer assurance, extensibility | API gateway, BFF, tenant-aware services, service chassis, contract tests, audit logging |
| Media/education/content | traffic spikes, personalization, search/read-heavy workloads, cost sensitivity | CDN/edge integration, CQRS/read models, API composition, serverless/container deployment, rate limiting |

This table is a starting force map, not a sector stereotype. Validate actual business model, regulation, data sensitivity, latency, cost, and team structure.

## Pattern Map
| Problem | Pattern candidates | Key validation |
|---|---|---|
| Decide application architecture | monolith, modular monolith, microservice architecture | business complexity, team count, release pain, ops maturity |
| Split services | decompose by business capability, decompose by subdomain | bounded context, data ownership, cohesion, communication load |
| Synchronous call failure | circuit breaker, timeout, retry budget, bulkhead, fallback | partial failure behavior and user impact |
| Find service instances | self-registration, third-party registration, client-side/server-side discovery | platform fit, failure behavior, security |
| Reliable event publication | transactional outbox, polling publisher, transaction log tailing | atomicity with local DB, relay idempotency, duplicate handling |
| Cross-service transaction | saga choreography, saga orchestration | compensation, retry, semantic locks, monitoring |
| Rich domain logic | aggregate, domain model, domain event, event sourcing | invariants, event retention, replay, schema evolution |
| Cross-service query | API composition, CQRS/materialized view | latency, data freshness, consistency, rebuild path |
| Client-facing API | API gateway, BFF | client diversity, backward compatibility, ownership |
| Test distributed behavior | consumer-driven contract, consumer-side contract, service component test | producer/consumer compatibility and failure cases |
| Production readiness | health check API, logs, metrics, tracing, exception tracking, audit logging, externalized config, chassis | deployability and operability evidence |
| Deployment | container, VM, serverless, service mesh, sidecar | release strategy, traffic control, isolation, cost |
| Legacy migration | strangler, anti-corruption layer | coexistence, routing, domain translation, data migration |

## Decomposition
Start from system operations, not class diagrams. Identify commands and queries that matter architecturally, then map them to capabilities/subdomains and data ownership.

Decompose by business capability when the organization already understands stable business functions. Decompose by subdomain when domain modeling reveals bounded contexts with different models, lifecycles, or language.

Do not map each capability mechanically to one service. Some capabilities remain together when:
- they share invariants that must be transactionally enforced;
- communication between them would be too chatty;
- the team cannot operate the additional service;
- the capability is not yet stable;
- splitting would create a distributed monolith.

Boundary checklist:
- service owns its write model and database tables/collections;
- external access happens through API/events, not shared tables;
- service API expresses domain operations, not CRUD leakage by default;
- team ownership and on-call ownership are clear;
- service can be tested and deployed independently;
- data migration and compatibility path are defined.

## Communication And Reliability
Choose interaction style by semantics:

| Interaction | Use when | Required controls |
|---|---|---|
| Synchronous request/response | caller needs immediate answer and dependency is acceptable | timeout, retry budget, circuit breaker, fallback, correlation ID |
| Asynchronous messaging | work can continue later or caller should not block | durable broker, idempotent consumer, ordering rule, DLQ, replay, correlation ID |
| Publish/subscribe event | many consumers react independently | event schema/versioning, subscription ownership, replay and poison-message handling |
| Request/async response | long-running response must return to initiator | response channel, correlation ID, timeout, orphan response handling |

Do not add a broker to hide unclear ownership. A broker shifts coupling into message schema, ordering, delivery, and operations.

## Data Consistency And Transactions
Each service should execute local transactions over its own data. Avoid distributed transactions unless a specific platform/constraint makes them viable and the operational cost is accepted.

Use sagas when a business transaction spans multiple services:
- choreography: participants react to events; useful for simpler flows but harder to see centrally.
- orchestration: coordinator commands participants; useful for explicit sequencing and visibility.

Saga design checklist:
- local transaction per step;
- compensating transaction for undoable steps;
- retriable transaction for steps that must eventually succeed;
- semantic lock or pending state where user-visible inconsistency matters;
- idempotent commands/events;
- correlation ID and saga instance state;
- timeout, retry, dead-letter, and operator recovery path;
- audit and reconciliation for money, inventory, entitlement, or legal state.

Transactional messaging checklist:
- persist business state and outbox message in the same local transaction;
- relay publishes outbox messages at-least-once;
- consumers deduplicate by message ID or idempotency key;
- relay lag and failed publish counts are observable;
- replay and schema evolution are documented.

Minimal outbox shape:

```sql
CREATE TABLE foo_outbox (
  id UUID PRIMARY KEY,
  aggregate_type TEXT NOT NULL,
  aggregate_id TEXT NOT NULL,
  event_type TEXT NOT NULL,
  payload JSONB NOT NULL,
  created_at TIMESTAMPTZ NOT NULL,
  published_at TIMESTAMPTZ NULL
);
```

```text
local transaction:
  update aggregate
  insert outbox event
commit

relay loop:
  read unpublished events
  publish to broker
  mark published or retry

consumer:
  reject duplicate message_id
  apply idempotent state change
  record processed message_id
```

## Querying And Read Models
When a query needs data from multiple services, choose deliberately:

| Option | Use when | Risk |
|---|---|---|
| API composition | query is small, low latency budget is achievable, data freshness matters | fan-out latency, partial failure, expensive in-memory joins |
| CQRS/materialized view | query is frequent, joins are expensive, read model can be eventually consistent | projection lag, rebuild complexity, duplicate data governance |
| Query service | a dedicated service owns read API and projection | another deployable and ownership boundary |

CQRS checklist:
- command model owns writes and invariants;
- query model is read-only from client perspective;
- events update projections;
- projection lag is measured and acceptable;
- rebuild/backfill procedure exists;
- stale reads and read-your-write expectations are documented;
- separate stores are justified by query shape, scale, or model complexity.

## External API
Use an API gateway when external clients need a stable entry point, routing, API composition, authentication/authorization mediation, monitoring, or protocol translation.

Use Backends for Frontends when client types have materially different interaction needs. Avoid one central gateway team becoming an enterprise service bus bottleneck.

External API checklist:
- gateway responsibilities: routing, composition, authn/authz handoff, rate limiting, monitoring, protocol adaptation;
- non-responsibilities: owning all service business logic or hiding broken service boundaries;
- API modules or BFFs have clear owners;
- backward compatibility and versioning strategy are explicit;
- public APIs have stronger compatibility and deprecation policy than internal APIs;
- gateway failure, timeout, and fallback behavior is documented;
- user identity and claims propagation are explicit.

## Production-Ready Service Baseline
Every service needs:
- health/readiness endpoint;
- externalized configuration;
- structured logs with correlation IDs;
- metrics for request rate, error rate, latency, saturation, queue lag, outbox lag, and business counters;
- distributed tracing for cross-service flows;
- exception tracking or error aggregation;
- audit logging for user, admin, money, security, and compliance actions;
- contract tests for APIs/events;
- smoke/canary checks and rollback path;
- ownership, runbook, SLO, alert routing, and incident contact.

A microservice chassis or platform/golden path should provide these cross-cutting concerns consistently. Avoid rewriting the same operational plumbing in every service.

## Deployment And Release
Separate deployment from release:
1. deploy version without routing normal traffic;
2. smoke test in production;
3. release to a small audience or low-risk route;
4. increase traffic gradually;
5. revert traffic or rollback when checks fail.

Evaluate deployment options:
- language package: simple but weak isolation;
- VM: strong isolation but heavier operations;
- container: common baseline for service-per-container and orchestration;
- serverless: event/request-driven workloads with platform limits and vendor coupling;
- service mesh/sidecar: traffic management, mTLS, telemetry, retries, and circuit breaking outside application code, but with platform complexity.

Do not add a service mesh to compensate for unclear service boundaries or weak ownership.

## Refactoring From Monolith
Prefer strangler migration over big-bang rewrite for valuable existing systems.

Strangler checklist:
- route old and new functionality through an API gateway or routing layer;
- implement new capability as a service only when it is sufficiently independent;
- use integration glue: inbound adapters, outbound adapters, event publisher/subscriber adapters, and database adapters as needed;
- add an anti-corruption layer when legacy and new domain models differ;
- identify which data is read-only, read/write, replicated, or migrated;
- define coexistence period, cutover criteria, and rollback;
- keep domain translation explicit instead of leaking legacy names/status values into the new service.

## Coding Readiness
Before coding a microservice, produce:

```markdown
## Service Contract
- Service name and business capability:
- Owner/on-call:
- Commands:
- Queries:
- Events published:
- Events consumed:
- API versioning:
- Data owned:
- Local transaction boundary:
- Consistency model:
- Idempotency keys:
- Authorization model:
- Health/metrics/logs/traces:
- Contract tests:
- Deployment/release plan:
- Rollback/reconciliation:
```

Implementation guidance:
- define API/event/schema contracts before business code;
- implement local transaction and outbox before publishing events;
- make consumers idempotent before enabling retries;
- add health, metrics, logs, traces, and audit events in the first slice;
- write contract tests for every public API/event;
- include failure scenarios: timeout, duplicate message, out-of-order message, stale read, projection rebuild, compensation failure, and gateway fallback.

## Prompt Templates
Microservices fit review:

```text
Evaluate whether this system should use microservices, modular monolith, SOA, or another style.
Use business drivers, team topology, data ownership, transaction boundaries, operational maturity, sector forces, existing-state constraints, and migration cost.
Lead with the strongest reason not to use microservices. Then provide the smallest viable architecture path and validation steps.
```

Pattern selection:

```text
Given this workflow and current architecture, select relevant microservices patterns: decomposition, IPC, service discovery, circuit breaker, outbox, saga, CQRS, API composition, API gateway/BFF, service chassis, service mesh/sidecar, strangler, anti-corruption layer, and testing patterns.
For each selected pattern, state problem, forces, implementation consequences, tests, observability, and red flags.
```

Coding plan:

```text
Turn this microservice architecture decision into coding tasks.
Include service contracts, API/event/schema definitions, data ownership, outbox/inbox, saga state if needed, idempotency, contract tests, component tests, health/readiness, metrics/logs/traces, deployment manifests, canary/release plan, rollback, and runbook updates.
```

## Red Flags
- Microservices are selected before business capabilities and data ownership are known.
- Services are split by technical layer: user-service, order-controller-service, database-service.
- Multiple services share write access to the same tables.
- Cross-service workflows rely on distributed transactions without explicit acceptance of complexity.
- Saga has no compensation, retry, timeout, or operator recovery path.
- Events lack schema ownership, versioning, idempotency, replay, and dead-letter handling.
- API gateway owns too much business logic or becomes a centralized queue for all changes.
- CQRS projection has no rebuild, lag metric, or stale-read contract.
- Strangler migration lacks anti-corruption layer and coexistence plan.
- Service mesh is proposed before service ownership, health checks, and basic observability exist.
