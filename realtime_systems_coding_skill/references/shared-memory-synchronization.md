# Shared-Memory Synchronization

## Mutual Exclusion Design
Use mutual exclusion when a set of statements must behave as one indivisible action with respect to other execution units. Always name:
- The shared data or resource being protected.
- The critical section boundary.
- The acquisition protocol.
- The restitution or release protocol.
- The invariant that must hold before and after the critical section.

## Low-Level Mechanisms
- Interrupt masking is fast but dangerous: it prevents real-time event handling, blocks unrelated work, breaks clock-dependent scheduling inside the section, and can deadlock if interrupts are not re-enabled.
- Test-and-set locks use an atomic read-modify-write operation. They avoid races around a lock word but can waste CPU through busy waiting and can starve contenders.
- Use one lock per independent protected resource group to maximize legal interleavings.
- When multiple locks are required, acquire them in a single documented hierarchy and release in reverse order.

## POSIX Locks
- Prefer `pthread_mutex_t` for thread-level mutual exclusion unless the task explicitly requires lower-level spinning or cross-process named synchronization.
- Static initialization is simplest when lifetime is static. Dynamic initialization is useful when attributes are needed, such as recursive behavior or sharing across processes.
- Do not sleep, block on unrelated I/O, or call long-running services while holding a mutex unless this is explicitly part of the design and bounded.
- Always check lock/unlock return values in systems code where failure affects correctness or observability.

## Semaphores
- A semaphore is an ADT with initialization, `wait`/`P`, and `signal`/`V`.
- Binary semaphores naturally model mutual exclusion. General semaphores naturally model resource counts or conditional synchronization.
- Semaphore operations must be atomic. If their internal steps interleave, both safety and liveness can fail.
- Do not inspect the protected value as a correctness decision; use the semaphore operations as the protocol.
- Avoid unnecessary `signal` operations because they can cause scheduler/context-switch overhead.
- POSIX unnamed semaphores are memory objects. Named semaphores use a shared system namespace and need explicit naming, permissions, open/close, and unlink lifecycle decisions.

## Semaphore Failure Modes
- Reversed acquisition order can deadlock: `P(s1); P(s2)` in one path and `P(s2); P(s1)` in another path is a red flag.
- Global semaphore objects are hard to reason about because distant code can affect the same blocking state.
- A semaphore signal does not necessarily choose the oldest waiter; do not assume FIFO fairness unless the implementation contract provides it.

## Monitors
- A monitor centralizes access to permanent shared variables and exposes procedures that execute under mutual exclusion.
- Condition variables have no stored count like semaphores. A signal with no waiter has no effect.
- Associate each logical wait condition with a distinct condition variable when the language allows it.
- A `wait` operation must release the monitor so another process can enter and make the condition true.
- Signal only after establishing the condition that lets a blocked process progress.

## Signal Semantics
- Automatic signals are compiler/runtime inserted.
- Signal-and-continue is explicit and non-preemptive; the signaled process may need to recheck the condition because another process can enter first.
- Signal-and-exit, signal-and-wait, and urgent signals are preemptive variants; they hand control toward the signaled process more directly.
- Avoid `signal_all` style loops under preemptive semantics unless each awakened process is guaranteed to satisfy its condition.
- Use priority condition variables when the wake-up order must follow urgency rather than FIFO order.
- For AS, SC, SX, SW, SU, signal stealing, urgent queues, equivalence rules, nested monitor calls, and monitor verification, read `monitor-signalling-semantics.md`.
- For canonical monitor pseudocode patterns, read `exercise-derived-patterns.md` before inventing a new wait/signal protocol.

## Java-Style Monitors
- `synchronized` methods or blocks protect code through an object lock.
- Java has a single implicit condition queue per object for `wait`, `notify`, and `notifyAll`, so unrelated wait conditions can wake together.
- Use `while (!condition) wait()` rather than `if` so the condition is rechecked after wakeup.
- `notifyAll` is often safer than `notify` when several logical conditions share one queue, but it can increase rescheduling.
- Avoid legacy `stop`, `suspend`, and `resume` patterns because they create hard-to-reason state transitions.

## Algorithmic Patterns
- Dijkstra's refinement method shows why strict alternation, late intent marking, and symmetric yielding can fail through safety, deadlock, or livelock.
- Dekker combines intent flags with a turn variable to resolve simultaneous entry attempts.
- Peterson gives a compact two-process mutual exclusion algorithm using intent flags and a turn variable.
- Software-only mutual exclusion algorithms are valuable for reasoning, but production code should prefer tested runtime primitives unless the target level requires custom primitives.
- For Dijkstra conditions, refinement stages, Dekker verification, Peterson N-process filters, and bounded overtaking reasoning, read `mutual-exclusion-algorithms.md`.
- For exercise-shaped problems such as producer-consumer, readers-writers, bridge traffic, dining philosophers, priority resources, FIFO/SJF allocation, rendezvous, and service pipelines, read `exercise-derived-patterns.md`.
