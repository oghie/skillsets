# Level -1: Silicon And Physical Circuits

## Scope
Use this level for ASIC and FPGA implementations where concurrency is physical, structural, or cycle-level rather than scheduled by an operating system.

## Typical Technologies
- ASIC datapaths and control logic.
- FPGA fabric, soft cores, custom accelerators, hardware state machines, streaming pipelines.
- HDL/HLS flows, simulation, synthesis, place-and-route, timing closure, and hardware-in-loop testing.

## Concurrency Model
- Parallelism is spatial: independent logic can operate in the same clock cycle.
- Atomicity is defined by clocked state transitions, handshake protocols, memory-port arbitration, and bus transactions.
- Synchronization is implemented with valid/ready handshakes, FIFOs, arbiters, clock-domain crossing logic, and reset sequencing.

## Real-Time Considerations
- Timing is bounded by clocks, pipeline depth, resource conflicts, memory latency, and I/O protocol timing.
- The main deadline proof is not an OS scheduler proof; it is timing closure plus protocol-level latency analysis.
- Clock-domain crossings and asynchronous resets require explicit design and verification.

## Coding Guidance
- Write a finite-state protocol before writing HDL/HLS.
- Separate datapath, control path, register interface, reset, and clock-domain crossing logic.
- Avoid implicit shared state across modules; define ownership and handshake semantics.
- Use bounded FIFOs and backpressure rather than unbounded queues.
- Treat metastability and bus arbitration as correctness risks, not only performance risks.

## Verification
- Run unit simulation for each module.
- Run integration simulation for handshake, backpressure, reset, and overflow/underflow.
- Add assertions for "never both writers", "eventually response after request" where bounded liveness can be expressed.
- Verify timing closure for target clock.
- Validate on hardware with instrumentation or logic analyzer when available.

## When Not To Use
- Do not move logic to Level -1 when ordinary CPU scheduling meets deadlines.
- Do not use FPGA/ASIC for convenience parallelism if the team cannot maintain simulation, synthesis, and hardware debug workflows.
