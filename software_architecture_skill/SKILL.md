---
name: software-architecture-engineering-uap
description: Use when designing, evaluating, documenting, modernizing, or implementing software architecture, including requirements refinement, system context analysis, architecture style selection, functional/information/behavior/deployment views, NFR tactics, architecture evaluation, ADR/RFC work, and engineering execution plans.
---

# Software Architecture Engineering UAP

## Core Rule
Treat architecture as traceable engineering: requirements -> context -> schematic style choices -> architecture views -> NFR tactics -> evaluation -> implementation work. Do not recommend structure, technology, or patterns without naming the forces, trade-offs, evidence, and validation path.

## First Pass
1. Classify the task: greenfield design, architecture review, modernization, decomposition, API/service design, data architecture, deployment planning, NFR design, evaluation, ADR/RFC, or implementation planning.
2. Identify scope and risk: users, stakeholders, business goals, current system evidence, constraints, critical workflows, quality attributes, team/deployment context, and reversibility.
3. Tailor the Unified Architecture Process: lightweight for local low-risk changes; full A1-A6 for high-risk, distributed, regulated, long-lived, or irreversible decisions.
4. Decide the visual artifacts needed: boundary/context, use case, component, class/data, activity, sequence, state, deployment, style schematic, or NFR conformance map.
5. Define verification before recommending: repository inspection, docs review, scenario walk-through, prototype, benchmark, threat model, operational review, or implementation test plan.

## Required Reads By Task
- Intake, scoping, or deciding how much process to use: `tasks/intake-and-tailoring.md`.
- Ambiguous requirements, stakeholder conflict, or missing acceptance criteria: `tasks/requirements-refinement.md`.
- External actors, integrations, data flows, system boundaries, or operational environment: `tasks/system-context-analysis.md` and `references/context-and-views.md`.
- Architecture style choice, schematic structure, decomposition, or modernization target: `tasks/schematic-architecture-design.md` and `references/architecture-style-catalog.md`.
- Functional, information, behavior, or deployment design: `tasks/architecture-view-design.md`, `references/context-and-views.md`, and `references/diagram-visualization-guide.md`.
- Performance, security, availability, modifiability, observability, compliance, or other NFR work: `tasks/nfr-and-conformance-design.md` and `references/nfr-tactics-and-conformance.md`.
- Architecture evaluation, review gate, design risk assessment, or validation plan: `tasks/architecture-evaluation.md` and `references/architecture-evaluation-methods.md`.
- Existing system review, refactor, migration, or modernization: `tasks/architecture-review-and-modernization.md`.
- ADR/RFC writing, implementation breakdown, rollout, tests, or repository mapping: `tasks/implementation-planning.md` and `references/engineering-translation.md`.
- Final architecture quality check: `references/review-checklist.md`.

## Decision Discipline
- Separate `Fact`, `Inference`, `Assumption`, and `Question`.
- For each major decision, state the decision, rationale, alternatives rejected, trade-offs, consequences, validation method, and engineering impact.
- Prefer the smallest viable architecture. Add distribution, indirection, async flow, shared platforms, or style complexity only when forces justify the cost.
- Treat diagrams as executable thinking aids: every diagram must clarify a boundary, ownership rule, interaction, deployment constraint, NFR impact, or implementation task.

## Architecture Heuristics
- Preserve dependency direction and data ownership before optimizing for frameworks.
- Prefer modular monoliths when independent deployment, team autonomy, or scale isolation is not yet justified.
- Use layered, MVC-family, N-tier, client-server, broker, dispatcher, event-driven, pub-sub, service-oriented, microservice, pipe-filter, repository, edge, controller, or plugin styles only when their forces match the system.
- Never accept "scalable", "secure", "fast", "reliable", or "cloud native" without measurable scenarios and verification.
- Connect every NFR tactic to affected views: functional components, data ownership, behavior/control flow, deployment topology, tests, observability, and operations.

## Evidence And Verification
- Inspect code, tests, schemas, API contracts, infra manifests, logs, ADRs, docs, and diagrams before judging an existing system.
- Current external facts such as service limits, pricing, regulations, CVEs, framework behavior, and product capabilities require live verification.
- Do not invent repository structure, requirements, latency numbers, uptime targets, security posture, compliance duties, or stakeholder priorities.
- Mark unknowns explicitly and explain why they affect architecture risk.

## Script Helper
- Run `scripts/architecture_static_audit.py <file-or-dir>` for a heuristic scan of architecture docs, ADRs, RFCs, and Markdown design plans for missing context, NFRs, view coverage, decision rationale, and common style risks.

## Output Standard
Lead with the architecture judgment or proposed path. Name assumptions, decision drivers, selected process depth, key diagrams/views, risks, validation commands or checks, and residual uncertainty. For implementation work, include repository impact, task breakdown, tests, rollout, observability, and rollback.
