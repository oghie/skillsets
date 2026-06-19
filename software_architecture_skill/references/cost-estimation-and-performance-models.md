# Cost Estimation And Performance Models

Use this reference when architecture decisions affect effort, schedule, operational cost, product performance, capacity, reliability investment, or risk reserve. Treat estimates as decision evidence with uncertainty, not as precise commitments.

## Table Of Contents
- [Estimation Discipline](#estimation-discipline)
- [Inputs Architects Must Provide](#inputs-architects-must-provide)
- [Technique Selection](#technique-selection)
- [Cost-Aware Architecture Decisions](#cost-aware-architecture-decisions)
- [Performance And Resource Usage Models](#performance-and-resource-usage-models)
- [Tracking And Update Loop](#tracking-and-update-loop)
- [Templates](#templates)

## Estimation Discipline

Architecture estimates must include:
- estimate target: size, effort, schedule, direct cost, operational cost, performance, reliability, defect risk, or maintenance cost;
- estimation method;
- assumptions and exclusions;
- confidence range or low/most-likely/high values;
- risk reserve;
- update trigger.

Use the uncertainty cone explicitly. Early estimates can be wide because users, external interfaces, constraints, performance bounds, algorithms, architecture, implementation technology, reliability, and workload scenarios may still be unknown.

Do not collapse uncertainty into a single number. Report ranges, confidence, and next evidence needed to narrow the range.

## Inputs Architects Must Provide

| Input | Why It Matters |
|---|---|
| Operational concept | Reveals users, operating modes, workload, environment, constraints, and usage frequency. |
| Key diagrams | Expose components, data flows, deployment shape, and interfaces that drive size and risk. |
| Product architecture | Partitions the system for sizing, WBS, integration, performance modeling, and ownership. |
| Quality attribute scenarios | Drive effort for performance, reliability, security, usability, modifiability, and compliance. |
| External software/COTS/SaaS choices | Shift effort from build to integration, licensing, governance, and operational risk. |
| Technology/runtime constraints | Affect productivity, staffing, performance, hardware, and deployment cost. |
| Reuse and migration assumptions | Require adaptation effort, compatibility work, and regression testing. |

Architectural decisions are estimation inputs. Every major architecture option should state cost drivers and uncertainty drivers.

## Technique Selection

| Technique | Use When | Output |
|---|---|---|
| Expert Judgment / Delphi | Historical data is weak and expert calibration is valuable. | Consensus estimate, assumptions, disagreement areas. |
| PERT | Work items have low/likely/high uncertainty. | Expected value, variance, risk reserve input. |
| Analogy | Comparable past systems exist. | Adjustment-based estimate. |
| Bottom-Up WBS | Scope can be decomposed into tasks/components. | Detailed effort/schedule plan. |
| Top-Down Allocation | Budget/schedule target exists and must be allocated. | Feasibility pressure and trade-off map. |
| Function Points / Use Case Points / SLOC | Functional size can be counted or approximated. | Size estimate for effort/cost models. |
| Parametric Models | Calibrated size and cost drivers exist. | Effort/schedule/cost projection. |
| COTS/Reuse Model | Integrating external/reused code dominates. | Adaptation and integration effort. |
| Risk Reserve | Risks are identified and impact can be estimated. | Contingency budget/schedule. |
| Earned Value / Status Tracking | Project is underway. | Actual-vs-plan feedback and estimate-to-complete. |

Use multiple models for important decisions. If models disagree, treat the gap as architecture risk and investigate.

## Cost-Aware Architecture Decisions

For each architecture option, evaluate:
- development effort and skill availability;
- operational cost: compute, storage, network, licensing, managed services, support;
- schedule risk and coordination overhead;
- migration and rollback cost;
- security/compliance evidence cost;
- testing and observability cost;
- total ownership cost over expected lifetime.

Common cost traps:
- microservices added without enough independent deployment value;
- event-driven infrastructure added without replay, schema, and observability budget;
- cloud services chosen without data egress, retention, and scale-floor analysis;
- custom platform/framework built before reuse demand is proven;
- performance targets accepted without workload model.

## Performance And Resource Usage Models

Use a resource-usage matrix before serious performance claims:

1. Define scenario/use case and execution count.
2. Identify software work units: calculations, DB accesses, messages, remote calls, cache operations, delays, file/object-store operations.
3. Map work units to computer resources: CPU, memory, disk, network, queue, external service, human/operator delay.
4. Estimate time/cost per unit.
5. Multiply by workload and identify bottlenecks.
6. Validate with benchmark, trace, load test, queueing model, simulation, or production measurement.

Queueing models and simulations are useful when contention, concurrency, service time, arrival rate, or network topology dominates latency/throughput. State their assumptions and limitations.

## Tracking And Update Loop

Update estimates when:
- requirements or operating modes change;
- architecture style, component partitioning, or external dependency changes;
- implementation technology changes;
- measured productivity/performance differs from assumptions;
- risk materializes or is retired;
- scope, quality targets, or staffing changes.

Track:
- size growth and volatility;
- productivity and cycle time;
- defect discovery/removal;
- performance/capacity measurements;
- cost-to-date and estimate-to-complete;
- risk reserve consumption.

## Templates

Estimate record:

```markdown
| Item | Method | Low | Likely | High | Assumptions | Risk Reserve | Update Trigger |
|---|---|---:|---:|---:|---|---:|---|
```

Architecture option cost model:

```markdown
| Option | Build Effort | Ops Cost | Schedule Risk | Migration/Rollback | Skill Risk | TCO Notes | Confidence |
|---|---:|---:|---|---|---|---|---|
```

Resource usage matrix:

```markdown
| Scenario | Executions | CPU Work | DB Accesses | Messages | External Calls | Delay/Wait | Bottleneck | Evidence |
|---|---:|---:|---:|---:|---:|---:|---|---|
```

Performance model traceability:

```text
Operational concept
  -> workload scenario
  -> software work units
  -> resource usage
  -> predicted response/cost
  -> benchmark/trace/load-test evidence
  -> revised architecture decision
```
