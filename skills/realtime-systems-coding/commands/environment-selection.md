# Environment Selection Command

## Goal
Choose the lowest abstraction level that can satisfy the timing, concurrency, and operational constraints without unnecessary complexity.

## Procedure
1. State the timing goal and correctness property.
2. Start from the highest maintainable level and move lower only when evidence demands it.
3. Compare candidate levels using `references/development-environments/abstraction-level-map.md`.
4. Identify the scheduling, clock, memory, and communication contract at each candidate level.
5. Select the level with the clearest validation path.

## Decision Hints
- Choose Level -1 for custom cycle-level datapaths.
- Choose Level 0 for accelerator/offload workloads where transfer overhead is justified.
- Choose Level 1 for direct hardware or hard real-time control.
- Choose Level 2 for isolated hosted systems with measured jitter tolerance.
- Choose Level 3 for scalable soft real-time services and distributed workloads.
- Choose Level 4 for locality, edge autonomy, and geographically distributed behavior.

## Output
- Selected level.
- Rejected alternatives and why.
- Required toolchain.
- Verification commands and measurements.
