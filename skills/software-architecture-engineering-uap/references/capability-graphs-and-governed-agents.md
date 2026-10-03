# Capability Graphs, Events, And Governed Agents

## Keep The Layers Separate
| Responsibility | Purpose | Not A Guarantee |
|---|---|---|
| Contract/catalog | Describe available behavior, events, constraints, ownership | That the implementation fulfills it |
| Discovery/exposure | Return eligible descriptors and expose callable interfaces | Permission to invoke or trust every result |
| Planner/agent | Propose a path toward a goal | Authority to grant rights, choose arbitrary side effects, or bypass policy |
| Validator/authority | Approve bounded actions under current policy/context | Atomicity of all future effects without a commit protocol |
| Executor/runtime | Bind and run approved operations, validate results, record evidence | Automatic compatibility, scaling, consensus, or recovery |

These are architectural responsibilities, not necessarily five independently deployed services. Reuse a simple fixed workflow for stable CRUD or well-understood sequences. Dynamic discovery can be useful without agents; agents can be useful without Wasm; Wasm does not require MCP.

## Event Contract Catalog
Treat an event as an owned, versioned domain fact with payload semantics, producer/consumer expectations, delivery and ordering scope, classification, retention, compatibility, and deprecation policy. Distinguish business events from commands and operational signals; do not disguise `do-next-step` as a factual event.

An ECCA-style event catalog is a reference design, not a universally implemented protocol. Prefer established schema registry, AsyncAPI, and CloudEvents mechanisms where they meet requirements. Keep adapters and consumers tested against the same contract assets.

| Transport Dimension | Must Be Stated And Tested |
|---|---|
| Delivery | Durable vs best effort, at-most/at-least once, retry and redelivery |
| Ordering | Per aggregate/partition/connection vs no guarantee; handling gaps and late arrivals |
| Acknowledgement | Receipt vs durable storage vs committed business effect |
| Replay | Retention/cursor, schema/model/state compatibility, side-effect policy |
| Consumer identity | Fan-out subscriptions vs competing workers; independent consumer groups |
| Overload | Bounded queues, backpressure, rate limits, shedding, DLQ and recovery |
| Authority | Producer/consumer identity, tenant scope, topic/resource permissions, revocation |

Kafka, MQTT, NATS, WebSocket, HTTP, and in-process delivery do not acquire equal guarantees from a common JSON envelope. Define the adapter's actual semantics rather than promising broker independence by name.

When using CloudEvents, preserve valid standard fields and lowercase alphanumeric extension names; define extension meanings. `time` follows RFC 3339 when present. Correlation attributes such as `traceparent` are not signatures, authorization tokens, or causal/global ordering proofs. If integrity/authenticity/replay protection is required, specify actual authenticated transport or signature mechanisms, trust keys, scope, freshness, and idempotency.

For deduplication, scope identity to the consumer and producer namespace (for example consumer + source + event ID), and preserve the identity across retries. "Check processed, perform effect, mark processed" is unsafe under concurrency/crash unless those operations have the required atomicity. A unique ID store alone does not fix an external payment/write in a separate transaction. Reuse outbox/inbox, saga, and reconciliation guidance in `microservices-pattern-language.md`.

## Build A Graph Without Inventing A Workflow
1. Validate contract structure and publication authority; register versioned capability/event descriptors.
2. Index producer event declarations and consumer requirements by exact event identity/version.
3. Generate candidate edges, then validate semantic compatibility, classification, tenant scope, placement, quality, and delivery requirements.
4. Decide fan-out vs selecting one provider/competing worker; multiple matches do not imply all should perform the same business effect.
5. Apply explicit resolution/tie-break rules and record the selected contract, provider, profile, policy revision, and reason.
6. Execute within bounded queue, concurrency, retries, and failure/compensation rules.
7. Reconcile declared, resolved, and observed graphs; expose drift and approved changes.

Use an event-keyed index to avoid repeatedly scanning all contracts, but account for matching subscribers, candidate authorization, schema checks, and the number of edges. A hash lookup does not make all discovery/dispatch constant time.

The declared graph is an architectural hypothesis. It omits undeclared database writes, sidecars, external callbacks, and host effects unless those are modeled. Observed traffic supplies additional evidence, not a complete replacement for domain requirements. A thumbnail capability absent from an image graph is not automatically a business gap.

## Graph Review And Evolution
- Required waiting consumers: missing producer, incompatible event/schema, wrong version, denied placement, or offline dependency?
- Orphaned emissions: intentionally external/audit-only or an accidentally removed consumer?
- Cycles: deliberate feedback with convergence/hop/time/rate limits, or an event storm?
- Fan-out: expected independent outcomes or duplicate competing effects and excess data exposure?
- Long chains/diamonds: added behavior, latency budget, correlation/join/failure semantics, and transaction boundaries?
- Overlapping providers: explicit selection policy and quality/state/authority compatibility, or unexplained runtime choice?
- Drift: missing observable edge, new undeclared effect, stale policy, unused constraint, or approved architecture change?

Snapshot and diff node/edge/required-dependency changes in CI. Validate consumers before activating a new binding: name/schema agreement is necessary but not sufficient. Specify registry availability, snapshot age, sync lag, partition behavior, revocation, caching, and recovery. A fleet running stale snapshots does not immediately stop when an entry is removed centrally.

Use `../scripts/capability_graph_audit.py` with `../examples/capability-graph.json`. Its local format is a reduced snapshot, not a UMA/MCP/AsyncAPI specification. It checks exact event and schema-reference strings, reports required waiting consumers, unconsumed emissions, exact cyclic components, and optional topology diffs. It does not open schemas, evaluate compatibility ranges/policies, query a live registry, or prove delivery/state semantics. Cycles and unconsumed emissions are review signals, not automatic architecture defects.

```bash
python3 scripts/capability_graph_audit.py examples/capability-graph.json
python3 scripts/capability_graph_audit.py current.json --previous baseline.json
python3 -m unittest discover -s scripts -p 'test_capability_graph_audit.py'
```

Run from the skill directory. Exit `0` means this limited structural check found no blocking required dependency; `1` means missing/incompatible required consumers; `2` means invalid input or a helper limit was reached. Do not call exit `0` production approval.

## MCP: Protocol, Not A Custom Registry API
MCP standardizes client/server interaction including tool discovery and invocation. Use negotiated protocol capabilities, `tools/list` (including pagination/change notification where supported), and `tools/call`. A server may delegate to a governed runtime; that is an implementation choice. Do not call a custom `GET /capabilities` endpoint or an arbitrary capability descriptor "standard MCP".

MCP does not automatically supply a semantic capability graph, placement solver, business policy engine, or Wasm runtime. Expose graph/query functionality through real tools/resources when needed. Pin and test the protocol/SDK/transport version; stdio and Streamable HTTP are standard transport choices, while custom WebSocket/Unix-socket paths require documented interoperable implementations.

Keep discovery metadata and tool annotations untrusted unless authenticated/approved. Schema/type matching, a natural-language intent, or an annotation saying read-only does not authorize a tool. Implement identity, resource/tenant authorization, input/output validation, timeouts, rate limits, credential audience/scope, and consent for sensitive actions. Prevent token passthrough, confused-deputy escalation, SSRF, prompt injection through descriptors/results, and data exfiltration.

## Governed Decision Lifecycle
Use `../templates/mermaid-governed-capability-execution.mmd` for the authority boundary:

```text
goal + trusted caller context
-> discover approved descriptors
-> propose capability IDs/versions, inputs, placement, budgets, effects, assumptions
-> authority checks semantics, grants, state, data locality, quality and cost
-> reject with bounded remediation OR approve a scoped expiring plan
-> bounded revision, if permitted; otherwise terminate/escalate
-> bind concrete compatible implementations and recheck authority at effect boundaries
-> execute, validate outputs, commit/reconcile, and record decision/effect evidence
```

The planner proposes; the authority approves; the executor acts within that approval. Local route hints and confidence scores are advisory unless explicitly delegated authority permits more. An agent cannot self-certify unresolved trust, compliance, or state preconditions.

Record approved plan identity/digest, allowed capabilities and effects, tenant/caller, artifact/contract/profile/policy/state versions, budgets, expiry, approver, decision reasons, and execution correlation. Approval grants no implicit permission to change placement, provider quality, inputs, permissions, or side effects. Revalidate or reapprove material changes; do not silently replan.

Bound iterations/revisions, total wall time, token/model/tool cost, invocations, fan-out, retries, and effect scope. One revision may be appropriate for a simple proposal; it is not a universal rule. Cancellation, no-progress loops, registry changes, invalid outputs, and exhausted budgets must terminate or escalate. Multiple agents sharing a catalog still require ownership, concurrency control, and atomic state transitions where invariants demand them.

## Decision Evidence, Not Hidden Reasoning
Preserve goal, descriptor snapshot, proposed plan, assumptions, rejection/remediation, revised plan, approval, resolved execution, output/quality/degradation, effect status, and trace identifiers. Log concise decision reasons and checked predicates, not private model chain-of-thought or secrets.

Make these artifacts queryable under access control and retention rules. A trace shows what was recorded; completeness, authenticity, and tamper evidence require separate controls. An execution log is not a proof that a generative model will produce the same answer next time. Deterministic replay needs captured external/model context and a side-effect-safe replay mode.

Fallback must preserve hard safety/security/authority constraints. If an allowed quality profile or output language changes, return explicit degraded status and provenance; when degradation is forbidden, fail clearly. "Same shape" is not enough to substitute a basic summary for a clinically validated or compliance-sensitive result.

## Reject Agent Overhead When
- The workflow is fixed and a tested orchestrator/rule-based selector suffices.
- Hard real-time deadlines cannot tolerate a variable decision loop.
- The domain requires pre-approved execution paths or missing controls make dynamic composition unsafe.
- Discovery/LLM overhead, data exposure, and operational burden exceed the benefit.

Explicit orchestration is not inherently fragile. Durable state machines/coordinators are often the correct choice for long-running, branching, audited, or compensated workflows. Choreography removes direct calls, not semantic coupling or the need to design recovery.

## Current Specification Checks
Verify [MCP tools](https://modelcontextprotocol.io/specification/2025-11-25/server/tools), [transports](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports), [security guidance](https://modelcontextprotocol.io/specification/2025-11-25/basic/security_best_practices), [CloudEvents](https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md), and [W3C Trace Context](https://www.w3.org/TR/trace-context/) when implementation details matter. Use project evidence for actual server/runtime guarantees.
