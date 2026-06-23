# Clean Code Review Checklist

Use this checklist for code reviews, refactoring plans, modernization increments, and architecture-to-implementation handoff.

## Baseline
- Requirements, use cases, stakeholders, acceptance criteria, and non-goals are clear when behavior can change.
- Target behavior is known or characterized.
- Tests, contracts, traces, or manual scenarios are identified.
- Cleanup scope and non-goals are explicit.
- Behavior change is separated from refactoring unless explicitly intended.
- NFR concerns are named when relevant: modifiability, performance, security, availability, deployability, observability, privacy, or cost.

## Names
- Names reveal intent, unit, lifecycle, and ownership.
- Domain concepts use domain vocabulary.
- Technical mechanisms use standard solution vocabulary.
- Similar concepts use one consistent word.
- Boolean names are positive and unambiguous.
- Names do not hide side effects.

## Functions
- Each function does one thing at one abstraction level.
- Arguments are few and meaningful.
- Flag arguments and output arguments are avoided.
- Commands and queries are separated.
- Side effects are explicit.
- Error translation is separated from core policy.

## Comments And Formatting
- Comments explain intent, warning, legal constraint, or non-obvious context.
- Obsolete, redundant, journal, noisy, and commented-out code are removed.
- Related code is close; unrelated concepts are separated.
- Formatting follows team conventions without noisy churn.

## Objects, Data, And Boundaries
- Domain behavior is not shaped by ORM, SDK, transport, or UI models.
- DTOs/records are limited to boundary and persistence needs.
- Third-party or volatile dependencies are isolated when risk justifies it.
- Deep navigation through foreign internals is avoided.
- API/event/data contracts do not leak private implementation detail.

## Errors, Nulls, And Failure Paths
- Failure modes are explicit and tested.
- Exceptions/results include caller-relevant context.
- Null is not used as an ambiguous control signal.
- Boundary adapters translate vendor/framework failures.
- Normal flow is not obscured by error plumbing.

## Tests
- Changed behavior is covered by unit, characterization, integration, or contract tests.
- Tests are quick enough for the local refactoring loop, independent, repeatable, self-validating, and timely where practical.
- Test helpers improve readability instead of hiding important setup.
- Boundary, failure, and near-bug cases are covered.
- Slow tests are separated from the quick refactoring loop.
- Performance-sensitive changes include workload, benchmark, load-test, p95/p99, or resource-usage evidence.

## Architecture Fit
- Code preserves dependency direction and ownership.
- Classes/modules have cohesive reasons to change and reduce coupling instead of moving it.
- Duplication is removed only when the concept is genuinely shared.
- Abstractions protect known variation points, not speculative future needs.
- Architecture decisions map to enforceable code boundaries, dependency constraints, import rules, or fitness functions.

## Deployment And Operations
- Development view and operation view impacts are explicit when package boundaries, repository structure, CI checks, or production procedures change.
- Build, packaging, runtime config, rollout, rollback, and observability impacts are known.
- Cleanup does not silently change health checks, logging, metrics, tracing, audit events, migrations, or runbooks.
- Cost-sensitive cleanup has an estimate, uncertainty driver, risk reserve, or ownership decision.

## Concurrency
- Shared mutable state is minimized or deliberately synchronized.
- Concurrency policy is separate from business logic.
- Critical sections are small.
- Shutdown, cancellation, timeout, and retry behavior are defined.
- Stress or scheduler-sensitive tests exist for risky concurrent code.

## Review Output
- Findings cite exact locations.
- Each finding names decision impact, smell, recommended fix, rationale/trade-off, and verification.
- Residual risk and follow-up cleanup trigger are visible.
