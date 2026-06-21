#!/usr/bin/env python3
"""Heuristic audit for data architecture design documents."""

from __future__ import annotations

import argparse
from pathlib import Path


CHECKS = {
    "workload": ["workload", "oltp", "olap", "htap", "read", "write", "query", "access pattern"],
    "data_model": ["schema", "model", "entity", "document", "graph", "vector", "time-series", "key"],
    "consistency": ["consistency", "transaction", "isolation", "staleness", "idempotent", "conflict"],
    "security": ["security", "tenant", "privilege", "role", "encryption", "tls", "audit", "mask"],
    "reliability": ["slo", "sli", "rpo", "rto", "backup", "restore", "failover", "availability"],
    "performance": ["index", "partition", "shard", "latency", "throughput", "explain", "p99"],
    "observability": ["monitor", "metric", "log", "trace", "replication lag", "lock", "wait"],
    "migration": ["migration", "backfill", "cutover", "rollback", "decommission", "validation"],
}

RED_FLAGS = [
    "select *",
    "no rollback",
    "eventual consistency by default",
    "cache as source of truth",
    "active-active",
    "no backup",
    "manual only",
    "plaintext",
    "no index",
]


def iter_files(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    return sorted(
        p for p in path.rglob("*")
        if p.is_file() and p.suffix.lower() in {".md", ".markdown", ".txt", ".sql"}
    )


def audit_file(path: Path) -> tuple[list[str], list[str]]:
    text = path.read_text(encoding="utf-8", errors="ignore").lower()
    missing = [
        name for name, terms in CHECKS.items()
        if not any(term in text for term in terms)
    ]
    red_flags = [flag for flag in RED_FLAGS if flag in text]
    return missing, red_flags


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit data architecture docs for missing coverage.")
    parser.add_argument("paths", nargs="+", help="Files or directories to audit")
    args = parser.parse_args()

    exit_code = 0
    for raw in args.paths:
        target = Path(raw)
        if not target.exists():
            print(f"[missing] {target}")
            exit_code = 2
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
