# Level 3: Dynamic Orchestration

## Scope
Use this level for containerized services, Kubernetes workloads, cloud-native systems, and dynamically scheduled application components.

## Typical Technologies
- Containers, cgroups, namespaces, OCI runtimes.
- Kubernetes, service meshes, sidecars, autoscalers, probes, and controllers.
- Brokered messaging, queues, streaming systems, and distributed service runtimes.
- SR-IOV device plugins, CNI dataplanes, eBPF CNIs, DPDK pods, and hugepage-backed workloads when packet processing is part of the service.

## Concurrency Model
- Threads run inside a process constrained by cgroups and orchestrator policy.
- Pods/containers can be rescheduled, restarted, throttled, or evicted.
- Network communication becomes part of the synchronization and liveness model.
- Hardware devices exposed to pods add placement constraints that the scheduler must satisfy explicitly.

## Real-Time Considerations
- CPU quotas, throttling, garbage collection, sidecars, network overlays, and noisy neighbors can add jitter.
- Suitable for soft real-time and high-throughput services when deadlines tolerate platform variance.
- Hard real-time paths should usually stay at lower levels and communicate with cloud-native services asynchronously.

## Coding Guidance
- Define backpressure, retry, timeout, and cancellation behavior for every remote call.
- Treat queue depth and consumer lag as scheduling signals.
- Configure CPU/memory requests and limits intentionally.
- For dataplane pods, configure CPU isolation, hugepages, device resources, NUMA hints, and queue ownership intentionally.
- Avoid lock-based coordination across services; use explicit messages, leases, or transactional boundaries.
- Make shutdown hooks release work leases and unblock waiters.

## Verification
- Test cgroup throttling, pod restart, rolling update, network partition, DNS delay, and broker backlog.
- Capture p99 latency, error budget burn, queue lag, and deadline misses.
- Validate readiness/liveness probes do not create cascading restarts.
- Run load tests with autoscaling and with autoscaling disabled.
- For SR-IOV/DPDK/eBPF dataplanes, test pod restart, node drain, device plugin restart, VF reset, CNI policy updates, and map/rule cleanup.

## When Not To Use
- Do not put tight device-control loops behind orchestrator scheduling.
- Do not confuse horizontal scaling with correctness; distributed state still needs invariants.
