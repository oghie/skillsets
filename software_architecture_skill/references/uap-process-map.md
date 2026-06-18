# Unified Architecture Process Map

Use this process as a configurable architecture lifecycle. Apply only the depth needed for the system risk, decision cost, and implementation uncertainty.

## Architecture Flow

| Phase | Purpose | Core Questions | Main Outputs |
|---|---|---|---|
| A0 Intake and Tailoring | Decide process depth and scope | What decision is being made? What evidence exists? What can fail? | Work plan, assumptions, risk focus |
| A1 Requirements Refinement | Make requirements architecture-ready | Who cares? What must the system do? Which qualities matter? | Stakeholders, refined FRs, measurable NFRs |
| A2 System Context Analysis | Define system boundary and external relationships | What is inside/outside? Who invokes what? What data and events cross boundaries? | Boundary, functional, information, and behavior context |
| A3 Schematic Architecture Design | Choose and integrate architecture styles | Which structures match the forces? How do styles compose? | Candidate styles, selected schematic, rationale |
| A4 Architecture View Design | Turn schematic structure into implementable views | What components, data, behavior, and deployment nodes exist? | Functional, information, behavior, deployment views |
| A5 NFR Design | Embed quality tactics into the architecture | Which facts/policies drive tactics? What do tactics change? | NFR tactics, conformance map, verification plan |
| A6 Architecture Evaluation | Validate design before or during implementation | Which elements carry risk? Which method will reveal defects? | Findings, risks, accepted trade-offs, actions |

## Phase Details

### A0 Intake and Tailoring
- Capture the product/system purpose, business goal, user groups, current state, target state, timeline, budget, team shape, deployment context, and risk tolerance.
- Identify architectural decision drivers: scale, compliance, safety, availability, latency, cost, integration, modifiability, data ownership, and operational ownership.
- Select a process profile:
  - `local`: small change inside known architecture.
  - `focused`: one major decision, bounded context, or NFR trade-off.
  - `full`: new system, modernization, distributed architecture, regulated domain, or irreversible decision.

### A1 Requirements Refinement
- Identify stakeholders and concerns.
- Refine functional requirements into actor-trigger-response acceptance criteria.
- Refine NFRs into measurable quality scenarios with stimulus, environment, response, and target.

### A2 System Context Analysis
- Boundary context: external actors, external systems, stores, data flows, and system border.
- Functional context: use cases, actor interactions, domain areas, and workflow ownership.
- Information context: key objects, persistent state, relationships, ownership, and external data.
- Behavior context: control flow, invocation patterns, events, timing, and failure paths.

### A3 Schematic Architecture Design
- Identify candidate styles from system type, constraints, and forces.
- Evaluate each style for fit, liabilities, operational burden, team fit, and NFR impact.
- Integrate multiple styles into one schematic. Most real systems combine styles.
- Refine names from generic style roles into domain-specific elements.

### A4 Architecture View Design
- Functional view: components, responsibilities, interfaces, packages, variation points.
- Information view: persistent objects, data components, stores, ownership, access rules.
- Behavior view: activity, sequence, state, event, and timing logic.
- Deployment view: devices, execution environments, artifacts, networks, and runtime topology.

### A5 NFR Design
- Derive facts and policies that constrain quality.
- Convert them into desirable criteria.
- Select candidate tactics and evaluate side effects.
- Integrate selected tactics into architecture views.
- Validate conformance with explicit links from NFRs to facts, tactics, impacted views, and verification.

### A6 Architecture Evaluation
- Identify target elements: schematic, functional view, information view, behavior view, deployment view, NFR design, interfaces, data ownership, and migration path.
- Select methods based on risk: scenario walk-through, checklist, prototype, benchmark, model review, threat model, test execution, operational rehearsal, or formal reasoning.
- Record findings as defects, risks, accepted trade-offs, or action items.

## Tailoring Rules

| Situation | Recommended Depth |
|---|---|
| Local code change in stable architecture | A0, affected A2/A4 slice, tests |
| New feature across multiple modules | A0, A1, A2, A4, targeted A5 |
| New service/API/data boundary | A0-A4 plus NFR scenarios and ADR |
| Distributed/event-driven design | Full A1-A6 with behavior, idempotency, ordering, schema/replay policy, and observability focus |
| Security/compliance-sensitive work | Full A1, A2, A5, A6; threat model required |
| Migration/modernization | Current-state A2/A4, target A3/A4, A5, evaluation, rollout |
| High cost of rollback | Full A1-A6 plus prototype or staged validation |

## Traceability Chain

Preserve a chain like this:

```text
Stakeholder concern
  -> requirement or NFR
  -> context element
  -> architecture style force
  -> view element
  -> tactic or decision
  -> implementation task
  -> verification evidence
```

Breaks in this chain are findings. Do not hide them behind polished diagrams.

## Minimal Work Plan Template

```markdown
## Architecture Work Plan
- Scope:
- Process depth:
- Known facts:
- Assumptions:
- Open questions:
- Highest-risk decision:
- Required artifacts:
- Verification:
```
