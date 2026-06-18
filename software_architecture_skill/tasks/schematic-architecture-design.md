# Schematic Architecture Design

Use this when selecting or changing the high-level architecture structure.

## Workflow

1. Identify design forces:
   - user workflows
   - data ownership
   - integration shape
   - NFR scenarios
   - deployment constraints
   - team ownership
   - migration constraints
2. Identify candidate architecture styles.
3. Evaluate candidates against benefits and liabilities.
4. Compose selected styles into one schematic.
5. Rename generic style roles into domain-specific elements.
6. Validate the schematic against critical scenarios.
7. Record decisions and alternatives.

## Candidate Evaluation Table

```markdown
| Style | Forces Matched | Benefits | Liabilities | NFR Impact | Team/Ops Fit | Decision |
|---|---|---|---|---|---|---|
```

## Integration Rules

- Compose styles deliberately; do not stack buzzwords.
- Make style boundaries visible. Example: UI pattern inside an app, event-driven integration between services, repository style for shared persistence.
- Avoid hidden shared data between supposedly independent components.
- Add gateways, adapters, brokers, or repositories only when they solve a named force.
- Keep the schematic technology-neutral until technology choices are needed for constraints.

## Schematic Output Template

```markdown
## Schematic Architecture
- Selected styles:
- Main elements:
- Interaction model:
- Data ownership:
- Deployment assumptions:
- NFR-driven tactics:
- Rejected alternatives:
- Validation:
```

## Common Findings

- Microservices chosen without independent deployment or team ownership.
- Event-driven design without consumer contracts, ordering, idempotency, or observability.
- Layered architecture with no enforced dependency direction.
- Shared repository used to avoid clear ownership.
- Broker or dispatcher introduced without availability and routing policy.
- Edge or control architecture without timing, safety, and recovery analysis.
