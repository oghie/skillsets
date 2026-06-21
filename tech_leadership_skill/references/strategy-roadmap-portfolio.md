# Strategy, Roadmap, And Portfolio

## Table Of Contents
- Strategy Inputs
- Horizon Model
- Portfolio Allocation
- Roadmap Quality
- Technical Debt
- Scalability And Resilience
- Over-Engineering Control

## Strategy Inputs
Start with:
- Business outcome: growth, margin, retention, regulatory readiness, operational resilience, market expansion, customer experience, or platform leverage.
- Constraints: budget, time, regulation, security posture, skill gaps, vendor contracts, legacy estate, customer commitments.
- Technology forces: architecture, data, integration, cloud, security, platform maturity, operability, scalability, technical debt.
- Organizational forces: decision rights, team topology, incentives, culture, manager capability, hiring market.

## Horizon Model
Use three horizons:

| Horizon | Focus | Typical output | Failure mode |
|---|---|---|---|
| 0-90 days | Stabilize and unblock | Incident fixes, decision clarity, risk triage | Reactive chaos |
| 3-12 months | Execute and improve | Roadmap, capacity allocation, control improvements | Too many priorities |
| 1-3 years | Build strategic capability | Platform evolution, cyber maturity, data/AI capability, org model | Vague transformation |

## Portfolio Allocation
Classify work into:
- Run: operations, support, compliance, reliability, security monitoring.
- Grow: product features, revenue enablement, customer improvements.
- Transform: platform modernization, data/AI, major architecture, operating model change.
- Protect: cybersecurity, resilience, audit remediation, technical debt that reduces material risk.

Do not let protect work become invisible. If security, reliability, and technical debt have no capacity allocation, they become surprise outages, audit findings, or breach exposure.

## Roadmap Quality
A roadmap must show:
- Objective and measurable outcome.
- Initiative owner and decision owner.
- Dependencies and critical path.
- Capacity and funding assumptions.
- Risk, cybersecurity, compliance, and operational impact.
- Entry and exit criteria.
- Kill or pivot criteria.
- Review cadence.

## Technical Debt
Classify debt by consequence:

| Debt type | Signal | Leadership action |
|---|---|---|
| Delivery drag | Slow changes, high coordination cost | Refactor or platform investment |
| Reliability risk | Incidents, fragile deploys, untested recovery | Stabilization roadmap |
| Cyber risk | unsupported components, weak IAM, unpatched exposure | risk remediation or acceptance |
| Compliance risk | missing evidence, manual controls, unclear ownership | control design and audit pack |
| Talent risk | few people understand critical systems | documentation, pairing, succession |

## Scalability And Resilience
Do not treat scale as only throughput. Review:
- user growth, transaction growth, data growth, regional growth, vendor growth, integration growth, compliance growth.
- failure domains, blast radius, graceful degradation, recovery, failover, observability, incident response.
- cyber scale: asset inventory, identity sprawl, secrets, vendor access, detection coverage, vulnerability backlog.

## Over-Engineering Control
Over-engineering often appears when:
- risk is hypothetical but cost is real.
- leaders chase industry fashion without local constraints.
- architecture decisions are made without operating ownership.
- teams build platform abstractions before repeated demand exists.
- security tooling is bought before process, ownership, and evidence exist.

Ask:
1. What problem is this solving now?
2. What happens if we do nothing for one quarter?
3. What is the cheapest reversible experiment?
4. Who will operate this after launch?
5. What risk remains even if this succeeds?

## Strategic Output
End with:
- Recommended portfolio allocation.
- Roadmap by horizon.
- Decision gates.
- Risks and accepted trade-offs.
- Metrics and review cadence.
- Communication plan for executives, peers, teams, and audit/security stakeholders.
