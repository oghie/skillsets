# Delivery, Incident, And Reliability Leadership

## Table Of Contents
- Delivery Predictability
- Unblocking
- Agile Without Ritual Theater
- On-Call
- Incident Management
- Postmortem
- Reliability Operating Model

## Delivery Predictability
Predictability is not promising exact dates. It is the ability to explain confidence, dependencies, risk, and recovery options.

Track:
- committed vs completed work.
- cycle time and lead time.
- blocked work age.
- dependency age.
- scope churn.
- incident interruption.
- defect escape.
- decision latency.
- capacity spent on run/grow/transform/protect work.

## Unblocking
Use a blocker taxonomy:

| Blocker | Signal | Leadership action |
|---|---|---|
| Decision | team waits for approval | clarify decision owner and deadline |
| Dependency | another team/vendor blocks work | escalate with specific ask |
| Capacity | people overloaded | reduce WIP, reallocate, cut scope |
| Risk | security/compliance/architecture concern | decide mitigation or acceptance |
| Ambiguity | unclear outcome | define success and owner |
| Skill gap | team cannot execute | pair, train, hire, or partner |

## Agile Without Ritual Theater
Agile fails when rituals replace ownership. Check:
- Are teams empowered to make decisions?
- Are priorities stable enough for planning?
- Are product and engineering jointly accountable?
- Are retrospectives producing real changes?
- Are security, reliability, and technical debt included in capacity?

## On-Call
Healthy on-call needs:
- service ownership.
- alert quality.
- runbooks.
- escalation path.
- compensation or rotation fairness where appropriate.
- manager awareness of burnout.
- post-incident improvement.

Red flag: teams are rewarded for heroics while alert noise and poor operability remain.

## Incident Management
Define:
- severity levels.
- incident commander.
- communication owner.
- technical lead.
- business/customer lead.
- legal/security/privacy role when needed.
- update cadence.
- recovery objective.
- decision authority.

For cyber incidents, include forensic preservation, containment authority, regulatory/privacy review, and executive communication.

## Postmortem
Postmortem output:
- timeline.
- contributing factors.
- customer/business impact.
- detection and response gaps.
- failed assumptions.
- prevention and recovery improvements.
- owners and due dates.
- recurrence risk.

Avoid blame. Human error is usually a signal to inspect system design, workload, training, guardrails, incentives, and escalation.

## Reliability Operating Model
Use reliability controls:
- SLO/SLI and error budget.
- dependency and failure-domain mapping.
- capacity and saturation monitoring.
- backup/restore drill.
- DR/tabletop.
- change failure rate.
- repeat incident elimination.
- resilience backlog.

## Red Flags
- Roadmaps ignore incident load.
- On-call has no executive visibility.
- Reliability is expected but not funded.
- Postmortems create action items nobody owns.
- Critical services have no SLO.
- Security incidents are handled like normal outages.
