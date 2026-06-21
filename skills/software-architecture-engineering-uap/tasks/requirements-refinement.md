# Requirements Refinement

Use this when requirements are vague, conflicting, incomplete, overbroad, or not testable.

## Stakeholder Analysis

Create a profile:

```markdown
| Stakeholder | Goals | Concerns | Decisions Influenced | Evidence | Priority |
|---|---|---|---|---|---|
```

Consider users, operators, developers, platform teams, business owners, support, security, compliance, legal, data owners, partner systems, procurement, and regulators.

## Functional Requirement Refinement

Flag requirements that are:
- Ambiguous.
- Incomplete.
- Inconsistent.
- Duplicated.
- Unverifiable.
- Too broad.
- Missing actor, trigger, input, output, precondition, postcondition, or exception path.
- Mixing implementation with requirement without rationale.

Use this table:

```markdown
| ID | Original | Deficiency | Refined Requirement | Acceptance Criteria | Source |
|---|---|---|---|---|---|
```

## NFR Refinement

Convert quality concerns into measurable scenarios:

```markdown
| ID | Attribute | Stimulus | Environment | Response | Target | Priority | Source |
|---|---|---|---|---|---|---|---|
```

Quality attributes to check:
- Performance and latency.
- Scalability and capacity.
- Availability and disaster recovery.
- Reliability and recoverability.
- Security and privacy.
- Compliance and auditability.
- Modifiability and maintainability.
- Interoperability and portability.
- Observability and operability.
- Deployability and release safety.
- Usability and accessibility.
- Cost and resource efficiency.

## Output

Produce:
- Stakeholder map.
- Refined functional requirements.
- Measurable NFR scenarios.
- Conflicts and trade-offs.
- Questions that block architecture.
- Requirements that can be deferred.

## Red Flags

- "Must be scalable" with no workload.
- "Secure" with no threat model or trust boundary.
- "Real-time" with no latency target.
- "High availability" with no dependency/failure model.
- "Easy to change" with no expected change scenarios.
- "Support all integrations" with no protocols, owners, or data contracts.
