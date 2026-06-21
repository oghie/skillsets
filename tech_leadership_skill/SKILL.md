---
name: tech-leadership
description: Use when advising, planning, reviewing, reporting, operating, or improving CTO and technology leadership work across engineering strategy, cybersecurity management, people, organization, delivery, risk, KPI, roadmap, budgeting, governance, audit, R&D, stakeholder communication, culture, politics, and sector-specific technology leadership.
---

# Tech Leadership

## Core Rule
Treat technology leadership as an operating system, not a motivational role. Convert business context into explicit priorities, decision rights, capacity, risk appetite, financial trade-offs, technical strategy, cybersecurity posture, people systems, execution rhythm, and measurable outcomes.

## First Pass
1. Classify the request: daily operating review, strategy, roadmap, portfolio, cybersecurity strategy, audit/compliance, board/shareholder report, delivery recovery, incident management, organization design, hiring/retention, appraisal, budget, vendor/partner strategy, R&D, AI/data transformation, culture, political risk, or cross-functional advisory.
2. Identify role level: CTO, VP Engineering, Head of Engineering, tech lead, engineering manager, platform leader, product/data/AI leader, non-executive tech leader, acting CTO, advisor, or founder-CTO.
3. Capture context: sector, geography, company stage, regulation, risk appetite, operating model, budget authority, reporting line, decision rights, team size, vendor dependence, technology estate, and current constraints.
4. Separate `Fact`, `Inference`, `Assumption`, and `Question`. Do not invent headcount, budget, maturity, compliance obligations, breach history, board priorities, or culture dynamics.
5. Choose the smallest useful output: decision memo, roadmap, dashboard, board report, audit pack, risk register, org map, meeting brief, policy, operating cadence, performance calibration, incident review, or change plan.
6. Define validation: stakeholder review, metric baseline, risk acceptance, financial model, delivery evidence, audit evidence, tabletop exercise, incident drill, pulse survey, architecture review, or post-implementation review.

## Required Reads By Task
- Operating cadence, daily/weekly/monthly leadership work, decision rights, or CTO operating model: `references/leadership-operating-system.md`.
- Strategy, short/mid/long-term planning, roadmap, portfolio trade-offs, technology bets, technical debt, scalability, resilience, or over-engineering: `references/strategy-roadmap-portfolio.md`.
- KPI, KRA, OKR, scorecard, dashboard, performance reporting, root cause analysis, balanced scorecard, or metric design: `references/metrics-kpi-dashboard.md`.
- Hiring, developing, retaining, mentoring, delegation, 1:1s, calibration, appraisal, 360 feedback, incentives, team allocation, or succession: `references/people-org-talent-appraisal.md`.
- Enterprise risk, audit readiness, compliance, policy, controls, reliability management, regulatory exposure, or governance: `references/governance-risk-compliance-audit.md`.
- Cybersecurity leadership, CISO/CTO boundary, cyber risk appetite, security roadmap, IAM, SOC, AppSec, cloud security, data security, third-party risk, incident/crisis leadership, or board cyber reporting: `references/cybersecurity-strategy-management.md`.
- Delivery predictability, unblocking, agile, incident/on-call, reliability, SLO, operational resilience, platform operations, or postmortem: `references/delivery-incident-reliability.md`.
- Budget, costing, ROI, value realization, business case, unit economics, vendor spend, cloud cost, or investment governance: `references/finance-roi-costing.md`.
- AI leadership, data/product leadership, R&D, technology research, innovation, experiments, hypotheses, evaluation, and adoption governance: `references/ai-data-rd-innovation.md`.
- Board, shareholder, executive, cross-functional, customer, vendor, and team communication; presentation, narrative, advisory, negotiation, and pushback: `references/stakeholder-board-communication.md`.
- Culture, incentives, Conway's Law, organizational politics, power mapping, psychological safety, cross-cultural leadership, and office politics defense: `references/culture-politics-cross-cultural.md`.
- Sector-specific leadership forces across banking, energy, government, insurance, consulting, FMCG, healthcare, manufacturing, logistics, agriculture, defense, real estate, media, education, non-profit, vendor, and multinational contexts: `references/sector-contexts-and-operating-models.md`.
- Red flags, anti-patterns, failure modes, weak assumptions, and leadership smell checks: `references/leadership-antipatterns-red-flags.md`.

## Task Playbooks
- 30/60/90-day CTO or tech leadership diagnostic: `tasks/cto-90-day-diagnostic.md`.
- Build a technology strategy and roadmap: `tasks/build-technology-roadmap.md`.
- Build a cybersecurity strategy and management plan: `tasks/build-cybersecurity-strategy.md`.
- Prepare board, shareholder, or executive report: `tasks/prepare-board-shareholder-report.md`.
- Run engineering organization review: `tasks/run-engineering-org-review.md`.
- Handle audit, risk, and compliance readiness: `tasks/handle-audit-risk-compliance.md`.
- Conduct performance appraisal and 360 calibration: `tasks/conduct-performance-calibration.md`.
- Recover delivery predictability and unblock execution: `tasks/recover-delivery-predictability.md`.
- Evaluate AI, data, R&D, or innovation initiative: `tasks/evaluate-ai-rd-initiative.md`.
- Navigate office politics and stakeholder conflict ethically: `tasks/navigate-office-politics.md`.

## Templates
- Board or shareholder report: `templates/board-report.md`.
- Technology roadmap: `templates/technology-roadmap.md`.
- Cybersecurity strategy brief: `templates/cybersecurity-strategy-brief.md`.
- KPI dashboard: `templates/kpi-dashboard.md`.
- Organization and capacity map: `templates/org-capacity-map.md`.
- Risk register: `templates/risk-register.md`.
- Cyber risk register: `templates/cyber-risk-register.md`.
- Technical debt register: `templates/technical-debt-register.md`.
- Decision memo: `templates/decision-memo.md`.
- Meeting brief: `templates/meeting-brief.md`.
- Appraisal and 360 calibration: `templates/appraisal-360.md`.
- Change or policy template: `templates/change-policy.md`.
- Leadership operating system diagram: `templates/mermaid-leadership-operating-system.mmd`.
- Risk and reliability diagram: `templates/mermaid-risk-reliability-view.mmd`.
- Cyber governance diagram: `templates/mermaid-cyber-governance-view.mmd`.

## Decision Discipline
- If current laws, sector regulations, cybersecurity frameworks, privacy rules, audit standards, vendor claims, pricing, market data, or product capabilities matter, say exactly: `This needs verification.`
- When working inside this repository and reference accuracy matters, recalibrate against `../REFERENCE/LEADER/*.pdf|epub`. Do not cite book names or page numbers unless the user asks for citation.
- Lead with the strongest concern when a proposed strategy is under-evidenced, politically naive, unaffordable, un-auditable, or operationally fragile.
- Do not turn every leadership problem into process. Check incentives, decision rights, capacity, trust, technical constraints, and business trade-offs first.
- Do not treat cybersecurity as a tool purchase or compliance checklist. Tie it to business risk, asset criticality, threat exposure, control ownership, incident readiness, evidence, and funding.
- Do not hide trade-offs: speed vs control, autonomy vs standardization, innovation vs operational resilience, centralization vs local ownership, cost reduction vs future optionality.
- Do not use generic cultural stereotypes. For Indonesia, Asia, Middle East, Western, Eurasian, or multinational settings, map decision norms, regulatory pressure, power distance, labor expectations, procurement, language, stakeholder hierarchy, and escalation paths from evidence.

## Output Standard
Lead with the leadership judgment and the recommended path. State business objective, role accountability, constraints, stakeholders, current evidence, risks, trade-offs, operating model, roadmap, metrics, cybersecurity implications, financial impact, people impact, communication plan, validation, and next decision needed.

## Script Helpers
- Run `scripts/generate_leadership_artifact.py --type <artifact> --output <file>` to create a starter report, roadmap, risk register, cyber strategy, appraisal, or meeting brief.
- Run `scripts/tech_leadership_static_audit.py <file-or-dir>` to scan leadership docs for missing strategy, metrics, risk, cybersecurity, people, finance, delivery, governance, stakeholder, and validation coverage.
