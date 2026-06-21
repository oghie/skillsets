# Task: Write Functional And Technical Requirements

## Goal
Turn ambiguous business, product, platform, migration, or compliance requests into requirements a team can build, test, secure, operate, and validate.

## Required Inputs
- Business problem and desired outcome.
- User, customer, operator, or process owner.
- Scope and non-scope.
- Existing systems, data, integrations, and constraints.
- Security, privacy, compliance, audit, and operational obligations.
- Delivery horizon and risk appetite.

## Steps
1. Separate facts, assumptions, questions, and decisions.
2. Draft functional requirements with actor, goal, preconditions, main flow, failure flow, business rules, data touched, and acceptance criteria.
3. Draft technical requirements with architecture boundary, interfaces, data lifecycle, IAM, security, privacy, compliance, performance, availability, scalability, observability, deployment, migration, rollback, and tests.
4. Rewrite vague non-functional requirements into measurable thresholds or explicit open questions.
5. Build traceability from business outcome to functional requirement, technical requirement, control/risk, test/evidence, and owner.
6. Review with product, engineering, security/privacy, operations, data, and compliance stakeholders where material.
7. Mark launch blockers, later-iteration items, rejected over-engineering, and verification items.

## Verification
- No requirement relies on words like fast, secure, scalable, reliable, or enterprise-grade without a measurable definition.
- Acceptance criteria can be tested.
- Data lifecycle and IAM are explicit when data or users are involved.
- Migration, rollout, rollback, and observability are covered.
- Current legal, regulatory, standard, or contract applicability is not asserted without `This needs verification.`

## Output
Use `templates/functional-technical-requirements.md` and optionally `templates/mermaid-requirements-flow.mmd`.
