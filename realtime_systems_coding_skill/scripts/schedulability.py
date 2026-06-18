#!/usr/bin/env python3
"""Small schedulability helper for concurrent real-time task sets.

It reports utilization checks and can simulate a preemptive single-processor
schedule over a bounded horizon. The simulation is a practical review aid, not
a replacement for a full system-specific schedulability proof.
"""

from __future__ import annotations

import argparse
import math
import sys
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Task:
    name: str
    c: Fraction
    t: Fraction
    d: Fraction
    phase: Fraction
    b: Fraction

    @property
    def effective_c(self) -> Fraction:
        return self.c + self.b


@dataclass
class Job:
    task_index: int
    release: Fraction
    deadline: Fraction
    remaining: Fraction
    sequence: int
    start: Fraction | None = None
    finish: Fraction | None = None


def parse_fraction(text: str) -> Fraction:
    try:
        value = Fraction(text.strip())
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"not a number: {text!r}") from exc
    if value < 0:
        raise argparse.ArgumentTypeError(f"value must be non-negative: {text!r}")
    return value


def is_number(text: str) -> bool:
    try:
        Fraction(text)
        return True
    except ValueError:
        return False


def parse_task(spec: str, index: int) -> Task:
    name = f"tau{index}"
    body = spec
    if ":" in spec:
        maybe_name, maybe_body = spec.split(":", 1)
        if maybe_name:
            name = maybe_name
            body = maybe_body
    fields = [part.strip() for part in body.split(",") if part.strip()]
    if fields and not is_number(fields[0]):
        name = fields[0]
        fields = fields[1:]
    if len(fields) < 2 or len(fields) > 5:
        raise argparse.ArgumentTypeError(
            "--task format is name:C,T[,D[,phase[,B]]] or C,T[,D[,phase[,B]]]"
        )
    c = parse_fraction(fields[0])
    t = parse_fraction(fields[1])
    if c <= 0:
        raise argparse.ArgumentTypeError("C must be greater than zero")
    if t <= 0:
        raise argparse.ArgumentTypeError("T must be greater than zero")
    d = parse_fraction(fields[2]) if len(fields) >= 3 else t
    phase = parse_fraction(fields[3]) if len(fields) >= 4 else Fraction(0)
    b = parse_fraction(fields[4]) if len(fields) >= 5 else Fraction(0)
    if d <= 0:
        raise argparse.ArgumentTypeError("D must be greater than zero")
    return Task(name=name, c=c, t=t, d=d, phase=phase, b=b)


def format_fraction(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    as_float = float(value)
    if abs(as_float) >= 1000 or abs(as_float) < 0.001:
        return f"{as_float:.6g}"
    return f"{as_float:.6f}".rstrip("0").rstrip(".")


def lcm(a: int, b: int) -> int:
    return abs(a * b) // math.gcd(a, b)


def lcm_many(values: Iterable[int]) -> int:
    result = 1
    for value in values:
        result = lcm(result, value)
    return result


def gcd_fraction(values: Iterable[Fraction]) -> Fraction:
    positives = [value for value in values if value > 0]
    if not positives:
        return Fraction(1)
    denominator = lcm_many(value.denominator for value in positives)
    numerators = [int(value * denominator) for value in positives]
    result = numerators[0]
    for value in numerators[1:]:
        result = math.gcd(result, value)
    return Fraction(result, denominator)


def infer_quantum(tasks: list[Task]) -> Fraction:
    values: list[Fraction] = []
    for task in tasks:
        values.extend([task.c, task.t, task.d, task.phase, task.b])
    quantum = gcd_fraction(values)
    return quantum if quantum > 0 else Fraction(1)


def infer_horizon(tasks: list[Task], quantum: Fraction, user_horizon: Fraction | None) -> Fraction:
    if user_horizon is not None:
        return user_horizon
    ticks = []
    for task in tasks:
        period_ticks = task.t / quantum
        if period_ticks.denominator != 1:
            raise ValueError("period is not aligned to inferred quantum")
        ticks.append(period_ticks.numerator)
    return Fraction(lcm_many(ticks)) * quantum


def priority_order(policy: str, task: Task) -> tuple[Fraction, Fraction, str]:
    if policy == "rms":
        return (task.t, task.d, task.name)
    if policy == "deadline-monotonic":
        return (task.d, task.t, task.name)
    return (task.t, task.d, task.name)


def generate_jobs(tasks: list[Task], horizon: Fraction) -> list[Job]:
    jobs: list[Job] = []
    sequence = 0
    for index, task in enumerate(tasks):
        release = task.phase
        while release < horizon:
            jobs.append(
                Job(
                    task_index=index,
                    release=release,
                    deadline=release + task.d,
                    remaining=task.effective_c,
                    sequence=sequence,
                )
            )
            sequence += 1
            release += task.t
    jobs.sort(key=lambda job: (job.release, job.task_index, job.sequence))
    return jobs


def select_job(policy: str, ready: list[Job], tasks: list[Task]) -> Job:
    if policy == "edf":
        return min(ready, key=lambda job: (job.deadline, job.release, job.task_index, job.sequence))
    return min(
        ready,
        key=lambda job: (
            priority_order(policy, tasks[job.task_index]),
            job.release,
            job.sequence,
        ),
    )


def simulate(
    tasks: list[Task],
    policy: str,
    quantum: Fraction,
    horizon: Fraction,
    max_steps: int,
) -> tuple[list[Job], list[tuple[Fraction, Fraction, str]]]:
    total_steps = horizon / quantum
    if total_steps.denominator != 1:
        raise ValueError("horizon must align with quantum")
    if total_steps > max_steps:
        raise ValueError(
            f"simulation requires {total_steps} steps; increase --quantum, reduce --horizon, "
            f"or raise --max-steps"
        )

    jobs = generate_jobs(tasks, horizon)
    pending = list(jobs)
    ready: list[Job] = []
    segments: list[tuple[Fraction, Fraction, str]] = []
    time = Fraction(0)

    for _ in range(total_steps.numerator):
        while pending and pending[0].release <= time:
            ready.append(pending.pop(0))
        runnable = [job for job in ready if job.remaining > 0]
        if runnable:
            job = select_job(policy, runnable, tasks)
            if job.start is None:
                job.start = time
            label = tasks[job.task_index].name
            job.remaining -= quantum
            if job.remaining <= 0:
                job.finish = time + quantum
                ready.remove(job)
        else:
            label = "idle"
        if segments and segments[-1][2] == label and segments[-1][1] == time:
            segments[-1] = (segments[-1][0], time + quantum, label)
        else:
            segments.append((time, time + quantum, label))
        time += quantum
    return jobs, segments


def print_task_table(tasks: list[Task]) -> None:
    print("Tasks:")
    print("name\tC\tB\tC*\tT\tD\tphase\tU=C*/T")
    for task in tasks:
        util = task.effective_c / task.t
        print(
            "\t".join(
                [
                    task.name,
                    format_fraction(task.c),
                    format_fraction(task.b),
                    format_fraction(task.effective_c),
                    format_fraction(task.t),
                    format_fraction(task.d),
                    format_fraction(task.phase),
                    format_fraction(util),
                ]
            )
        )


def report_utilization(tasks: list[Task], policy: str) -> None:
    n = len(tasks)
    utilization = sum((task.effective_c / task.t for task in tasks), Fraction(0))
    print(f"\nTotal utilization: {format_fraction(utilization)}")
    if policy == "rms":
        bound = Fraction.from_float(n * (2 ** (1 / n) - 1)).limit_denominator(1_000_000)
        print(f"RMS Liu-Layland sufficient bound: {format_fraction(bound)}")
        if utilization <= bound:
            print("RMS utilization result: PASS as a sufficient test under the simple model.")
        else:
            print("RMS utilization result: INCONCLUSIVE; the bound is sufficient but not necessary.")
    elif policy == "edf":
        if all(task.d == task.t for task in tasks):
            print("EDF simple-model bound: 1")
            if utilization <= 1:
                print("EDF utilization result: PASS under the simple model with D = T.")
            else:
                print("EDF utilization result: FAIL under the simple model with D = T.")
        else:
            print("EDF note: D differs from T for at least one task; use simulation or stronger analysis.")
    else:
        print("Deadline-monotonic note: use simulation or response-time analysis for evidence.")


def report_simulation(tasks: list[Task], jobs: list[Job], horizon: Fraction) -> None:
    misses = [
        job
        for job in jobs
        if job.deadline <= horizon and (job.finish is None or job.finish > job.deadline)
    ]
    print(f"\nSimulated horizon: {format_fraction(horizon)}")
    if misses:
        print(f"Deadline misses: {len(misses)}")
        for job in misses[:20]:
            task = tasks[job.task_index]
            finish = "unfinished" if job.finish is None else format_fraction(job.finish)
            print(
                f"- {task.name}[{job.sequence}] release={format_fraction(job.release)} "
                f"deadline={format_fraction(job.deadline)} finish={finish}"
            )
        if len(misses) > 20:
            print(f"- ... {len(misses) - 20} more")
    else:
        print("Deadline misses: 0 within simulated horizon.")

    response_by_task: dict[str, Fraction] = {}
    for job in jobs:
        if job.finish is None:
            continue
        response = job.finish - job.release
        name = tasks[job.task_index].name
        response_by_task[name] = max(response_by_task.get(name, Fraction(0)), response)
    if response_by_task:
        print("Max response time:")
        for name in sorted(response_by_task):
            print(f"- {name}: {format_fraction(response_by_task[name])}")


def write_timeline(path: Path, segments: list[tuple[Fraction, Fraction, str]]) -> None:
    lines = ["start,end,label"]
    for start, end, label in segments:
        lines.append(f"{format_fraction(start)},{format_fraction(end)},{label}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Utilization and bounded timeline checks for periodic real-time tasks."
    )
    parser.add_argument(
        "--task",
        action="append",
        required=True,
        help="Task as name:C,T[,D[,phase[,B]]] or C,T[,D[,phase[,B]]]. B is blocking time.",
    )
    parser.add_argument(
        "--policy",
        choices=["rms", "deadline-monotonic", "edf"],
        default="rms",
        help="Scheduling policy for simulation and utilization interpretation.",
    )
    parser.add_argument("--quantum", type=parse_fraction, help="Simulation time quantum.")
    parser.add_argument("--horizon", type=parse_fraction, help="Simulation horizon.")
    parser.add_argument("--max-steps", type=int, default=200_000, help="Maximum simulation steps.")
    parser.add_argument("--timeline-csv", type=Path, help="Write compressed schedule timeline as CSV.")
    args = parser.parse_args(argv)

    try:
        tasks = [parse_task(spec, index + 1) for index, spec in enumerate(args.task)]
        quantum = args.quantum or infer_quantum(tasks)
        if quantum <= 0:
            raise ValueError("quantum must be greater than zero")
        horizon = infer_horizon(tasks, quantum, args.horizon)
        if horizon <= 0:
            raise ValueError("horizon must be greater than zero")
        print_task_table(tasks)
        report_utilization(tasks, args.policy)
        jobs, segments = simulate(tasks, args.policy, quantum, horizon, args.max_steps)
        report_simulation(tasks, jobs, horizon)
        print(f"Simulation quantum: {format_fraction(quantum)}")
        if args.timeline_csv:
            write_timeline(args.timeline_csv, segments)
            print(f"Timeline CSV: {args.timeline_csv}")
    except (ValueError, argparse.ArgumentTypeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
