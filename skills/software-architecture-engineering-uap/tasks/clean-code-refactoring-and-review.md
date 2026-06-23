# Clean Code Refactoring And Review

Use this task when a user asks for clean code, code review, refactoring, craftsmanship, readability, maintainability, code smells, technical debt reduction, or implementation hygiene inside architecture work.

## Inputs

Collect only what is needed:
- Target files, modules, services, packages, or diff.
- Intended behavior and user-visible constraints.
- Relevant requirements, use cases, stakeholders, non-goals, and acceptance criteria when the cleanup affects observable behavior.
- Existing tests, CI commands, coverage signals, and known flaky tests.
- Architecture decisions that must be preserved: dependency direction, data ownership, API contracts, security policy, transaction boundaries, concurrency model, and operational constraints.
- Deployment, runtime, rollout, rollback, and observability constraints when the refactor changes build artifacts, service behavior, migrations, or production support.
- Risk tolerance: behavior-preserving refactor, bug fix, modernization increment, or feature implementation.

If behavior is unclear, state that the work is characterization-first.

## Review Workflow

1. Establish facts from code, tests, contracts, and docs.
2. Separate `Fact`, `Inference`, `Assumption`, and `Question`.
3. Identify the driving force: correctness, modifiability, security, performance, concurrency safety, operational support, or cost.
4. Classify findings by smell and impact:
   - naming, functions, comments, formatting/shape;
   - objects/data structures, classes/modules, boundaries;
   - error handling, nulls, side effects;
   - tests, build/test friction, CI;
   - concurrency, shared mutable state, shutdown;
   - architecture drift, dependency direction, package/service ownership.
5. Recommend the smallest change that removes risk without speculative abstraction.
6. Define verification for every recommendation.

## Refactoring Workflow

Use small behavior-preserving transformations:

```text
baseline behavior
  -> characterization or missing tests
  -> rename for intent
  -> extract functions at one abstraction level
  -> split classes/modules by responsibility
  -> isolate boundaries and error translation
  -> remove duplication where the concept is truly shared
  -> enforce dependency direction
  -> run verification
  -> repeat
```

Do not mix cleanup and new behavior unless the user explicitly asks for both. If both are required, separate commits or at least separate sections of the implementation plan.

## Decision Rules

| Situation | Action |
|---|---|
| No tests and behavior is nontrivial | Add characterization tests before refactoring. |
| Duplicate code expresses different business concepts | Keep separate or introduce explicit domain names; do not DRY blindly. |
| Multiple controllers/services repeat authorization | Centralize policy enforcement or create a tested policy boundary. |
| Domain code depends on SDK/ORM/framework | Introduce a project-owned port/adapter if volatility or test friction justifies it. |
| Long function mixes IO, policy, and formatting | Extract policy first, then adapters/formatters. |
| Flags select behavior | Split functions or use strategy/state only when variation is real. |
| Nulls cross API/module boundary | Replace with explicit optional/result/validation contract. |
| Concurrency failures are intermittent | Treat as candidate threading bug; add stress/instrumented tests. |
| Refactor would require large-bang rewrite | Plan increments with fitness checks and rollback. |

## Output

For reviews, lead with findings:

```markdown
## Findings
- Severity:
  Location:
  Smell:
  Architecture force:
  Risk:
  Recommended fix:
  Verification:

## Open Questions
## Residual Risk
```

For implementation planning:

```markdown
## Clean-Code Refactoring Plan
- Behavior baseline:
- Target forces:
- Scope:
- Non-goals:
- Steps:
- Tests and checks:
- Rollout/rollback:
- Residual risk:
```

## Verification

Pick the tightest available evidence:
- Unit tests for extracted logic and domain policy.
- Characterization tests for legacy behavior.
- Integration or contract tests for API, event, data, or adapter boundaries.
- Static dependency checks, import rules, or fitness functions for package/layer/module direction.
- Stress/failure tests for concurrency.
- Workload model, benchmark, load test, p95/p99 target, or resource-usage check when performance is affected.
- Cost estimate, uncertainty driver, risk reserve, or ownership decision when refactoring is justified by delivery or operating cost.
- Build/CI command proving cleanup did not break compilation or test execution.
- Manual scenario walkthrough only when automation is not feasible; state the limitation.
