# Clean Code Craftsmanship

Use this reference when architecture work reaches code-level maintainability: refactoring, code review, implementation planning, module decomposition, service internals, test strategy, error handling, concurrency boundaries, or technical-debt reduction.

## Table Of Contents
- [Core Position](#core-position)
- [Architecture Connection](#architecture-connection)
- [Clean Code Guidance](#clean-code-guidance)
- [Clean Code Review Flow](#clean-code-review-flow)
- [Refactoring Loop](#refactoring-loop)
- [Smell To Architecture Mapping](#smell-to-architecture-mapping)
- [Testing And Verification](#testing-and-verification)
- [Cross-Skill Invocation Map](#cross-skill-invocation-map)
- [Prompt Templates](#prompt-templates)
- [Red Flags](#red-flags)

## Core Position

Clean code is not formatting preference. It is the local expression of architecture. If functions, names, tests, boundaries, and dependencies are careless, the architecture diagram is fiction.

Use clean-code reasoning to answer:
- Can another engineer safely read, change, and test this code?
- Does the code make business intent explicit?
- Are dependencies, side effects, error paths, and concurrency policies visible?
- Is the implementation cheaper to evolve than to replace?
- Does the code protect architecture decisions rather than bypass them?

Do not turn clean code into aesthetic policing. Style-only churn is waste unless it reduces ambiguity, risk, coupling, or change cost.

## Architecture Connection

Treat the design stack as a chain:

```text
OOD and language primitives
  -> naming, functions, classes, modules
  -> design principles and patterns
  -> package/component boundaries
  -> architecture styles and runtime topology
```

If a low-level rule conflicts with a higher-level architecture force, resolve the force explicitly. Example: a tiny duplicated validation rule may be safer than a shared utility that couples two bounded contexts. Conversely, duplicated authorization decisions are dangerous because they fracture policy enforcement.

## Clean Code Guidance

### Code As Requirement Precision
- Code is where requirements become executable detail. Vague requirements become bugs unless code, tests, and contracts force precision.
- Bad code has compounding cost: change cost rises, defects spread, teams add people to a system they cannot understand, and redesign becomes a symptom of earlier neglect.
- The quickest sustainable route is usually to keep code clean while delivering, not to defer cleanup indefinitely.

### Meaningful Names
- Names must reveal why something exists, what it means, and how it is used.
- Use domain terms for domain concepts and solution terms for technical mechanisms.
- Avoid disinformation: names that imply the wrong type, protocol, lifecycle, ownership, or unit.
- Avoid noise words such as `Data`, `Info`, `Manager`, `Processor`, and numbered variants unless the distinction is real.
- Prefer pronounceable, searchable names for concepts that outlive a tiny local scope.
- Use one word per concept. Do not mix `fetch`, `get`, `load`, and `retrieve` unless their semantics differ.
- Boolean names should be positive and answer a clear predicate: `isActive`, `hasPermission`, `canRetry`.
- A name that requires a comment is usually a design smell.

### Functions
- Functions should do one thing at one level of abstraction.
- Keep a readable top-to-bottom stepdown: high-level policy calls lower-level detail instead of mixing both in one block.
- Prefer few arguments. Many arguments often signal a missing object, misplaced responsibility, or broad command object.
- Avoid flag arguments that make one function perform multiple behaviors. Split the operation or use polymorphism/strategy when variation is real.
- Separate commands from queries. A method that both changes state and answers a question hides side effects.
- Make side effects explicit in names and contracts.
- Extract `try/catch` and error translation so business logic is not buried in control noise.
- Duplication is a signal that a concept is missing, but removing duplication must not merge different responsibilities.

### Comments
- A comment must not compensate for unclear code that can be improved.
- Good comments explain legal requirements, non-obvious intent, warning conditions, domain constraints, or temporary TODOs with owner/context.
- Bad comments restate code, drift from reality, hide dead code, journal history, create noise, or document private implementation as if it were a contract.
- Public APIs can need contract documentation; internal code should first communicate through names, structure, and tests.

### Formatting And Shape
- Formatting is a communication protocol for the team.
- Keep related code close and separate unrelated concepts with whitespace.
- Preserve vertical ordering from high-level policy to detail when possible.
- Avoid horizontal alignment and line shapes that make diffs noisy or hide meaning.
- Group code into paragraphs: each paragraph should express one idea.
- Suspicious shapes include long spikes, walls of comments, dense conditionals, and intensive use of one foreign object.

### Objects And Data Structures
- Objects hide data behind behavior; data structures expose data with little behavior. Mixing both casually creates hybrids that are hard to reason about.
- Respect dependency direction: domain behavior should not depend on transport, ORM, vendor SDK, or UI shape.
- Do not chain through foreign internals. If code navigates deep object graphs, ownership boundaries are leaking.
- DTOs and records are acceptable at boundaries, serialization edges, and persistence mapping. They are dangerous when mistaken for rich domain models.
- Active Record can be pragmatic for simple CRUD, but becomes a liability when business rules, transactions, and policies grow.

### Error Handling
- Error handling is part of design, not cleanup.
- Prefer exceptions or typed results over scattered error codes when they preserve readable control flow.
- Add context at the boundary where failure is understood; do not leak vendor-specific errors through the domain.
- Define exception/result types by caller need, not by every low-level failure variant.
- Do not return or accept `null` casually. Use explicit optional/result types, defaults, guard clauses, or contract validation.
- Write the failure path first when it defines the boundary contract.

### Boundaries
- Wrap third-party APIs, frameworks, SDKs, and external services behind project-owned interfaces when the dependency is volatile or pervasive.
- Use learning tests or characterization tests around external APIs and legacy behavior.
- When a dependency does not exist yet, define the interface your code needs rather than letting a future vendor shape the domain.
- Boundary adapters are architecture enforcement points; they should translate protocols, errors, timeouts, retries, auth context, and data formats.

### Tests
- Test code must be clean enough to change safely. Messy tests slow refactoring as much as messy production code.
- Tests enable modifiability. Untested code may look clean but is unsafe to evolve.
- Prefer tests that are quick enough for the local refactoring loop, independent, repeatable, self-validating, and timely.
- One test should verify one concept, even if it uses multiple assertions for one coherent outcome.
- Use test data builders, object mothers, or domain-specific test helpers when they improve readability and reduce brittle setup.
- Coverage is a signal, not proof. Missing boundary, failure, and near-bug tests matter more than a raw percentage.

### Classes And Modules
- Classes and modules should be small because they own one responsibility, not because of arbitrary line limits.
- High cohesion means fields and methods work together toward one reason to change.
- Low cohesion usually means split by capability, lifecycle, policy, workflow, or adapter responsibility.
- Organize for change: put volatile decisions behind stable seams, and keep stable domain policy independent of volatile infrastructure.
- Encapsulation is not hiding everything; it is exposing the contract that lets callers ignore implementation detail.

### Systems
- Separate construction from use. Object creation, dependency wiring, configuration, and framework setup should not pollute domain flow.
- Use factories, dependency injection, or composition roots when they make dependencies explicit and testable.
- Cross-cutting concerns need deliberate composition points: logging, metrics, tracing, auth, transactions, retry, caching invalidation/TTL/consistency, and security policy.
- Test-drive system architecture where feasible: prove dependency direction, module boundaries, and critical flows with tests, dependency constraints, or fitness functions.
- Standards and frameworks are valuable only when they add demonstrable value. Cargo-cult adoption adds accidental complexity.
- Domain-specific language can be useful when it makes core business rules more expressive and safer to change.

### Emergent Design
- Simple design is not naive design. It requires passing tests, removing duplication, expressing intent, and minimizing needless entities.
- Refactor after tests pass. Do not preserve ugly code just because it works.
- Expressive code often needs better names, smaller functions/classes, and clearer abstractions rather than more comments.
- Minimize classes/methods after duplication and expressiveness have been addressed; otherwise "minimal" becomes dense and obscure.

### Concurrency
- Concurrency is a design concern with its own lifecycle, tests, and failure modes.
- Separate concurrency policy from business logic.
- Limit shared mutable data. Prefer immutable data, copies, queues, actors, ownership transfer, or thread-confined state.
- Keep synchronized/critical sections small and avoid dependencies between synchronized methods.
- Know the execution model: producer-consumer, readers-writers, dining philosophers/resource ordering, executor pools, nonblocking primitives, cancellation, and shutdown.
- Treat spurious failures as evidence, not noise. Thread bugs are often intermittent.
- Make concurrent code tunable and test under different thread counts, scheduler conditions, platforms, and forced interleavings.

### Successive Refinement
- Do not wait for a perfect design before making code work. Make it work, then make it right, in small behavior-preserving steps.
- Refactoring is a sequence, not a leap. Each step should keep tests green.
- Rough drafts are acceptable only when the next step is explicit cleanup, not permanent settlement.
- Characterization tests are mandatory when current behavior is uncertain.

### Framework Internals And Legacy Refactoring
- Studying framework internals is useful because mature libraries reveal naming, decomposition, and refactoring trade-offs.
- Legacy code should first be characterized, then simplified.
- Rename aggressively when tests and tooling support it.
- Move constants, methods, and responsibilities to the owner that makes the concept clearer.
- Delete dead/commented code instead of preserving fear in the codebase.

### Smells And Heuristics
- Comments: inappropriate information, obsolete comments, redundant comments, poor writing, commented-out code.
- Environment: build/test requires too many manual steps.
- Functions: too many arguments, output arguments, flag arguments, dead functions.
- General: wrong abstraction level, dead code, artificial coupling, feature envy, selector arguments, obscured intent, misplaced responsibility, inappropriate static, magic numbers, negative conditionals, hidden temporal coupling, transitive navigation.
- Names: vague, encoded, ambiguous, wrong abstraction level, hidden side effects.
- Tests: insufficient tests, missing boundary tests, skipped trivial tests, slow tests, ignored tests, uncovered bug neighborhoods.

## Clean Code Review Flow

1. Establish behavior evidence: tests, contracts, traces, user-visible behavior, and known defects.
2. Identify the architectural force: modifiability, correctness, security, performance, operational safety, domain clarity, or cost.
3. Classify smells by risk, not taste.
4. Find the smallest behavior-preserving refactor that reduces the risk.
5. Require verification: unit/integration/contract tests, characterization tests, static checks, or architecture fitness functions.
6. Separate cleanup from behavior change in the diff when possible.
7. Report residual risk and next cleanup trigger.

## Refactoring Loop

```text
Observe unclear or risky code
  -> characterize behavior
  -> add or tighten tests
  -> perform one small transformation
  -> run verification
  -> simplify names/functions/classes/boundaries
  -> repeat until the targeted force is addressed
```

Use this loop for code review, modernization, service extraction, IAM/auth implementation, concurrency fixes, and microservice chassis work.

## Smell To Architecture Mapping

| Code Smell | Architecture Risk | Preferred Response |
|---|---|---|
| Long function mixes policy, IO, error handling, and formatting | Business rule is not independently testable | Extract policy, adapter, and error translation layers. |
| `Manager` or `Processor` class owns unrelated workflows | Low cohesion and unclear ownership | Split by capability, actor workflow, or lifecycle. |
| Utility package accumulates domain behavior | Hidden shared kernel without governance | Move behavior to owning domain; keep utilities generic. |
| Repeated auth checks in controllers | Fractured policy enforcement | Centralize enforcement point and test authorization matrix. |
| ORM entities leak through API | Persistence model controls external contract | Add DTO/mapper boundary and contract tests. |
| Vendor SDK used throughout domain | Vendor lock-in and hard-to-test code | Wrap behind project-owned port/adapter. |
| Flag arguments and switches select behavior | OCP pressure or missing strategy/state | Split functions or introduce polymorphism only when variation is real. |
| Nulls cross boundaries | Ambiguous contract and latent failures | Use explicit optional/result types, validation, or boundary translation. |
| Shared mutable state in concurrent flow | Race conditions and nondeterministic defects | Confine state, copy data, use queues/locks deliberately, add stress tests. |
| Tests require many manual steps | Low delivery reliability | Automate build/test path and reduce fixture complexity. |
| Slow tests block frequent refactoring | Refactoring becomes expensive | Split quick unit tests from slower integration/system suites. |
| Big Ball of Mud packages | Architecture exists only as intent | Recover seams incrementally, add dependency checks, and document ownership. |

## Testing And Verification

For clean-code changes, require at least one of:
- Existing test suite covering changed behavior.
- New unit/characterization tests for changed logic.
- Contract tests for changed API/event/schema behavior.
- Static dependency check for boundary fixes.
- Concurrency stress or scheduler-sensitive tests for threading changes.
- Workload model, benchmark, load test, p95/p99 target, or resource-usage check when performance is affected.
- Cost estimate, uncertainty driver, risk reserve, or ownership decision when refactoring is justified by delivery or operating cost.
- Manual scenario trace only when automation is impossible; document why.

Verification must answer:
- Did behavior change? If yes, was it intended and accepted?
- Did readability improve because names, boundaries, or tests became clearer?
- Did coupling decrease or only move?
- Did the change reduce future modification cost without adding speculative framework complexity?

## Cross-Skill Invocation Map

Avoid loops: use this reference as a secondary read only when code-level maintainability, refactoring, review, testability, or implementation structure is material.

| Primary User Prompt | Primary Skill | When To Also Use This Clean-Code Reference |
|---|---|---|
| Architecture design/review/modernization | `software-architecture-engineering-uap` | Always when modules, packages, service internals, implementation plan, or refactoring are in scope. |
| IAM/auth implementation | `software-architecture-engineering-uap` | When designing auth code paths, policy enforcement, token/session modules, recovery flows, audit code, or security tests. |
| Microservices implementation | `software-architecture-engineering-uap` | When creating service chassis, adapters, gateway/BFF modules, saga/outbox code with idempotency/deduplication, contracts, or tests. |
| Data architecture or migration | `data-architect-engineering` | When writing repository/query modules, migration scripts, ETL code, data-access boundaries, or characterization tests for legacy behavior. |
| Realtime/concurrent systems | `realtime-systems-coding` | When shared state, synchronization, shutdown, queues, or concurrency tests appear in code. |
| UI/UX frontend engineering | `uiux-frontend-engineering` | When component naming, state ownership, rendering side effects, accessibility helpers, design-system adapters, or frontend tests become tangled. |
| Device driver development | `device-driver-development` | When driver modules, error paths, locking, resource ownership, and test scaffolding need maintainable structure without hiding hardware constraints. |
| Tech leadership | `tech-leadership` | When quantifying technical debt, refactoring investment, code health gates, staffing impact, or engineering standards. |
| Academic research | `academic-research-journal` | Rarely; only when building reproducible research code, analysis scripts, or artifact-review checklists. |

## Prompt Templates

### Code Review
```markdown
Review this code for clean-code and architecture risks.
Separate facts, inferences, assumptions, and questions.
Classify findings by impact: correctness, modifiability, security, performance, operations, or testability.
For each finding: cite file/line, name the smell, explain the architecture force, propose the smallest behavior-preserving fix, and define verification.
```

### Refactoring Plan
```markdown
Create a behavior-preserving refactoring plan.
First identify current behavior evidence and missing characterization tests.
Then sequence small transformations for naming, function extraction, class/module responsibility, boundary adapters, error handling, and tests.
Do not mix feature changes with cleanup unless explicitly required.
```

### Implementation Cleanliness Gate
```markdown
Before implementing this architecture, map each decision to code boundaries, contracts, tests, error paths, and ownership.
Flag speculative abstractions, hidden side effects, broad interfaces, duplicated policy, framework leakage, and untestable construction.
```

## Red Flags

- "We will clean it later" with no test-backed cleanup task.
- Refactor proposal that lacks behavior evidence.
- Clean-code review that only debates formatting.
- Functions with flags, hidden side effects, or mixed abstraction levels.
- Names that encode type/framework instead of domain meaning.
- Comments explaining what code should have said directly.
- Public API shaped by ORM, SDK, framework, or database leakage.
- Boundary wrappers with no tests.
- Error handling that drops context or exposes internal failures.
- Concurrency code with shared mutable state and no stress/failure tests.
- Architecture document that claims modularity while implementation has cycles and shared mutable utilities.
