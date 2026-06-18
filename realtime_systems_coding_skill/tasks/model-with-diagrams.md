# Model With Diagrams

## Use When
The user asks for a design, code review, bug diagnosis, or implementation plan where concurrency or timing behavior would be unclear without a diagram.

## Workflow
1. Select the diagram pattern from `references/flow-and-diagram-patterns.md`.
2. Keep one diagram focused on one question.
3. Label processes, queues, resources, and timing events with domain names from the code or design.
4. Show the failure path first when debugging.
5. Show the corrected path after the invariant or protocol is defined.
6. Tie every diagram edge to a code location, message, lock, condition, or task event.

## Diagram Choices
- Process state model: lifecycle and blocked/runnable ambiguity.
- Interleaving diagram: race conditions and non-atomic read-modify-write.
- Producer-consumer buffer: mutual exclusion plus full/empty conditions.
- Monitor with conditions: condition queue design and signal placement.
- Signal semantics comparison: AS/SC/SX/SW/SU selection.
- Message-passing timeline: blocking, buffered, and non-blocking communication.
- CSP guarded server: selective wait and server process design.
- Periodic drift: timer loops and absolute release scheduling.
- Priority inversion: shared resources in real-time tasks.
- RMS/EDF timeline: deadline and response-time analysis.

## Output Rules
- Do not use decorative diagrams.
- Do not draw a diagram that hides a missing assumption.
- Include a short "What this proves" or "What this does not prove" note.
- If using Mermaid, keep syntax simple so it renders in common Markdown viewers.

## Review Questions
- Does the diagram show every queue involved?
- Does it distinguish blocked, ready, and running states?
- Does it identify the atomic handoff point?
- Does it show where a signal can be stolen or lost?
- Does it show where a buffer becomes safe to reuse?
- Does it show release/start/finish/deadline for real-time tasks?
