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
        "development_or_operation",
        (
            r"\bdevelopment view\b",
            r"\boperation view\b",
            r"\brepositor(y|ies)\b",
            r"\bpackage(s)?\b",
            r"\bmodule boundary\b",
            r"\brunbook\b",
            r"\bbackup\b",
            r"\brestore\b",
        ),
        "Document should address development view, operation view, repository/package boundaries, or production operations when architecture decisions affect implementation or runtime support.",
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
        (r"\bindependent deploy", r"\bteam autonomy\b", r"\bbounded context(s)?\b", r"\bbusiness capabilit(y|ies)\b", r"\bsubdomain(s)?\b", r"\bdata ownership\b"),
        "Microservices mentioned without common justifying forces such as independent deployment, team autonomy, business capabilities/subdomains, bounded contexts, or data ownership.",
    ),
    (
        "microservices_without_production_readiness",
        r"\bmicroservice(s)?\b",
        (r"\bhealth(check)?\b", r"\breadiness\b", r"\bdistributed tracing\b", r"\bmetrics\b", r"\blog aggregation\b", r"\bcontract test(s)?\b", r"\brunbook\b"),
        "Microservices mentioned without production-readiness signals such as health/readiness, tracing, metrics, logs, contract tests, or runbooks.",
    ),
    (
        "saga_without_compensation",
        r"\bsaga(s)?\b",
        (r"\bcompensat(e|ing|ion)\b", r"\bretriable\b", r"\bidempotenc(y|e)\b", r"\btimeout\b", r"\breconciliation\b"),
        "Saga mentioned without compensation, retriable steps, idempotency, timeout, or reconciliation.",
    ),
    (
        "outbox_without_idempotency",
        r"\boutbox\b|\btransactional messaging\b",
        (r"\bidempotenc(y|e)\b", r"\bdedup(lication)?\b", r"\brelay\b", r"\bat[- ]least[- ]once\b", r"\bmessage id\b"),
        "Outbox/transactional messaging mentioned without relay, at-least-once delivery, deduplication, idempotency, or message IDs.",
    ),
    (
        "cqrs_without_projection_controls",
        r"\bcqrs\b|\bmaterialized view(s)?\b|\bquery service\b",
        (r"\bprojection\b", r"\brebuild\b", r"\bstale\b", r"\bfreshness\b", r"\blag\b", r"\beventual consistency\b"),
        "CQRS/materialized views mentioned without projection, rebuild, lag/freshness, stale-read, or eventual-consistency controls.",
    ),
    (
        "api_gateway_without_ownership",
        r"\bapi gateway\b|\bbff\b|\bbackends? for frontends?\b",
        (r"\bowner(ship)?\b", r"\bbackward compatib", r"\bversion(ing)?\b", r"\bauth", r"\brate limit", r"\bcomposition\b"),
        "API gateway/BFF mentioned without ownership, backward compatibility/versioning, auth, rate limit, or composition responsibility.",
    ),
    (
        "strangler_without_acl_or_coexistence",
        r"\bstrangler\b|\banti[- ]corruption layer\b|\bacl\b",
        (r"\bcoexist(ence|ing)?\b", r"\bintegration glue\b", r"\badapter(s)?\b", r"\bdomain translation\b", r"\bcutover\b", r"\brollback\b"),
        "Strangler/ACL migration mentioned without coexistence, integration glue/adapters, domain translation, cutover, or rollback.",
    ),
    (
        "service_mesh_without_operating_model",
        r"\bservice mesh\b|\bsidecar\b",
        (r"\btraffic\b", r"\bmtls\b", r"\btelemetry\b", r"\bpolicy\b", r"\bowner(ship)?\b", r"\brollout\b"),
        "Service mesh/sidecar mentioned without traffic policy, mTLS/security, telemetry, ownership, or rollout model.",
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
        (
            r"\btrust boundar(y|ies)\b",
            r"\bleast privilege\b",
            r"\baudit\b",
            r"\bthreat model\b",
            r"\brole(s)?\b",
            r"\breference monitor\b",
            r"\bpolicy enforcement\b",
            r"\bpolicy decision\b",
        ),
        "Security mentioned without trust boundaries, least privilege, audit, threat model, roles, or explicit policy enforcement/decision model.",
    ),
    (
        "availability_without_failure_model",
        r"\bavailability\b|\bhighly available\b|\bha\b|\bfailover\b",
        (r"\bfailure\b", r"\bdependency\b", r"\brecovery\b", r"\brto\b", r"\brpo\b", r"\bbackup\b"),
        "Availability mentioned without dependency failure, recovery, RTO/RPO, backup, or failover analysis.",
    ),
)

ARCHITECTURE_AS_CODE_RISKS = (
    (
        "layered_without_fitness_function",
        r"\blayered\b|\blayer(s)?\b",
        (r"\bfitness function(s)?\b", r"\bdependency rule\b", r"\barchitecture[- ]as[- ]code\b", r"\bimport rule\b", r"\bconstraint\b"),
        "Layered architecture mentioned without dependency constraints, fitness functions, or architecture-as-code checks.",
    ),
    (
        "architecture_as_code_without_mapping",
        r"\barchitecture[- ]as[- ]code\b|\bfitness function\b|\bADL\b",
        (r"\bdirectory\b", r"\bpackage\b", r"\bnamespace\b", r"\bpath\b", r"\bconstraint\b", r"\bcomponent\b"),
        "Architecture-as-code mentioned without mapping logical components to physical directories/packages/namespaces and constraints.",
    ),
)

COST_ESTIMATION_RISKS = (
    (
        "cost_without_estimation_model",
        r"\bcost\b|\beffort\b|\bschedule\b|\btco\b|\boperational cost\b",
        (r"\bestimat(e|ion)\b", r"\bPERT\b", r"\bWBS\b", r"\bfunction point(s)?\b", r"\brisk reserve\b", r"\bresource usage\b"),
        "Cost/effort/schedule mentioned without estimation method, WBS, PERT, function points, risk reserve, or resource-usage model.",
    ),
    (
        "performance_without_workload_model",
        r"\bperformance\b|\blatency\b|\bthroughput\b|\bcapacity\b",
        (r"\bworkload\b", r"\bresource usage\b", r"\bqueueing\b", r"\bbenchmark\b", r"\bload test\b", r"\bp95\b", r"\bp99\b"),
        "Performance mentioned without workload, resource-usage, queueing, benchmark, load-test, or percentile target.",
    ),
)

PRINCIPLE_RISKS = (
    (
        "modularity_without_principles",
        r"\bmodule(s)?\b|\bcomponent(s)?\b|\bpackage(s)?\b|\bservice(s)?\b",
        (r"\bcohesion\b", r"\bcoupling\b", r"\bKISS\b", r"\bYAGNI\b", r"\bDRY\b", r"\bSOLID\b", r"\bseparation of concerns\b"),
        "Modularity mentioned without coupling/cohesion or design-principle reasoning.",
    ),
)


CLEAN_CODE_RISKS = (
    (
        "refactor_without_behavior_baseline",
        r"\brefactor(ing)?\b|\bclean code\b|\bcode smell(s)?\b|\btechnical debt\b|\bcleanup\b",
        (
            r"\bbehavior\b",
            r"\bcharacterization test(s)?\b",
            r"\bunit test(s)?\b",
            r"\bcontract test(s)?\b",
            r"\btest(s|ing)?\b",
            r"\bverification\b",
            r"\bvalidation\b",
        ),
        "Refactor/clean-code work mentioned without behavior baseline, tests, or verification.",
    ),
    (
        "clean_code_without_architecture_force",
        r"\bclean code\b|\bcode smell(s)?\b|\brefactor(ing)?\b|\bcleanup\b",
        (
            r"\bcorrectness\b",
            r"\bmodifiability\b",
            r"\bmaintainability\b",
            r"\bsecurity\b",
            r"\bperformance\b",
            r"\bconcurrency\b",
            r"\boperation(s|al)?\b",
            r"\bcost\b",
            r"\brisk\b",
            r"\bchange cost\b",
        ),
        "Clean-code/refactoring discussion should name the force it protects, not only style preference.",
    ),
    (
        "boundary_cleanup_without_tests",
        r"\bthird[- ]party\b|\bsdk\b|\bframework\b|\bORM\b|\badapter(s)?\b|\bboundar(y|ies)\b",
        (
            r"\blearning test(s)?\b",
            r"\bcontract test(s)?\b",
            r"\bcharacterization test(s)?\b",
            r"\bunit test(s)?\b",
            r"\bintegration test(s)?\b",
            r"\bverification\b",
        ),
        "Boundary/adapter cleanup mentioned without tests or verification around the boundary.",
    ),
    (
        "concurrency_refactor_without_stress_tests",
        r"\bconcurrency\b|\bthread(s|ed)?\b|\bsynchronized\b|\block(s|ing)?\b|\bshared mutable\b",
        (
            r"\bstress test(s)?\b",
            r"\bfailure injection\b",
            r"\binterleav(ing|e)\b",
            r"\bscheduler\b",
            r"\btunable\b",
            r"\bdifferent platform(s)?\b",
            r"\bverification\b",
        ),
        "Concurrency-related cleanup mentioned without stress, interleaving, scheduler, platform, or failure-path verification.",
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

    for name, trigger, guards, message in ARCHITECTURE_AS_CODE_RISKS:
        if re.search(trigger, text, re.IGNORECASE) and not has_any(text, guards):
            findings.append(f"{path}: warn: {name}: {message}")

    for name, trigger, guards, message in COST_ESTIMATION_RISKS:
        if re.search(trigger, text, re.IGNORECASE) and not has_any(text, guards):
            findings.append(f"{path}: warn: {name}: {message}")

    for name, trigger, guards, message in PRINCIPLE_RISKS:
        if re.search(trigger, text, re.IGNORECASE) and not has_any(text, guards):
            findings.append(f"{path}: warn: {name}: {message}")

    for name, trigger, guards, message in CLEAN_CODE_RISKS:
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
