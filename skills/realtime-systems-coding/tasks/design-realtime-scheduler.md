# Design Real-Time Scheduler

## Use When
The task involves deadlines, periodic loops, timer precision, RMS, EDF, priority inversion, sporadic/aperiodic tasks, or missed-deadline analysis.

## Workflow
1. Classify timing criticality: hard, firm, or soft/permissive.
2. Record task attributes: `C`, `T`, `D`, priority, phase, jitter, blocking `B`, and resource use.
3. Confirm clock and timer behavior: monotonicity, resolution, overflow interval, and timeout mechanism.
4. Choose a scheduling model:
   - RMS for static priorities when `D = T` and the simple model mostly holds.
   - Deadline monotonic when `D < T` and fixed priority is required.
   - EDF when dynamic priority overhead and overload behavior are acceptable.
   - Server-based handling for aperiodic work.
5. Include blocking time if tasks share resources.
6. Run utilization checks and timeline simulation.
7. Instrument runtime to capture release, start, finish, blocking, and deadline misses.

## Periodic Loop Pattern
Use absolute next release:
1. `next = clock_now()`
2. Loop:
3. Execute the periodic action.
4. `next += period`
5. Delay until `next`

This avoids accumulated drift caused by repeated relative delays.

## RMS
- Priority is inverse to period.
- Liu-Layland utilization bound is sufficient, not necessary.
- If utilization exceeds the bound, do not declare failure without a stronger check.
- The simple model excludes blocking, aperiodic work, and overhead.

## EDF
- Chooses the ready task with the nearest deadline.
- Under the simple model with `D = T`, total utilization <= 1 is feasible.
- Dynamic priority updates can add overhead and make overload behavior less aligned with criticality.

## Priority Inversion Mitigation
- Non-preemptive critical sections are simple but can block unrelated higher-priority tasks.
- Priority inheritance reduces inversion by boosting the resource holder while it blocks higher-priority tasks.
- Priority ceiling protocols predefine resource ceilings and can prevent deadlock, transitive blocking, and repeated blocking on uniprocessors.

## Aperiodic Work
- Background server is simple and low priority.
- Polling server reserves capacity each period.
- Deferred server preserves capacity inside the server period and improves responsiveness.
- Include server utilization in feasibility checks.

## Verification Checklist
- Are all WCET values measured or justified?
- Are deadlines relative or absolute?
- Does any high-priority path block on a lower-priority resource?
- Is drift controlled?
- Does overload preserve critical tasks?
- Does the analysis include scheduler overhead and interrupt latency where relevant?
