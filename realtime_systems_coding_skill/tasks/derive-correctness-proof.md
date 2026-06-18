# Derive Correctness Proof

## Use When
The task requires more than testing: custom synchronization, monitor design, message-passing protocol, real-time scheduling, or review of a proposed concurrency fix.

## Workflow
1. State the target property: safety, liveness, fairness, bounded blocking, or deadline satisfaction.
2. Define the state variables: shared variables, monitor permanent variables, protocol states, ranks/tags, task timing attributes, and auxiliary proof variables.
3. Define atomic actions at the selected abstraction level.
4. Define the forbidden state as `NOTSAFE` when proving safety.
5. Define the invariant:
   - Global invariant for shared state or distributed protocol.
   - Monitor invariant for monitor permanent variables.
   - Timing invariant for release/deadline assumptions.
6. Prove initialization establishes the invariant.
7. Prove each atomic action preserves the invariant.
8. Prove `Invariant -> not(NOTSAFE)`.
9. For liveness/fairness, name the scheduler, hardware, signalling, or selection assumption.
10. Translate proof obligations into tests, traces, and code review checks.

## Shared-Memory Proof
- Critical section safety: prove no two process predicates for "in CS" can be true together.
- Liveness: prove a waiting process cannot remain waiting forever under stated assumptions.
- Fairness: prove bounded overtaking or state that fairness depends on scheduler/hardware.

## Monitor Proof
- Initialization establishes monitor invariant.
- Every procedure assumes and restores monitor invariant.
- Before every `wait`, monitor invariant is true.
- Signal semantics is explicit:
  - Under SC, waiters recheck conditions.
  - Under SX/SW/SU, the signalled process can rely on stronger immediate-resumption assumptions only where the semantics provides them.
- Missing signals are a liveness failure even if safety invariants hold.

## Message-Passing Proof
- Each send has a compatible receive in the legal states.
- Blocking pairs cannot form an unmatched cycle.
- Non-blocking operations include a completion state before buffer reuse.
- CSP guarded commands are side-effect free.
- Nondeterministic alternatives preserve correctness for every possible selection.

## Real-Time Proof
- State the scheduling model before applying formulas.
- Validate the simple model assumptions before RMS or EDF utilization claims.
- Add blocking `B` when shared resources exist.
- Add server utilization for aperiodic handling.
- Treat drift control as part of the proof for periodic tasks.

## Evidence Output
Return:
- Property.
- Model.
- Invariant.
- Forbidden state.
- Atomic actions.
- Assumptions.
- Verification commands or traces.
- Remaining gaps.
