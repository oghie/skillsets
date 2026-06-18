# Design Shared-Memory Concurrency

## Use When
The task involves threads/processes sharing memory, critical sections, locks, semaphores, monitors, condition variables, or Java synchronized blocks.

## Workflow
1. Draw the shared state boundary.
2. Decide whether the problem is mutual exclusion, conditional synchronization, or both.
3. Choose a primitive:
   - Mutex/lock for critical sections.
   - Semaphore for resource counts or low-level synchronization.
   - Monitor/condition variable for stateful resource abstractions.
   - Atomic variable only for narrow lock-free state with a clear memory-order contract.
4. Define acquisition and release order.
5. Write the invariant and forbidden state.
6. For monitors, name the signal semantics: AS, SC, SX, SW, or SU.
7. For custom mutual exclusion, prove the Dijkstra-style conditions or use `references/mutual-exclusion-algorithms.md`.
8. Add cancellation, timeout, and error-path release rules.
9. Verify with static review plus stress or sanitizer/model checking when available.

## Mutex Pattern
- One mutex protects one coherent group of shared state.
- Avoid long critical sections.
- Avoid blocking calls while holding the mutex unless bounded and necessary.
- Keep lock order global and documented.

## Semaphore Pattern
- Initialize semaphores to match the invariant.
- Use binary semaphores for mutual exclusion, general semaphores for counts or producer/consumer state.
- Avoid relying on FIFO wake ordering unless guaranteed.
- Avoid nested semaphores unless the acquisition hierarchy is explicit.

## Monitor Pattern
- Put permanent shared variables inside the monitor abstraction.
- Use one condition per logical waiting condition when possible.
- Check condition before waiting and after wake.
- Signal only after making the condition true.
- Be explicit about signal semantics: SC requires rechecking; SX requires signal-and-exit discipline; SU uses an urgent signaller queue.
- Read `references/monitor-signalling-semantics.md` before designing or changing monitor signalling behavior.
- For nontrivial monitors, draw a queue diagram using `tasks/model-with-diagrams.md`.

## Java Pattern
- Prefer `synchronized` or `java.util.concurrent` primitives over ad hoc volatile flags.
- Use `while` around `wait`.
- Use `notifyAll` when multiple conditions share an implicit queue and the correct waiter cannot be selected.
- Avoid `Thread.stop`, `suspend`, and `resume`.

## Verification Checklist
- Can two processes enter the critical section together?
- Can all processes be waiting forever?
- Can one process be overtaken forever?
- Can a signal be lost?
- Can a signal be stolen?
- Does the monitor invariant hold before every wait and procedure exit?
- Does signal placement match AS/SC/SX/SW/SU semantics?
- Can nested monitor calls block progress?
- Can a timeout path leave the state locked?
- Can an invariant be false between protected operations?
