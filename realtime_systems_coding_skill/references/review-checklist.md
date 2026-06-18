# Review Checklist

## Model
- Execution units are named.
- Shared mutable state is listed.
- Resource ownership is clear.
- Communication channels/tags/communicators are named.
- Timing requirements distinguish hard, firm, and soft expectations.

## Safety
- Critical sections protect exactly the intended state.
- Lock/semaphore acquisition order is documented and consistent.
- Wait conditions are checked before blocking and rechecked after wake.
- Non-blocking buffers are not reused before completion.
- Message types, tags, and ranks cannot cross protocol contexts accidentally.
- Unsafe states are named as `NOTSAFE` or equivalent.
- Custom mutual exclusion protocols identify Dijkstra condition assumptions, intent flags, turn/tie-break state, and bounded waiting arguments.
- Monitor code names the signal semantics: AS, SC, SX, SW, or SU.
- SX/SW/SU code does not treat preemptive signal behavior as if it were SC.
- SC code rechecks conditions after wake and is safe against signal stealing.
- Nested monitor calls are forbidden, modeled, or explicitly supported by the runtime.

## Liveness And Fairness
- Deadlock scenarios were considered.
- Starvation scenarios were considered.
- Fairness assumptions are explicit and tied to scheduler/runtime/hardware evidence.
- Signal/notify operations cannot leave waiters blocked indefinitely.
- Timeout and cancellation paths release resources.
- Guarded alternatives do not rely on nondeterministic choice being random.
- CSP repetitive orders have termination, failure, or matching-communication paths.
- Remote calls and rendezvous accept paths cannot leave clients queued forever without timeout or termination policy.

## Real-Time
- `Ci`, `Ti`, `Di`, priority, phase, and blocking `Bi` are recorded.
- Clock granularity and overflow behavior are known.
- Periodic loops use absolute next release or an equivalent drift-control pattern.
- Blocking operations are bounded or excluded from hard-deadline paths.
- Priority inversion mitigation is selected and analyzed.
- RMS/EDF claims match their assumptions.

## Performance
- Critical sections are bounded and measured.
- Busy waiting is justified by measured wait duration and core budget.
- Non-blocking communication overlaps with independent work.
- Benchmarks include tail latency, jitter, and deadline misses.
- Placement across CPUs, NUMA, accelerators, VMs, containers, or edge regions is intentional.

## Implementation
- Error paths unlock, signal, close, or cancel consistently.
- Resource lifetimes outlive outstanding work.
- Thread/rank/task creation and joining are structured.
- Logs do not introduce new blocking inside hot locks.
- Tests include stress, schedule perturbation, and regression cases for the bug class.
- Diagrams or timelines exist for nontrivial interleavings, monitor queues, message passing, priority inversion, or task deadlines.
