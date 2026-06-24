#!/usr/bin/env python3
"""Heuristic Rust library surface audit for crate architecture reviews."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python <3.11 fallback path.
    tomllib = None  # type: ignore[assignment]


@dataclass(frozen=True)
class Finding:
    severity: str
    path: Path
    message: str

    def render(self) -> str:
        return f"{self.path}: {self.severity}: {self.message}"


PUBLIC_ITEM = re.compile(r"(?m)^\s*pub\s+(?:async\s+)?(?:unsafe\s+)?(?:fn|struct|enum|trait|type|const|static)\b")
PUBLIC_FIELD_STRUCT = re.compile(r"(?ms)^\s*(?:#\[[^\]]+\]\s*)*pub\s+struct\s+\w+\s*\{[^}]*\bpub\s+\w+\s*:")
PUBLIC_TUPLE_STRUCT = re.compile(r"(?m)^\s*pub\s+struct\s+\w+\s*\(\s*pub\s+")
PUBLIC_ENUM = re.compile(r"(?m)^\s*(?:#\[[^\n]*\]\s*)*pub\s+enum\s+\w+")
PUBLIC_TRAIT = re.compile(r"(?m)^\s*pub\s+trait\s+\w+")
PUBLIC_UNSAFE_FN = re.compile(r"(?m)^\s*pub\s+unsafe\s+fn\s+\w+")
UNSAFE_BLOCK = re.compile(r"unsafe\s*\{")
PUB_ASYNC_FN = re.compile(r"(?m)^\s*pub\s+async\s+fn\b")
PANICISH = re.compile(r"\bpanic!|\bunwrap\s*\(|\bexpect\s*\(")
REEXPORT = re.compile(r"(?m)^\s*pub\s+use\s+")
NO_STD = re.compile(r"#!\s*\[\s*no_std\s*\]")
DOC_SAFETY = re.compile(r"^///\s*#\s*Safety\b|^//!+\s*#\s*Safety\b", re.MULTILINE)
SAFETY_COMMENT = re.compile(r"^\s*//\s*SAFETY:", re.MULTILINE)
DOC_ERRORS = re.compile(r"^///\s*#\s*Errors\b|^//!+\s*#\s*Errors\b", re.MULTILINE)
DOC_PANICS = re.compile(r"^///\s*#\s*Panics\b|^//!+\s*#\s*Panics\b", re.MULTILINE)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def load_manifest(path: Path) -> dict:
    if tomllib is None:
        raise RuntimeError("tomllib is required; use Python 3.11+")
    with path.open("rb") as handle:
        return tomllib.load(handle)


def rust_files(root: Path) -> list[Path]:
    src = root / "src"
    if not src.exists():
        return []
    return sorted(src.rglob("*.rs"))


def nearby_text(text: str, start: int, radius: int = 280) -> str:
    return text[max(0, start - radius):start]


def audit_manifest(root: Path, manifest_path: Path) -> list[Finding]:
    findings: list[Finding] = []
    try:
        manifest = load_manifest(manifest_path)
    except Exception as exc:
        return [Finding("error", manifest_path, f"cannot parse Cargo.toml: {exc}")]

    package = manifest.get("package", {})
    features = manifest.get("features", {})
    dependencies = manifest.get("dependencies", {})

    for field in ("description", "license", "repository", "readme", "rust-version"):
        if field == "license" and ("license" in package or "license-file" in package):
            continue
        if field not in package:
            findings.append(Finding("warn", manifest_path, f"package metadata missing `{field}`"))

    if package.get("publish") is False:
        findings.append(Finding("info", manifest_path, "package is marked publish=false; public release checks may be internal-only"))

    if features:
        if "default" not in features:
            findings.append(Finding("info", manifest_path, "features exist but no explicit `default` feature set is declared"))
        suspicious = [name for name in features if re.search(r"(no[-_]?std|disable|without)", name, re.IGNORECASE)]
        if suspicious:
            findings.append(
                Finding(
                    "warn",
                    manifest_path,
                    "feature names suggest subtractive behavior; prefer additive features such as `std`: "
                    + ", ".join(sorted(suspicious)),
                )
            )

    optional_deps = sorted(name for name, spec in dependencies.items() if isinstance(spec, dict) and spec.get("optional"))
    if optional_deps and not features:
        findings.append(Finding("warn", manifest_path, "optional dependencies exist but no explicit features section was found"))

    include = package.get("include")
    exclude = package.get("exclude")
    if include is None and exclude is None and package.get("publish") is not False:
        findings.append(Finding("info", manifest_path, "published package has no include/exclude policy; review packaged files with `cargo package --list`"))

    return findings


def audit_rust_file(path: Path) -> list[Finding]:
    text = read_text(path)
    findings: list[Finding] = []

    if PUBLIC_ITEM.search(text) and path.name != "lib.rs" and "//! " not in text[:1000] and "///" not in text[:1000]:
        findings.append(Finding("info", path, "public items found; ensure docs describe contract, errors, panics, and examples where relevant"))

    if PUBLIC_FIELD_STRUCT.search(text) or PUBLIC_TUPLE_STRUCT.search(text):
        findings.append(Finding("warn", path, "public struct fields/tuple fields expose layout and can constrain future compatibility"))

    for match in PUBLIC_ENUM.finditer(text):
        before = nearby_text(text, match.start())
        if "#[non_exhaustive]" not in before:
            findings.append(Finding("info", path, "public enum without nearby `#[non_exhaustive]`; verify exhaustive matching is intended"))

    for match in PUBLIC_TRAIT.finditer(text):
        trait_block = text[match.start(): match.start() + 900]
        before = nearby_text(text, match.start())
        if "sealed" not in trait_block.lower() and "fn " in trait_block and "=" not in trait_block:
            findings.append(Finding("warn", path, "public trait appears implementable by downstream crates; verify evolution/default-method strategy"))
        if "#[doc(hidden)]" in before:
            findings.append(Finding("info", path, "doc-hidden public trait still affects generated or downstream contracts; document internal contract"))

    for match in PUBLIC_UNSAFE_FN.finditer(text):
        before = nearby_text(text, match.start(), radius=600)
        if not DOC_SAFETY.search(before):
            findings.append(Finding("error", path, "public unsafe function lacks nearby `# Safety` documentation"))

    for match in UNSAFE_BLOCK.finditer(text):
        before = nearby_text(text, match.start(), radius=180)
        if not SAFETY_COMMENT.search(before):
            findings.append(Finding("warn", path, "unsafe block lacks nearby `SAFETY:` invariant comment"))

    if REEXPORT.search(text):
        findings.append(Finding("info", path, "public re-export found; dependency versions/types may become part of the public contract"))

    if PUB_ASYNC_FN.search(text) and not re.search(r"tokio|async-std|runtime|executor|blocking|cancel", text, re.IGNORECASE):
        findings.append(Finding("warn", path, "public async API found without obvious runtime, blocking, or cancellation contract nearby"))

    if NO_STD.search(text):
        findings.append(Finding("info", path, "`#![no_std]` found; verify target build, `alloc` policy, panic/OOM behavior, and additive `std` feature"))

    if PANICISH.search(text):
        if not DOC_PANICS.search(text):
            findings.append(Finding("info", path, "panic/unwrap/expect found; public panic behavior may need `# Panics` docs or fallible API"))

    if re.search(r"Result\s*<", text) and PUBLIC_ITEM.search(text) and not DOC_ERRORS.search(text):
        findings.append(Finding("info", path, "public Result-returning API found; verify `# Errors` docs and error contract tests"))

    return findings


def audit_tests(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    if not (root / "tests").exists():
        findings.append(Finding("warn", root, "no `tests/` directory found; public contract integration tests may be missing"))
    if not any(root.glob("examples/*.rs")):
        findings.append(Finding("info", root, "no Rust examples found; public crates benefit from examples that compile"))
    if not any(root.glob("benches/*.rs")):
        findings.append(Finding("info", root, "no benchmarks found; add only when performance is part of the contract"))
    return findings


def audit(root: Path) -> list[Finding]:
    root = root.resolve()
    manifest_path = root / "Cargo.toml"
    if not manifest_path.exists():
        return [Finding("error", root, "Cargo.toml not found")]

    findings: list[Finding] = []
    findings.extend(audit_manifest(root, manifest_path))

    files = rust_files(root)
    if not files:
        findings.append(Finding("error", root / "src", "no Rust source files found under src/"))
        return findings

    for file_path in files:
        findings.extend(audit_rust_file(file_path))

    lib_rs = root / "src" / "lib.rs"
    if not lib_rs.exists():
        findings.append(Finding("warn", root / "src", "library crate should normally expose `src/lib.rs`; verify crate type if absent"))

    findings.extend(audit_tests(root))
    return findings


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("crate_root", type=Path, help="Path containing Cargo.toml")
    parser.add_argument("--max-findings", type=int, default=200, help="Maximum findings to print")
    args = parser.parse_args(argv)

    findings = audit(args.crate_root)
    if findings:
        for finding in findings[: args.max_findings]:
            print(finding.render())
        remaining = len(findings) - args.max_findings
        if remaining > 0:
            print(f"... {remaining} more finding(s) omitted")
        return 1 if any(f.severity in {"error", "warn"} for f in findings) else 0

    print("OK: no heuristic Rust library surface gaps found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
