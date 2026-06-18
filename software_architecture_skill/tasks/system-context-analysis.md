# System Context Analysis

Use this to define boundaries, actors, external systems, data flows, domain objects, and behavior before internal design.

## Boundary Context

Steps:
1. Draw or list the system boundary.
2. Place external actors, systems, devices, stores, and organizations outside it.
3. Name all flows crossing the boundary.
4. Identify trust, data ownership, operational, and network boundaries.
5. Mark unknown external contracts.

Output:

```markdown
| External Element | Type | Flow In | Flow Out | Owner | Trust Level | Failure Impact |
|---|---|---|---|---|---|---|
```

## Functional Context

Steps:
1. Identify actors.
2. List actor goals and use cases.
3. Group related use cases by domain area.
4. Add operational/admin/support use cases when they affect architecture.
5. Mark use cases that drive NFRs.

Output:

```markdown
| Actor | Use Case | Trigger | Outcome | Priority | NFR Driver |
|---|---|---|---|---|---|
```

## Information Context

Steps:
1. Identify domain objects and external data.
2. Distinguish persistent, session, derived, cached, and transient data.
3. Define identity, lifecycle, cardinality, and ownership.
4. Mark privacy, retention, audit, and consistency constraints.

Output:

```markdown
| Data/Object | Owner | Persistent? | Source Of Truth | Lifecycle | Constraints |
|---|---|---|---|---|---|
```

## Behavior Context

Steps:
1. Select critical workflows.
2. Identify invocation pattern: sequential, explicit, closed loop, parallel, event-based, or timed.
3. Model happy path and important alternatives.
4. Add failure paths, retries, timeouts, compensations, and state transitions.

Output:

```markdown
| Scenario | Trigger | Participants | Pattern | State Changes | Failure Handling |
|---|---|---|---|---|---|
```

## Completion Criteria

Context analysis is ready when:
- Boundaries are explicit.
- Each external dependency has an owner and failure impact.
- Use cases map to actors and outcomes.
- Important data has ownership.
- Critical behavior is understandable without reading implementation code.
