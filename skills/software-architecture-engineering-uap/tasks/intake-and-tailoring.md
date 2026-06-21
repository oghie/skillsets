# Intake And Tailoring

Use this when the architecture task is unclear, broad, or high risk.

## Inputs To Gather
- Product/system purpose.
- User roles and stakeholders.
- Existing system or greenfield status.
- Business goals and non-goals.
- Critical workflows.
- Current technology stack and deployment environment.
- Data sensitivity, compliance, safety, and security constraints.
- Latency, throughput, availability, cost, and timeline constraints.
- Team structure and operational ownership.
- Decision deadline and rollback cost.

## Tailoring Workflow

1. State the decision being made.
2. Separate known facts, inferences, assumptions, and questions.
3. Identify highest-risk unknowns.
4. Choose process depth:
   - `local`: affected modules/views only.
   - `focused`: one architecture decision or NFR trade-off.
   - `full`: A1-A6.
5. Select required artifacts and diagrams.
6. Define validation before implementation.

## Output Template

```markdown
## Architecture Work Plan
- Scope:
- Decision:
- Process depth:
- Required reads/artifacts:
- Known facts:
- Inferences:
- Assumptions:
- Open questions:
- Highest-risk unknown:
- Validation plan:
```

## Escalation Triggers

Use a full process when any are true:
- Multiple stakeholder groups conflict.
- Data ownership is unclear.
- External integrations are critical.
- NFRs drive success or failure.
- Security, privacy, compliance, or safety matters.
- Deployment topology changes.
- Migration or rollback is expensive.
- Distributed consistency or async behavior is involved.
- The design will become a long-lived platform boundary.
