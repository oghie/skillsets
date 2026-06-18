# Architecture View Design

Use this when converting schematic architecture into implementable functional, information, behavior, and deployment views.

## A4a Functional View

Steps:
1. Refine use cases.
2. Group cohesive responsibilities into functional components.
3. Define provided and required interfaces.
4. Allocate components to modules, packages, services, or layers.
5. Add variation points only where real variability exists.

Output:

```markdown
| Component | Responsibility | Provided Interfaces | Required Interfaces | Owner | Module/Service |
|---|---|---|---|---|---|
```

## A4b Information View

Steps:
1. Refine persistent object model.
2. Identify data components and stores.
3. Allocate data to stores or services.
4. Define data component interfaces and access rules.
5. Design persistence, migration, retention, and consistency.

Output:

```markdown
| Data Component | Owns | Reads | Writes | Store | Consistency | Migration Notes |
|---|---|---|---|---|---|---|
```

## A4c Behavior View

Steps:
1. Refine system control flows from important scenarios.
2. Identify key behavioral elements: commands, events, jobs, workflows, state machines.
3. Define detailed control flows with success, alternative, and failure paths.
4. Add timeout, retry, idempotency, compensation, and observability rules.

Output:

```markdown
| Flow | Participants | Sync/Async | State Changes | Failure Paths | Observability |
|---|---|---|---|---|---|
```

## A4d Deployment View

Steps:
1. Define computing devices and runtime nodes.
2. Define execution environments.
3. Define network connectivity and trust zones.
4. Allocate software artifacts.
5. Add secrets, configuration, scaling, health checks, and release path.

Output:

```markdown
| Artifact | Runtime Node | Execution Environment | Network Dependencies | Config/Secrets | Release/Health |
|---|---|---|---|---|---|
```

## Cross-View Validation

Before finalizing:
- Every component has data and behavior implications.
- Every data owner has allowed writers/readers.
- Every critical behavior maps to deployed runtimes.
- Every external dependency appears in context and deployment views.
- Every NFR tactic is visible in at least one view.
