---
name: software-architecture-engineering-uap
description: Use when designing, evaluating, documenting, modernizing, reviewing, refactoring, or implementing software architecture and code-level structure, including requirements, context, architecture style selection, microservices patterns, clean code, code smells, Rust crate/library API architecture, Cargo feature/MSRV/SemVer policy, unsafe/FFI/no_std/library testing, modularity, views, NFR tactics, IAM/auth, security patterns, cost estimation, architecture-as-code fitness functions, ADR/RFC work, and engineering execution plans.
version: 0.1.0
author: oghie
license: MIT
metadata:
  hermes:
    tags: ['software-development', 'architecture', 'design', 'patterns']
    source: https://github.com/oghie/skillsets
---

# Software Architecture Engineering UAP

## Core Rule
Treat architecture as traceable engineering: requirements -> context -> schematic style choices -> architecture views -> NFR tactics -> evaluation -> implementation work. Do not recommend structure, technology, or patterns without naming the forces, trade-offs, evidence, and validation path.

## First Pass
1. Classify the task: greenfield design, architecture review, modernization, decomposition, clean-code review/refactoring, Rust library/crate architecture, microservices pattern design, API/service design, data architecture, IAM/auth design, security-pattern design, cost-aware decision, deployment/operation planning, architecture-as-code governance, NFR design, evaluation, ADR/RFC, or implementation planning.
2. Identify scope and risk: users, stakeholders, business goals, current system evidence, constraints, critical workflows, quality attributes, team/deployment context, and reversibility.
3. Tailor the Unified Architecture Process: lightweight for local low-risk changes; full A1-A6 for high-risk, distributed, regulated, long-lived, or irreversible decisions.
4. Decide the visual artifacts needed: boundary/context, use case, component, class/data, activity, sequence, state, deployment, development/operation, style schematic, NFR conformance map, policy enforcement map, or fitness-function map.
5. Define verification before recommending: repository inspection, docs review, scenario walk-through, prototype, benchmark, threat model, operational review, or implementation test plan.

## Required Reads By Task
- Intake, scoping, or deciding how much process to use: `tasks/intake-and-tailoring.md`.
- Ambiguous requirements, stakeholder conflict, or missing acceptance criteria: `tasks/requirements-refinement.md`.
- External actors, integrations, data flows, system boundaries, or operational environment: `tasks/system-context-analysis.md` and `references/context-and-views.md`.
- Architecture style choice, schematic structure, decomposition, or modernization target: `tasks/schematic-architecture-design.md` and `references/architecture-style-catalog.md`.
- Microservices, modular monolith vs microservices, service decomposition, saga compensation/retry/idempotency, outbox relay/deduplication, CQRS projection/rebuild/lag, API composition, API gateway, BFF, service discovery, circuit breaker, event schema/order/replay/DLQ, contract testing, service chassis, service mesh, sidecar, strangler migration, anti-corruption layer, or production-ready service design: `tasks/microservices-pattern-architecture-design.md` and `references/microservices-pattern-language.md`.
- Design principles, modularity, coupling/cohesion, KISS, SOLID, DRY, YAGNI, SoC, package boundaries, or code-level architecture heuristics: `references/design-principles-and-modularity.md`.
- Clean code, code smells, refactoring, code review, craftsmanship, naming/functions/classes/comments/error handling/tests, behavior-preserving cleanup, technical debt reduction, or implementation hygiene: `tasks/clean-code-refactoring-and-review.md`, `references/clean-code-craftsmanship.md`, and `templates/clean-code-review-checklist.md`.
- Rust library, crate, SDK, parser, reusable package, public API design, Cargo features, MSRV, SemVer, `unsafe`, FFI, `no_std`, macro crate, async crate, or senior QA/testing plan for a Rust library: `tasks/rust-library-design-review-and-testing.md`, `references/rust-library-architecture.md`, `templates/rust-library-contract-matrix.md`, and `templates/rust-library-release-flow.mmd`.
- Functional, information, behavior, deployment, development, or operation design: `tasks/architecture-view-design.md`, `references/context-and-views.md`, `references/development-and-operation-views.md`, and `references/diagram-visualization-guide.md`.
- Identity, IAM, authentication, authorization, sessions, tokens, MFA, passwordless, account lifecycle, admin users, audit logs, or auth API design: `tasks/identity-access-design.md` and `references/iam-auth-architecture.md`.
- Security patterns, access-control models, policy engines, reference monitor, RBAC/ABAC/PBAC/ACL/capability, security logger/auditor, secure middleware/network patterns, misuse cases, or threat-driven design: `tasks/security-pattern-architecture-design.md` and `references/security-architecture-patterns.md`.
- Cost, estimation, schedule/effort risk, operational cost, total ownership cost, performance capacity, resource-usage modeling, PERT/WBS/function points/COCOMO-style reasoning, or queueing models: `tasks/cost-aware-architecture-decision.md` and `references/cost-estimation-and-performance-models.md`.
- Architecture-as-code, ADL-lite constraints, dependency rules, layer/database constraints, fitness functions, repository/package alignment, or architecture drift: `tasks/architecture-as-code-governance.md` and `references/architecture-as-code-and-fitness-functions.md`.
- Performance, security, availability, modifiability, observability, compliance, or other NFR work: `tasks/nfr-and-conformance-design.md` and `references/nfr-tactics-and-conformance.md`.
- Architecture evaluation, review gate, design risk assessment, or validation plan: `tasks/architecture-evaluation.md` and `references/architecture-evaluation-methods.md`.
- Existing system review, refactor, migration, or modernization: `tasks/architecture-review-and-modernization.md`.
- ADR/RFC writing, implementation breakdown, rollout, tests, or repository mapping: `tasks/implementation-planning.md` and `references/engineering-translation.md`.
- When a prompt primarily belongs to another skill but code-level maintainability is material, use the cross-skill map in `references/clean-code-craftsmanship.md`; do not load clean-code material for pure strategy, research, or architecture-only prompts without code/refactoring/testability impact.
- Quick UAP activity-step-task reminders or SRS intake extraction: `references/uap-appendix-artifact-playbooks.md`.
- Final architecture quality check: `references/review-checklist.md`.

## Decision Discipline
- Separate `Fact`, `Inference`, `Assumption`, and `Question`.
- For each major decision, state the decision, rationale, alternatives rejected, trade-offs, consequences, validation method, and engineering impact.
- Prefer the smallest viable architecture. Add distribution, indirection, async flow, shared platforms, or style complexity only when forces justify the cost.
- Treat diagrams as executable thinking aids: every diagram must clarify a boundary, ownership rule, interaction, deployment constraint, NFR impact, or implementation task.
- For cost-sensitive decisions, report estimate range, assumptions, uncertainty drivers, risk reserve, and update trigger.
- For governed boundaries, turn architecture rules into fitness functions or local verification commands when feasible.

## Architecture Heuristics
- Preserve dependency direction and data ownership before optimizing for frameworks.
- Treat clean code as component-level architecture: names, functions, classes, tests, error paths, and boundary adapters must preserve architecture decisions in executable form.
- Treat Rust libraries as public-contract architecture: every public item, feature flag, dependency type, auto-trait, MSRV promise, doc example, and release gate can become a compatibility boundary.
- Prefer modular monoliths when independent deployment, team autonomy, or scale isolation is not yet justified.
- Use layered, MVC-family, N-tier, client-server, broker, dispatcher, event-driven, pub-sub, service-oriented, microservice, pipe-filter, repository, edge, controller, or plugin styles only when their forces match the system.
- For microservices, require business capability/subdomain decomposition, data ownership, transaction/consistency strategy, API/event contracts, testing strategy, production-readiness baseline, team ownership, deployment/release path, and migration strategy when relevant.
- For refactoring, require behavior evidence first. Do not approve style-only churn unless it reduces ambiguity, coupling, risk, or change cost.
- Treat identity and access as a cross-cutting architecture boundary: session/token design, authorization checks, MFA recovery, admin surfaces, audit logs, and key management must be explicit.
- Treat security as pattern-driven architecture, not only auth endpoints: define protected resources, subjects, policy model, enforcement points, decisions, audit events, and misuse cases.
- Never accept "scalable", "secure", "fast", "reliable", or "cloud native" without measurable scenarios and verification such as SLO, p95/p99, RTO/RPO, workload, or load-test evidence.
- Connect every NFR tactic to affected views: functional components, data ownership, behavior/control flow, deployment topology, development structure, operations, tests, observability, and rollback.

## Evidence And Verification
- Inspect code, tests, schemas, API contracts, infra manifests, logs, ADRs, docs, and diagrams before judging an existing system.
- Current external facts such as service limits, pricing, regulations, CVEs, framework behavior, and product capabilities require live verification.
- Do not invent repository structure, requirements, latency numbers, uptime targets, security posture, compliance duties, or stakeholder priorities.
- Mark unknowns explicitly and explain why they affect architecture risk.

## Script Helper
- Run `scripts/architecture_static_audit.py <file-or-dir>` for a heuristic scan of architecture docs, ADRs, RFCs, and Markdown design plans for missing context, NFRs, view coverage, decision rationale, and common style risks.
- Run `scripts/architecture_constraint_audit.py --root <repo> --config <constraints.json>` for lightweight architecture-as-code checks over component path mappings, allowed dependencies, and forbidden imports.
- Run `scripts/rust_library_surface_audit.py <crate-root>` for a heuristic Rust crate review over `Cargo.toml`, public API shape, docs, unsafe comments, feature/dependency posture, examples, and integration-test signals.

## Output Standard
Lead with the architecture judgment or proposed path. Name assumptions, decision drivers, selected process depth, key diagrams/views, risks, cost/uncertainty when relevant, validation commands or checks, and residual uncertainty. For implementation work, include repository impact, task breakdown, tests, rollout, observability, and rollback.
