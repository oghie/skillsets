---
name: realtime-systems-coding
description: Use when designing, implementing, reviewing, debugging, testing, profiling, or porting concurrent, parallel, distributed, high-performance, network dataplane, kernel-bypass, or real-time software, including locks, semaphores, monitors, MPI, CSP rendezvous, DPDK, VPP, eBPF, XDP, AF_XDP, SR-IOV, RSS, RoCEv2/RDMA, RMS/EDF, priority inversion, and environment selection from silicon to edge.
version: 0.1.0
author: oghie
license: MIT
metadata:
  hermes:
    tags: ['software-development', 'realtime', 'concurrency', 'systems']
    source: https://github.com/oghie/skillsets
---

# Realtime Systems Coding

## Core Rule
Treat every task as a state, timing, and synchronization contract. Identify the execution units, shared state, communication mode, timing limits, platform abstraction level, and correctness properties before writing or changing code.

## Knowledge Grounding
- Use `references/knowledge-map.md` for the conceptual map.
- Use `references/shared-memory-synchronization.md` for locks, semaphores, monitors, condition variables, and Java/POSIX patterns.
- Use `references/mutual-exclusion-algorithms.md` for Dijkstra conditions, refinement flow, Dekker, Peterson, N-process filters, busy waiting, and custom mutual exclusion proof.
- Use `references/monitor-signalling-semantics.md` for AS, SC, SX, SW, SU, signal stealing, urgent queues, nested monitor calls, and monitor verification rules.
- Use `references/exercise-derived-patterns.md` for canonical synchronization pseudocode: monitor semaphores, rendezvous, encoded-count buffers, readers-writers, bridge traffic, dining philosophers, priority allocation, FIFO/SJF queues, controller wakeups, and service pipelines.
- Use `references/message-passing-distributed.md` for rendezvous, buffered/non-blocking communication, MPI, and SPMD systems.
- Use `references/distributed-programming-models.md` for CSP guarded commands, alternative/repetitive orders, lack of fairness, RPC/RMI, remote invocation, and rendezvous entry points.
- Use `references/realtime-scheduling-analysis.md` for clocks, timers, drift, task attributes, RMS, EDF, blocking, priority inversion, and aperiodic servers.
- Use `references/network-dataplane-and-kernel-bypass.md` for DPDK, VPP, eBPF, XDP, AF_XDP, Linux TC, RSS, NAPI, IRQ suspension, SR-IOV, RoCEv2/RDMA, SmartNIC/DPU offload, TCP handoff, and IOAM-style telemetry.
- Use `references/flow-and-diagram-patterns.md` when a diagram, timeline, proof flow, monitor queue model, message-passing sequence, or Gantt-style task model would make the work safer.
- Use `references/development-environments/abstraction-level-map.md` before choosing ASIC/FPGA, accelerator/offload, bare-metal, VM, container, or edge targets.

## First Pass
1. Classify the work: concurrency bug, shared-memory design, message passing design, network dataplane design, real-time scheduling, performance tuning, environment selection, or code review.
2. Identify execution units: process, thread, task, ISR, server, actor, MPI rank, kernel thread, accelerator kernel, VM, container, isolate, or edge worker.
3. Identify interaction mode: shared memory, lock/semaphore/monitor, condition queue, synchronous rendezvous, buffered channel, non-blocking message, RPC/RMI, hardware offload queue, NIC RX/TX queue, or completion queue.
4. State correctness properties: safety, liveness, fairness, absence of deadlock/starvation, data consistency, bounded blocking, and deadline satisfaction.
5. Define verification evidence: invariant, interleaving argument, Gantt/timeline, schedulability test, stress test, trace, benchmark, or platform measurement.

## Required Reads By Task
- Intake, modeling, or ambiguous requirements: `tasks/intake-and-modeling.md`.
- Shared-memory synchronization: `tasks/design-shared-memory-concurrency.md`, plus `tasks/apply-exercise-patterns.md` for canonical monitor/semaphore pseudocode, `references/mutual-exclusion-algorithms.md` for custom protocols, and `references/monitor-signalling-semantics.md` for monitor/condition signalling.
- Message passing, MPI, distributed server processes, CSP, RPC/RMI, or rendezvous: `tasks/design-message-passing-system.md` and `references/distributed-programming-models.md`.
- Network dataplane, kernel bypass, packet steering, RDMA, SR-IOV, eBPF/XDP/Linux TC, DPDK, VPP, SmartNIC/DPU, or TCP handoff: `tasks/design-network-dataplane-system.md`.
- Periodic, sporadic, aperiodic, deadline, or priority work: `tasks/design-realtime-scheduler.md`.
- High-performance implementation: `tasks/implement-high-performance-pattern.md`.
- Race, deadlock, starvation, drift, missed deadline, or intermittent failures: `tasks/diagnose-concurrency-bug.md`.
- Correctness argument, invariants, non-interference, monitor proof, or property review: `tasks/derive-correctness-proof.md`.
- Diagram, timeline, state machine, queue model, or Gantt-style explanation: `tasks/model-with-diagrams.md`.
- Final validation and review: `tasks/verify-and-test-concurrent-realtime.md` and `references/review-checklist.md`.

## Design Heuristics
- Do not assume process speed, scheduling order, or interleaving unless the platform contract explicitly guarantees it.
- Minimize excluded interleavings: lock only the shared state that needs atomicity, and keep critical sections bounded.
- Prefer blocking primitives over busy waiting unless latency constraints, hardware context, or a measured spin duration justify spinning.
- Use hierarchical lock/semaphore ordering for nested resources; document the order and release in reverse order.
- For monitors, associate each logical wait condition with the narrowest available condition variable and signal only when the condition is true.
- For monitor signalling, name the assumed semantics. SC, SX, SW, and SU have different post-signal obligations.
- For canonical synchronization problems, start from invariant-driven patterns before inventing new wait/signal code.
- For message passing, choose blocking for safety and simplicity; choose non-blocking only with explicit completion checks before mutating buffers.
- For network dataplanes, define queue-to-core mapping, buffer ownership, rule lifecycle, completion signal, rollback, and reset behavior before tuning throughput.
- For guarded alternatives, never depend on nondeterministic choice being random or fair unless the runtime contract proves it.
- For real-time work, distinguish sufficient tests from exact evidence; utilization alone is not proof when blocking, sporadic jobs, or resource sharing exists.

## Script Helpers
- Run `scripts/schedulability.py --help` to compute RMS/EDF utilization checks and simulate preemptive schedules over a bounded horizon.
- Run `scripts/concurrency_static_scan.py <path>` for heuristic checks around locks, semaphores, waits, notifications, MPI, sleeps, and drift risks.
- Run `scripts/tooling_probe.sh` to inspect local tooling for C/C++, POSIX, MPI, RT Linux, containers, FPGA, and edge/Wasm targets.

## Verification Gate
- For shared memory, name the protected data, synchronization object, acquisition order, blocking behavior, and invariant.
- For monitors, name AS/SC/SX/SW/SU semantics, condition predicates, signal placement, and any nested monitor call policy.
- For message passing, name sender, receiver, channel/tag/communicator, buffering mode, completion rule, and deadlock scenario considered.
- For network dataplanes, name hook placement, RSS/NAPI/queue mapping, IRQ strategy, NUMA placement, buffer ownership, hardware/software rule lifecycle, and reset handling.
- For real-time tasks, name Ci, Ti, Di, priority, phase, blocking Bi, clock granularity, timeout policy, and drift-control method.
- Validate with code inspection plus at least one dynamic strategy: stress interleavings, sanitizer, deterministic scheduler, timeline simulation, trace, or runtime deadline monitor.
- Do not claim correctness from a passing run alone; tie the claim to a property and evidence.

## Output Standard
Lead with the chosen concurrency or real-time model. State assumptions, task/resource map, synchronization or communication protocol, schedulability/performance evidence, commands run, and residual platform risks.
