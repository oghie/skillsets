# Level 4: Spatial Distribution And Edge

## Scope
Use this level when geography, proximity to users/devices, intermittent connectivity, or data locality is a first-class part of the design.

## Typical Technologies
- Cloudflare Workers and isolate-style runtimes.
- AWS Greengrass.
- V8 isolates.
- WasmEdge and other WebAssembly runtimes.
- KubeEdge, OpenYurt, EdgeX Foundry, and K3s.

## Concurrency Model
- Work is distributed across locations, devices, regions, isolates, or lightweight runtimes.
- Local execution may be fast, but global coordination is constrained by network latency and partial failure.
- State can be local, replicated, cached, eventually consistent, or coordinated through a central service.

## Real-Time Considerations
- Edge placement can reduce user/device latency but cannot eliminate network variability.
- Local control loops should remain local when missed deadlines affect safety.
- Remote updates and configuration propagation must be treated as asynchronous events.
- Runtime limits in isolates or Wasm environments can constrain CPU time, memory, sockets, filesystem, and timers.

## Coding Guidance
- Put latency-sensitive reads and device reactions near the edge.
- Put global invariants, durable audit, and complex coordination in a level that can enforce them.
- Design for offline mode, replay, idempotency, and conflict resolution.
- Keep message schemas versioned and backward compatible.
- Separate local safety decisions from eventual cloud synchronization.

## Verification
- Test cold start, isolate startup, Wasm module load, regional failover, offline operation, and reconnection.
- Measure local latency and end-to-end replicated latency separately.
- Simulate network partitions, stale configuration, duplicate messages, and delayed updates.
- Validate resource limits for the exact edge runtime.

## When Not To Use
- Do not use edge distribution as a substitute for local hard real-time control.
- Do not store global mutable state at the edge without a conflict and ownership model.
