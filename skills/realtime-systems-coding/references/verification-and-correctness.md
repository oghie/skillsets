# Verification And Correctness

## Why Testing Alone Is Not Enough
Concurrent programs can have an enormous number of interleavings. Debugging samples only a small subset and cannot prove that transient errors are absent. Treat testing as evidence, not proof.

## Property Vocabulary
- Safety: no execution reaches a forbidden state.
- Liveness: some desired state is eventually reached.
- Fairness: ready processes obtain opportunity according to an explicit justice rule.
- Deadlock: no relevant process can proceed.
- Starvation: at least one process remains unable to make useful progress while others may continue.
- Bounded blocking: blocking is limited by a known upper bound.
- Deadline satisfaction: each task completes before its time limit under stated assumptions.

## Invariants
Use invariants to replace unbounded interleaving reasoning with a stable property over shared state.
- Define the invariant using shared variables or protocol state.
- Prove it holds initially.
- Prove each atomic action preserves it.
- Define `NOTSAFE` as a predicate for a forbidden state.
- Show `Invariant -> not(NOTSAFE)`.

## Atomic Actions
- Identify the smallest operation that is indivisible under the selected abstraction.
- A statement with multiple machine instructions is not atomic unless protected by synchronization or the language/runtime specifies atomicity.
- In monitor, lock, or synchronized blocks, the protected block can be treated as a larger atomic action only with respect to the protected state and lock contract.

## Non-Interference
For two concurrent proof fragments, an atomic action in one process must not invalidate a critical assertion in another process.
- Rename local variables when necessary to avoid accidental aliasing in the proof.
- If critical assertions are written as `Invariant and LocalPredicate`, global invariant reasoning can reduce the amount of non-interference proof needed.

## Message Passing Proof Points
- Synchronous rendezvous creates a joint state transition between sender and receiver.
- For safe communication, sender-side buffer mutation after send must not affect the value received.
- For non-blocking communication, the proof must include the completion point after which buffers are safe.
- In CSP-style reasoning, matched input/output commands execute as one communication event.

## Real-Time Verification
- Verify both functional state and temporal state.
- State the scheduling model before applying any test.
- RMS utilization is sufficient, not necessary, under the simple periodic model.
- EDF utilization <= 1 is an exact feasibility criterion under the simple model with deadlines equal to periods.
- Add blocking time, server utilization, release jitter, overhead, and drift control when the simple model assumptions do not hold.

## Practical Evidence Stack
- Static inspection for shared mutable state, lock order, wait conditions, and buffer completion.
- Deterministic or randomized stress runs that perturb scheduling.
- Thread sanitizers, race detectors, lock-order checkers, or model checking when available.
- Timeline/Gantt simulation for task sets.
- Runtime traces for release time, start time, finish time, blocking intervals, and missed deadlines.
- Benchmarks that report distribution, jitter, tail latency, and overload behavior rather than only mean throughput.
