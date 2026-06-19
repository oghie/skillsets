# Architecture Review And Modernization

Use this for existing systems, refactors, decomposition, migrations, platform redesign, or architecture debt review.

## Evidence Collection

Inspect before judging:
- Repository structure.
- Build and dependency graph.
- API contracts and schemas.
- Database migrations and data ownership.
- Background jobs, queues, events, and schedulers.
- Infrastructure and deployment manifests.
- CI/CD, tests, observability, logs, alerts, and runbooks.
- Architecture fitness functions, dependency rules, package boundaries, and import constraints.
- Existing ADRs, RFCs, diagrams, incidents, and support tickets.

## Current-State Model

Build a concise current-state view:

```markdown
| Area | Current Evidence | Risk | Unknown |
|---|---|---|---|
| Context |
| Functional components |
| Data ownership |
| Behavior flows |
| Deployment |
| Development structure |
| Operation |
| NFRs |
```

## Modernization Workflow

1. Identify business and engineering drivers.
2. Map current architecture and pain points.
3. Separate symptoms from root causes.
4. Define target qualities and constraints.
5. Compare alternatives.
6. Select migration strategy.
7. Plan increments with compatibility and rollback.
8. Define validation and operational readiness.
9. Add architecture-as-code checks for target boundaries that need ongoing enforcement.

## Migration Strategies

| Strategy | Use When | Risks |
|---|---|---|
| In-place refactor | Boundaries are clear and risk is local | Long-running branch, hidden coupling |
| Strangler fig | Legacy surface can be replaced incrementally | Routing, dual behavior, data sync |
| Modularization first | Distribution is premature but boundaries are weak | Requires discipline without deployment boundary |
| Extract service | Ownership, scale, or release cadence justify split | Distributed data and ops cost |
| Replatform | Current platform blocks required NFRs | Cutover, skill gap, vendor risk |
| Parallel run | Correctness must be proven before switch | Cost, reconciliation, duplicated effort |

## Modernization Findings To Look For

- Circular dependencies and unclear module ownership.
- Shared database as integration layer.
- Implicit workflows hidden in callbacks or jobs.
- No contract tests for APIs/events.
- Missing migration rollback.
- Environment drift.
- Observability afterthought.
- Over-distribution without team or NFR justification.
- Security and privacy controls added only at the edge.
- Diagrams and ADRs no longer match repository/package/service structure.
- No cost or uncertainty model for modernization alternatives.

## Output

Produce:
- Current-state architecture risks.
- Target architecture.
- Decision rationale.
- Migration increments.
- Data compatibility plan.
- Testing and observability plan.
- Architecture fitness checks or manual governance checks.
- Rollout and rollback plan.
