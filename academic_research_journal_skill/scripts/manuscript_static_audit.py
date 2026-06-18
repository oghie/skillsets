#!/usr/bin/env python3
"""Heuristic static audit for academic manuscripts.

This is not a substitute for expert review. It surfaces text signals that
deserve closer academic evaluation.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


SECTION_PATTERNS = {
    "abstract": r"\babstract\b",
    "introduction": r"\bintroduction\b",
    "literature_review": r"\b(literature review|background)\b",
    "methods": r"\b(methods?|methodology|data and methods)\b",
    "sample_or_data": r"\b(sample|participants|data source|dataset|recruitment)\b",
    "measures": r"\b(measures?|measurement|variables?|constructs?|instrument)\b",
    "analysis": r"\b(analysis|analytical strategy|model|coding)\b",
    "results": r"\b(results?|findings)\b",
    "discussion": r"\bdiscussion\b",
    "limitations": r"\b(limitations?|strengths and limitations)\b",
    "ethics": r"\b(ethics|ethical approval|irb|institutional review board|consent)\b",
    "references": r"\b(references|bibliography|works cited)\b",
}

OVERCLAIM_PATTERNS = {
    "proof_language": r"\b(proves?|proved|proven|demonstrates conclusively|settles)\b",
    "universal_language": r"\b(always|never|all|none|everyone|no one|entirely|completely)\b",
    "causal_language": r"\b(causes?|caused|causal|impact|impacts|effect|effects|influence|leads to)\b",
    "vague_implications": r"\b(implications are discussed|future research is discussed)\b",
}

HUMAN_SUBJECT_CUES = r"\b(participants?|respondents?|interviews?|survey|patients?|students?|consent|recruitment)\b"
SIGNIFICANCE_CUES = r"\b(statistically significant|p\s*[<=>]|p-value|significance)\b"
EFFECT_SIZE_CUES = r"\b(effect size|cohen'?s d|odds ratio|or\b|risk ratio|rr\b|confidence interval|ci\b|beta|coefficient)\b"
REFERENCE_CUES = r"\bdoi\b|https?://|\b[A-Z][A-Za-z-]+,\s+[A-Z]\."


def count_matches(pattern: str, text: str) -> int:
    return len(re.findall(pattern, text, flags=re.IGNORECASE))


def audit(text: str) -> list[tuple[str, str, str]]:
    findings: list[tuple[str, str, str]] = []

    for section, pattern in SECTION_PATTERNS.items():
        if not re.search(pattern, text, flags=re.IGNORECASE):
            findings.append(("missing-section-cue", section, "No obvious heading or term found."))

    for name, pattern in OVERCLAIM_PATTERNS.items():
        count = count_matches(pattern, text)
        if count:
            findings.append(("claim-language", name, f"{count} possible overclaiming cue(s)."))

    if re.search(HUMAN_SUBJECT_CUES, text, flags=re.IGNORECASE) and not re.search(
        SECTION_PATTERNS["ethics"], text, flags=re.IGNORECASE
    ):
        findings.append(("ethics-risk", "human-subjects", "Human-participant cues appear without ethics/consent cue."))

    if re.search(SIGNIFICANCE_CUES, text, flags=re.IGNORECASE) and not re.search(
        EFFECT_SIZE_CUES, text, flags=re.IGNORECASE
    ):
        findings.append(("statistics-risk", "significance-without-magnitude", "Significance cues appear without effect-size/uncertainty cues."))

    percent_count = count_matches(r"\d+(\.\d+)?\s*%", text)
    n_count = count_matches(r"\b(n\s*=|N\s*=|sample size|participants?)\b", text)
    if percent_count >= 3 and n_count == 0:
        findings.append(("statistics-risk", "percent-without-counts", "Several percentages appear without obvious count/sample cues."))

    if not re.search(REFERENCE_CUES, text):
        findings.append(("source-risk", "reference-signals", "No obvious DOI, URL, or citation metadata cues found."))

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a heuristic static audit on an academic manuscript.")
    parser.add_argument("file", type=Path, help="Plain-text, Markdown, or lightly extracted manuscript file.")
    args = parser.parse_args()

    text = args.file.read_text(encoding="utf-8", errors="replace")
    words = re.findall(r"\b\w+\b", text)
    findings = audit(text)

    print(f"file: {args.file}")
    print(f"words: {len(words)}")
    print(f"findings: {len(findings)}")

    if not findings:
        print("No heuristic issues found. This does not prove journal readiness.")
        return 0

    for category, item, message in findings:
        print(f"- {category}: {item} - {message}")

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
