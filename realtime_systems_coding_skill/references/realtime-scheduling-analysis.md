# Real-Time Scheduling Analysis

## Time Model
- Absolute time needs an epoch or external reference.
- Relative time measures intervals between events.
- Real-time clocks combine an oscillator, counter, and conversion software.
- Clock accuracy is the smallest distinguishable time grain. Counter width and accuracy determine overflow interval.
- If an application runs longer than the counter overflow interval, time becomes non-monotonic unless overflow cycles are tracked.

## Timers, Delays, And Drift
- Timers can be one-shot or periodic.
- A relative `delay(duration)` suspends for at least the requested duration, but actual execution can resume later because of clock granularity, preemption, or scheduler delay.
- Repeating a relative delay in a loop accumulates drift.
- Periodic tasks should compute the next absolute activation instant and delay until `next_release - now`.
- Use timeouts for blocking services so a task cannot remain suspended indefinitely when a peer, device, or service fails.

## Simple Periodic Task Model
The simple task model assumes:
- A fixed set of tasks.
- No runtime task creation or destruction.
- Periodic activations with known fixed periods.
- Independent tasks with no semaphores, shared resources, or blocking synchronization.
- Deadline equal to period.
- Known worst-case execution time, `C`.
- Ignored context-switch and minor overheads.

## Temporal Attributes
Record these values when analyzing a task:
- Priority `P`.
- Activation or release time `ta`.
- Start time `ts`.
- Finish time `tf`.
- Absolute deadline `tl`.
- Period `T`.
- Latency `J = ts - ta`.
- Computation time `c`.
- WCET `C`.
- Elapsed execution time `e = tf - ts`.
- Response time `R = J + e`.
- Relative deadline `D`.
- Phase `Phi`.
- Release jitter and absolute fluctuation.
- Lateness/excess time.
- Slack or laxity `H = D - c`.

## Rate Monotonic Scheduling
- RMS is a static priority scheme for periodic tasks.
- Shorter period means higher priority.
- Under the simple model, RMS is optimal among fixed-priority assignments when deadlines equal periods.
- Liu-Layland Theorem I gives a sufficient utilization bound: sum(Ci/Ti) <= N * (2^(1/N) - 1).
- The RMS utilization test is sufficient but not necessary. A task set can miss the bound and still be schedulable.
- For large N, the bound approaches about 69.3 percent.
- If the bound is exceeded, use a timeline/Gantt simulation over the relevant period window or a stronger response-time analysis before declaring failure.

## EDF
- Earliest Deadline First is dynamic: the task with the closest current deadline runs first.
- Under the simple task model, EDF can schedule task sets up to total utilization <= 1.
- EDF is theoretically stronger than fixed priority for the simple model, but dynamic priority recalculation adds overhead and can make transient overload less predictable with respect to task criticality.

## General Task Models
- If `D < T`, Deadline Monotonic Priority Ordering is the static-priority criterion to consider instead of pure RMS.
- Sporadic tasks are event triggered with a minimum inter-arrival time; worst-case analysis assumes they arrive as frequently as allowed.
- Aperiodic tasks have irregular arrivals and permissive deadlines; they often need a server to improve response without harming strict periodic tasks.
- Shared resources invalidate the simple task model unless blocking time is included.

## Priority Inversion
- Priority inversion occurs when a high-priority task waits for a resource held by a low-priority task while intermediate-priority tasks run.
- Unmanaged priority inversion can invalidate RMS-style predictions.
- Non-preemptive critical sections bound inversion by preventing preemption inside critical sections, but they can unnecessarily delay unrelated tasks.
- Priority inheritance temporarily raises the priority of a resource holder to the highest priority of the task it blocks. It reduces inversion but can still allow multiple blocking and transitive chains.
- Priority ceiling protocols define a resource ceiling equal to the highest priority of any task that may use the resource.
- Immediate priority ceiling raises a task's dynamic priority when it locks a resource; it can prevent deadlock, transitive blocking, and repeated blocking on uniprocessors.

## Blocking Time
- With non-preemptive critical sections, a task can be blocked at most once by the longest lower-priority critical section active at release.
- With priority inheritance, blocking estimates must include direct and indirect blocking and are often pessimistic.
- With priority ceiling protocols, a high-priority task can experience a single initial blocking by lower-priority critical sections whose ceiling is not lower than the task's priority.
- In feasibility checks, use adjusted WCET `Ci* = Ci + Bi` when the selected protocol requires a blocking factor `Bi`.

## Aperiodic Servers
- Background/slack server handles aperiodic requests at the lowest priority; periodic guarantees remain simple but response can be poor.
- Polling server reserves `Cs` every `Ts`; unused polling capacity can be returned to periodic work, but a request may wait for the next poll.
- Deferred server preserves capacity within its period and can serve requests immediately at high priority until capacity is exhausted.
- Server utilization must be included in schedulability analysis.
