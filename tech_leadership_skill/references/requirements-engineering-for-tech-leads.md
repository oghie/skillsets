# Requirements Engineering For Tech Leads

## Table Of Contents
- Purpose
- Functional vs Technical Requirements
- Requirements Flow
- Functional Requirement Structure
- Technical Requirement Structure
- Non-Functional Requirements
- Traceability
- Review Questions
- Example
- Prompt Templates
- Red Flags

## Purpose
Tech leads translate business intent into requirements that teams can build, operate, secure, test, and change. A requirement is not ready because it sounds reasonable. It is ready when its owner, scope, constraints, acceptance evidence, risk, dependencies, and validation path are explicit.

Use this module for functional requirements, technical requirements, product/engineering specifications, architecture-ready stories, migration requirements, compliance-driven requirements, platform requirements, and review of ambiguous delivery requests.

## Functional vs Technical Requirements
Functional requirements describe behavior visible to users, operators, business processes, integrations, or policy rules.

Technical requirements describe qualities, constraints, interfaces, controls, operational behavior, and implementation boundaries needed to make the functional behavior safe and sustainable.

| Requirement type | Answers | Examples |
|---|---|---|
| Functional | What must the system do? For whom? Under what business rule? | register user, approve invoice, search policy, reconcile payment |
| Technical | What must be true about performance, security, data, deployment, operation, integration, and maintainability? | p95 latency, idempotency, encryption, retention, rollback, observability |
| Non-functional | What quality attribute must be achieved and measured? | availability, scalability, accessibility, privacy, reliability, cost |
| Constraint | What decision is already bounded? | jurisdiction, budget, vendor, legacy interface, device, network |
| Acceptance criteria | How will stakeholders know it is done? | testable examples, thresholds, evidence source |

## Requirements Flow
```text
business problem
  -> outcome and user/process owner
  -> scope and non-scope
  -> actors, journeys, use cases, business rules
  -> data and integration boundaries
  -> non-functional requirements
  -> security/privacy/compliance constraints
  -> operational and support model
  -> acceptance criteria and test evidence
  -> traceability to roadmap, risk, and controls
  -> stakeholder sign-off or risk acceptance
```

## Functional Requirement Structure
Use this structure for each meaningful behavior:

```text
ID:
Title:
Actor:
Goal:
Business objective:
Preconditions:
Trigger:
Main flow:
Alternative flow:
Failure flow:
Business rules:
Data created/changed/read:
External systems:
Acceptance criteria:
Out of scope:
Owner:
Validation evidence:
```

Functional requirement checks:
- Can a non-engineering stakeholder verify the behavior?
- Is the actor explicit?
- Are preconditions and failure paths written?
- Are business rules separated from UI preference?
- Are edge cases named instead of hidden in discussion?
- Is the requirement testable without guessing intent?

## Technical Requirement Structure
Use this structure for the engineering specification:

```text
ID:
Related functional requirement IDs:
Architecture context:
System boundary:
Interfaces/API/events:
Data model and lifecycle:
Security controls:
Privacy and compliance constraints:
Performance target:
Availability/reliability target:
Scalability assumption:
Observability:
Operational runbook impact:
Deployment and rollout:
Migration/backfill:
Rollback:
Testing strategy:
Dependencies:
Open risks:
Owner:
Validation evidence:
```

Technical requirement checks:
- Is each target measurable?
- Are data retention, deletion, audit, and lineage addressed?
- Is authentication, authorization, and identity flow explicit where needed?
- Are failure modes and retry/idempotency rules defined?
- Are observability and operational ownership included?
- Does rollout include migration, compatibility, and rollback?
- Are cost and capacity assumptions visible?

## Non-Functional Requirements
Do not accept vague NFRs such as "fast", "secure", "scalable", or "highly available".

| Dimension | Requirement shape | Evidence |
|---|---|---|
| Performance | p50/p95/p99 latency, throughput, batch window | load test, APM, benchmark |
| Scalability | expected users, tenants, data growth, concurrency, partitioning | forecast, capacity model |
| Availability | service hours, allowed downtime, RTO/RPO | SLO, incident history, DR test |
| Reliability | retries, idempotency, failure handling, degradation mode | chaos/tabletop, integration test |
| Security | authn/authz, secrets, encryption, logging, abuse controls | threat model, control test |
| Privacy | data minimization, consent/legal basis, retention, deletion, access | DPIA/privacy review when applicable |
| Compliance | named obligation, control owner, evidence, retention | audit pack, control mapping |
| Operability | runbook, alert, dashboard, ownership, support hours | on-call review |
| Accessibility | WCAG level or equivalent target where applicable | accessibility test |
| Maintainability | modularity, code ownership, upgrade path, documentation | review checklist |
| Cost | budget threshold, unit cost, cloud/resource forecast | FinOps model |

When exact laws, standards, sector rules, or contract terms determine an NFR, say exactly: `This needs verification.`

## Traceability
Maintain a chain:

```text
business outcome -> roadmap item -> functional requirement -> technical requirement
  -> test/evidence -> operational control -> metric -> owner
```

Minimum traceability table:

| Business outcome | Functional req | Technical req | Risk/control | Test/evidence | Owner |
|---|---|---|---|---|---|
| | | | | | |

## Review Questions
Business/product:
- What business outcome changes if this ships?
- Who is the user, buyer, operator, approver, and support recipient?
- What is out of scope?
- What failure is acceptable and what failure is not?
- What decision must be made now versus after discovery?

Engineering:
- What existing system becomes harder to change?
- What data grows fastest and what must be archived or deleted?
- What dependency can block delivery or runtime?
- What is the simplest reversible implementation?
- What must be measured from day one?

Security/privacy/compliance:
- What identity, role, permission, and audit trail is required?
- What sensitive data is processed, stored, logged, exported, or inferred?
- Which requirement is legal, contractual, customer-driven, or internal policy?
- Who accepts residual risk?
- What evidence must exist before launch?

Operations/support:
- Who gets paged?
- What alert means user impact?
- What is the rollback and communication path?
- What support procedure changes?
- What should the dashboard show during launch?

## Example
```text
Functional requirement:
The system shall allow an authenticated account owner to deactivate a workspace.
Precondition: account owner is active and workspace has no unpaid invoice hold.
Business rule: deactivation disables new writes immediately and schedules deletion after the retention window.
Acceptance: owner can deactivate, members lose write access, audit event is recorded, recovery is available before deletion.

Technical requirement:
Deactivation must be idempotent, emit WorkspaceDeactivated event once, write an immutable audit log, remove active sessions for workspace-scoped tokens, preserve billing records, show p95 API latency under the agreed threshold, and expose dashboard counters for deactivation failures.
Retention window and deletion obligations: This needs verification.
```

## Prompt Templates
Requirement drafting prompt:

```text
Convert this business request into functional and technical requirements.
Separate facts, assumptions, questions, and decisions.
Produce functional requirements with actor, goal, preconditions, main flow, failure flow, business rules, data touched, and acceptance criteria.
Produce technical requirements covering architecture boundary, API/events, data lifecycle, IAM, security/privacy/compliance, performance, availability, observability, rollout, rollback, migration, tests, owners, and validation evidence.
Flag vague NFRs and rewrite them as measurable thresholds. If current law, standard, or contractual obligation matters, say: This needs verification.
```

Requirement review prompt:

```text
Review these requirements as a skeptical tech lead.
Find ambiguity, missing owners, hidden coupling, missing failure modes, untestable acceptance criteria, security/privacy gaps, operational gaps, migration risk, cost risk, and stakeholder misalignment.
Return must-fix issues first, then questions, then a revised requirement outline.
```

Scope control prompt:

```text
Given this requirement set, identify what belongs in MVP, what belongs in later iteration, what is a hard compliance/security gate, and what should be rejected as over-engineering.
Explain decision criteria and validation needed before implementation.
```

## Red Flags
- "Fast", "secure", "scalable", "reliable", or "enterprise-grade" without thresholds.
- Functional requirement includes implementation detail without a reason.
- Technical requirement ignores user outcome or business rule.
- No acceptance criteria.
- No owner for requirement, risk, data, operation, or evidence.
- Security/privacy review is delayed until implementation is complete.
- Migration/backfill/rollback is missing.
- No traceability from requirement to test or control evidence.
- Requirements are written as a solution before the problem is understood.
- Stakeholders approve wording they cannot validate.
