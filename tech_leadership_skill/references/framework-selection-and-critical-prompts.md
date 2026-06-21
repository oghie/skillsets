# Framework Selection And Critical Prompts

## Table Of Contents
- Core Rule
- Framework Families
- Selection Matrix
- When Not To Use A Framework
- Critical Questions
- Prompt Templates
- Output Shape
- Red Flags

## Core Rule
Frameworks are decision aids, not substitutes for leadership judgment. Select a framework only after naming the business problem, regulatory or contractual driver, decision owner, operating model, evidence burden, cost of adoption, and failure mode.

If exact standard edition, certification status, jurisdiction, regulator position, audit scope, vendor ranking, pricing, or legal applicability matters, say exactly: `This needs verification.`

## Framework Families
| Framework / reference | Use when | Do not use when | Typical output |
|---|---|---|---|
| ITSM | The organization must manage IT services, incidents, requests, service catalog, SLAs, support ownership, and operational accountability | The problem is product discovery or architecture design | service model, incident/problem/change process, SLA/OLA |
| ITIL | The leader needs a recognized ITSM practice model and common service-management vocabulary | The team only needs lightweight startup operations | adapted ITSM practices, service value stream, change enablement |
| COBIT | Board, audit, risk, or enterprise governance needs clear control objectives and governance over information and technology | A delivery team needs sprint mechanics | governance objectives, control mapping, maturity assessment |
| TOGAF | Enterprise architecture needs business/data/application/technology alignment, target architecture, transition roadmap, and architecture governance | A single product needs a small design review | architecture vision, capability map, transition roadmap, governance |
| ISO/IEC/IEEE | International standard alignment is needed for architecture description, lifecycle, requirements, quality, security, privacy, service management, or risk | The team cannot name which standard and why | standard-specific checklist, conformance evidence |
| PCI DSS | Cardholder data environment, payment card processing, or payment ecosystem obligations are in scope | The product never stores, processes, or transmits payment card data | CDE scope, control mapping, segmentation evidence |
| PMBOK | Large projects/programs need scope, schedule, cost, stakeholder, procurement, risk, and governance discipline | Product discovery needs fast iteration and uncertain scope | project charter, WBS, risk register, integrated plan |
| CMMI | The organization needs process capability improvement, maturity benchmarking, or contract-driven maturity evidence | The problem is lack of product-market clarity | maturity appraisal plan, capability improvement roadmap |
| AICPA/SOC 2 | Customers need assurance over service organization controls for security, availability, confidentiality, processing integrity, or privacy | A technical team only needs internal control hygiene | audit scope, trust service criteria mapping, evidence plan |
| CNCF | Cloud-native platform, Kubernetes ecosystem, service mesh, observability, runtime, or platform maturity choices are in scope | A team wants vendor popularity as architecture proof | technology shortlist, maturity/risk assessment, platform roadmap |
| Gartner Magic Quadrant | Market/vendor shortlisting needs an external market-research input | A leader wants to outsource architecture, procurement, or risk analysis to a quadrant | vendor evaluation input, not final decision |
| HIPAA | US healthcare protected health information or covered-entity/business-associate context may apply | Healthcare is only a loose market label with no PHI handling | HIPAA applicability review, safeguard/evidence plan |
| GDPR | EU/EEA personal data processing, data subject rights, lawful basis, international transfer, or processor/controller duties may apply | The organization has no EU/EEA personal data exposure | privacy requirements, DPIA trigger, transfer/control review |
| PDP | Indonesian personal data protection obligations may apply | The system has no Indonesian personal data, entity, user, or processing nexus | PDP applicability review, privacy controls, evidence plan |
| SAFe | Many teams, shared value streams, regulatory dependencies, and portfolio coordination require scaling discipline | It will preserve command-and-control while relabeling it agile | portfolio/value-stream model, PI planning guardrails |
| Lean Six Sigma | Process defects, waste, variation, rework, and measurable operational inefficiency need reduction | The work is creative discovery with high uncertainty | DMAIC charter, root cause, control plan |
| DORA / MTTR | Software delivery and operational performance need quantified improvement | Metrics will be used to punish teams or rank individuals | metric baseline, improvement hypotheses, reliability actions |

## Selection Matrix
Start by classifying the problem:

| Problem driver | Primary lens | Secondary lens |
|---|---|---|
| Board governance and risk oversight | COBIT | ISO/IEC, SOC 2, cybersecurity framework |
| Enterprise architecture transformation | TOGAF | ISO/IEC/IEEE 42010, portfolio governance |
| Service outage, support chaos, weak change control | ITSM/ITIL | DORA, Lean Six Sigma |
| Payment card exposure | PCI DSS | SOC 2, ISO/IEC 27001, threat model |
| Customer assurance for SaaS | SOC 2 | ISO/IEC 27001, privacy law review |
| Healthcare data in US context | HIPAA | SOC 2, ISO/IEC 27001/27701 |
| EU personal data processing | GDPR | privacy engineering, ISO/IEC 27701 |
| Indonesia personal data processing | PDP | privacy engineering, local legal review |
| Large program coordination | SAFe or lighter portfolio model | PMBOK, DORA |
| Process defect or operational variation | Lean Six Sigma | ITSM, DORA |
| Cloud-native technology choice | CNCF landscape and maturity | architecture review, vendor due diligence |
| Vendor shortlist | Gartner Magic Quadrant plus internal criteria | proof-of-concept, TCO, risk review |

## When Not To Use A Framework
Do not introduce a framework when:
- the problem is unclear.
- the accountable owner is missing.
- the organization wants certification theater without changing behavior.
- the team lacks capacity to operate the framework.
- a smaller artifact would work: decision memo, risk register, service catalog, ADR, runbook, or one policy.
- adoption cost is greater than the risk being controlled.
- framework vocabulary will obscure business accountability.

## Critical Questions
Universal:
- What decision will this framework improve?
- What risk does it reduce and how will that be evidenced?
- Who owns adoption, funding, operation, audit evidence, and exceptions?
- What current process will be removed or simplified?
- What is the minimum viable implementation?
- What failure mode will the framework create if misused?
- What current edition, legal applicability, certification scope, or market claim requires verification?

ITSM/ITIL:
- What is a service, who owns it, and what is the customer promise?
- Are incident, problem, change, request, configuration, and knowledge management separated correctly?
- What changes need formal change enablement and what changes should remain lightweight?
- How are SLAs, OLAs, SLOs, and support hours connected?

COBIT:
- Which governance objectives matter to board/audit/risk now?
- What control is missing: evaluate, direct, monitor, align, build, deliver, or assess?
- What evidence proves governance is working beyond policy existence?
- What will be right-sized for company stage and sector?

TOGAF:
- What business capability, value stream, data domain, application estate, and technology estate are in scope?
- Which stakeholders and concerns require architecture views?
- What is baseline, target, transition architecture, and migration risk?
- What architecture governance is needed without blocking delivery?

ISO/IEC/IEEE:
- Which exact standard is relevant: requirements, lifecycle, architecture description, quality, security, privacy, risk, service management, continuity, or testing?
- Is conformance required, or is it only a source of good practice?
- What edition and scope apply? This needs verification.

PCI/HIPAA/GDPR/PDP/SOC 2:
- What data is in scope and where does it flow?
- Who is controller/processor, covered entity/business associate, merchant/service provider, or service organization as applicable?
- What controls are required by law, contract, audit scope, or customer expectation?
- What evidence must exist before launch or audit?
- Who accepts residual risk?

CNCF/Gartner:
- Is this market scan, architecture decision, procurement, or platform strategy?
- What workload, operating model, skills, lock-in, support, and total cost constraints matter?
- What proof-of-concept will disprove the vendor/tool choice?
- What criteria matter more than market position?

SAFe/PMBOK/Lean Six Sigma/DORA:
- Is the problem coordination, project control, process variation, or delivery performance?
- Are metrics used for learning or punishment?
- What ceremonies or reports will be removed?
- What is the shortest feedback loop to validate improvement?

## Prompt Templates
Framework selector:

```text
Act as a skeptical CTO advisor. Given this context: [context], select whether ITSM/ITIL, COBIT, TOGAF, ISO/IEC/IEEE, PCI DSS, PMBOK, CMMI, SOC 2, CNCF, Gartner Magic Quadrant, HIPAA, GDPR, PDP, SAFe, Lean Six Sigma, DORA/MTTR, or no framework is appropriate.
Start with the strongest reason not to add a framework.
Then provide a decision matrix: problem driver, applicable framework, why, adoption cost, evidence required, owner, minimum viable implementation, and misuse risk.
For any current law, standard edition, audit rule, vendor claim, or jurisdiction question, say: This needs verification.
```

Compliance applicability:

```text
Determine whether [framework/law/standard] is applicable to [system/company/context].
Separate legal/contractual requirement, customer assurance expectation, internal policy, and good practice.
Map data/process scope, accountable owner, evidence source, exceptions, launch blockers, and unresolved questions.
Do not assert current legal obligations without verification. Use: This needs verification.
```

Governance adoption:

```text
Design a minimum viable adoption plan for [framework] in [organization].
Include scope, non-scope, accountable executive, operating owner, policy changes, process changes, evidence, metrics, rollout phases, training, tooling, exception handling, and stop conditions.
Call out where the framework would create bureaucracy or false confidence.
```

Vendor evaluation:

```text
Evaluate vendors/tools for [capability] using Gartner/CNCF/external market input only as one signal.
Build criteria for workload fit, security, compliance, data residency, integration, operability, support, lock-in, migration path, TCO, skill availability, roadmap risk, and proof-of-concept tests.
Return a decision memo and disqualifying red flags.
```

DORA improvement:

```text
Assess delivery and operational performance using DORA/MTTR without weaponizing metrics.
Define baseline, segmentation by service/team, leading indicators, qualitative context, improvement hypotheses, experiment cadence, and guardrails against metric gaming.
```

## Output Shape
For framework work, produce:
- decision summary.
- strongest objection.
- selected framework or "no framework".
- scope and non-scope.
- owner and decision rights.
- minimum viable implementation.
- evidence and audit path.
- metrics and cadence.
- adoption risks and anti-patterns.
- verification items.

## Red Flags
- Framework is chosen because a leader likes the brand.
- Gartner Magic Quadrant is treated as architecture proof.
- SAFe is used to preserve command-and-control while claiming agility.
- DORA metrics become individual performance targets.
- MTTR is optimized while incident prevention and customer impact are ignored.
- COBIT or ISO is used as documentation theater with no operating evidence.
- ITIL is used to slow low-risk change instead of improving service management.
- TOGAF is run as a heavyweight ceremony for a narrow product decision.
- SOC 2 is treated as a security program instead of assurance over scoped controls.
- PCI/HIPAA/GDPR/PDP applicability is asserted without current legal verification.
