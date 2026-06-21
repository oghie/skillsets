# Verify And Test Concurrent Realtime Work

## Use When
Before claiming a concurrent, distributed, high-performance, or real-time change is complete.

## Verification Layers
1. Static protocol review.
2. Build/type/lint checks.
3. Unit tests for deterministic state transitions.
4. Stress and schedule perturbation tests.
5. Runtime tracing or instrumentation.
6. Schedulability or timeline analysis.
7. Performance benchmark with tail metrics.

## Static Review
- Run `scripts/concurrency_static_scan.py <path>`.
- Inspect every shared mutable state.
- Inspect every wait/notify path.
- Inspect every lock/semaphore acquisition order.
- Inspect every non-blocking operation for completion.
- Inspect every periodic loop for drift.
- Inspect monitor signal semantics: AS, SC, SX, SW, or SU.
- Inspect guarded commands for side effects, deadlock, and fairness assumptions.
- Inspect diagrams or timelines for nontrivial protocols.

## Dynamic Tests
- Run with different CPU counts and affinities.
- Run with high iteration counts.
- Add randomized yielding in test builds where possible.
- Run under sanitizer/race detector support where language/runtime provides it.
- Test cancellation, timeout, and peer termination.

## Real-Time Tests
- Run `scripts/schedulability.py` for task sets when task parameters are known.
- Capture release, start, finish, and deadline miss events.
- Verify clock granularity and overflow assumptions.
- Run under background load to expose inversion and jitter.
- Test overload behavior and confirm critical task preservation.

## Distributed Tests
- Test message delay, duplication, peer crash, queue saturation, and partition.
- Verify communicator/tag/channel isolation.
- Verify in-flight operations complete or cancel during shutdown.
- Test remote call timeout and server-side shared data protection.
- Test rendezvous selection and accept queue behavior when multiple clients are ready.

## Network Dataplane Tests
- Verify RSS/queue/worker/NUMA mapping with runtime evidence.
- Capture IRQ counts, NAPI or poll-loop behavior, queue drops, ring occupancy, and NIC counters.
- Test low-load idle behavior and high-load saturation for busy polling or IRQ suspension designs.
- Test eBPF map churn, Linux TC rule insert/remove, hardware offload fallback, and rollback after partial failure.
- Test SR-IOV VF reset, PF reset, device plugin restart, link flap, and queue resize where applicable.
- For RDMA/RoCEv2, test CQ overflow, QP error, memory deregistration, congestion, and completion handling.

## Completion Report
Report:
- Properties verified.
- Commands run.
- Evidence observed.
- Assumptions still unproven.
- Residual risks tied to platform timing, scheduler, hardware, or external services.
