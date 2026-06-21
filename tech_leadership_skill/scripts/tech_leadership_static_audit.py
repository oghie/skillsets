#!/usr/bin/env python3
"""Heuristic audit for technology leadership documents."""

from __future__ import annotations

import argparse
from pathlib import Path


CHECKS = {
    "strategy": ["strategy", "roadmap", "portfolio", "objective", "priority", "horizon"],
    "business_value": ["business", "customer", "revenue", "cost", "mission", "roi", "value"],
    "metrics": ["kpi", "kra", "okr", "metric", "dashboard", "scorecard", "target"],
    "performance_management": ["csf", "critical success factor", "balanced scorecard", "benchmarking", "root cause", "fmea"],
    "cybersecurity": ["cyber", "security", "iam", "soc", "appsec", "vulnerability", "incident", "control"],
    "risk": ["risk", "audit", "compliance", "resilience", "reliability", "governance", "control"],
    "reliability_leadership": ["barrier", "redundancy", "recovery", "near miss", "just culture", "human reliability"],
    "people": ["people", "talent", "hiring", "retention", "manager", "appraisal", "360", "succession"],
    "senior_leadership": ["cto", "vp engineering", "true north", "role model", "executive", "senior leadership"],
    "delivery": ["delivery", "agile", "roadmap", "dependency", "blocker", "incident", "on-call", "slo"],
    "finance": ["budget", "cost", "forecast", "roi", "vendor", "cloud", "funding"],
    "stakeholder": ["stakeholder", "board", "shareholder", "executive", "communication", "decision"],
    "culture": ["culture", "incentive", "conway", "politics", "trust", "psychological safety", "career ladder"],
    "engineering_process": ["code review", "architecture review", "postmortem", "learning review", "sustaining engineering"],
    "ai_data_research": ["ai", "agent", "data product", "hypothesis", "observability", "autonomy", "data value"],
    "validation": ["verify", "evidence", "validation", "review", "owner", "due date", "cadence"],
}

RED_FLAGS = [
    "all top priority",
    "no owner",
    "no rollback",
    "security later",
    "compliance only",
    "tool-first",
    "no evidence",
    "manual forever",
    "no budget",
    "no decision",
]


def iter_files(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    return sorted(
        p for p in path.rglob("*")
        if p.is_file() and p.suffix.lower() in {".md", ".markdown", ".txt"}
    )


def audit_text(text: str) -> tuple[list[str], list[str]]:
    lower = text.lower()
    missing = [
        name for name, terms in CHECKS.items()
        if not any(term in lower for term in terms)
    ]
    red_flags = [flag for flag in RED_FLAGS if flag in lower]
    return missing, red_flags


def audit_file(path: Path) -> tuple[list[str], list[str]]:
    return audit_text(path.read_text(encoding="utf-8", errors="ignore"))


def audit_directory(path: Path) -> tuple[list[str], int]:
    files = iter_files(path)
    corpus = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in files)
    missing, _ = audit_text(corpus)
    return missing, len(files)


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit leadership docs for missing coverage.")
    parser.add_argument("paths", nargs="+", help="Files or directories to audit")
    args = parser.parse_args()

    exit_code = 0
    for raw in args.paths:
        target = Path(raw)
        if not target.exists():
            print(f"[missing] {target}")
            exit_code = 2
            continue
        if target.is_dir():
            missing, file_count = audit_directory(target)
            if missing:
                exit_code = max(exit_code, 1)
                print(f"[review] {target}")
                print(f"  files: {file_count}")
                print(f"  missing: {', '.join(missing)}")
            else:
                print(f"[ok] {target} corpus ({file_count} files)")
            continue
        for path in iter_files(target):
            missing, red_flags = audit_file(path)
            if missing or red_flags:
                exit_code = max(exit_code, 1)
                print(f"[review] {path}")
                if missing:
                    print(f"  missing: {', '.join(missing)}")
                if red_flags:
                    print(f"  red_flags: {', '.join(red_flags)}")
            else:
                print(f"[ok] {path}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
