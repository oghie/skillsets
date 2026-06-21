---
name: academic-research-journal
description: Use when evaluating, designing, drafting, revising, stress-testing, or preparing academic articles, empirical research reports, literature reviews, systematic reviews, meta-analyses, journal submissions, reviewer responses, research methods, sampling, measurement, analysis, publication readiness, or citation/source audits.
---

# Academic Research Journal

## Core Rule
Evaluate and build academic work as a chain of claims: problem -> literature gap -> question -> design -> data -> measurement -> analysis -> interpretation -> contribution. Do not reward polish when the research logic is weak, and do not dismiss useful work merely because realistic constraints create limitations.

## First Pass
1. Classify the task: evaluate, design, draft, revise, review, respond to reviewers, audit sources, or plan evidence synthesis.
2. Classify the article type: quantitative, qualitative, mixed methods, experimental, quasi-experimental, survey, field, case study, action research, policy/program evaluation, computational/big-data, literature review, systematic review, meta-analysis, theory, commentary, critique, or non-academic essay.
3. Extract the research skeleton: problem, purpose, question, theory, population/case, sample/data, measures, design, analysis, findings, limitations, contribution, and claim strength.
4. Identify the intended inference: exploratory insight, description, association, causality, mechanism, prediction, interpretation, policy/practice decision, or cumulative evidence.
5. Define the evidence needed and mark gaps as `I/I = insufficient information`; mark inapplicable criteria as `N/A`.

## Required Reads By Task
- Existing paper, essay, or article evaluation: `tasks/evaluate-existing-work.md`, `references/research-quality-principles.md`, and `references/journal-readiness-scorecard.md`.
- Article type or methods classification: `references/article-type-matrix.md`.
- Section-level critique: `references/section-evaluation-matrix.md`.
- Sampling, measures, experiments, qualitative, quantitative, mixed methods, survey, or program evaluation: `references/methods-evaluation-matrix.md`.
- Literature review, systematic review, or meta-analysis: `tasks/evidence-synthesis.md` and `references/evidence-synthesis-and-review.md`.
- Drafting a manuscript, essay, thesis chapter, or journal article: `tasks/manuscript-production.md`.
- Research design or empirical validation planning: `tasks/design-research-project.md`.
- Reviewer simulation, revision strategy, or response letter: `tasks/revision-and-peer-review.md`.
- Reference, citation, source, ethics, or integrity audit: `tasks/source-and-reference-audit.md` and `references/integrity-and-source-audit.md`.

## Evaluation Protocol
Use the 1-5 scale unless the user requests another format:
`5` strong; `4` mostly strong; `3` adequate but limited; `2` major weaknesses; `1` invalid or not journal-ready; `N/A`; `I/I`.

Always evaluate fit between the claim and the method:
- Generalization requires a defensible population, sampling frame, recruitment logic, response/nonresponse handling, and subgroup size.
- Causal language requires random assignment, credible quasi-experimental logic, temporal ordering, comparison conditions, and confound control.
- Measurement claims require conceptual definitions, operational alignment, reliability, validity, and bias mitigation.
- Qualitative claims require design fit, sampling rationale, recruitment detail, coding transparency, reflexivity, context, triangulation or other credibility checks, and analyzed evidence.
- Mixed methods claims require explicit design, clear strand roles, integration, value added, and handling of contradictory findings.
- Evidence-synthesis claims require transparent search, inclusion/exclusion criteria, study quality/bias assessment, heterogeneity handling, and interpretable synthesis.

## Evidence And Verification
- Never invent sources, quotations, statistics, DOI links, journal facts, methods, datasets, reviewer comments, or results.
- Current facts such as journal scope, instructions, rankings, indexing, impact factor, citation counts, reporting standards, and software versions need live verification.
- Treat statistical significance as limited evidence; check magnitude, practical importance, sampling assumptions, model choice, robustness, and replication.
- Treat missing methods detail as an evaluation finding, not permission to infer.
- Separate evidence, inference, speculation, and recommendation.

## Script Helper
- Run `scripts/manuscript_static_audit.py <file>` for a heuristic scan of section coverage, overclaiming, missing limitations/ethics cues, significance-language risks, and reference signals.

## Output Standard
Lead with the highest-impact judgment. Name assumptions, article type, intended inference, strongest contribution, fatal or major weaknesses, concrete fixes, and residual uncertainty. Use scorecards and claim-audit tables for evaluations; use manuscript architecture and section builders for drafting.
