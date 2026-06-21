#!/usr/bin/env python3
"""Heuristic audit for data architecture design documents."""

from __future__ import annotations

import argparse
from pathlib import Path


CHECKS = {
    "workload": ["workload", "oltp", "olap", "htap", "read", "write", "query", "access pattern"],
    "necessity": ["need a database", "no db", "sqlite", "embedded", "file", "object storage"],
    "data_model": ["schema", "model", "entity", "document", "graph", "vector", "time-series", "key"],
    "sql_standard": ["iso", "9075", "standard", "dialect", "portable", "compatibility"],
    "consistency": ["consistency", "transaction", "isolation", "staleness", "idempotent", "conflict"],
    "cdc": ["cdc", "debezium", "binlog", "wal", "logical replication", "outbox", "change data"],
    "security": ["security", "tenant", "privilege", "role", "encryption", "tls", "audit", "mask"],
    "reliability": ["slo", "sli", "rpo", "rto", "backup", "restore", "failover", "availability"],
    "performance": ["index", "partition", "shard", "latency", "throughput", "explain", "p99"],
    "storage_internals": ["page", "slotted", "buffer pool", "tuple", "record id", "compression", "b+tree"],
    "query_execution": ["query plan", "optimizer", "join", "scan", "cardinality", "histogram", "pipeline"],
    "recovery_internals": ["wal", "checkpoint", "mvcc", "lock", "latch", "aries", "recovery"],
    "hardware": ["cpu", "gpu", "fpga", "nvme", "rdma", "cxl", "numa", "simd", "accelerat"],
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


def audit_text(text: str) -> tuple[list[str], list[str]]:
    text = text.lower()
    missing = [
        name for name, terms in CHECKS.items()
        if not any(term in text for term in terms)
    ]
    red_flags = [flag for flag in RED_FLAGS if flag in text]
    return missing, red_flags


def audit_file(path: Path) -> tuple[list[str], list[str]]:
    return audit_text(path.read_text(encoding="utf-8", errors="ignore"))


def audit_directory(path: Path) -> tuple[list[str], int]:
    files = iter_files(path)
    corpus = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in files)
    missing, _red_flags = audit_text(corpus)
    return missing, len(files)


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
