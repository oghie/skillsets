# Level 1: Direct Hardware Access

## Scope
Use this level for bare-metal firmware, RTOS applications, direct device control, or Linux paths with strong real-time constraints and direct hardware interaction.

## Typical Technologies
- Bare-metal C/C++ or Rust.
- RTOS tasks, ISRs, timers, semaphores, queues, and priority scheduling.
- Direct MMIO, DMA, UART/SPI/I2C/CAN/Ethernet, GPIO, PWM, ADC, and interrupt controllers.
- Linux PREEMPT_RT or tuned real-time Linux paths when applicable.
- Linux network fast paths such as NAPI, RSS, XDP/eBPF, AF_XDP, Linux TC, IRQ suspension, DPDK, or VPP when direct queue ownership matters.

## Concurrency Model
- Interrupt handlers, task priorities, timers, and device callbacks define execution order.
- Shared state exists across ISR and task context; lock choice depends on whether code can sleep.
- Atomic sections must be bounded because they delay interrupts and timing-critical work.
- Network queues, NAPI poll loops, poll-mode drivers, and completion rings can become the scheduling boundary.

## Real-Time Considerations
- Use monotonic hardware timers for intervals.
- Avoid accumulated drift by scheduling against absolute next-release time.
- Bound ISR duration and defer long work to lower-priority context.
- Include interrupt latency, critical-section duration, DMA completion, and bus contention in timing budgets.

## Coding Guidance
- Name each context: ISR, high-priority task, low-priority task, DMA callback, timer callback.
- Keep shared data ownership obvious and small.
- Use priority inheritance or ceiling protocols where available for resources shared across task priorities.
- Avoid dynamic allocation and unbounded loops in hard real-time paths unless bounded by design.
- Avoid logging or blocking I/O under high-priority locks.
- For network dataplanes, pin workers to queues, document RSS/NAPI mapping, and keep packet buffer ownership explicit.
- For DPDK/VPP, treat hugepages, NUMA locality, mbuf/mempool lifetime, and poll-mode core budget as part of the design.

## Verification
- Measure ISR latency, task response time, lock hold time, timer drift, and missed deadlines.
- Use hardware traces, logic analyzer, GPIO toggles, RTOS trace, ftrace, or perf where appropriate.
- Test worst-case input burst, device timeout, lost interrupt, and reset recovery.
- Re-run with lower-priority load to reveal priority inversion.
- For network paths, measure IRQ counts, queue drops, RX/TX ring occupancy, p99 latency, and behavior under queue resize or link flap.

## When Not To Use
- Do not choose bare-metal only for speed if a hosted runtime can meet deadlines and maintainability matters more.
- Do not bypass OS primitives when scheduler integration is required for bounded blocking.
