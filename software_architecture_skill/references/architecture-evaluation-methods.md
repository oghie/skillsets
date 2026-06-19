# Architecture Evaluation Methods

Architecture evaluation checks whether the design satisfies requirements, handles risks, and is ready for implementation or operation.

## Evaluation Targets

Evaluate the target elements that carry decision risk:
- Requirements and NFR scenarios.
- Boundary context and integrations.
- Schematic architecture and style selection.
- Functional components and interfaces.
- Information ownership, schemas, persistence, and consistency.
- Behavior flows, async semantics, state machines, and failure handling.
- Deployment topology, runtime environments, networks, and operations.
- NFR tactics and conformance map.
- Migration, rollout, rollback, and compatibility plans.

## Method Catalog

| Method | Best For | Output |
|---|---|---|
| Checklist Review | Broad defect discovery and completeness | Findings, missing artifacts, risk list |
| Scenario Walk-Through | Quality attributes and critical workflows | Scenario pass/fail, gaps, decisions |
| Trade-Off Analysis | Competing NFRs or style alternatives | Rationale, accepted costs, rejected alternatives |
| ATAM | Quality attribute trade-offs, risks, sensitivity points | Trade-off points, risks, non-risks, sensitivity points |
| CBAM | Architecture strategy prioritization under cost constraints | Benefit/cost reasoning and investment priorities |
| SAAM | Modifiability and change-impact evaluation | Direct, indirect, and non-supportable scenario findings |
| SBAR | Brownfield architecture reengineering | Current-state deficiencies and refactoring priorities |
| PATS | Performance evaluation through scenarios | Performance risks, bottlenecks, scenario metrics |
| Model-Based Evaluation | Structural, behavioral, or quality modeling | Quantitative/qualitative model findings |
| Architecture Fitness Function | Governed architecture rules and drift detection | Executable constraint result and remediation path |
| PoC-Based Evaluation | Feasibility of a narrow technical assumption | Go/no-go evidence for a specific uncertainty |
| Prototype/Spike | Unknown technical feasibility | Evidence, constraints, revised design |
| Benchmark/Load Test | Performance, latency, throughput, capacity | Metrics, bottlenecks, tuning actions |
| Threat Model | Security/privacy risk | Trust boundaries, threats, mitigations |
| Dependency/Code Inspection | Existing system review | Coupling, boundary violations, risks |
| Model Review | Data, state, interaction, or deployment correctness | Consistency findings |
| Formal/Static Analysis | Protocols, safety, invariants, concurrency, schemas | Proofs, counterexamples, warnings |
| Operational Readiness Review | Release and production support | Runbook, alerts, SLOs, rollback plan |

## Scenario Walk-Through Template

```markdown
| Scenario | Stimulus | Architecture Path | Expected Response | Risk | Finding | Action |
|---|---|---|---|---|---|---|
```

Walk the scenario through context, functional, information, behavior, deployment, and NFR views. Stop when a view lacks enough detail to answer.

## Finding Severity

| Severity | Meaning |
|---|---|
| Critical | Design can fail a core requirement, safety/compliance duty, or unrecoverable production scenario |
| High | Major risk to NFR, data integrity, security, delivery, or operations |
| Medium | Significant ambiguity, maintainability issue, or unverified assumption |
| Low | Documentation or local clarity issue that does not change the decision |

## Evaluation Report Template

```markdown
## Evaluation Scope
- Target elements:
- Evaluation methods:
- Evidence reviewed:

## Findings
| Severity | Finding | Evidence | Impact | Recommendation |
|---|---|---|---|---|

## Accepted Trade-offs
| Trade-off | Why accepted | Revisit trigger |
|---|---|---|

## Required Actions
| Action | Owner | Verification |
|---|---|---|
```

## Evaluation Rules

- Prefer executable evidence when possible: tests, traces, benchmarks, prototypes, schemas, or deployment manifests.
- A diagram can be evaluated only if it has enough semantics: named nodes, relationships, responsibilities, and boundaries.
- Do not claim a risk is mitigated until the mitigation appears in the relevant architecture view and verification plan.
- Record rejected alternatives and revisit triggers for decisions that depend on uncertain assumptions.

## Scenario-Based Evaluation

Use scenario-based evaluation when stakeholders need to test how architecture responds to realistic use cases, quality scenarios, growth, and stress conditions.

Scenario types:
- Use case scenarios for normal and exception workflows.
- Growth scenarios for increased load, data, users, tenants, regions, or features.
- Exploratory scenarios for faults, attacks, degraded dependencies, or abnormal conditions.

Representative methods:
- ATAM: expose quality attribute trade-offs, risks, sensitivity points, and non-risks.
- CBAM: compare architecture strategies by utility, cost, and risk.
- SAAM: evaluate modifiability and classify change scenarios as direct, indirect, or non-supportable.
- SBAR: evaluate and guide reengineering of existing systems.
- PATS: evaluate performance through scenario-driven analysis.

## Model-Based Evaluation

Use model-based evaluation when abstract structural, behavioral, or quality models can reveal issues before implementation.

Common models:
- Component-and-connector models for structure and dependency risk.
- Dependency graphs for modularity and change impact.
- Queueing models for latency, throughput, and resource contention.
- Resource-usage matrices for workload-to-resource cost/performance reasoning.
- Markov models for reliability and state-transition probabilities.
- Statecharts for complex state-dependent behavior with hierarchy or concurrency.
- Network simulation models for topology, latency, packet/flow behavior, and capacity.

## Formal Method-Based Evaluation

Use formal methods when correctness, safety, concurrency, protocol behavior, or critical invariants require mathematical rigor.

Representative techniques:
- Architecture Description Languages (ADL) for precise architecture specification.
- OCL or constraint specifications for model invariants.
- Abstract State Machines for operational semantics.
- Petri Nets for concurrency, synchronization, liveness, deadlock, and reachability.
- Temporal logic/model checking for ordering, safety, and liveness properties.

## Architecture-As-Code Evaluation

Use architecture-as-code evaluation when the design contains rules that can be checked repeatedly:
- allowed dependency direction;
- logical component to package/path mapping;
- layer and database access constraints;
- contract compatibility;
- security enforcement paths;
- code metrics with thresholds.

Treat a failed fitness function as evidence of misalignment. Decide whether code, diagrams, constraint specs, or the architecture decision should change.

## PoC And Prototype Evaluation

Use a PoC for a narrow uncertainty, such as whether one integration, library, deployment mode, or tactic is feasible.

Use a prototype when multiple design elements must work together under realistic conditions. Prototype evaluation is especially useful for NFRs such as performance, reliability, scalability, security, usability, and operability.
