# Flow And Diagram Patterns

## Purpose
Use this file to turn a concurrency or real-time design into explicit process diagrams before coding or review. The diagrams are intentionally small so they can be copied into design notes, ADRs, code comments, or test plans.

## Process State Model

```mermaid
flowchart LR
  New[created/new] --> Ready[runnable/ready]
  Ready --> Running[running]
  Running --> Ready
  Running --> Blocked[blocked/waiting]
  Blocked --> Ready
  Running --> Done[terminated]
```

Use for:
- Threads and tasks.
- Java thread lifecycle reviews.
- Debugging hangs where a task is runnable versus blocked.

## Instruction Interleaving

```mermaid
sequenceDiagram
  participant P1
  participant M as Shared memory
  participant P2
  P1->>M: load x
  P2->>M: load x
  P1->>M: store x + 1
  P2->>M: store x - 1
  Note over M: final value depends on interleaving
```

Use for:
- Showing why a read-modify-write sequence is not atomic.
- Explaining transient race failures.

## Producer-Consumer Buffer

```mermaid
flowchart LR
  P[Producer] -->|insert when not full| B[(Circular buffer)]
  B -->|take when not empty| C[Consumer]
  P -. mutual exclusion .- B
  C -. mutual exclusion .- B
```

Review separation:
- Mutual exclusion protects buffer indices and slots.
- `not_full` prevents overwriting unconsumed data.
- `not_empty` prevents consuming nonexistent data.

## Monitor With Conditions

```mermaid
flowchart TD
  Input[Monitor input queue] --> Proc[Procedure running]
  Proc -->|wait not_empty| NE[not_empty queue]
  Proc -->|wait not_full| NF[not_full queue]
  NE -->|signal not_empty| Proc
  NF -->|signal not_full| Proc
  Proc -->|exit| Out[Outside]
```

Use for:
- Bounded buffers.
- Alarm/timer monitors.
- Any monitor with more than one logical wait condition.

## Signal Semantics Comparison

```mermaid
flowchart TD
  Signal[c.signal()] --> HasWaiter{waiter exists?}
  HasWaiter -- no --> Continue[No condition waiter resumed]
  HasWaiter -- yes --> SC[SC: signaller continues]
  HasWaiter -- yes --> SX[SX: signaller exits]
  HasWaiter -- yes --> SW[SW: signaller waits in input queue]
  HasWaiter -- yes --> SU[SU: signaller waits in urgent queue]
  SC --> Risk[Waiter must recheck condition]
  SX --> Direct[Waiter resumes before input queue]
  SW --> Direct
  SU --> Urgent[Signaller later resumes before input queue]
```

Use for:
- Explaining why the same monitor code can work under one signal type and fail under another.

## Message-Passing Timeline

```mermaid
sequenceDiagram
  participant A as Sender
  participant Q as Buffer or channel
  participant B as Receiver
  A->>Q: send
  alt synchronous unbuffered
    B->>Q: receive
    Q-->>A: send returns after rendezvous
  else buffered
    Q-->>A: send returns after safe enqueue/copy
    B->>Q: receive later
  else non-blocking
    Q-->>A: request accepted
    A->>A: do independent work
    A->>Q: test/wait completion
  end
```

Use for:
- MPI send/receive ordering.
- Async offload queues.
- Buffer ownership reviews.

## Network Dataplane Pipeline

```mermaid
flowchart LR
  NIC[NIC queue] --> XDP[XDP/eBPF]
  XDP -->|pass| K[Kernel stack]
  XDP -->|redirect| UX[AF_XDP or devmap]
  K --> TC[Linux TC/eBPF]
  TC --> S[Socket application]
  NIC --> PMD[DPDK/VPP poll-mode]
  PMD --> UA[User dataplane]
```

Use for:
- Choosing kernel socket, XDP, AF_XDP, Linux TC, DPDK, or VPP placement.
- Showing where packet ownership changes and where completion is observed.

## TCP Handoff Timeline

```mermaid
sequenceDiagram
  participant A as Current owner
  participant B as Target owner
  participant R as Redirect plane
  A->>A: quiesce flow
  A->>B: transfer TCP/TLS state
  B->>R: install target rewrite
  B-->>A: owner ready
  A->>R: install redirect
  A->>A: unblock flow
```

Use for:
- TCP connection offload, flow migration, and software-to-hardware redirect transitions.
- Checking stale-rule, partial-handoff, and packet-reorder failures.

## CSP Guarded Server

```mermaid
flowchart TD
  Start[Server loop] --> Eval[Evaluate guarded commands]
  Eval --> P{producer ready and size < N?}
  Eval --> C{consumer ready and size > 0?}
  P -- yes --> Put[Accept producer message]
  C -- yes --> Take[Accept consumer request]
  P -- no --> Wait[Wait or try other guard]
  C -- no --> Wait
  Put --> Start
  Take --> Start
```

Use for:
- Avoiding server blocking on a passive client.
- Checking guard side effects.

## Periodic Drift

```mermaid
flowchart TD
  Bad[Relative delay loop] --> LD[Local drift per cycle]
  LD --> AD[Accumulated drift]
  Good[Absolute next release] --> Next[next_release += period]
  Next --> Delay[delay until next_release]
  Delay --> Stable[No accumulated drift under same assumptions]
```

Use for:
- Rewriting `sleep(period)` loops.
- Real-time timer review.

## Priority Inversion

```mermaid
sequenceDiagram
  participant L as Low priority
  participant M as Medium priority
  participant H as High priority
  L->>L: lock resource
  H->>L: blocks on resource
  M->>M: runs while H waits
  Note over H,L: high priority indirectly delayed by medium priority
  L->>L: release resource
  H->>H: resumes
```

Mitigation diagrams:
- Priority inheritance: low priority temporarily runs at high priority while holding the resource.
- Priority ceiling: resource raises holder priority to the ceiling when locked.

## RMS/EDF Timeline Checklist
Use a Gantt-style table when Mermaid is too noisy.

```text
time: 0 1 2 3 4 5 6 7 8
cpu : A A B A C C idle ...
rel : A,B,C     A   B
ddl :     A B   A     C
miss: none
```

Record:
- Release.
- Start.
- Finish.
- Deadline.
- Blocking interval.
- Preemptions.
- Missed deadline count.
