# Cost-Aware Architecture Decision

Use this task when architecture alternatives materially affect effort, schedule, operational cost, performance capacity, migration cost, or risk reserve.

## Procedure

1. Define the decision and alternatives.
2. Extract operational concept: users, modes, workload, data volume, external systems, operating environment, and constraints.
3. Identify cost drivers: size, complexity, integrations, COTS/SaaS, staffing, runtime resources, compliance evidence, migration, and operations.
4. Choose estimation methods: expert/Delphi, PERT, analogy, WBS, top-down allocation, function points/use case points/SLOC, parametric model, COTS/reuse model, or resource-usage model.
5. Produce ranges, not single values.
6. Define risk reserve and uncertainty drivers.
7. Compare alternatives by benefit, cost, risk, reversibility, and total ownership cost.
8. Define update triggers and evidence needed to narrow uncertainty.

## Output

```markdown
## Cost-Aware Decision
- Decision:
- Alternatives:
- Operational concept summary:
- Estimation method(s):
- Cost drivers:
- Estimate range:
- Risk reserve:
- TCO notes:
- Decision:
- Revisit/update trigger:
```

## Required Reads

- `references/cost-estimation-and-performance-models.md`
- `references/architecture-evaluation-methods.md` when CBAM, trade-off analysis, queueing model, benchmark, PoC, or prototype is needed.
