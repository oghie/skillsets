# Development Environment Abstraction Levels

## Purpose
Use this map before choosing the implementation target for concurrent or real-time code. The same algorithm can have very different correctness and performance risks depending on whether it runs in circuits, accelerators, bare-metal firmware, virtual machines, containers, or edge runtimes.

## Level Summary
| Level | Name | Typical Targets | Main Risk |
| --- | --- | --- | --- |
| -1 | Silicon and physical circuits | ASIC, FPGA | Hardware timing, synthesis, signal integrity, verification cost |
| 0 | Delegated execution and offload | DPU, SmartNIC, GPU, TPU, QPU | Transfer latency, queue completion, memory ownership |
| 1 | Direct hardware access | Bare-metal, RTOS, MCU, direct Linux RT paths | Interrupt latency, timer precision, bounded blocking |
| 2 | Infrastructure virtualization | VM, IaaS, virtual NIC/storage | Hypervisor jitter, noisy neighbors, clock drift |
| 3 | Dynamic orchestration | Containers, Kubernetes, cloud-native runtimes | cgroups, scheduling interference, network variability |
| 4 | Spatial distribution and edge | Workers, Greengrass, V8 isolates, WasmEdge, KubeEdge, OpenYurt, EdgeX Foundry, K3s | Geographic latency, consistency, runtime limits |

## Selection Rules
- If nanosecond-level determinism or custom datapath parallelism dominates, evaluate Level -1 or Level 0.
- If interrupt response, direct timer control, or device access dominates, evaluate Level 1.
- If operational isolation matters more than tight deadlines, evaluate Level 2 or Level 3.
- If user/device proximity, network locality, or data sovereignty dominates, evaluate Level 4.
- If hard real-time guarantees are required, every level above bare metal must prove its scheduling and timing contract rather than assume it.

## Cross-Level Questions
- Where is the authoritative clock?
- Where can a task be preempted?
- What is the smallest atomic action at this level?
- What memory is shared, copied, pinned, mapped, or transferred?
- What is the completion signal for asynchronous work?
- What scheduling fairness or priority policy is actually enforced?
- What failure mode releases resources and unblocks waiters?

## Verification By Level
- Level -1: simulation, formal/property checks, timing closure, hardware-in-loop.
- Level 0: queue completion tests, transfer benchmarks, memory coherence checks, device reset/error recovery.
- Level 1: ISR latency, timer drift, WCET, lock hold time, deadline trace.
- Level 2: vCPU pinning evidence, clocksource checks, host load tests, network jitter.
- Level 3: cgroup quota tests, pod disruption tests, service latency histograms, autoscaling behavior.
- Level 4: regional latency, isolate/Wasm runtime limits, offline behavior, eventual consistency, remote update safety.
