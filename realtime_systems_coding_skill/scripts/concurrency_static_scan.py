#!/usr/bin/env python3
"""Heuristic scanner for concurrent and real-time code review.

This tool intentionally reports review candidates, not formal findings.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


TEXT_EXTENSIONS = {
    ".c",
    ".cc",
    ".cpp",
    ".cxx",
    ".h",
    ".hpp",
    ".hh",
    ".rs",
    ".go",
    ".java",
    ".kt",
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".m",
    ".mm",
    ".cu",
    ".md",
}


@dataclass(frozen=True)
class Issue:
    severity: str
    path: Path
    line: int
    rule: str
    message: str


def iter_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_file():
            files.append(path)
        elif path.is_dir():
            for child in path.rglob("*"):
                if child.is_file() and child.suffix.lower() in TEXT_EXTENSIONS:
                    files.append(child)
    return sorted(files)


def read_text(path: Path) -> str | None:
    try:
        data = path.read_bytes()
    except OSError:
        return None
    if b"\0" in data[:4096]:
        return None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return data.decode("latin-1", errors="replace")


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def add_regex_issues(
    issues: list[Issue],
    path: Path,
    text: str,
    severity: str,
    rule: str,
    pattern: str,
    message: str,
    flags: int = 0,
) -> None:
    for match in re.finditer(pattern, text, flags):
        issues.append(Issue(severity, path, line_number(text, match.start()), rule, message))


def find_reversed_pairs(text: str, names: list[str]) -> set[tuple[str, str]]:
    pairs: set[tuple[str, str]] = set()
    if len(names) < 2:
        return pairs
    for a, b in zip(names, names[1:]):
        if a != b:
            pairs.add((a, b))
    reversed_pairs = set()
    for a, b in pairs:
        if (b, a) in pairs:
            reversed_pairs.add((a, b))
    return reversed_pairs


def scan_path(path: Path) -> list[Issue]:
    if path.resolve() == Path(__file__).resolve():
        return []
    text = read_text(path)
    if text is None:
        return []
    issues: list[Issue] = []

    add_regex_issues(
        issues,
        path,
        text,
        "warning",
        "busy-wait",
        r"while\s*\([^)]*\)\s*;",
        "empty while loop can be busy waiting; justify spin duration or use blocking primitive",
    )
    add_regex_issues(
        issues,
        path,
        text,
        "warning",
        "volatile-sync",
        r"\bvolatile\b(?!\s+sig_atomic_t)",
        "volatile is not a synchronization primitive by itself",
    )
    add_regex_issues(
        issues,
        path,
        text,
        "warning",
        "relative-delay-loop",
        r"(while|for)\s*\([^)]*\)\s*\{(?:(?!\n\}).){0,1200}\b(sleep|usleep|nanosleep|Thread\.sleep|setTimeout)\b",
        "relative delay inside loop can accumulate drift; consider absolute next-release scheduling",
        flags=re.S,
    )
    add_regex_issues(
        issues,
        path,
        text,
        "warning",
        "blocking-inside-mutex",
        r"pthread_mutex_lock\s*\([^;]+;(?:(?!pthread_mutex_unlock).){0,1600}\b(sleep|usleep|nanosleep|pthread_join|sem_wait|MPI_Recv)\b",
        "blocking call appears between mutex lock and unlock; verify bounded blocking and context",
        flags=re.S,
    )
    add_regex_issues(
        issues,
        path,
        text,
        "warning",
        "java-wait-if",
        r"\bif\s*\([^)]*\)\s*\{?\s*(?:[A-Za-z0-9_$.]+\.)?wait\s*\(",
        "wait guarded by if; use while to recheck the condition after wake",
        flags=re.S,
    )
    add_regex_issues(
        issues,
        path,
        text,
        "info",
        "java-notify",
        r"\bnotify\s*\(",
        "notify selects an unspecified waiter; verify one shared condition or consider notifyAll",
    )
    add_regex_issues(
        issues,
        path,
        text,
        "error",
        "java-thread-stop",
        r"\.(stop|suspend|resume)\s*\(",
        "legacy thread control can leave shared state inconsistent",
    )
    add_regex_issues(
        issues,
        path,
        text,
        "warning",
        "mpi-blocking-order",
        r"MPI_Send\s*\([^;]+;(?:(?!MPI_Recv).){0,1200}MPI_Send\s*\(",
        "multiple blocking sends before receives can deadlock depending on buffering and peer order",
        flags=re.S,
    )

    if re.search(r"\bMPI_I(send|recv)\s*\(", text) and not re.search(r"\bMPI_(Wait|Waitall|Waitany|Test|Testall|Testany)\s*\(", text):
        issues.append(
            Issue(
                "warning",
                path,
                1,
                "mpi-nonblocking-completion",
                "MPI non-blocking operation appears without Wait/Test completion in this file",
            )
        )

    mutex_locks = re.findall(r"pthread_mutex_lock\s*\(\s*&?([A-Za-z_][A-Za-z0-9_]*)", text)
    for a, b in sorted(find_reversed_pairs(text, mutex_locks)):
        first = text.find(a)
        issues.append(
            Issue(
                "warning",
                path,
                line_number(text, first) if first >= 0 else 1,
                "mutex-order",
                f"mutex acquisition order includes both {a}->{b} and {b}->{a}; verify global order",
            )
        )

    semaphore_waits = re.findall(r"sem_wait\s*\(\s*&?([A-Za-z_][A-Za-z0-9_]*)", text)
    for a, b in sorted(find_reversed_pairs(text, semaphore_waits)):
        first = text.find(a)
        issues.append(
            Issue(
                "warning",
                path,
                line_number(text, first) if first >= 0 else 1,
                "semaphore-order",
                f"semaphore wait order includes both {a}->{b} and {b}->{a}; verify deadlock freedom",
            )
        )

    waits = len(re.findall(r"\b(wait|sem_wait|pthread_cond_wait|MPI_Recv)\s*\(", text))
    posts = len(re.findall(r"\b(signal|notify|notifyAll|sem_post|pthread_cond_signal|pthread_cond_broadcast|MPI_Send)\s*\(", text))
    if waits > 0 and posts == 0:
        issues.append(
            Issue(
                "info",
                path,
                1,
                "wait-without-signal",
                "wait-like operations appear without signal/send-like operations in this file; verify peer code",
            )
        )
    return issues


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Heuristic concurrent-code scanner.")
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument(
        "--fail-on",
        choices=["none", "error", "warning", "info"],
        default="none",
        help="Exit non-zero when issues at this severity or higher are found.",
    )
    args = parser.parse_args(argv)

    files = iter_files(args.paths)
    issues: list[Issue] = []
    for path in files:
        issues.extend(scan_path(path))

    severity_rank = {"error": 3, "warning": 2, "info": 1}
    for issue in sorted(issues, key=lambda item: (item.path.as_posix(), item.line, -severity_rank[item.severity])):
        print(f"{issue.severity.upper()} {issue.path}:{issue.line} [{issue.rule}] {issue.message}")
    print(f"Scanned {len(files)} files; issues: {len(issues)}")

    if args.fail_on == "none":
        return 0
    threshold = severity_rank[args.fail_on]
    if any(severity_rank[issue.severity] >= threshold for issue in issues):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
