# Design Principles And Modularity

Use these principles to keep architecture decisions implementable at module, package, service, and code level. They are not slogans; apply them only after naming the force they control and the trade-off they introduce.

## Table Of Contents
- [Complexity Control](#complexity-control)
- [Coupling And Cohesion](#coupling-and-cohesion)
- [Clean Code As Local Architecture](#clean-code-as-local-architecture)
- [SOLID At Architecture Boundaries](#solid-at-architecture-boundaries)
- [Boundary Heuristics](#boundary-heuristics)
- [Overuse Warnings](#overuse-warnings)
- [Review Questions](#review-questions)

## Complexity Control

| Principle | Architecture Use | Warning |
|---|---|---|
| KISS | Prefer the simplest structure that satisfies measured requirements and known constraints. | Do not remove necessary safety, resilience, audit, or extensibility controls just to look simple. |
| YAGNI | Defer speculative platforms, plugins, service splits, queues, and abstraction layers until a concrete scenario requires them. | Does not apply to cheap guardrails that preserve maintainability or safety. |
| DRY | Remove duplicated business rules, policy decisions, schema definitions, and protocol transformations. | Do not merge two things merely because they currently look similar; accidental similarity can create false coupling. |
| Separation of Concerns | Keep domain rules, transport, persistence, identity, policy, workflow, and presentation concerns independently changeable. | Cross-cutting concerns still need explicit composition points. |
| Information Hiding | Hide volatile decisions behind stable interfaces: storage details, provider APIs, algorithms, policy engines, protocol details. | Hiding everything behind generic interfaces can erase useful domain semantics. |

Use these principles as decision filters:
1. Name the complexity being reduced.
2. Identify the volatile decision being hidden or deferred.
3. State what becomes easier to change.
4. State what becomes harder to see, test, or optimize.

## Coupling And Cohesion

High cohesion means a module has one coherent reason to exist. Loose coupling means a module can change with limited ripple effects.

| Signal | Architectural Interpretation | Action |
|---|---|---|
| Many unrelated methods or workflows in one component | Low cohesion | Split by business capability, lifecycle, data ownership, or actor workflow. |
| One change requires edits across many layers/modules | Tight structural coupling | Introduce stable interfaces, move behavior to owning component, or collapse pointless layers. |
| Shared database tables are updated by multiple components | Data ownership coupling | Define write owner, compatibility rules, and access/API boundaries. |
| Transport concerns leak into domain logic | Concern coupling | Isolate adapters, mappers, and protocol-specific error handling. |
| Shared utility package grows domain behavior | Hidden dependency hub | Move behavior back to domain modules; keep utilities small and generic. |
| Circular package/service dependencies | Boundary failure | Reassign responsibility or introduce event/API boundary with clear ownership. |

Coupling types to watch:
- Content coupling: one component reaches into another component's internals.
- Common coupling: components depend on shared global state or shared mutable configuration.
- Control coupling: one component passes flags that steer another component's internal logic.
- Stamp/data-structure coupling: components exchange a large object but use only fragments.
- Message/data coupling: lower risk when contracts are stable and semantically clear.

Cohesion ladder:
- Avoid coincidental, logical, and temporal grouping as stable architecture boundaries.
- Use procedural or sequential grouping only for workflow/pipeline components.
- Prefer communicational and functional cohesion for domain components.

## Clean Code As Local Architecture

Read `clean-code-craftsmanship.md` when the task involves source-level review, refactoring, implementation planning, or technical debt. Use clean-code signals to test whether architecture survives contact with implementation:

| Local Signal | Architecture Meaning | Action |
|---|---|---|
| Names hide intent, unit, lifecycle, or ownership | Domain model is implicit | Rename or introduce explicit concept before adding comments. |
| Function mixes policy, IO, formatting, and error translation | Boundary and responsibility are blurred | Extract policy, adapter, formatter, and error mapping. |
| Class/module has unrelated reasons to change | Low cohesion | Split by capability, lifecycle, workflow, or adapter role. |
| Domain code imports framework, ORM, SDK, or transport objects | Dependency direction is inverted | Add project-owned port/adapter when volatility or test friction justifies it. |
| Repeated auth, validation, retry, or transaction code | Cross-cutting policy is fragmented | Centralize enforcement or composition point and test it. |
| Tests are slow, brittle, or absent | Modifiability claim lacks evidence | Add characterization/unit/contract tests before refactoring. |

Clean-code review is not a formatting debate. It should name the force being protected: correctness, modifiability, security, performance, concurrency safety, operations, or cost.

## SOLID At Architecture Boundaries

| Principle | Architecture Translation | Useful For |
|---|---|---|
| SRP | A component/service/module owns one business capability, policy area, or operational concern. | Preventing service/module bloat. |
| OCP | Extend behavior through explicit variation points without editing stable core code. | Plugins, pricing rules, workflows, provider adapters. |
| LSP | Substitutable implementations preserve contracts, invariants, and error semantics. | Storage/provider swaps, strategy implementations, plugin APIs. |
| ISP | Consumers depend on focused interfaces rather than broad service objects. | Preventing fat APIs, reducing test setup and change blast radius. |
| DIP | High-level policy depends on abstractions; adapters depend on domain-owned contracts. | Isolating infrastructure, vendor SDKs, frameworks, and protocols. |

Apply SOLID only at useful seams. A small module can be simpler without explicit abstraction. Add abstraction when it protects a known variation point, supports testing of important policy, or prevents a dependency direction violation.

## Boundary Heuristics

Use this order when defining architecture boundaries:
1. Business capability and ubiquitous language.
2. Data ownership and write authority.
3. Lifecycle and transaction boundary.
4. Security/trust boundary.
5. Performance and scaling isolation.
6. Team ownership and release cadence.
7. Technology/runtime constraint.

Prefer modular monolith boundaries until independent deployment, independent scaling, regulatory isolation, or team autonomy justifies distributed boundaries.

For Rust crates, the boundary is often the public API rather than a runtime service. Treat `pub` items, feature flags, re-exports, generic bounds, trait implementations, error variants, and MSRV as architecture boundaries because downstream crates compile against them.

## Overuse Warnings

- Too much DRY can merge concepts that should evolve separately.
- Too much OCP can create plugin frameworks before variation is real.
- Too much DIP can hide concrete failure modes and make debugging harder.
- Too much layering can create pass-through code and scatter one business change across every layer.
- Too much service decomposition can turn simple consistency into distributed coordination.

## Review Questions

- Which part of the design is intentionally simple, and which complexity is still necessary?
- Which requirements justify every abstraction, layer, queue, service, plugin, or policy engine?
- Which component owns each business rule, data write, authorization decision, and external adapter?
- What change scenario would break the current boundaries?
- What test or fitness function proves dependency direction and boundary integrity?
