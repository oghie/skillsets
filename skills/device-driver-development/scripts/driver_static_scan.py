#!/usr/bin/env python3
"""Heuristic static review for Linux driver directories."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

SOURCE_SUFFIXES = {".c", ".h", ".dts", ".dtsi", ".yaml", ".yml"}
BUILD_NAMES = {"Kconfig", "Makefile"}


def iter_files(root: Path):
    if root.is_file():
        yield root
        return
    for path in root.rglob("*"):
        if path.is_file() and (path.suffix in SOURCE_SUFFIXES or path.name in BUILD_NAMES):
            if ".git" not in path.parts:
                yield path


def line_no(text: str, needle: str) -> int:
    idx = text.find(needle)
    if idx < 0:
        return 1
    return text.count("\n", 0, idx) + 1


def add(findings, severity, path, text, message):
    findings.append((severity, str(path), line_no(text, message.split("`")[1]) if "`" in message else 1, message))


def scan_c(path: Path, text: str, findings):
    if "module_" in text and "MODULE_LICENSE" not in text:
        findings.append(("error", str(path), 1, "module source has init/driver macros but no MODULE_LICENSE"))
    if "of_device_id" in text and "MODULE_DEVICE_TABLE(of" not in text:
        findings.append(("warn", str(path), line_no(text, "of_device_id"), "OF match table appears without MODULE_DEVICE_TABLE(of, ...)"))
    if "platform_driver" in text and ".probe" not in text:
        findings.append(("warn", str(path), line_no(text, "platform_driver"), "platform_driver without visible .probe callback"))
    if "copy_from_user" in text:
        for match in re.finditer(r"copy_from_user\s*\([^;]+;", text, re.S):
            stmt = match.group(0)
            if not re.search(r"if\s*\(|ret\s*=|return\s+", text[max(0, match.start()-40):match.start()+len(stmt)+20]):
                findings.append(("warn", str(path), text.count("\n", 0, match.start()) + 1, "copy_from_user result may be unchecked"))
    if "copy_to_user" in text:
        for match in re.finditer(r"copy_to_user\s*\([^;]+;", text, re.S):
            stmt = match.group(0)
            if not re.search(r"if\s*\(|ret\s*=|return\s+", text[max(0, match.start()-40):match.start()+len(stmt)+20]):
                findings.append(("warn", str(path), text.count("\n", 0, match.start()) + 1, "copy_to_user result may be unchecked"))
    if re.search(r"(?<!devm_)ioremap\s*\(", text):
        findings.append(("warn", str(path), line_no(text, "ioremap"), "raw ioremap found; prefer devm_ioremap_resource for platform resources"))
    if re.search(r"\*\s*\([^)]*__iomem[^)]*\)", text):
        findings.append(("error", str(path), line_no(text, "__iomem"), "possible direct __iomem dereference; use read/write accessors"))
    if "request_irq" in text and "devm_request_irq" not in text and "free_irq" not in text:
        findings.append(("warn", str(path), line_no(text, "request_irq"), "request_irq without devm_request_irq or visible free_irq"))
    if "INIT_WORK" in text and not re.search(r"cancel_work_sync|flush_work|destroy_workqueue", text):
        findings.append(("warn", str(path), line_no(text, "INIT_WORK"), "work item initialized without visible cancellation/flush"))
    if "timer_setup" in text and not re.search(r"del_timer_sync|timer_delete_sync", text):
        findings.append(("warn", str(path), line_no(text, "timer_setup"), "timer initialized without visible sync deletion"))
    if "spin_lock" in text and re.search(r"spin_lock[^;]+;[\s\S]{0,300}(i2c_|spi_sync|regmap_.*read|regmap_.*write|mutex_lock|msleep|schedule)", text):
        findings.append(("error", str(path), line_no(text, "spin_lock"), "sleepable operation appears near spinlock; verify atomic context"))
    if "debugfs_create" in text and re.search(r"debugfs_create.*mode\s*[,)]", text):
        findings.append(("info", str(path), line_no(text, "debugfs_create"), "debugfs present; ensure it is not required ABI"))
    if "DEVICE_ATTR" in text and re.search(r"sprintf\s*\(", text):
        findings.append(("warn", str(path), line_no(text, "sprintf"), "sysfs show path may use sprintf; prefer sysfs_emit"))


def scan_dt(path: Path, text: str, findings):
    if path.suffix in {".yaml", ".yml"} and not (
        "$schema" in text and ("compatible:" in text or "properties:" in text)
    ):
        return
    if "compatible" in text and "reg" not in text and "gpio" not in text and "interrupt" not in text:
        findings.append(("info", str(path), line_no(text, "compatible"), "DT node/binding has compatible but no obvious resources; verify this is intentional"))
    if path.suffix in {".yaml", ".yml"} and "additionalProperties" not in text and "unevaluatedProperties" not in text:
        findings.append(("warn", str(path), 1, "binding schema lacks additionalProperties/unevaluatedProperties constraint"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--format", choices=["text", "markdown"], default="markdown")
    args = parser.parse_args()

    findings = []
    for path in iter_files(args.path):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            findings.append(("error", str(path), 1, f"could not read file: {exc}"))
            continue
        if path.suffix in {".c", ".h"}:
            scan_c(path, text, findings)
        elif path.suffix in {".dts", ".dtsi", ".yaml", ".yml"}:
            scan_dt(path, text, findings)

    order = {"error": 0, "warn": 1, "info": 2}
    findings.sort(key=lambda row: (order[row[0]], row[1], row[2]))
    if args.format == "markdown":
        print("# Driver Static Scan")
        if not findings:
            print("\nNo heuristic findings.")
        else:
            print("\n| Severity | Location | Finding |")
            print("|---|---|---|")
            for sev, path, line, msg in findings:
                print(f"| {sev} | `{path}:{line}` | {msg} |")
    else:
        if not findings:
            print("No heuristic findings.")
        for sev, path, line, msg in findings:
            print(f"{sev}: {path}:{line}: {msg}")
    return 1 if any(sev == "error" for sev, *_ in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
