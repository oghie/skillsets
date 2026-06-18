# Level 0: Delegated Execution And Hardware Offload

## Scope
Use this level when a CPU delegates work to domain-specific or near-device hardware while software remains responsible for orchestration, buffer ownership, and completion.

## Typical Technologies
- DPU and SmartNIC datapaths.
- GPU kernels and streams.
- TPU or other ML accelerators.
- QPU jobs with host orchestration.
- DMA engines, accelerator queues, and device-side runtimes.

## Concurrency Model
- Host code submits work asynchronously.
- Device queues, streams, command buffers, or doorbells become the synchronization boundary.
- Buffers may be copied, mapped, pinned, shared coherently, or owned exclusively by the device until completion.

## Real-Time Considerations
- Offload is useful only if transfer latency, queueing delay, and completion handling fit the deadline.
- Device scheduling may be opaque; measure queue delay and tail latency.
- If a hard real-time loop depends on offload, define the fallback when the device is busy, reset, or throttled.

## Coding Guidance
- Make buffer lifetime explicit: host-owned, in-flight, device-owned, completed, reusable.
- Do not mutate input or output buffers until completion is proven.
- Separate submission, synchronization, completion, and error recovery paths.
- Batch only when batching delay is acceptable.
- Keep host/device clock assumptions explicit; timestamps from different domains may not be directly comparable.

## Verification
- Test early completion, late completion, timeout, cancellation, device reset, and partial failure.
- Benchmark copy time, enqueue time, execution time, completion latency, and p99 tail.
- Verify memory visibility and cache coherency rules for the platform.
- Stress with multiple outstanding operations and queue saturation.

## When Not To Use
- Do not offload small tasks where transfer and synchronization dominate.
- Do not offload if the completion contract cannot be made explicit in code review.
