#!/usr/bin/env python3
"""Audit lightweight architecture-as-code dependency constraints."""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".mjs",
    ".cjs",
    ".java",
    ".kt",
    ".kts",
    ".go",
    ".rs",
    ".cs",
    ".php",
    ".rb",
    ".swift",
    ".c",
    ".cc",
    ".cpp",
    ".h",
    ".hpp",
}

IMPORT_LINE = re.compile(
    r"^\s*(import\b|from\b|require\s*\(|using\b|package\b|#include\b|use\b|mod\b|pub\s+mod\b)",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Component:
    name: str
    paths: tuple[str, ...]
    may_depend_on: tuple[str, ...]
    forbidden_imports: tuple[str, ...]
    markers: tuple[str, ...]


def load_config(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text)

    if path.suffix.lower() in {".yml", ".yaml"}:
        try:
            import yaml  # type: ignore[import-not-found]
        except ModuleNotFoundError as exc:
            raise SystemExit(
                "YAML config requires PyYAML. Use JSON config or install PyYAML."
            ) from exc
        data = yaml.safe_load(text)
        if not isinstance(data, dict):
            raise SystemExit("YAML config must contain a mapping at the top level.")
        return data

    raise SystemExit("Unsupported config extension. Use .json, .yml, or .yaml.")


def normalize_pattern(pattern: str) -> str:
    return pattern.replace("\\", "/").lstrip("./")


def marker_from_pattern(pattern: str) -> str:
    pattern = normalize_pattern(pattern)
    marker = re.split(r"[*?\[]", pattern, maxsplit=1)[0].rstrip("/")
    if marker.endswith("/"):
        marker = marker[:-1]
    return marker


def module_markers(patterns: tuple[str, ...], fallback: str) -> tuple[str, ...]:
    markers: set[str] = {fallback}
    for pattern in patterns:
        marker = marker_from_pattern(pattern)
        if marker:
            markers.add(marker)
            markers.add(marker.replace("/", "."))
            markers.add(marker.split("/")[-1])
    return tuple(sorted(markers, key=len, reverse=True))


def parse_components(config: dict[str, Any]) -> dict[str, Component]:
    raw = config.get("components")
    if not isinstance(raw, dict) or not raw:
        raise SystemExit("Config must define non-empty 'components' mapping.")

    components: dict[str, Component] = {}
    for name, data in raw.items():
        if not isinstance(name, str) or not isinstance(data, dict):
            raise SystemExit("Each component must be a mapping keyed by component name.")
        paths = tuple(normalize_pattern(str(item)) for item in data.get("paths", ()))
        if not paths:
            raise SystemExit(f"Component '{name}' must define at least one path pattern.")
        may_depend_on = tuple(str(item) for item in data.get("may_depend_on", ()))
        forbidden_imports = tuple(str(item) for item in data.get("forbidden_imports", ()))
        components[name] = Component(
            name=name,
            paths=paths,
            may_depend_on=may_depend_on,
            forbidden_imports=forbidden_imports,
            markers=module_markers(paths, name),
        )

    known = set(components)
    for component in components.values():
        for target in component.may_depend_on:
            if target not in known:
                raise SystemExit(f"Component '{component.name}' may_depend_on unknown component '{target}'.")

    return components


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def owning_component(rel_path: str, components: dict[str, Component]) -> Component | None:
    matches = [
        component
        for component in components.values()
        if any(fnmatch.fnmatch(rel_path, pattern) for pattern in component.paths)
    ]
    if not matches:
        return None
    return max(matches, key=lambda component: max(len(marker_from_pattern(pattern)) for pattern in component.paths))


def iter_source_files(root: Path, extensions: set[str]) -> list[Path]:
    ignored_dirs = {".git", "node_modules", "vendor", "dist", "build", ".venv", "target", "__pycache__"}
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in extensions:
            continue
        if any(part in ignored_dirs for part in path.parts):
            continue
        files.append(path)
    return sorted(files)


def line_mentions_marker(line: str, marker: str) -> bool:
    normalized = line.replace("\\", "/")
    candidates = {
        marker,
        marker.replace("/", "."),
        marker.replace("/", "_"),
        f"@/{marker}",
        f"~/{marker}",
    }
    return any(candidate and candidate in normalized for candidate in candidates)


def audit_file(
    path: Path,
    root: Path,
    owner: Component,
    components: dict[str, Component],
    shared_forbidden: tuple[str, ...],
) -> list[str]:
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as exc:
        return [f"{path}: error: unreadable: {exc}"]

    findings: list[str] = []
    rel_path = rel(path, root)
    allowed = set(owner.may_depend_on) | {owner.name}
    forbidden = shared_forbidden + owner.forbidden_imports

    for number, line in enumerate(lines, 1):
        import_like = bool(IMPORT_LINE.search(line))
        for token in forbidden:
            if token and token in line:
                findings.append(
                    f"{rel_path}:{number}: forbidden-import: component '{owner.name}' uses forbidden token '{token}'."
                )
        if not import_like:
            continue
        for target in components.values():
            if target.name in allowed:
                continue
            if any(line_mentions_marker(line, marker) for marker in target.markers):
                findings.append(
                    f"{rel_path}:{number}: dependency-violation: component '{owner.name}' imports '{target.name}' but may_depend_on={list(owner.may_depend_on)}."
                )

    return findings


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True, help="Repository/source root to audit")
    parser.add_argument("--config", type=Path, required=True, help="JSON/YAML architecture constraint config")
    parser.add_argument("--max-findings", type=int, default=200)
    args = parser.parse_args(argv)

    root = args.root.resolve()
    if not root.exists() or not root.is_dir():
        print(f"Root does not exist or is not a directory: {root}", file=sys.stderr)
        return 2

    config = load_config(args.config)
    components = parse_components(config)
    shared_forbidden = tuple(str(item) for item in config.get("shared_forbidden_imports", ()))
    extensions = {
        str(item) if str(item).startswith(".") else f".{item}"
        for item in config.get("file_extensions", DEFAULT_EXTENSIONS)
    }

    findings: list[str] = []
    owned = 0
    for source in iter_source_files(root, extensions):
        rel_path = rel(source, root)
        owner = owning_component(rel_path, components)
        if owner is None:
            continue
        owned += 1
        findings.extend(audit_file(source, root, owner, components, shared_forbidden))

    if findings:
        for finding in findings[: args.max_findings]:
            print(finding)
        remaining = len(findings) - args.max_findings
        if remaining > 0:
            print(f"... {remaining} more finding(s) omitted")
        return 1

    print(f"OK: audited {owned} owned source file(s); no architecture constraint violations found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
