#!/usr/bin/env python3
"""Heuristic architecture-document audit for Markdown/text design artifacts."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


TEXT_EXTENSIONS = {".md", ".mdx", ".txt", ".rst", ".adoc"}


@dataclass(frozen=True)
class Check:
    name: str
    patterns: tuple[str, ...]
    message: str
    severity: str = "warn"


REQUIRED_COVERAGE = (
    Check(
        "scope",
        (r"\bscope\b", r"\bgoal(s)?\b", r"\bnon[- ]?goal(s)?\b", r"\bproblem\b"),
        "Document should state scope, goals/non-goals, or problem framing.",
    ),
    Check(
        "requirements",
        (r"\brequirement(s)?\b", r"\buse case(s)?\b", r"\bacceptance criteria\b", r"\bstakeholder(s)?\b"),
        "Document should connect architecture to requirements, use cases, or stakeholders.",
    ),
    Check(
        "nfr",
        (
            r"\bnon[- ]?functional\b",
            r"\bnfr(s)?\b",
            r"\bquality attribute(s)?\b",
            r"\bperformance\b",
            r"\bavailability\b",
            r"\bsecurity\b",
            r"\bprivacy\b",
        ),
        "Document should include measurable NFR or quality-attribute concerns.",
    ),
    Check(
        "context",
        (r"\bcontext\b", r"\bboundar(y|ies)\b", r"\bexternal\b", r"\bintegration(s)?\b", r"\bactor(s)?\b"),
        "Document should identify system context, boundaries, external actors, or integrations.",
    ),
    Check(
        "components",
        (r"\bcomponent(s)?\b", r"\bmodule(s)?\b", r"\bservice(s)?\b", r"\bpackage(s)?\b", r"\binterface(s)?\b"),
        "Document should describe functional components, modules, services, or interfaces.",
    ),
    Check(
        "data",
        (r"\bdata\b", r"\bschema(s)?\b", r"\bdatabase\b", r"\bstore\b", r"\bpersistence\b", r"\bownership\b"),
        "Document should address data, persistence, schemas, or ownership.",
    ),
    Check(
        "behavior",
        (r"\bflow(s)?\b", r"\bsequence\b", r"\bevent(s)?\b", r"\bworkflow(s)?\b", r"\bstate\b", r"\bretry\b"),
        "Document should address behavior flows, events, workflows, state, or failure handling.",
    ),
    Check(
        "deployment",
        (r"\bdeploy(ment|able)?\b", r"\bruntime\b", r"\bnode(s)?\b", r"\bcontainer(s)?\b", r"\bnetwork\b", r"\binfrastructure\b"),
        "Document should address deployment, runtime, network, or infrastructure.",
    ),
    Check(
        "decision",
        (r"\bdecision\b", r"\brationale\b", r"\balternative(s)?\b", r"\btrade[- ]?off(s)?\b"),
        "Document should record decisions, rationale, alternatives, or trade-offs.",
    ),
    Check(
        "verification",
        (r"\bverification\b", r"\bvalidation\b", r"\btest(s|ing)?\b", r"\bbenchmark\b", r"\bmonitor(ing)?\b", r"\brollout\b"),
        "Document should define validation, tests, rollout, monitoring, or other verification evidence.",
    ),
)


STYLE_RISKS = (
    (
        "microservices_without_forces",
        r"\bmicroservice(s)?\b",
        (r"\bindependent deploy", r"\bteam autonomy\b", r"\bbounded context(s)?\b", r"\bdata ownership\b"),
        "Microservices mentioned without common justifying forces such as independent deployment, team autonomy, bounded contexts, or data ownership.",
    ),
    (
        "event_driven_without_semantics",
        r"\bevent[- ]?driven\b|\bpub[- ]?sub\b|\bmessage broker\b|\bqueue(s)?\b",
        (r"\bidempotenc(y|e)\b", r"\border(ing)?\b", r"\bschema\b", r"\breplay\b", r"\bdead[- ]?letter\b"),
        "Event-driven design mentioned without idempotency, ordering, schema evolution, replay, or dead-letter policy.",
    ),
    (
        "cache_without_consistency",
        r"\bcache|caching\b",
        (r"\binvalidat(e|ion)\b", r"\bttl\b", r"\bstale\b", r"\bconsistency\b", r"\brefresh\b"),
        "Caching mentioned without invalidation, TTL, stale-read, refresh, or consistency rules.",
    ),
    (
        "shared_database_without_ownership",
        r"\bshared database\b|\bshared schema\b|\bshared table(s)?\b",
        (r"\bowner(ship)?\b", r"\bwrite authority\b", r"\bgovernance\b", r"\bcompatib(ility|le)\b"),
        "Shared database/schema/table mentioned without ownership, write authority, governance, or compatibility rules.",
    ),
    (
        "security_without_boundary",
        r"\bsecure\b|\bsecurity\b|\bauthentication\b|\bauthorization\b",
        (r"\btrust boundar(y|ies)\b", r"\bleast privilege\b", r"\baudit\b", r"\bthreat model\b", r"\brole(s)?\b"),
        "Security mentioned without trust boundaries, least privilege, audit, threat model, or roles.",
    ),
    (
        "availability_without_failure_model",
        r"\bavailability\b|\bhighly available\b|\bha\b|\bfailover\b",
        (r"\bfailure\b", r"\bdependency\b", r"\brecovery\b", r"\brto\b", r"\brpo\b", r"\bbackup\b"),
        "Availability mentioned without dependency failure, recovery, RTO/RPO, backup, or failover analysis.",
    ),
)


AUTH_RISKS = (
    (
        "auth_without_session_model",
        r"\b(auth|authentication|login|logout|session|refresh token|access token)\b",
        (r"\bsession\b", r"\btoken\b", r"\bttl\b", r"\bexpir(y|ation|e)\b", r"\brevok(e|ation)\b", r"\blogout\b"),
        "Auth mentioned without session/token TTL, expiration, revocation, or logout model.",
    ),
    (
        "jwt_without_key_controls",
        r"\bjwt\b|\bjson web token\b",
        (r"\bissuer\b", r"\baudience\b", r"\bexpiry\b", r"\bexp\b", r"\bkey id\b", r"\bkid\b", r"\bjwks\b", r"\brotation\b"),
        "JWT mentioned without issuer/audience/expiry/key-id/JWKS/rotation controls.",
    ),
    (
        "refresh_token_without_rotation",
        r"\brefresh token(s)?\b",
        (r"\brotat(e|ion)\b", r"\breuse detection\b", r"\btoken family\b", r"\brevok(e|ation)\b"),
        "Refresh tokens mentioned without rotation, reuse detection, token-family, or revocation rules.",
    ),
    (
        "password_without_storage_controls",
        r"\bpassword(s)?\b",
        (r"\bargon2\b", r"\bbcrypt\b", r"\bscrypt\b", r"\bhash(ed|ing)?\b", r"\bsalt\b", r"\bpepper\b", r"\brate[- ]?limit\b"),
        "Passwords mentioned without hashing/KDF, salt/pepper, or rate-limit controls.",
    ),
    (
        "mfa_without_recovery",
        r"\bmfa\b|\bmulti[- ]?factor\b|\btotp\b|\bwebauthn\b|\bpasskey(s)?\b",
        (r"\brecover(y)?\b", r"\bbackup code(s)?\b", r"\bstep[- ]?up\b", r"\bdevice loss\b", r"\bdisable\b"),
        "MFA mentioned without recovery, backup codes, step-up, device-loss, or disable rules.",
    ),
    (
        "admin_users_without_audit",
        r"\badmin user(s)?\b|\brole change\b|\buser status\b|\bprivilege\b",
        (r"\baudit\b", r"\bseparation of duties\b", r"\bself[- ]?escalation\b", r"\btenant\b"),
        "Admin/user privilege operations mentioned without audit, separation-of-duties, self-escalation, or tenant controls.",
    ),
)


VAGUE_QUALITY = re.compile(
    r"\b(fast|scalable|secure|reliable|resilient|robust|high performance|cloud native)\b",
    re.IGNORECASE,
)
MEASUREMENT = re.compile(
    r"\b(\d+(\.\d+)?\s*(ms|s|sec|seconds?|rps|qps|req/s|%|percent|gb|mb|tb|users?|minutes?|hours?)|slo|sla|p95|p99|rto|rpo)\b",
    re.IGNORECASE,
)


def iter_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_dir():
            files.extend(p for p in path.rglob("*") if p.is_file() and p.suffix.lower() in TEXT_EXTENSIONS)
        elif path.is_file():
            files.append(path)
    return sorted(set(files))


def has_any(text: str, patterns: tuple[str, ...]) -> bool:
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)


def audit_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    lower = text.lower()
    findings: list[str] = []

    for check in REQUIRED_COVERAGE:
        if not has_any(text, check.patterns):
            findings.append(f"{path}: {check.severity}: {check.name}: {check.message}")

    for name, trigger, guards, message in STYLE_RISKS:
        if re.search(trigger, text, re.IGNORECASE) and not has_any(text, guards):
            findings.append(f"{path}: warn: {name}: {message}")

    for name, trigger, guards, message in AUTH_RISKS:
        if re.search(trigger, text, re.IGNORECASE) and not has_any(text, guards):
            findings.append(f"{path}: warn: {name}: {message}")

    vague_hits = VAGUE_QUALITY.findall(text)
    if vague_hits and not MEASUREMENT.search(text):
        words = sorted({hit[0].lower() if isinstance(hit, tuple) else hit.lower() for hit in vague_hits})
        findings.append(
            f"{path}: warn: unmeasured_quality_claim: Vague quality claim(s) without measurable target: {', '.join(words)}."
        )

    looks_like_adr = (
        path.stem.lower().startswith("adr")
        or re.search(r"(?im)^#\s*(adr|architecture decision record)\b", text)
        or re.search(r"(?im)^title:\s*.*\badr\b", text)
    )
    if looks_like_adr and not re.search(r"(?im)^##?\s*status\b|\bstatus\s*:", text):
        findings.append(f"{path}: info: adr_status: ADR-like document should include decision status.")

    return findings


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path, help="Markdown/text files or directories to audit")
    parser.add_argument("--max-findings", type=int, default=200, help="Maximum findings to print")
    args = parser.parse_args(argv)

    files = iter_files(args.paths)
    if not files:
        print("No Markdown/text files found.", file=sys.stderr)
        return 2

    findings: list[str] = []
    for file_path in files:
        findings.extend(audit_file(file_path))

    if findings:
        for finding in findings[: args.max_findings]:
            print(finding)
        remaining = len(findings) - args.max_findings
        if remaining > 0:
            print(f"... {remaining} more finding(s) omitted")
        return 1

    print(f"OK: audited {len(files)} file(s); no heuristic architecture gaps found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
