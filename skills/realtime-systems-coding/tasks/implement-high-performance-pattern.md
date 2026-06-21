# Implement High-Performance Pattern

## Use When
The task asks for performance, throughput, low latency, offload, lock reduction, MPI optimization, or real-time efficiency.

## Workflow
1. Define the metric: throughput, latency, jitter, p99, deadline misses, CPU use, memory bandwidth, or energy.
2. Choose the abstraction level using `references/development-environments/abstraction-level-map.md`.
3. Establish a simple baseline before optimizing.
4. Identify the bottleneck: lock contention, memory locality, scheduler delay, communication, serialization, I/O, device transfer, or queueing.
5. Change one dimension at a time.
6. Verify correctness properties after each performance change.
7. Report before/after metrics with environment details.

## Shared Memory Patterns
- Shard state to reduce contention.
- Prefer per-thread/per-rank local accumulation with a merge phase when exact real-time visibility is not required.
- Use bounded queues for producer-consumer pipelines.
- Avoid global semaphores for unrelated resources.
- Keep allocation and logging out of hot locks.

## Message Passing Patterns
- Overlap non-blocking communication with independent work.
- Use communicators/tags to keep protocol phases isolated.
- Batch only when latency budget permits.
- Avoid all-to-all communication unless the algorithm requires it.
- Use collective operations for collective phases.

## Real-Time Patterns
- Prefer static allocation and bounded loops in hard-deadline paths.
- Precompute schedules or lookup tables when feasible.
- Use priority protocols for shared resources.
- Keep high-priority work short and delegate noncritical work.
- Record timing in production when deadlines matter.

## Offload Patterns
- Measure host-device transfer cost before offloading.
- Keep buffer ownership explicit.
- Use streams/queues to overlap transfer and execution where supported.
- Add fallback and reset handling.
- Include device queue delay in latency budget.

## Network Dataplane Patterns
- For DPDK, VPP, eBPF, XDP, AF_XDP, Linux TC, SR-IOV, RoCEv2/RDMA, or SmartNIC/DPU work, use `tasks/design-network-dataplane-system.md`.
- Define RSS, queue, NAPI, IRQ, worker, and NUMA placement before comparing throughput.
- Treat map updates, hardware rules, queue pairs, completion queues, and packet buffers as shared state with explicit ownership.
- Measure low-load CPU burn and high-load p99 latency; both matter for busy polling and kernel bypass.

## Verification
- Run the static scanner.
- Run unit tests and stress tests.
- Run benchmarks with tail metrics.
- For real-time code, run schedulability checks and runtime traces.
- For distributed code, test overload, partition, cancellation, and timeout behavior.
