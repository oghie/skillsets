# Design Network Dataplane System

## Use When
The task involves DPDK, VPP, eBPF, XDP, AF_XDP, Linux TC, RSS, NAPI, IRQ suspension, SR-IOV, SmartNIC/DPU, RoCEv2, RDMA, packet steering, kernel-bypass networking, TCP connection handoff, or in-band dataplane telemetry.

## Workflow
1. Read `references/network-dataplane-and-kernel-bypass.md`.
2. State the target metric: throughput, p50/p99 latency, jitter, packet loss, CPU budget, or deadline.
3. Choose the datapath: kernel sockets, XDP/eBPF, Linux TC, AF_XDP, DPDK, VPP, SR-IOV VF, RDMA/RoCEv2, SmartNIC/DPU, or hybrid.
4. Draw the packet path and identify every ownership boundary: NIC queue, descriptor ring, skb, UMEM, mbuf, RDMA memory region, socket buffer, or hardware rule.
5. Define queue topology: RX/TX queue count, RSS fields, indirection table, worker mapping, IRQ affinity, NAPI IDs, and NUMA placement.
6. Define completion and rollback:
   - Packet buffer reusable after which ring/CQ/completion?
   - Flow rule active after which kernel/device acknowledgment?
   - Connection handoff complete after which owner-ready and redirect-ready states?
   - Reset path clears which software and hardware state?
7. Identify correctness hazards: packet reordering, stale redirect rule, dropped completion, CQ overflow, VF reset, map eviction, queue resize, flow migration race, or fabric congestion.
8. Add observability: NIC counters, queue drops, IRQ counts, perf/ftrace/bpftool/ethtool/tc/rdma evidence, and tail latency histograms.
9. Verify with stress under realistic traffic mix, low-load idle behavior, high-load saturation, device reset, and rule churn.

## Selection Hints
| Situation | Starting Point |
| --- | --- |
| Ordinary TCP correctness dominates | Kernel socket path. |
| Early drop or redirect | XDP/eBPF. |
| Policy after skb metadata exists | Linux TC eBPF. |
| User-space packet processing with kernel integration | AF_XDP. |
| Dedicated line-rate packet processing | DPDK or VPP. |
| VM/container direct NIC access | SR-IOV with explicit VF lifecycle. |
| Zero-copy remote memory semantics | RoCEv2/RDMA. |
| Hardware-assisted flow steering | Linux TC hardware offload, SmartNIC, or DPU. |
| Per-packet telemetry in a limited domain | IOAM direct export style pipeline. |

## Output Shape
Return:
- Chosen datapath and rejected alternatives.
- Packet-path diagram.
- Queue/core/NUMA map.
- Buffer and rule ownership model.
- Completion, rollback, and reset behavior.
- Benchmark and tracing plan.
- Residual risks.

## Red Flags
- "Kernel bypass" is selected before queue/core/NUMA ownership is known.
- RSS is enabled but worker affinity is unspecified.
- A buffer is reused before a completion ring, CQ, or TX completion proves ownership returned.
- eBPF map updates are treated as atomic protocol migration without state versioning.
- Hardware rule install is assumed synchronous when it is not proven.
- SR-IOV is used without VF reset and observability plans.
- RoCEv2 is selected without congestion/loss discipline and CQ overflow handling.
- TCP handoff does not freeze or account for in-flight packets and queued bytes.
