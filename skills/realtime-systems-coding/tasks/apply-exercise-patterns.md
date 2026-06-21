# Apply Exercise-Derived Patterns

## Use When
The task asks for pseudocode, monitor design, semaphore design, custom mutual exclusion, or a canonical synchronization problem such as producer-consumer, readers-writers, rendezvous, bridge traffic, dining philosophers, resource allocation, service pipeline, account withdrawal, memory frames, or exact group synchronization.

## Workflow
1. Match the problem to `references/exercise-derived-patterns.md`.
2. Name the process types, resources, shared variables, and blocked queues.
3. Select the signal semantics: SC, SX, SW, SU, or the runtime-specific equivalent.
4. Write the monitor invariant before writing pseudocode.
5. Write each wait as `predicate -> queue -> signal source`.
6. Add the failure scenario the pattern prevents: signal stealing, lost signal, deadlock, starvation, unfair bypass, or double allocation.
7. Translate the pseudocode to the target language only after the invariant and queue policy are explicit.
8. Verify with at least one interleaving test, stress harness, deterministic scheduler, or model-check sketch.

## Pattern Selection
| User Problem | Read |
| --- | --- |
| "Can this mutual exclusion algorithm work?" | Property audit patterns and `references/mutual-exclusion-algorithms.md`. |
| "Implement semaphore using monitor" | Portable semaphore monitor and monitor signalling semantics. |
| "Producer/consumer without queue inspection" | Encoded-count buffer. |
| "Wake one side when the other arrives" | Rendezvous and lost-signal patterns. |
| "Prevent writer starvation" | Readers-writers writer-priority monitor. |
| "One resource shared by directions or groups" | Bridge fairness batch or group rendezvous. |
| "Allocate printers/memory/resources by priority" | Priority resource allocation and FIFO/SJF queues. |
| "Controller wakes refill/service process" | Urgent-signal controller patterns. |
| "Barber/car wash/service simulation" | Service pipeline monitors. |

## Output Shape
Return:
- Selected pattern.
- Assumed semantics.
- State variables.
- Invariant.
- Pseudocode.
- Safety argument.
- Liveness/fairness argument.
- Verification cases.

## Red Flags
- Pseudocode uses `if wait` under SC for a predicate that can be invalidated.
- A signal can happen before the peer records that it is waiting.
- A monitor signal is followed by state mutation that invalidates the wake condition.
- A semaphore implementation assumes FIFO because its underlying semaphore is FIFO.
- Priority or FIFO behavior is required but not encoded in monitor state.
- A blocked process can lose its position by re-waiting on an ordinary condition queue.
- A resource is returned as free while it has already been assigned to a waiting process.
