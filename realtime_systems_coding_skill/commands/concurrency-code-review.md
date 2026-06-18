# Concurrency Code Review Command

## Goal
Review code for races, deadlocks, starvation, lost signals, unsafe message passing, and unbounded blocking.

## Procedure
1. List execution units and shared state.
2. Run `scripts/concurrency_static_scan.py <path>`.
3. Inspect lock/semaphore/condition ownership manually.
4. Search for sleeps, blocking calls, logging, allocation, and remote calls inside critical sections.
5. Search for non-blocking operations and verify completion before buffer reuse.
6. Identify one plausible bad interleaving for each risky area.
7. Recommend the smallest protocol change that restores the violated property.

## Output
- Findings first, ordered by severity.
- File and line references.
- Violated property: safety, liveness, fairness, bounded blocking, or deadline.
- Suggested fix.
- Tests or traces required.
