#!/usr/bin/env python3
"""Heuristic audit for UI/UX and frontend design documents."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


TEXT_EXTS = {".md", ".mdx", ".txt", ".rst", ".adoc"}


@dataclass(frozen=True)
class Check:
    name: str
    patterns: tuple[str, ...]
    message: str


REQUIRED = (
    Check(
        "user_and_goal",
        (r"\buser(s)?\b", r"\bpersona(s)?\b", r"\baudience\b", r"\bjob[- ]?to[- ]?be[- ]?done\b", r"\bgoal(s)?\b"),
        "Name the user segment, goal, or job-to-be-done.",
    ),
    Check(
        "task_flow",
        (r"\bflow\b", r"\bjourney\b", r"\bscenario\b", r"\btask\b", r"\bpath\b", r"\bonboarding\b"),
        "Describe the task flow, journey, or scenario.",
    ),
    Check(
        "states",
        (r"\bempty state\b", r"\bloading\b", r"\berror\b", r"\bsuccess\b", r"\bdisabled\b", r"\bfocus\b", r"\bstate(s)?\b"),
        "Cover UI states such as loading, empty, error, focus, disabled, and success.",
    ),
    Check(
        "accessibility",
        (r"\baccessib", r"\ba11y\b", r"\bkeyboard\b", r"\bfocus\b", r"\bcontrast\b", r"\bscreen reader\b", r"\baria\b", r"\breduced motion\b"),
        "Include accessibility requirements and checks.",
    ),
    Check(
        "responsive",
        (r"\bresponsive\b", r"\bmobile\b", r"\bbreakpoint(s)?\b", r"\bviewport\b", r"\bconstraint(s)?\b", r"\bcontainer quer"),
        "Define responsive/mobile behavior and layout constraints.",
    ),
    Check(
        "validation",
        (r"\btest\b", r"\busability\b", r"\bvalidate\b", r"\bexperiment\b", r"\bmetric\b", r"\bQA\b", r"\bscreenshot\b"),
        "Define validation method, metric, or QA check.",
    ),
)


RISK_CHECKS = (
    (
        "visual_without_task",
        r"\bbeautiful\b|\bmodern\b|\bpolish(ed)?\b|\baesthetic\b|\bvisual\b",
        (r"\btask\b", r"\buser\b", r"\bgoal\b", r"\bflow\b", r"\bmetric\b"),
        "Visual language appears without user task, flow, goal, or metric.",
    ),
    (
        "figma_without_handoff",
        r"\bFigma\b|\bdesign file\b|\bprototype\b",
        (r"\bhandoff\b", r"\btoken(s)?\b", r"\bcomponent(s)?\b", r"\bstate(s)?\b", r"\bdeveloper\b", r"\bQA\b"),
        "Figma/prototype mentioned without handoff, tokens, components, states, developer, or QA detail.",
    ),
    (
        "component_without_states",
        r"\bbutton\b|\binput\b|\bcard\b|\bmodal\b|\btab(s)?\b|\btable\b|\bcomponent(s)?\b",
        (r"\bhover\b", r"\bfocus\b", r"\bactive\b", r"\bdisabled\b", r"\bloading\b", r"\berror\b", r"\bstate(s)?\b"),
        "Components mentioned without interaction state coverage.",
    ),
    (
        "theme_without_tokens",
        r"\btheme\b|\bstyle\b|\bdesign system\b|\bbrand\b",
        (
            r"\btoken(s)?\b",
            r"\bCSS variable(s)?\b",
            r"\bTailwind\b",
            r"\bRadix\b",
            r"\bshadcn\b",
            r"\bMUI\b",
            r"\bAnt Design\b",
            r"\bMantine\b",
            r"\bBulma\b",
            r"\bLinaria\b",
            r"\bPostCSS\b",
            r"\bvanilla CSS\b",
            r"\bcolor\b",
            r"\bradius\b",
            r"\bspacing\b",
        ),
        "Theme/style mentioned without token mapping.",
    ),
    (
        "framework_without_rationale",
        r"\bTailwind\b|\bRadix\b|\bshadcn\b|\bMUI\b|\bAnt Design\b|\bMantine\b|\bBulma\b|\bLinaria\b|\bPostCSS\b|\bvanilla CSS\b|\bcomponent librar(y|ies)\b|\bUI framework\b",
        (r"\btrade[- ]?off\b", r"\brationale\b", r"\bexisting stack\b", r"\baccessib", r"\btheme\b", r"\bbundle\b", r"\bSSR\b", r"\bmaintain", r"\bdensity\b"),
        "Frontend stack/library mentioned without rationale, existing-stack fit, accessibility, theming, bundle, SSR, density, or maintenance trade-off.",
    ),
    (
        "ai_without_ethics",
        r"\bAI\b|\bGenAI\b|\bgenerative\b|\bLLM\b|\bsynthetic\b",
        (r"\bethic", r"\bsourc", r"\blicen[cs]", r"\bprivacy\b", r"\btransparen", r"\bdisclos", r"\bIP\b"),
        "AI usage mentioned without sourcing, privacy, transparency, licensing, or ethics review.",
    ),
    (
        "xr_without_comfort",
        r"\bXR\b|\bVR\b|\bAR\b|\bMR\b|\bWebXR\b|\bspatial\b|\b3D\b",
        (r"\bcomfort\b", r"\blocomotion\b", r"\bfield of view\b", r"\bFOV\b", r"\binput\b", r"\bgaze\b", r"\bhand\b", r"\bsafety\b"),
        "XR/spatial work mentioned without comfort, input, locomotion, field-of-view, or safety detail.",
    ),
)


def has_any(text: str, patterns: tuple[str, ...]) -> bool:
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)


def iter_files(target: Path) -> list[Path]:
    if target.is_file():
        return [target] if target.suffix.lower() in TEXT_EXTS else []
    return sorted(path for path in target.rglob("*") if path.is_file() and path.suffix.lower() in TEXT_EXTS)


def audit_file(path: Path) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(encoding="latin-1")

    findings: list[str] = []
    for check in REQUIRED:
        if not has_any(text, check.patterns):
            findings.append(f"{path}: missing:{check.name}: {check.message}")

    for name, trigger, guards, message in RISK_CHECKS:
        if re.search(trigger, text, re.IGNORECASE) and not has_any(text, guards):
            findings.append(f"{path}: warn:{name}: {message}")

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit UI/UX and frontend design docs for missing operational detail.")
    parser.add_argument("target", type=Path, help="Markdown/text file or directory to audit")
    args = parser.parse_args()

    if not args.target.exists():
        print(f"error: target does not exist: {args.target}", file=sys.stderr)
        return 2

    files = iter_files(args.target)
    if not files:
        print(f"warning: no supported text files found under {args.target}")
        return 0

    findings: list[str] = []
    for file_path in files:
        findings.extend(audit_file(file_path))

    if findings:
        print("\n".join(findings))
        return 1

    print(f"OK: audited {len(files)} UI/UX document(s); no heuristic gaps found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
