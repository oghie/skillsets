# Level 2: Infrastructure Virtualization

## Scope
Use this level for VM and IaaS deployments where the application runs inside a guest OS and shares physical hosts through a hypervisor.

## Typical Technologies
- Cloud VMs and private virtualization.
- Virtual NICs, virtual disks, vCPU scheduling, paravirtual drivers.
- Guest Linux/Windows real-time tuning where available.

## Concurrency Model
- Application threads are scheduled by the guest OS, then vCPUs are scheduled by the hypervisor.
- Apparent CPU availability can differ from physical CPU availability.
- Virtual devices add queues and host-side scheduling to I/O paths.

## Real-Time Considerations
- Hypervisor scheduling can introduce jitter.
- Clocksource behavior, time synchronization, pause/resume, live migration, and host contention affect timing.
- Hard real-time guarantees are difficult unless the provider/environment offers explicit isolation and the deployment verifies it.

## Coding Guidance
- Prefer monotonic clocks and record clocksource in diagnostics.
- Avoid assuming that vCPU count equals dedicated physical cores.
- Use CPU pinning, reserved capacity, or dedicated hosts only when validated by measurement.
- Treat network and disk latency as variable and include p95/p99 in budgets.

## Verification
- Run latency benchmarks under host and guest load.
- Capture scheduler latency, steal time, clock drift, and network jitter.
- Test VM restart, migration if applicable, and virtual device reset.
- Compare bare-metal and VM traces before accepting tight deadlines.

## When Not To Use
- Do not use general-purpose VMs for hard real-time control loops without measured and contract-backed isolation.
- Do not trust average latency for deadline claims; use tail latency and miss counts.
