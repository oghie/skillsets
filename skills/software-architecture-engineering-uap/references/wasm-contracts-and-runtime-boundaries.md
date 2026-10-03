# Capability Contracts And Runtime Boundaries

## Three Artifacts, Three Responsibilities
| Artifact | Responsibility | Does Not Establish |
|---|---|---|
| Capability contract | Outcome, semantic I/O, errors, quality, budgets, events, owner, state, policy, compatibility | That the code or host enforces any declaration |
| Portable core | Domain calculation under explicit inputs/context | Networking, persistence, authorization authority, or placement |
| Host envelope | Binding, validation, authoritative grants, I/O, limits, lifecycle, telemetry | Semantic equivalence to another adapter merely because interface names match |

Keep transport DTOs, SDK/ORM objects, UI widgets, clocks, randomness, filesystem, storage, GPU handles, and framework state outside the domain core. Model host interactions as explicit ports. Pin the external context used by a supposedly pure operation: a filename without file contents/version is not a complete input.

Stateless, stateful, and subscribable describe different dimensions, not mutually exclusive kinds. A stateless handler can produce non-idempotent effects. A subscribable operation does not imply durable replay. A stateful Wasm instance does not provide portable durable storage or an automatic migration protocol.

## Contract Completeness
| Concern | Minimum Definition | Verification |
|---|---|---|
| Identity/ownership | Capability and contract version, owner, publisher identity, lifecycle status | Authorized publishing and artifact/contract binding |
| Outcome | Business meaning, invariant, quality profile, non-goals | Domain examples, properties, stakeholder acceptance |
| Inputs/outputs | Schema, units, encoding, bounds, optionality, degraded results | Structural and semantic positive/negative tests |
| Errors | Stable categories, retryability, side-effect status, remediation | Invalid input, unavailable dependency, denial, trap, timeout tests |
| State | Authority, version, scope, consistency, concurrency, retention | CAS/transaction, crash, replay, migration, reconciliation tests |
| Events | Named fact, schema version, owner, delivery/ordering scope | Consumer tests and transport-specific failure tests |
| Runtime needs | Artifact kind, world/ABI, imports, features, target profiles | Binary inspection and real host instantiation |
| Quality/budgets | Workload, accuracy/freshness/SLO, memory/time/output/concurrency limits | Statistical measurements and enforcement-denial tests |
| Policy | Requested rights, classification, eligible placements, policy references | Authoritative grants and authorization at invocation/effect boundaries |
| Observability | Lifecycle, decisions, metrics, correlation, redaction/retention | Evidence completeness, failure visibility, privacy tests |
| Evolution | Compatibility, deprecation, offline support window, state schema | Consumer matrix, coexisting versions, upgrade/rollback |

Define CPU units precisely: core fraction, CPU-time budget, scheduling weight, and instruction fuel are different. A p99 SLO is a population statistic; a request deadline is an individual limit. Availability is an end-to-end property, not the presence of an `availability` key.

Use an existing schema/IDL/policy format when it fits. If creating a local manifest, label it as local, version its schema, reject invalid security-critical fields, and map every operational field to implemented code and tests. Optional annotations may remain descriptive only if they are not presented as enforcement.

## Artifact And Interface Profiles
| Profile | Boundary | Critical Checks |
|---|---|---|
| Core Wasm module | Core exports/imports and explicit memory/function ABI | Argument layout, allocation/free ownership, pointer/length bounds, traps, feature support |
| WASI 0.1 / P1 | Core module using `wasi_snapshot_preview1` | Actual imports and supported subset; do not infer HTTP, threads, or process support |
| WASI 0.2 / P2 component | Component Model with versioned WIT interfaces | World, Canonical ABI, generated bindings, host support, resource lifetime |
| WASI 0.3 / P3 component | Native async component interfaces | Exact WIT/toolchain/runtime release, async cancellation/backpressure, interface migration |
| Browser embedding | WebAssembly JS API plus explicit host glue | Worker lifecycle, browser engine/features, JS boundary, permissions, offline storage |
| Native implementation | Host ABI/SDK/process boundary | OS/CPU build, privileges, isolation, cleanup, semantic parity |

WASI generations are not interchangeable labels. P1 is a legacy module interface; P2/P3 use components. P3 adds async primitives and changes interfaces; it is not "P2 plus a flag". Choose based on the pinned toolchain and target fleet, not novelty. Recheck current runtime support and release-specific WIT before prescribing APIs.

Browsers do not automatically provide WASI or direct Component Model instantiation. A WASI shim or component transpilation/binding path must supply the required imports and be tested; a Wasmtime CLI demo is not browser validation. Separately compiled native ARM/x86 binaries are not the same artifact as a `.wasm` module. Precompiled runtime caches may also be runtime/CPU-specific.

WIT describes typed imports/exports, interfaces, worlds, records, variants, and resource handles. It does not define business semantics, authorization, SLOs, network discovery, or distributed transactions. It also does not turn a component into an HTTP/MCP service without an actual adapter.

Use `../examples/portable-quote/world.wit` for a small typed boundary and `../examples/portable-quote/core.rs` for host-independent calculation. These are separate examples, not a generated/exported component implementation. Generate and test bindings with the selected toolchain before claiming a runnable component.

## Semantic Example: Local Quote, Not Payment Approval
The example computes `floor(subtotal_minor * (10000 - discount_bps) / 10000)` for a non-negative subtotal and a discount in `[0, 10000]`. Currency minor-unit convention and rounding are owned by the contract. It has no authentication, settlement, tax, database, or clock behavior; callers must not reinterpret its result as payment authorization.

At the JSON/JavaScript boundary, use a documented decimal-string encoding or a bounded safe-integer range for 64-bit values. WIT `u64`, JavaScript `number`, Rust `u64`, and a JSON consumer are not automatically lossless equivalents. Preserve units and reject invalid values before calculation.

Example transport payload, not a WIT encoding specification:

```json
{
  "subtotal_minor": "10005",
  "currency": "USD",
  "discount_bps": 500,
  "rule_version": "quote-floor-v1"
}
```

Expected domain amount is `9504` minor units. Neither locale formatting nor floating-point arithmetic belongs in this core. Near-limit integers, zero, full discount, invalid discounts, and randomized arithmetic properties belong in the same test corpus across hosts.

## Host Binding And Lifecycle
Use `../templates/mermaid-portable-capability-flow.mmd` to instantiate this pipeline:

```text
load bounded contract + artifact
verify artifact provenance/integrity and contract binding
validate structure -> semantic consistency -> authoritative policy
resolve exact target ABI/imports and eligible adapter profile
create isolated invocation context with bounded grants/resources
validate caller, tenant, input and state preconditions
run core; mediate every host effect with current authorization
validate output/events; commit effects with the required atomicity
record lifecycle and observed quality; return explicit outcome
```

Any required unsupported interface, denied grant, or incompatible contract rejects execution before business side effects. A post-execution schema failure cannot undo a payment or external write: design validation and commit boundaries accordingly.

Lifecycle states can be `loaded -> validated -> bound -> initialized -> running -> completed | failed | cancelled -> closed`. Name legal transitions, cleanup, trap recovery, state reset, and retry ownership. Distinguish a denied preflight from a failed execution with unknown effect status.

Bind an invocation to a contract digest, artifact digest, target profile, adapter identity/config digest, policy revision, input/fixture identity, and state version. Do not let a mutable registry update silently change an approved operation between validation and effect. Recheck or abort when required authority/context becomes stale.

## Adapter Semantics
- **Network:** allowlisted destination/method, redirect and DNS handling, request/response limits, timeouts, credential scope, and error translation. Browser Fetch and native sockets have different CORS, cookie, TLS, and lifecycle behavior.
- **Persistence:** transactions/CAS, durability, consistency, retry safety, key namespaces, quotas, serialization, deletion, and migration. IndexedDB, local files, Redis, and a database are not interchangeable merely because each has `get`/`put`.
- **Clock/random:** distinguish wall time, monotonic duration, logical sequence, and reproducible test context. Deterministic fixtures must never replace secure production randomness for credentials or keys.
- **GPU/inference:** declare backend, weights/model/preprocessing version, precision, quality threshold, transfer cost, and CPU fallback. GPU availability is not automatically exposed by WASI; verify the selected host interface/proposal implementation.
- **Events:** declare transport mapping, durability, acknowledgements, ordering, replay, deduplication, and backpressure; use existing outbox/inbox/saga references for business effects.
- **Telemetry:** bound output volume, tenant-sensitive fields, access, retention, and behavior when the sink is unavailable. Do not turn logging into an unbounded or privileged side channel.

Adapter composition order matters. `retry(cache(network))` and `cache(retry(network))` differ in failure, freshness, and side-effect behavior. Cache keys must include relevant tenant/auth scope, operation/input, contract/model version, and freshness rules. Record the binding configuration, not only a human-readable adapter label.

Generated bindings reduce marshalling work; they do not generate equivalent storage, retry, security, or workflow semantics. An adapter stub returning a stable error is unsupported functionality, not evidence of successful portability.

## Stateful And Subscribable Operations
Keep domain state explicit where possible: `(input, state_version, state) -> (result, proposed_state, effects)`. The authoritative store commits a transition atomically or rejects stale state. Merely validating a version before a later write allows a check/use race.

For shared/remote state, specify transaction or CAS scope, conflict rules, idempotency identity, leases/fencing if needed, and retry behavior. A per-invocation event counter is neither a distributed lock nor a consensus protocol. Wasm isolation does not serialize concurrent updates to host data.

For offline work, define durable local capture, quota/eviction policy, acknowledgement, synchronization cursor, ordering scope, duplicate handling, stale-data limits, conflict reconciliation, and explicit rejection/degradation after expiry. Cloud connectivity is also fallible. Porting core code does not migrate state, device credentials, leases, or broker offsets.

## Evolution Rules
- Track contract, implementation artifact, bindings, adapters, policy, model/data, and state schema versions independently but release compatible combinations together.
- Optional fields can break strict consumers; enum/variant additions can break exhaustive bindings; changed units, rounding, side effects, quality, or permissions can break behavior despite a compatible shape.
- Verify old consumer/new provider and new consumer/old provider separately. Backward and forward compatibility are different claims.
- Preserve compatible versions for a defined fleet/support window; measure usage before deprecation. Do not use unlimited ranges or mutable "latest" to obtain reproducibility.
- Data rollback, policy rollback, and artifact rollback have different safety conditions. Never roll back a revocation or security fix solely to preserve compatibility.

## Specification Checks
When current API details matter, verify the [WASI releases](https://wasi.dev/releases), [WIT reference](https://component-model.bytecodealliance.org/design/wit.html), [Rust component workflow](https://component-model.bytecodealliance.org/language-support/building-a-simple-component/rust.html), and [Rust P1 target contract](https://doc.rust-lang.org/rustc/platform-support/wasm32-wasip1.html). Record versions in project evidence; these external documents are not deployment dependencies.
