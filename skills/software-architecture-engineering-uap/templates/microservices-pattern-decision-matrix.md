# Microservices Pattern Decision Matrix

## Context
- Business objective:
- Stakeholder requirements/use cases:
- Sector/context:
- Current architecture:
- Main pain:
- Team topology:
- Operations maturity:
- Critical workflows:
- Measurable NFRs:
- Non-goals:

## Architecture Path
| Option | Fit | Benefits | Liabilities | Decision |
|---|---|---|---|---|
| Modular monolith | | | | |
| Service-oriented design | | | | |
| Microservices | | | | |
| Strangler migration | | | | |

## Service Boundaries
| Candidate service | Capability/subdomain | Commands | Queries | Data owned | Team owner | Keep together/split rationale |
|---|---|---|---|---|---|---|
| | | | | | | |

## Modularity And Implementation Structure
| Area | Decision | Coupling/cohesion concern | Dependency or fitness check | Repository/package/development view impact | Operation view impact |
|---|---|---|---|---|---|
| | | | | | |

## Pattern Selection
| Problem | Selected pattern | Why | Consequences | Tests/evidence |
|---|---|---|---|---|
| IPC | Sync / Async / Pub-sub / Request-async-response | | | |
| Reliability | Circuit breaker / Timeout / Retry budget / Fallback | | | |
| Discovery | Client-side / Server-side / Platform-native | | | |
| Transactional messaging | Outbox / Polling publisher / Log tailing | | | |
| Consistency | Saga choreography / Saga orchestration / Local only | | | |
| Query | API composition / CQRS / Query service | | Projection rebuild, lag, stale-read/freshness contract | |
| External API | API gateway / BFF / Public API module | | | |
| Production readiness | Chassis / Platform golden path / Manual controls | | | |
| Deployment | Container / VM / Serverless / Mesh / Sidecar | | | |
| Migration | Strangler / ACL / Parallel run | | | |

## Cost, Performance, And Availability Model
| Concern | Target/model | Evidence | Owner |
|---|---|---|---|
| Workload | users, RPS/QPS, data growth, peak shape | | |
| Latency | p95/p99 target | | |
| Availability | dependency failure model, recovery, RTO/RPO, backup/restore | | |
| Cost | WBS/PERT/TCO/resource usage/risk reserve | | |

## Coding Readiness
| Item | Decision | Owner | Evidence |
|---|---|---|---|
| API/event schemas | | | |
| Data migrations | | | |
| Local transaction boundary | | | |
| Idempotency keys | | | |
| Outbox/inbox | | | |
| Saga state/compensation | | | |
| Contract tests | | | |
| Health/readiness | | | |
| Logs/metrics/traces | | | |
| Rollout/rollback | | | |

## Residual Risks
| Risk | Trigger | Mitigation | Revisit |
|---|---|---|---|
| | | | |
