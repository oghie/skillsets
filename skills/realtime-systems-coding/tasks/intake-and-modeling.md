# Intake And Modeling Workflow

## Use When
The request is ambiguous, the codebase is unfamiliar, or the concurrency/real-time model has not been made explicit.

## Steps
1. Identify the platform abstraction level using `references/development-environments/abstraction-level-map.md`.
2. List execution units: threads, tasks, processes, ranks, ISRs, callbacks, server processes, workers, accelerator kernels, or edge instances.
3. List shared resources: variables, buffers, files, devices, message queues, semaphores, locks, monitors, channels, communicators, clocks, and timers.
4. Classify interactions as mutual exclusion, conditional synchronization, message passing, offload submission, or scheduling.
5. Define the property goal: safety, liveness, fairness, bounded blocking, drift control, or deadline satisfaction.

## Required Facts
- Language, runtime, OS/kernel/RTOS, compiler, and deployment target.
- Scheduler policy if known.
- Clock source and timer resolution if time matters.
- `Ci`, `Ti`, `Di`, phase, jitter, and blocking estimates for real-time tasks.
- Communication mode and buffer ownership for message passing.

## Output
Produce a small model before implementation:
- Execution unit table.
- Shared resource table.
- Synchronization or communication protocol.
- Timing assumptions.
- Verification plan.

## Stop Conditions
Do not implement yet if:
- A hard deadline exists but no clock/timer/scheduler facts are available.
- Shared resource ownership cannot be identified.
- Non-blocking or offload buffers have no completion rule.
- A proposed fix depends on process speed or lucky scheduling.
