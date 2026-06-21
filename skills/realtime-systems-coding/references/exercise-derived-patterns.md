# Exercise-Derived Synchronization Patterns

## Purpose
Use this reference when a task resembles a canonical shared-memory synchronization problem and needs a state model, invariant, pseudocode, and proof checklist before implementation.

These patterns are intentionally abstract. Adapt `condition.queue()`, priority waits, signal semantics, and `signal_all()` to the target runtime instead of assuming every monitor API exposes them.

## Table Of Contents
- Selection map
- Property audit patterns
- Monitor and condition-variable hazards
- Portable semaphore monitor
- Rendezvous and lost-signal patterns
- Producer-consumer encoded-count buffer
- Readers-writers writer-priority monitor
- One-lane bridge fairness batch
- Dining philosophers deadlock gate
- Priority resource allocation
- Strict FIFO versus shortest-request queues
- Urgent-signal controller patterns
- Group rendezvous by counted release
- Service pipeline monitors

## Selection Map
| Problem Shape | Pattern To Start With | Main Risk |
| --- | --- | --- |
| Custom mutual exclusion | Property audit, ticket/tie-break, atomic primitive lock | Safety proof assumes unavailable atomicity. |
| Monitor over semaphores | Condition simulation hazard | Release-and-block is not atomic. |
| Semaphore as monitor | Portable semaphore monitor | Signal stealing makes `s` negative. |
| Two processes must meet | Rendezvous pattern | Signal sent before peer waits is lost. |
| Bounded buffer | Encoded-count producer-consumer | Unnecessary signals or missing blocked-peer counts. |
| Readers and writers | Writer-priority monitor | Writer starvation or reader convoy errors. |
| One-lane directional resource | Bridge fairness batch | Opposite direction starves. |
| Circular resource acquisition | Dining philosophers gate | Everyone holds one resource and waits forever. |
| Many resources, priority clients | Priority resource allocation | Wrong waiter gets released or resource is double-assigned. |
| Account, memory frames | FIFO versus shortest-request queues | Head-of-line blocking versus unfair bypass. |
| Controller refill/wakeup | Urgent-signal or SC loop rewrite | Signal-before-wait race. |
| Exact group formation | Counted group rendezvous | External entrants interleave with exiting group. |
| Barber, car wash, service station | Service pipeline monitor | Worker serves or charges the wrong client. |

## Property Audit Patterns
When reviewing a mutual-exclusion algorithm, separate these properties:
- Safety: no two processes can be in the critical section together and no forbidden state is reachable.
- Reachability: if contenders exist, at least one can enter; no global deadlock.
- Liveness: each waiting process eventually progresses under stated scheduling assumptions.
- Fairness: overtaking is bounded or the scheduler/runtime contract provides fairness.

Dijkstra-style conditions are enough to discuss safety and reachability, but not enough to prove starvation freedom or fairness.

Counterexample workflow:

```text
audit(protocol):
    define NOTSAFE = "Pi in CS and Pj in CS"
    try finite interleaving for NOTSAFE
    try infinite schedule where one process remains waiting
    if proof uses "eventually scheduled":
        name the scheduler or memory-arbitration assumption
    if proof uses "oldest waiter":
        verify FIFO or priority queue contract exists
```

Ticket/tie-break entry shape:

```text
enter(i, j):
    ticket[i] = 1                  # provisional nonzero claim
    ticket[i] = ticket[j] + 1
    while ticket[j] != 0 and peer_precedes_me(j, i):
        spin
    critical_section()
    ticket[i] = 0
```

The provisional nonzero claim closes the race where both contenders read zero before either publishes intent.

Atomic primitive lock shapes:

```text
test_and_set_enter():
    repeat:
        old = atomic_test_and_set(lock_word, 1)
    until old == 0
    critical_section()
    lock_word = 0
```

```text
exchange_enter():
    owns = false
    repeat:
        atomic_swap(lock_free, owns)
    until owns
    critical_section()
    atomic_swap(lock_free, owns)
```

If the primitive is replaced by its load/store expansion, the safety proof no longer applies.

## Monitor And Condition-Variable Hazards
A monitor wait must release exclusion and block as one runtime operation. If a hand-written semaphore simulation performs these as two interruptible steps, a process can release the monitor, be preempted before it blocks, and later observe a signal that was meant for another waiter.

Unsafe shape:

```text
condition_wait(c):
    c.waiters += 1
    release_monitor()      # if preempted here, the wait is not yet registered safely
    wait(c.sem)
    c.waiters -= 1
```

Review rule:
- Do not claim FIFO condition-variable behavior from FIFO semaphore behavior alone.
- Do not simulate monitor `wait` with semaphore code unless release-and-block atomicity is provided by the runtime.
- Treat monitor procedures as reentrant code: local variables and program counters must be private to each caller.

## Portable Semaphore Monitor
This monitor shape is robust across SC, SW, and SU because a signalled waiter consumes the `V()` directly rather than relying on a stored permit that can be stolen.

```text
monitor Semaphore:
    int s = initial_permits
    int blocked = 0
    condition c

    P():
        if s == 0:
            blocked += 1
            c.wait()
        else:
            s -= 1

    V():
        if blocked > 0:
            blocked -= 1
            c.signal()
        else:
            s += 1
```

If the monitor API exposes an exact `c.queue()` predicate, use that instead of `blocked`. If not, decrement `blocked` in `V()` when a signal is actually issued; under SC the signalled process may no longer be in the condition queue even though it has not yet resumed.

Avoid this SC-fragile shape:

```text
P():
    if s == 0: c.wait()
    s -= 1

V():
    s += 1
    c.signal()
```

Under SC, another entrant can consume the permit before the signalled waiter resumes.

## Rendezvous And Lost-Signal Patterns
The common failure is sending a signal before the peer has entered the corresponding wait queue.

Lost-signal-safe alternation:

```text
monitor Alternation:
    bool follower_ready = false
    condition p, q

    stop():
        while not follower_ready:
            p.wait()
        do_stop_work()
        follower_ready = false
        q.signal()

    follow():
        follower_ready = true
        p.signal()
        while follower_ready:
            q.wait()
```

Use this shape when `follow()` may run before `stop()`. The Boolean state carries the signal across the scheduling gap.

Two-party rendezvous checklist:
- One side records arrival in permanent monitor state before signalling.
- A signal with no waiter must still leave state that lets a later peer proceed.
- The second side must not wait on an acknowledgement before the first side has a way to send it.
- Under SC, waits are loops over permanent predicates.

## Producer-Consumer Encoded-Count Buffer
Use an encoded count to avoid `condition.queue()` while still signalling only when a peer is blocked.

Invariant:
- `0 <= n <= N`: no blocked producers or consumers; `n` is the number of buffered items.
- `n < 0`: `abs(n)` consumers are blocked waiting for items.
- `n > N`: `n - N` producers are blocked waiting for space.

```text
monitor EncodedBuffer:
    int n = 0
    condition not_empty, not_full

    put(item):
        n += 1
        if n > N:
            not_full.wait()
        insert_item(item)
        if n <= 0:
            not_empty.signal()

    take() -> item:
        n -= 1
        if n < 0:
            not_empty.wait()
        item = remove_item()
        if n >= N:
            not_full.signal()
        return item
```

Proof obligations:
- Pointer and slot updates happen only after the relevant wait returns or the guard is already true.
- A producer signal happens only when encoded `n` proves at least one consumer was blocked.
- A consumer signal happens only when encoded `n` proves at least one producer was blocked.

## Readers-Writers Writer-Priority Monitor
Separate reader and writer queues when writers must not starve.

```text
monitor ReadersWriters:
    int active_readers = 0
    int waiting_writers = 0
    bool writing = false
    condition readers, writers

    begin_read():
        while writing or waiting_writers > 0:
            readers.wait()
        active_readers += 1
        readers.signal()       # admit a batch when the semantics supports handoff

    end_read():
        active_readers -= 1
        if active_readers == 0:
            writers.signal()

    begin_write():
        if active_readers > 0 or writing:
            waiting_writers += 1
            while active_readers > 0 or writing:
                writers.wait()
            waiting_writers -= 1
        writing = true

    end_write():
        writing = false
        if waiting_writers > 0:
            writers.signal()
        else:
            readers.signal()
```

If the runtime is SC with ordinary condition variables, keep `while` guards and consider `signal_all()` for readers when one queue multiplexes several conditions.

## One-Lane Bridge Fairness Batch
Safety alone allows all cars in the same direction to pass forever. Add a batch limit when the opposite side is waiting.

```text
enter(dir):
    opp = opposite(dir)
    while passing[opp] > 0 or (waiting[opp] > 0 and batch[dir] >= LIMIT):
        waiting[dir] += 1
        gate[dir].wait()
        waiting[dir] -= 1
    passing[dir] += 1
    if waiting[opp] > 0:
        batch[dir] += 1
    if batch[dir] < LIMIT and waiting[dir] > 0:
        gate[dir].signal()

exit(dir):
    passing[dir] -= 1
    if passing[dir] == 0:
        batch[dir] = 0
        gate[opposite(dir)].signal()
```

Use a different `LIMIT` only after naming the fairness and throughput trade-off.

## Dining Philosophers Deadlock Gate
Resource-level mutual exclusion is not enough. Prevent the all-hold-one-fork state by gating the first acquisition.

```text
monitor Forks:
    bool busy[N] = false
    int holding_one = 0
    condition fork[N], gate

    take_first(i):
        while holding_one == N - 1:
            gate.wait()
        take_fork(i)
        holding_one += 1

    take_second(i):
        take_fork((i + 1) mod N)
        holding_one -= 1
        gate.signal()

    take_fork(k):
        while busy[k]:
            fork[k].wait()
        busy[k] = true

    release_fork(k):
        busy[k] = false
        fork[k].signal()
```

The gate ensures at least one participant can acquire both resources and break circular wait.

## Priority Resource Allocation
For `n` processes and `m` interchangeable resources, keep free-resource state and pending request state separately.

```text
monitor Resources:
    bool free[m] = true
    bool pending[n] = false
    int assigned[n]
    condition changed

    request(pid) -> resource:
        r = first_free_resource()
        if r exists:
            free[r] = false
            return r

        pending[pid] = true
        while pending[pid]:
            changed.signal()       # chain through lower-priority ineligible waiters
            changed.wait()
        return assigned[pid]

    release(r):
        pid = highest_priority_pending()
        if pid exists:
            assigned[pid] = r
            pending[pid] = false
            changed.signal()
        else:
            free[r] = true
```

Priority rule:
- Lower process index can mean higher priority.
- If a priority condition variable exists, `changed.wait(priority=pid)` can replace chaining.
- If no priority support exists, scan pending state under the monitor and signal until the eligible process observes its predicate.

## Strict FIFO Versus Shortest-Request Queues
Requests for money, memory frames, or other divisible resources need an explicit queue policy.

Strict arrival order with head-of-line blocking:

```text
request(amount):
    ticket = next_ticket
    next_ticket += 1
    while ticket != serving or available < amount:
        q.wait(priority=ticket)
    available -= amount
    serving += 1
    q.signal()
```

Shortest request first:

```text
request(amount):
    while available < amount:
        q.wait(priority=amount)
    available -= amount
    q.signal()
```

Trade-off:
- Strict FIFO preserves arrival order but can delay small eligible requests behind a large request.
- Shortest-request priority improves utilization but can starve large requests unless aging or quotas are added.

## Urgent-Signal Controller Patterns
Some controller problems signal first and then wait. That requires SU if the signal must not be lost before the caller reaches its wait.

SU shape:

```text
use_resource(amount):
    if empty:
        controller.signal()
        users.wait()
    consume_up_to(amount)
    if users_waiting_and_resource_remains:
        users.signal()

controller_sleep():
    if not empty:
        controller.wait()

controller_refill():
    refill_to_capacity()
    users.signal()
```

SC rewrite:

```text
use_resource(amount):
    if empty:
        controller.signal()
    while empty:
        users.wait()
    consume_up_to(amount)

controller_refill():
    refill_to_capacity()
    users.signal_all()
```

Rule: under SC, encode the condition as permanent state and wait in loops. Do not rely on handoff ordering.

## Group Rendezvous By Counted Release
When exactly one `A` and ten `B` processes must leave together, use counts plus a release chain. SU keeps the release group from being interrupted by new entrants.

```text
monitor Group:
    int a_inside = 0
    int b_inside = 0
    int a_leaving = 0
    int b_leaving = 0
    condition qa, qb

    enter_A():
        a_inside += 1
        if b_inside < 10:
            qa.wait()
        a_leaving += 1
        qb.signal()

    enter_B():
        b_inside += 1
        if a_inside == 0 or b_inside < 10:
            qb.wait()
        if a_leaving == 0:
            qa.signal()
        b_leaving += 1
        if b_leaving < 10:
            qb.signal()
        else:
            reset_counts()
```

If SU is unavailable, add a `phase` or `closing` flag so new entrants cannot mix into the group being released.

## Service Pipeline Monitors
Barber-shop and car-wash designs are generalized rendezvous pipelines:
- A client claims a service slot.
- A worker selects exactly one waiting client.
- The worker signals completion to that client.
- The client pays or acknowledges that same worker before either can re-enter.

State model:

```text
slot[i].waiting
slot[i].in_service
slot[i].done
slot[i].paid
```

Pseudocode shape:

```text
client(i):
    wait_for_available_slot()
    slot[i].waiting = true
    worker_ready.signal()
    while not slot[i].done:
        service_done[i].wait()
    slot[i].paid = true
    payment[i].signal()

worker():
    while no_waiting_slot():
        worker_ready.wait()
    i = reserve_one_waiting_slot()
    perform_service(i)
    slot[i].done = true
    service_done[i].signal()
    while not slot[i].paid:
        payment[i].wait()
    clear_slot(i)
```

The reservation step prevents two workers from selecting the same client.

## Proof Checklist
For any pattern adapted from this file, output:
- Monitor invariant.
- Unblocking condition for each wait.
- Signal semantics and why it is sufficient.
- Counterexample prevented by the chosen state variables.
- Liveness or fairness assumption.
- Stress/model-check scenario that would fail if the pattern were wrong.
