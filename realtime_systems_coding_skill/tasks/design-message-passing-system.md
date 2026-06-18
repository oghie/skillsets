# Design Message-Passing Systems

## Use When
The task involves channels, actors, MPI, distributed processes, RPC/RMI-like calls, worker queues, offload queues, or any process boundary without shared memory.

## Workflow
1. Name each process/rank/worker and its role.
2. Define the protocol state machine.
3. Name every message: source, destination, channel/tag/communicator, payload type, ordering requirement, and idempotency rule.
4. Choose communication mode:
   - Synchronous rendezvous for simple safety and explicit coordination.
   - Buffered communication to decouple sender and receiver.
   - Non-blocking communication to overlap communication with independent computation.
5. Define the completion rule and buffer ownership.
6. Write deadlock and termination scenarios.
7. Add timeout, cancellation, and peer-failure behavior.

## Synchronous Design
- Ensure every blocking send has a matching receive in all legal states.
- Avoid symmetric send-before-receive patterns unless buffering semantics prove safety.
- Use rendezvous points as proof points for shared protocol assertions.

## Buffered Design
- Bound queues or define backpressure.
- Decide whether send completion means "copied to buffer" or "received by peer".
- Account for buffer memory, queue saturation, and retry behavior.

## Non-Blocking Design
- Separate submit, in-flight, completed, failed, and cancelled states.
- Do not reuse buffers before `Wait`, `Test`, callback, completion queue, or equivalent confirms completion.
- Ensure all in-flight operations are joined or cancelled before scope/lifetime ends.

## Guarded Server Pattern
- Use guarded selection when a server accepts requests from multiple clients and cannot predict the arrival order.
- Guards must be side-effect free.
- Recompute guard readiness each loop iteration.
- Add a termination message or condition so server processes do not wait forever after clients stop.

## MPI Notes
- Use communicators to isolate protocol contexts.
- Use tags to distinguish message categories.
- Check return codes.
- Pair non-blocking `Isend`/`Irecv` with `Wait`/`Test`.
- Consider collective operations when all ranks participate in the same phase.

## Verification Checklist
- Can all peers block waiting for receives or sends?
- Can a buffer be modified while still in transmission?
- Can a message be received in the wrong protocol state?
- Can a server wait forever after all clients terminate?
- Can cancellation leak an in-flight operation?
