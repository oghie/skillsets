#!/usr/bin/env python3
"""Read the static theme catalog without requiring a YAML dependency."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def load_index(root: Path) -> list[dict[str, object]]:
    index_path = root / "index.yaml"
    if not index_path.exists():
        raise FileNotFoundError(index_path)

    styles: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    current_key: str | None = None

    for raw in index_path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped or stripped == "---":
            continue
        if stripped.startswith("- id:"):
            if current:
                styles.append(current)
            current = {"id": stripped.split(":", 1)[1].strip(), "keywords": []}
            current_key = "id"
            continue
        if current is None:
            continue
        if stripped.startswith("- ") and current_key == "keywords":
            current.setdefault("keywords", [])
            keywords = current["keywords"]
            if isinstance(keywords, list):
                keywords.append(stripped[2:].strip())
            continue
        if ":" in stripped:
            key, value = stripped.split(":", 1)
            key = key.strip()
            value = value.strip()
            current_key = key
            if key == "keywords":
                current["keywords"] = []
            elif key in {"id", "name", "category", "path", "primary_mode", "summary"}:
                current[key] = value
            continue
        if current_key in {"summary", "name"} and stripped:
            previous = str(current.get(current_key, ""))
            current[current_key] = f"{previous} {stripped}".strip()

    if current:
        styles.append(current)
    return styles


def matches(style: dict[str, object], category: str | None, keyword: str | None) -> bool:
    if category and str(style.get("category", "")).lower() != category.lower():
        return False
    if keyword:
        haystack = " ".join(
            [
                str(style.get("id", "")),
                str(style.get("name", "")),
                str(style.get("summary", "")),
                " ".join(str(item) for item in style.get("keywords", []) if item),
            ]
        ).lower()
        if keyword.lower() not in haystack:
            return False
    return True


def print_style(style: dict[str, object]) -> None:
    keywords = ", ".join(str(item) for item in style.get("keywords", []) if item)
    print(f"{style.get('id')} [{style.get('category')}] {style.get('name')}")
    print(f"  mode: {style.get('primary_mode')}")
    print(f"  path: {style.get('path')}")
    print(f"  summary: {style.get('summary')}")
    if keywords:
        print(f"  keywords: {keywords}")


def main() -> int:
    parser = argparse.ArgumentParser(description="List and filter uiux_frontend_skill/theme styles.")
    parser.add_argument("--root", type=Path, default=Path("uiux_frontend_skill/theme"), help="Path to the theme directory")
    parser.add_argument("--list", action="store_true", help="List style ids")
    parser.add_argument("--category", choices=("sharp", "rounded", "hybrid"), help="Filter by category")
    parser.add_argument("--keyword", help="Filter by keyword/name/summary substring")
    parser.add_argument("--show", help="Show one style id in detail")
    args = parser.parse_args()

    try:
        styles = load_index(args.root)
    except FileNotFoundError:
        print(f"error: theme index not found under {args.root}", file=sys.stderr)
        return 2

    selected = [style for style in styles if matches(style, args.category, args.keyword)]
    if args.show:
        selected = [style for style in styles if style.get("id") == args.show]
        if not selected:
            print(f"error: style id not found: {args.show}", file=sys.stderr)
            return 1

    if args.list and not args.show:
        for style in selected:
            print(f"{style.get('id')}\t{style.get('category')}\t{style.get('primary_mode')}\t{style.get('name')}")
        return 0

    for idx, style in enumerate(selected):
        if idx:
            print()
        print_style(style)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
