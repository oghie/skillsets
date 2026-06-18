# Diagnose Concurrency Or Real-Time Bugs

## Use When
The issue is intermittent, timing-sensitive, deadlocked, starving, racing, losing messages, drifting, or missing deadlines.

## Workflow
1. Reproduce or capture evidence without changing behavior too much.
2. Classify symptom:
   - Race or data corruption.
   - Deadlock.
   - Starvation or unfairness.
   - Lost signal or missed notification.
   - Message protocol mismatch.
   - Buffer reuse before completion.
   - Drift or deadline miss.
   - Priority inversion.
3. Build a minimal state timeline from logs, traces, or code.
4. Identify the first violated property.
5. Form a hypothesis tied to a specific interleaving, wait state, or timing window.
6. Add targeted instrumentation.
7. Fix the protocol, not the timing luck.
8. Add a regression test that increases the chance of the bad interleaving or deadline miss.

## Evidence To Collect
- Thread/rank/task IDs.
- Lock/semaphore acquisition and release times.
- Wait/notify or signal events.
- Message send/receive/completion events.
- Task release/start/finish/deadline times.
- CPU affinity, priorities, scheduler policy, and system load.
- Clock source and timer resolution.

## Red Flags
- Sleeping to "fix" a race.
- Checking a condition without holding the lock that protects it.
- Using `if` around condition-variable wait.
- Holding a mutex while calling remote services or unbounded I/O.
- Reversed lock or semaphore order.
- Non-blocking send/receive without wait/test.
- Relative delay inside a periodic loop.
- High-priority task waiting on a low-priority resource without inheritance or ceiling.

## Fix Categories
- Add or narrow mutual exclusion.
- Convert lost signal to state predicate plus condition variable.
- Add lock ordering.
- Split hot shared state.
- Add completion tracking.
- Add timeout and cleanup.
- Change scheduling priority or protocol.
- Move work to a lower-priority or asynchronous path.

## Verification
- Force bad scheduling with stress, sleeps in test-only hooks, randomized yields, or deterministic schedulers.
- Use sanitizers/race detectors when available.
- Re-run under load and with CPU count variations.
- For real-time bugs, compare before/after deadline miss count and response-time distribution.
