# Metrics, KPI, And Dashboard

## Table Of Contents
- Metric Discipline
- KPI/KRA/OKR
- CSF To KPI Cascade
- Balanced Scorecard Adaptation
- Benchmarking And Targets
- Root Cause And Improvement
- Performance Management System
- Dashboard Design
- Leadership Review Questions

## Metric Discipline
Good leadership metrics connect strategy to action. Avoid vanity metrics.

Each metric needs:
- objective.
- owner.
- formula.
- data source.
- refresh cadence.
- target/threshold.
- decision it informs.
- known bias or blind spot.

## KPI/KRA/OKR
- KRA: area of responsibility or result area.
- KPI: measurable indicator that shows whether the result area is healthy.
- OKR: objective plus measurable key results for a time-bound change.

Use KPIs for operating control and OKRs for change focus. Do not overload OKRs with every operational metric.

## CSF To KPI Cascade
Use critical success factors to prevent KPI sprawl:
1. Strategic objective: what must be true for the organization.
2. Critical success factor: condition that must hold for the objective to succeed.
3. Critical information set: information needed to judge the factor.
4. KPI: measurable indicator with owner, source, threshold, and action.
5. Review cadence: forum where the KPI changes a decision.

Example:

| Objective | CSF | Critical information | KPI | Decision |
|---|---|---|---|---|
| Reduce customer-impacting incidents | Production risk visible before release | Change risk, test coverage, unresolved defects, rollback readiness | High-risk changes with verified rollback | Approve, delay, or add control |

Avoid copying another company's KPI catalog. A KPI is weak when it is not linked to strategy, owner authority, data quality, and a decision path.

## Balanced Scorecard Adaptation
For technology leadership, use perspectives:

| Perspective | Example questions |
|---|---|
| Business value | Are technology investments improving revenue, cost, risk, customer, or mission outcomes? |
| Customer/stakeholder | Are product, business, audit, and operational stakeholders getting what they need? |
| Internal process | Are delivery, security, incident, change, architecture, and governance processes predictable? |
| Learning and capability | Are teams building skills, platforms, and knowledge that improve future execution? |
| Risk and resilience | Are cyber, operational, regulatory, and continuity risks inside appetite? |

Use the scorecard as a cascade:
- enterprise objective.
- technology objective.
- team KRA.
- operating KPI.
- threshold and trigger.
- named forum and decision.

Do not mix diagnostic metrics and accountability metrics without saying which is which. Diagnostic metrics help teams learn; accountability metrics drive executive action and can distort behavior if incentives are wrong.

## Benchmarking And Targets
Benchmarking can be useful, but only after context is normalized.

Check:
- sector, regulation, and criticality.
- system age and architecture.
- team size, skill, and vendor dependence.
- service tier and SLO.
- run/grow/transform/protect allocation.
- incident, audit, and security burden.

Targets should have:
- baseline.
- expected range.
- stretch range.
- unacceptable range.
- confidence level.
- owner with authority.
- consequence of missing target.

Red flag: leadership asks for "industry benchmark" because it lacks its own operating baseline.

## Root Cause And Improvement
Use structured RCA when a metric misses target:
- 5 Whys for simple causal chain.
- Fishbone for multi-factor issues.
- FMEA for failure modes and control gaps.
- Current reality tree for reinforcing constraints.
- DMAIC-style framing when process stability matters.

Do not accept a metric miss explanation that blames people before checking system design, incentives, capacity, tools, decision latency, and unclear expectations.

Choose the improvement method by problem type:

| Situation | Better tool |
|---|---|
| Repeated incident class | Problem review, causal map, barrier/recovery redesign |
| Process variance | DMAIC-style measurement and control plan |
| Failure mode in planned change | FMEA with detection, prevention, and contingency |
| Conflicting constraints across teams | Current reality tree or dependency map |
| Unknown driver behind metric drift | Segment analysis, correlation, and qualitative interviews |

## Performance Management System
Performance management is not the annual appraisal. It is the loop connecting strategy, operational metrics, review cadence, improvement action, and people accountability.

Minimum system:
- strategic objectives and KRAs.
- scorecard and KPI definitions.
- metric owners and evidence owners.
- review cadence by altitude: team, department, executive, board.
- RCA path for misses.
- improvement backlog with owners.
- appraisal/calibration link for leadership behavior, not individual metric gaming.
- reporting principles: trend, variance, explanation, decision, action, due date.

Do not let the dashboard become a report-only artifact. If no decision changes after repeated red metrics, the operating system is broken.

For CTO, VP Engineering, board, or manager-system quantification, use `executive-managerial-quantification.md` to separate executive decision metrics from managerial diagnostic metrics.

## Dashboard Design
Recommended dashboard panels:
- Strategic outcomes: revenue enablement, cost reduction, risk reduction, customer commitments.
- Delivery: throughput, cycle time, predictability, dependency age, WIP, roadmap confidence.
- Reliability: availability, SLO/error budget, incident severity, MTTR, repeat incidents.
- Cybersecurity: critical findings age, patch SLA, MFA/PAM coverage, detection coverage, backup test, audit gaps.
- Finance: budget variance, run/grow/transform spend, cloud cost, vendor concentration, forecast.
- People: attrition, hiring, manager span, engagement, growth plans, performance calibration distribution.

Dashboard quality checks:
- Every panel has a decision owner.
- Every metric has a definition and data source.
- Trend is visible, not only current value.
- Thresholds are tied to risk appetite or business target.
- Narrative explains signal vs noise.
- Exceptions are dated and reviewed.
- Goodhart risk is named where incentives could distort behavior.

## Metric Red Flags
- A dashboard has no decision owner.
- Targets are copied from another company without context.
- Security metrics count tickets closed but not risk reduction.
- Delivery metrics reward output volume while quality and incident rates worsen.
- People metrics are used punitively and stop producing honest signals.
- A KPI is reported to the board but nobody can explain the formula.

## Leadership Review Questions
1. What changed since last review?
2. Is the change signal or noise?
3. Which decision does this require?
4. Which owner can act?
5. What risk rises if no action is taken?
6. What evidence should be reviewed next time?
