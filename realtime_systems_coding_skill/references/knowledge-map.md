# Knowledge Map

## Conceptual Model
- A process or task is an active software entity with state, not merely a sequence of instructions. Relevant state includes program counter, stack, heap, registers, resources, and visible shared variables.
- Concurrency expresses potential parallelism. It remains meaningful whether execution is truly parallel on multiple processors or logically parallel through interleaving on fewer processors.
- The observable behavior of a concurrent program is the set of possible interleavings of atomic actions. This is why intermittent failures can exist even when many runs appear correct.

## Abstract Concurrency Principles
- Atomicity and instruction interleaving: each atomic action executes indivisibly, but the order among processes is not predictable.
- Data consistency after concurrent access: hardware memory arbitration should prevent raw corruption, but logical results can still be nondeterministic.
- Unrepeatability: repeated executions rarely follow the same interleaving, making transient bugs hard to reproduce.
- Relative speed independence: correctness must not depend on one process being faster than another, except in explicitly designed real-time priority systems.
- Finite progress: if a process starts an action, it must not be able to halt indefinitely due to hidden state or platform behavior.

## Hardware Execution Shapes
- Multi-core: many logical processes often share fewer cores, so interleaving and preemption matter.
- Multiprocessor with shared memory: true parallelism exists, and shared memory synchronization must preserve consistency.
- Multi-computer or distributed processors: each processor has independent memory; communication requires messages over an interconnect.
- Multiprocessing models include SISD, SIMD, MISD, and MIMD. MIMD maps naturally to modern multi-threaded and multi-process software but creates contention and deadlock risks.

## Synchronization Families
- Mutual exclusion prevents more than one process from executing a critical section at the same time.
- Conditional synchronization blocks a process until a state predicate becomes true.
- Low-level options include interrupt masking, test-and-set locks, and semaphores.
- High-level options include monitors, condition variables, Java synchronized methods/blocks, and language-native channel/actor abstractions.
- Message-passing options include synchronous rendezvous, buffered communication, non-blocking operations, guarded commands, MPI point-to-point, and collective communication.

## Correctness Properties
- Safety: forbidden states are never reached. Examples include "two tasks never enter the same critical section together" and "a consumer never removes from an empty buffer."
- Liveness: desired progress eventually occurs. Examples include "a waiting process eventually enters the critical section" and "a producer eventually deposits data."
- Fairness: ready processes are treated justly. This property is stronger than liveness and often depends on scheduler or hardware policy.
- Real-time systems intentionally violate general fairness when priorities encode criticality or timing requirements.

## Real-Time System Shape
- Time is an explicit correctness dimension. Required facts include clock granularity, overflow behavior, timers, delays, timeouts, task periods, WCET, deadlines, jitter, response time, and blocking time.
- A simple periodic task model assumes fixed tasks, known periods, known WCET, deadline equal to period, no resource blocking, and ignored overheads.
- General models add shorter deadlines, shared resources, sporadic tasks, aperiodic tasks, and blocking due to synchronization or communication.

## Visual Mental Models
- Interleaving diagrams show why two locally correct instruction sequences can produce multiple global outcomes.
- Producer-consumer buffer diagrams separate mutual exclusion from empty/full conditional synchronization.
- Monitor queue diagrams separate input queue, condition queues, and urgent signaler queues.
- Message-passing timeline diagrams distinguish rendezvous waiting, buffered copy, and non-blocking unsafe-buffer intervals.
- Gantt charts expose task release, preemption, response time, deadline misses, and priority inversion.
