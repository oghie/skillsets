# Context And Architecture Views

Use context and views to turn architecture from an abstract statement into coordinated design evidence. Each view answers a different class of question and should be consistent with the others.

## Boundary Context

Purpose: define what is inside the system, what is outside, and what crosses the boundary.

Include:
- External users, roles, organizations, devices, partner systems, platforms, and data providers.
- Inputs, outputs, commands, queries, events, files, messages, and shared data stores.
- Trust boundaries, ownership boundaries, network boundaries, and operational boundaries.
- Manual steps and support/operations interfaces when they affect architecture.

Common mistakes:
- Treating a partner service as an internal component.
- Omitting batch jobs, admin tools, support workflows, or data exports.
- Drawing a boundary without naming the data/control flows through it.
- Ignoring failure behavior at integrations.

## Functional Context And Functional View

Functional context identifies what the system does from actors and use cases. The functional view defines components that provide those functions.

Steps:
1. List actors and actor goals.
2. Group use cases by domain responsibility, not by UI screen alone.
3. Refine use cases with trigger, preconditions, main flow, alternatives, outputs, and acceptance criteria.
4. Derive functional components from cohesive use case groups.
5. Define provided and required interfaces for each component.
6. Allocate components to packages, services, modules, or deployment units.
7. Design variability only where real variation exists.

Functional component checklist:
- Single clear responsibility.
- Explicit input/output contracts.
- Named dependencies.
- Clear owner or team boundary when relevant.
- No hidden data ownership.
- Variation points are governed by interfaces, not scattered conditionals.

## Information Context And Information View

Information context identifies important domain objects and persistent state. The information view defines data components, stores, ownership, and access paths.

Analyze:
- Persistent objects and volatile/session objects.
- Associations, aggregations, compositions, inheritance, and cardinalities.
- Identity, lifecycle, consistency, retention, and privacy.
- Object ownership and update authority.
- Relationship strength and whether data should live together or apart.
- External source of truth versus internally owned state.

Data component rules:
- Every persistent object has an owner.
- Shared tables or shared databases require governance and compatibility rules.
- Data duplication needs a synchronization, reconciliation, and stale-read policy.
- Event streams and caches are data stores with schema and lifecycle responsibilities.
- Analytics, audit, and reporting paths must not corrupt transactional ownership.

## Behavior Context And Behavior View

Behavior context describes how the system acts over time. The behavior view defines detailed control flow, message flow, state, timing, and failure behavior.

Invocation patterns to identify:
- Sequential invocation.
- Explicit invocation between components.
- Closed-loop control.
- Parallel or concurrent invocation.
- Event-based invocation.
- Timed/scheduled invocation.

Behavior artifacts:
- Activity diagrams for workflow and branching.
- Sequence diagrams for collaborations and request/message order.
- State machines for lifecycle-heavy objects.
- Event flow diagrams for publish/subscribe or event-driven designs.
- Failure path tables for retries, idempotency, timeouts, compensations, and dead-letter handling.

Behavior checks:
- Every async operation has retry, ordering, idempotency, and observability rules.
- Every state transition has a trigger and owner.
- Every external call has timeout, error handling, and fallback or escalation.
- Long-running workflows have compensation or recovery strategy.

## Deployment Context And Deployment View

Deployment context identifies physical and logical runtime environment. The deployment view maps software artifacts to nodes and execution environments.

Include:
- Devices, servers, clients, containers, virtual machines, functions, runtimes, and managed services.
- Execution environments: web server, application server, DBMS, message broker, scheduler, edge runtime, mobile runtime, browser.
- Software artifacts: deployable packages, services, modules, images, jobs, libraries, and configuration.
- Network paths, protocols, ports, zones, regions, trust boundaries, and bandwidth/latency assumptions.
- Secrets, credentials, configuration, service discovery, and operational ownership.

Deployment checks:
- A component that stores state has backup, migration, restore, and retention strategy.
- A network link that matters has protocol, trust boundary, timeout, and failure mode.
- A deployable artifact has build, release, rollback, and health-check path.
- Environment parity and configuration drift are addressed.

## Cross-View Consistency

Use these checks before handing off architecture:

| Check | Question |
|---|---|
| Context to functional | Does every use case map to one or more functional components? |
| Functional to information | Does every component know which data it owns, reads, or mutates? |
| Functional to behavior | Are important interactions represented in control/message flow? |
| Information to deployment | Are data stores placed where ownership, latency, compliance, and availability allow? |
| Behavior to deployment | Do network hops, async boundaries, and runtime constraints support the flow? |
| NFR to views | Do quality tactics visibly change components, data, behavior, or deployment? |

Missing cross-view links are architecture defects, not documentation gaps.
