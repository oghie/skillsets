# Architecture Evaluation

Use this for architecture review gates, design validation, risk assessment, or pre-implementation checks.

## Workflow

1. Identify evaluation target elements.
2. Select evaluation methods.
3. Gather evidence.
4. Walk through critical scenarios.
5. Record findings with severity and evidence.
6. Decide actions, accepted trade-offs, and revisit triggers.

## Target Elements

Evaluate:
- Requirements and NFR scenarios.
- Context and boundaries.
- Schematic architecture and style choices.
- Functional components and interfaces.
- Information ownership and persistence.
- Behavior flows and failure handling.
- Deployment topology and operations.
- NFR tactics and conformance.
- Migration and implementation plan.

## Scenario Walk-Through

Use:

```markdown
| Scenario | Architecture Path | Expected Response | Evidence | Gap/Risk | Action |
|---|---|---|---|---|---|
```

## Finding Format

```markdown
| Severity | Finding | Evidence | Impact | Recommendation |
|---|---|---|---|---|
```

Severity:
- `Critical`: core requirement or production safety can fail.
- `High`: major NFR, data integrity, security, or delivery risk.
- `Medium`: meaningful ambiguity or maintainability risk.
- `Low`: clarity/documentation issue.

## Evaluation Methods

Choose one or more:
- Checklist review.
- Scenario walk-through.
- Trade-off analysis.
- Prototype/spike.
- Benchmark/load test.
- Threat model.
- Code/dependency inspection.
- Model review.
- Static/formal analysis.
- Operational readiness review.

## Output

Finish with:
- Go/no-go or conditional recommendation.
- Highest risks.
- Required actions.
- Accepted trade-offs.
- Verification evidence still missing.
