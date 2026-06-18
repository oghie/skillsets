# Timing Benchmark Command

## Goal
Measure latency, jitter, and deadline behavior without hiding tail risk behind averages.

## Procedure
1. Pin environment: CPU, clock source, OS/kernel, container/VM limits, compiler flags, runtime version, and load.
2. Warm up runtime where needed.
3. Capture release time, start time, finish time, response time, and deadline miss count.
4. Report min, p50, p95, p99, max, and missed deadlines.
5. Repeat under background CPU, memory, I/O, and network load as appropriate.
6. Compare against baseline and include raw command lines.

## Output
- Environment.
- Workload.
- Timing distribution.
- Deadline miss count.
- Interpretation tied to the original timing requirement.
