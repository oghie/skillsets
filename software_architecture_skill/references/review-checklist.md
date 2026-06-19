# Architecture Review Checklist

Use this checklist before finalizing architecture, ADRs, RFCs, modernization plans, or implementation plans.

## Requirements And Scope
- Stakeholders and concerns are named.
- Functional requirements have actors, triggers, outcomes, and acceptance criteria.
- NFRs are measurable scenarios.
- Non-goals and boundaries are explicit.
- Assumptions and open questions are separated from facts.

## Context And Boundary
- System boundary is clear.
- External actors, systems, devices, stores, and operators are included.
- Data/control/event flows crossing the boundary are named.
- Trust, ownership, network, and compliance boundaries are addressed.

## Schematic And Styles
- Candidate styles are evaluated against forces.
- Selected styles have clear benefits and costs.
- Style integration is coherent; generic roles are mapped to domain elements.
- Simpler alternatives are considered.
- KISS/YAGNI/DRY/SOLID/SoC trade-offs are applied where they affect boundaries or implementation complexity.
- The design is not driven by fashion or tool preference.

## Functional View
- Components have cohesive responsibilities.
- Interfaces are explicit.
- Dependency direction is defensible.
- Variation points are governed by contracts.
- Components can map to repository structure or services.

## Information View
- Persistent objects and stores are identified.
- Data ownership and update authority are clear.
- Cardinality, identity, lifecycle, retention, and privacy are considered.
- Shared data has governance and compatibility rules.
- Cache, replica, stream, and analytics stores have consistency rules.

## Behavior View
- Critical workflows are modeled.
- Async, retries, timeouts, ordering, idempotency, and dead-letter paths are defined.
- State transitions have triggers and owners.
- Failure, compensation, and recovery paths are not ignored.

## Deployment View
- Runtime nodes and execution environments are clear.
- Artifacts are allocated to nodes.
- Network paths, protocols, regions/zones, trust boundaries, and secrets are addressed.
- Build, release, health check, rollback, and operational ownership are defined.

## Development And Operation Views
- Logical components map to repositories, packages, modules, namespaces, services, or generated-code areas when implementation structure matters.
- Dependency rules, layer constraints, and database-access rules have checks or clear review criteria.
- Operational procedures cover backup/restore, migrations, upgrades, runbooks, SLOs, alerts, and incident ownership when relevant.
- Architecture diagrams, constraint specs, repository structure, and fitness functions are kept aligned when architecture-as-code is used.

## NFR Conformance
- NFRs link to facts/policies, criteria, selected tactics, impacted views, and verification.
- Tactics are evaluated for side effects.
- Security, privacy, observability, availability, performance, and deployability are not just claimed.
- Cost-sensitive decisions include estimate ranges, assumptions, uncertainty drivers, risk reserve, and update triggers.

## Identity And Access
- Authentication, authorization, identity, credential, and session responsibilities are separated.
- Protected resources, subjects, enforcement points, policy model, decision semantics, and audit events are explicit.
- RBAC/ABAC/PBAC/ACL/capability/reference-monitor choices are justified against threats and policy needs.
- Session/token TTL, rotation, revocation, logout-all, and stolen-token response are defined.
- MFA setup, challenge, disable, recovery, and factor deletion include step-up and abuse controls.
- Passwordless, password reset, email verification, and resend flows resist account enumeration.
- Admin role/status APIs prevent self-escalation, tenant escape, and unaudited privilege changes.
- Audit events cover login, refresh, logout, password reset/change, MFA changes, session revocation, account lifecycle, and admin changes.
- Cryptographic keys, token signing keys, reset tokens, recovery codes, and secrets have storage, rotation, and malformed-input handling rules.

## Evaluation
- Highest-risk elements have an evaluation method.
- Scenario walk-throughs cover critical workflows and quality attributes.
- Model-based, formal, PoC/prototype, queueing, benchmark, threat-model, or architecture fitness checks are selected when scenario review is insufficient.
- Findings have severity, evidence, impact, and action.
- Accepted trade-offs have revisit triggers.

## Engineering Readiness
- ADR/RFC artifacts are sufficient for implementation.
- API/event/schema contracts are versioned or migration-safe.
- Tests cover success, failure, migration, and rollback paths.
- Observability and runbooks support production operation.
- The plan has owners, sequencing, and validation gates.
