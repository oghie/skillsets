# Engineering Culture, Structure, And Process

## Table Of Contents
- Structure As Learning
- Scale-Stage Structure
- Career Ladders
- Cross-Functional Teams
- Sustaining Engineering
- Engineering Process As Risk Management
- Code Review
- Architecture Review
- Learning Reviews
- Red Flags

## Structure As Learning
Do not frame structure as bureaucracy by default. Structure is how organizations encode learning and make success repeatable.

Use structure when failure patterns repeat:
- new hires slow teams down because onboarding is ad hoc.
- people leave because growth path is unclear.
- production incidents repeat because access or review rules are informal.
- roadmap changes create uncontrolled thrash.
- architecture decisions depend on whoever is loudest or closest.

Avoid structure too early when a small team is working well, risks are low, and communication is direct. The goal is the right amount of structure for current scale, risk tolerance, and business maturity.

## Scale-Stage Structure
Assess:

| Force | Leadership question |
|---|---|
| People | How much coordination is needed to move in one direction? |
| Age | Which habits are entrenched and which still need shaping? |
| Infrastructure | How much code, data, physical, or business infrastructure constrains change? |
| Risk tolerance | What mistakes are acceptable given regulation, customer impact, safety, and money at risk? |

As people, age, infrastructure, and risk grow, hidden power structures and informal decisions become expensive.

## Career Ladders
A career ladder should clarify:
- levels and scope.
- technical and management tracks.
- salary band relationship.
- promotion evidence.
- keystone promotions worth celebrating.
- behavioral expectations.
- leadership and operational ownership.
- security/reliability expectations where relevant.

Do not copy a ladder blindly. It must reflect the organization today and the organization being built.

## Cross-Functional Teams
Cross-functional teams improve product collaboration by putting engineering, product, design, data, operations, customer support, and other needed roles near the same problem.

Trade-off: they may reduce pure engineering optimization because communication structure shifts toward product delivery. Use central platform/infrastructure/security teams to preserve shared standards, core systems, and technical depth.

Leadership questions:
- Does day-to-day work follow product/business needs while management still supports technical growth?
- Which central teams set standards and provide leverage?
- How are platform, security, data, mobile, core infrastructure, and specialist needs handled?
- Are business-unit teams duplicating architecture or security mistakes?

## Sustaining Engineering
Reserve capacity for:
- refactoring.
- bugs.
- developer tooling.
- support.
- on-call improvements.
- test/deploy improvements.
- security and vulnerability remediation.
- small technical debt cleanup.

A useful default is to make sustaining work visible as a recurring capacity allocation. Large rewrites and major remediation still need explicit roadmap treatment.

## Engineering Process As Risk Management
Process should make hidden risk visible. It should be light for common low-risk activity and heavier for rare or high-risk change.

Ask:
- How often should this activity happen?
- What is the risk if it happens poorly?
- Can the process still create value when followed imperfectly?
- Does this process socialize risk to affected people?
- Does it slow down low-risk work unnecessarily?

## Code Review
Code review is partly quality control and partly socialization.

Guidelines:
- make expectations explicit.
- use tests for defect detection, not review theater.
- use linters/formatters for style.
- monitor review backlog and reviewer load.
- prevent reviews from becoming bullying or unrealistic standard enforcement.
- tune process to risk and team size.

## Architecture Review
Use architecture review for major systems/tooling changes:
- new language.
- new framework.
- new storage system.
- new developer tooling.
- new production dependency.
- major operational model change.

Prepared questions:
- How many people can maintain this?
- Do production standards exist?
- What rollout and training are needed?
- What new operational, security, and cost risks appear?
- Who is affected and must be in the review group?

The review board should include impacted operators and consumers, not unrelated gatekeepers. The value is often in preparing the review because it forces risk articulation.

## Learning Reviews
For outages and incidents, prefer learning review posture:
- resist blame.
- reconstruct context and contributing factors.
- identify missing tests, tools, runbooks, permissions, alerts, training, or communication.
- choose one or two high-risk follow-ups instead of a long unactioned list.
- explicitly decide which improvement ideas are deferred.

## Red Flags
- Structure is absent because leaders prefer hidden power.
- Structure is added because leaders want control, not learning.
- Career ladder is disconnected from salary and promotion reality.
- Cross-functional pods hide technical debt and on-call work.
- Product roadmap consumes all capacity and leaves no sustaining engineering.
- Architecture review is used to veto unrelated teams.
- Code review becomes style debate or public shaming.
- Learning reviews produce large lists with no prioritization.
