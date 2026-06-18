# Schedulability Review Command

## Goal
Evaluate whether a task set can meet deadlines under the stated scheduling model.

## Procedure
1. Capture task table: name, `C`, `T`, `D`, phase, priority, blocking `B`, and resource use.
2. Confirm whether the simple task model holds.
3. Run `scripts/schedulability.py` with RMS, deadline-monotonic, or EDF as appropriate.
4. If RMS utilization bound passes, report it as sufficient evidence.
5. If RMS bound fails, report it as inconclusive and use simulation or stronger response-time evidence.
6. Include blocking time for shared resources.
7. Check drift and clock assumptions for actual implementation.

## Output
- Scheduling model and assumptions.
- Utilization and bound.
- Simulated deadline misses or response times.
- Priority inversion risks.
- Instrumentation needed in runtime.
