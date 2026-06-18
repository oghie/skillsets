# Performance Engineering

## Performance Questions First
- What is the throughput, latency, jitter, or deadline objective?
- What is the execution level: silicon/FPGA, accelerator, bare-metal, VM, container, or edge?
- What is the shared bottleneck: CPU, memory bus, cache, lock, scheduler, network, storage, PCIe, accelerator queue, or clock/timer resolution?
- What correctness property must not be traded away?

## Concurrency Efficiency
- Avoid excluding unrelated interleavings. Use separate locks or queues for independent state.
- Prefer blocking waits when wait time is unbounded or CPU resources are scarce.
- Use spinning only when the expected wait is shorter than the cost of blocking and the core budget allows it.
- Avoid long critical sections. Move allocation, I/O, logging, serialization, compression, and remote calls outside locks unless they are part of the protected invariant.
- Measure contention, not only total runtime.

## Real-Time Efficiency
- Use monotonic clocks for intervals.
- Avoid relative-delay loops for periodic tasks; schedule against absolute next releases.
- Keep ISR or high-priority sections bounded and delegate long work to lower-priority contexts.
- Include blocking time and scheduler overhead in the budget before declaring spare capacity.
- Prefer static priority when overload predictability and criticality ordering matter.

## Message Passing Efficiency
- Batch messages only when batching delay is acceptable.
- Use non-blocking operations to overlap communication with independent computation, then wait/test before buffer reuse.
- Keep protocol tags, ranks, and communicators explicit enough to avoid accidental cross-talk.
- Avoid symmetric blocking send patterns without a proven matching receive order.
- Use topology-aware placement and communicator grouping when communication is not all-to-all.

## Hardware And Runtime Placement
- Offload work when transfer overhead, synchronization overhead, and error handling are lower than CPU execution cost.
- Keep control loops near the timing source and actuator when jitter matters.
- Use VM/container isolation only after quantifying scheduler jitter and resource contention.
- For edge systems, treat network delay and regional placement as part of the timing model.

## Benchmark Discipline
- Pin versions, compiler flags, CPU governor, container limits, VM type, accelerator model, and clock source.
- Warm up runtimes that JIT or lazily initialize.
- Capture min, p50, p95, p99, max, deadline miss count, and jitter.
- Compare against a sequential or simpler baseline.
- Re-run with stress on unrelated resources to reveal hidden coupling.
