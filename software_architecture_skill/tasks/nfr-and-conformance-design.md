# NFR And Conformance Design

Use this when quality attributes drive design or when quality claims need validation.

## Workflow

1. Identify facts and policies.
2. Derive desirable criteria.
3. Define candidate tactics.
4. Evaluate tactics against trade-offs.
5. Integrate selected tactics into architecture views.
6. Validate conformance.
7. Add cost, uncertainty, and operation/development impacts when tactics affect delivery or runtime ownership.

## Facts And Policies

Capture facts such as:
- User volume and workload shape.
- Critical workflow priority.
- Data sensitivity.
- Integration reliability.
- Deployment and region constraints.
- Team and operational limits.

Capture policies such as:
- Compliance obligations.
- Retention and deletion rules.
- Access control rules.
- Audit requirements.
- Availability targets or SLOs.

## Tactic Selection

Use:

```markdown
| NFR | Criterion | Candidate Tactic | Benefit | Cost/Side Effect | Selected? |
|---|---|---|---|---|---|
```

## Conformance Map

Use:

```markdown
| NFR | Facts/Policies | Criteria | Selected Tactics | Functional Impact | Information Impact | Behavior Impact | Deployment Impact | Verification |
|---|---|---|---|---|---|---|---|---|
```

Use the extended table in `references/nfr-tactics-and-conformance.md` when development or operation views matter.

## Integration Guidance

- Performance tactics often affect information and deployment views.
- Reliability tactics often affect behavior and data consistency.
- Security tactics affect all boundaries, interfaces, data stores, and deployment nodes.
- Observability tactics affect behavior flows, runtime artifacts, and incident response.
- Modifiability tactics affect component boundaries, interfaces, tests, and dependency rules.
- Cost tactics affect estimate assumptions, runtime resources, workload models, and update triggers.
- Architecture-as-code tactics affect development view, dependency rules, and CI checks.

## Completion Criteria

NFR design is ready when:
- NFRs are measurable.
- Selected tactics are visible in views.
- Side effects are acknowledged.
- Verification is concrete.
- Residual risk is accepted or assigned.
