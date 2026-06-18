# Message Passing And Distributed Concurrency

## When To Use Message Passing
Use message passing when execution units do not share memory, when ownership transfer is clearer than shared mutation, or when the target architecture is a multi-computer, cluster, process boundary, accelerator boundary, or distributed service boundary.

## Communication Safety
- A safe send means the receiver observes the value as it was at the send call, even if the sender later mutates its local variable.
- Blocking operations tend to preserve safety automatically, but can introduce idle waiting and deadlock.
- Non-blocking operations improve overlap between communication and computation, but the program must prove when the transmitted or received buffer is safe to read or modify.

## Synchronous Rendezvous
- In unbuffered synchronous communication, sender and receiver both wait until the matching operation is ready.
- The rendezvous point provides synchronization and can be used as a proof point for assertions about both sides.
- Blocking send/send or receive/receive pairs can deadlock when no matching operation is scheduled.

## Buffered Communication
- Buffered send places the message into a queue or internal buffer, allowing the sender to continue earlier than a rendezvous design.
- The receiver still blocks if no message is available.
- Specialized communication hardware can relax synchronization because data transfer can proceed without suspending the receiving process.
- Without dedicated support, buffer management and internal synchronization can dominate performance.

## Non-Blocking Communication
- Non-blocking send/receive returns before the transfer is complete.
- The code must retain buffer ownership until completion is proven by a check, test, wait, future, completion queue, interrupt, or callback contract.
- Good non-blocking code separates "operation submitted", "operation completed", and "buffer can be reused" states.
- Review every early return, cancellation, error path, and timeout for lost completion or double reuse.

## Guarded Commands And Server Processes
- A server process often cannot predict which client will communicate next.
- A guarded command is ready only when its Boolean condition is true and the receive operation can complete.
- Selective wait chooses one ready guarded command nondeterministically.
- Re-execute the selective wait loop to recompute readiness; readiness is determined at the start of one select execution.
- Guards should not have side effects. This allows failed or waiting guards to be evaluated without changing process state.

## CSP-Style Modeling
- CSP-style processes communicate only by messages; global shared variables are not allowed.
- Input and output must match by process name, channel/operation, arity, and type.
- A parallel command terminates only when all component processes terminate.
- Deadlock exists when a group of processes tries to communicate but no commands match and no command fails.
- This model is useful for designing protocols before implementing them in channels, actors, MPI, or RPC frameworks.

## MPI And SPMD
- MPI usually follows an SPMD model: multiple processes run the same program while rank and communicator determine behavior.
- `MPI_COMM_WORLD` contains all launched processes by default; additional communicators isolate communication contexts.
- Every message has source, destination, communicator, tag, and payload.
- Tags should represent protocol states or message categories, not incidental constants.
- Blocking MPI operations are simpler but can deadlock when sends and receives are ordered symmetrically.
- Non-blocking MPI operations can hide communication overhead but require matching `Wait`/`Test` or equivalent completion handling.

## High-Level Mechanisms
- Remote procedure calls and remote method invocation make distributed interaction look local, but failure, latency, retries, and partial execution remain distributed-system concerns.
- Rendezvous-style entry points can encode both service selection and synchronization.
- Nondeterministic service selection can improve responsiveness, but priority selection changes the fairness model.

## Design Checklist
- Name the source, destination, channel/tag/communicator, data type, buffer owner, and completion signal.
- Decide whether ordering is required.
- Decide whether lost, duplicated, delayed, or reordered messages are possible at the implementation layer.
- State what happens on peer termination, timeout, cancellation, and partial transfer.
- Write at least one deadlock scenario and explain why the protocol avoids it.
