# SME And COE Operating Model

## Table Of Contents
- Purpose
- SME Model
- COE Model
- SME vs COE Decision
- Operating Flow
- Decision Rights
- Metrics
- Prompt Templates
- Red Flags

## Purpose
Subject Matter Experts (SMEs) and Centers of Excellence (COEs) are mechanisms for repeatable technical judgment. They should improve decision quality, reduce duplicated learning, and preserve scarce expertise without turning expertise into bureaucracy.

Use this module when the leader needs expert review, capability uplift, reusable practice, architecture/security/platform standards, deep domain knowledge, regulatory interpretation, legacy system understanding, vendor evaluation, or cross-team consistency.

## SME Model
Use an SME when the problem requires deep judgment in a narrow domain:
- regulated domain interpretation.
- legacy system behavior and migration risk.
- security, privacy, IAM, cryptography, infrastructure, data, AI, or architecture specialization.
- incident investigation where a failure mode is unusual.
- design review where a wrong decision is expensive or hard to reverse.
- requirements validation where domain rules are subtle.

SME responsibilities:
- clarify constraints, invariants, terminology, and failure modes.
- expose edge cases and hidden coupling.
- review risk and feasibility.
- propose options with trade-offs.
- teach teams enough to reduce repeated dependency.
- record reusable decision notes or guardrails.

SME is not a permanent veto unless authority is explicitly delegated. If an SME can block a decision, the escalation path, evidence threshold, and risk owner must be named.

## COE Model
Use a COE when the organization repeatedly needs a capability across teams:
- cloud platform engineering.
- cybersecurity and IAM practice.
- data engineering, analytics, AI governance, or MLOps.
- architecture review and reference patterns.
- DevOps, SRE, incident management, observability, and reliability.
- UX, accessibility, design systems, or frontend quality.
- compliance evidence automation.
- vendor/tooling standardization.

COE modes:

| Mode | When useful | Output | Risk |
|---|---|---|---|
| Advisory | Teams need expert guidance but retain delivery ownership | office hours, review notes, patterns | ignored advice |
| Enablement | Capability must spread across teams | training, playbooks, embedded coaching | activity without adoption |
| Platform/service | Shared tooling or paved road is needed | platform, templates, golden paths, automation | central bottleneck |
| Governance | Wrong decisions create enterprise risk | standards, exception process, audit evidence | theater and slow approvals |
| Community of practice | Knowledge sharing is the bottleneck | demos, shared problems, internal examples | low accountability |

COEs should have a lifecycle:
1. Bootstrap: define the capability, problem scope, owners, and first patterns.
2. Standardize: create reusable guidance, automation, templates, and evidence.
3. Federate: train champions inside teams and reduce central dependency.
4. Retire or narrow: sunset the COE when capability becomes normal practice or no longer matters.

## SME vs COE Decision
Use an SME when the question is deep and specific. Use a COE when the question is recurring and organizational.

| Trigger | Prefer SME | Prefer COE |
|---|---|---|
| One high-risk decision | yes | sometimes |
| Repeated team confusion | no | yes |
| Specialized regulatory interpretation | yes | if repeated |
| Tooling standardization | sometimes | yes |
| Incident root cause in a rare subsystem | yes | no |
| Capability uplift across departments | no | yes |
| Architecture exception review | yes | if pattern recurs |
| Audit evidence consistency | sometimes | yes |

## Operating Flow
```text
problem repeats or risk is high
  -> classify: expert judgment, repeatable capability, or both
  -> name decision owner and risk owner
  -> assign SME review or COE pattern ownership
  -> define output: recommendation, standard, template, training, or platform
  -> set adoption evidence and review cadence
  -> record exceptions and feedback
  -> federate, adjust, or sunset
```

## Decision Rights
Do not leave SME/COE authority implicit.

| Decision | Typical owner | SME role | COE role |
|---|---|---|---|
| Product priority | product/business owner | advise on domain risk | provide reusable constraints |
| Technical design | accountable engineering leader | validate feasibility and risk | maintain patterns and review gates |
| Security exception | risk acceptor named by policy | assess technical exposure | maintain standard and evidence path |
| Platform standard | platform leader | advise on edge cases | own golden path and lifecycle |
| Architecture exception | architecture authority or CTO delegate | provide specialist view | track exception and recurring pattern |
| Audit control | accountable control owner | interpret evidence quality | standardize evidence collection |

## Metrics
Measure whether expertise improves outcomes:
- adoption rate of COE patterns and golden paths.
- number and age of exceptions.
- repeated questions reduced.
- cycle time for review and enablement.
- incidents, audit findings, or production defects reduced in the covered area.
- time-to-enable a team.
- training completion with applied evidence, not attendance alone.
- SME bottleneck time and single-point-of-failure risk.
- team satisfaction with usefulness of COE support.

## Prompt Templates
SME review prompt:

```text
Act as a rigorous SME for [domain]. Review this decision/request/design.
Separate facts, assumptions, and missing evidence.
Identify hidden constraints, failure modes, edge cases, regulatory/security/data implications, and operational burden.
Provide: must-fix issues, acceptable trade-offs, questions for the accountable owner, and a recommendation with confidence.
If current law, standard version, vendor claim, or regulator position matters, say: This needs verification.
```

COE design prompt:

```text
Design a COE for [capability] in [organization context].
Classify the COE mode: advisory, enablement, platform/service, governance, or community of practice.
Define mission, non-mission, decision rights, service catalog, reusable assets, intake model, exception model, metrics, staffing, funding, first 90-day roadmap, and sunset/federation strategy.
Lead with the biggest risk that could make this COE become bureaucracy.
```

Capability reuse prompt:

```text
Given this recurring problem across teams: [problem], decide whether to solve it with SME review, COE enablement, platform automation, policy, training, or local team ownership.
Return a decision table with cost, speed, adoption risk, accountability, auditability, and long-term maintainability.
```

## Red Flags
- SME becomes the only person who can make progress.
- SME vetoes without risk owner, evidence, or alternatives.
- COE success is measured by documents created instead of adoption and outcomes.
- COE owns standards but not support, tooling, training, or exception handling.
- COE approvals are added to low-risk work.
- Teams outsource thinking to the COE and stop building local capability.
- Expert advice bypasses product, customer, operations, security, or compliance evidence.
- COE standardizes prematurely before seeing enough team variation.
