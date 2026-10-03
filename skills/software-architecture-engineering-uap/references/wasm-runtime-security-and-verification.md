# Wasm Runtime Security, Evidence, And Verification

## Claims Must Have Mechanisms
A contract is a declaration. A validated binary establishes format/type constraints. Neither proves business correctness, tenant isolation, deterministic output, acceptable latency, or compliance. For each claim, name its enforcement point, exact target/configuration, negative test, operational evidence, and remaining gap.

Use `declared`, `implemented`, `verified`, `unsupported`, and `blocked` consistently. "Verified" always has a scope: target, artifact/version, fixture/workload, policy, and date. A proposed runtime architecture and a teaching/demo implementation are not interchangeable evidence.

## Threat Boundaries
| Threat | Required Control | Negative Test |
|---|---|---|
| Forged publisher or modified module | Trusted signing identity, artifact/contract binding, digest/signature verification | Spoofed publisher label, substituted artifact, revoked/expired signer |
| Overprivileged host import | Authoritative scoped grants, minimum exposed interfaces, per-effect checks | Undeclared/denied file/network/write capability |
| Cross-tenant leakage | Tenant context from trusted identity, scoped state/cache/credentials, isolated lifecycle | Same key/input in two tenants, reused instance state, forged tenant argument |
| CPU/memory/output exhaustion | Guest limits plus host/process budgets, concurrency admission, bounded I/O | Infinite loop, growth, deep input, decompression bomb, output flood |
| Compromised registry/policy | Controlled publishing, authenticated distribution, freshness/revocation, recoverable audit | Tampered snapshot, stale cache, unreachable registry, revoked capability |
| Event cascade or abusive invocation | Subscription grants, rate/hop/cost limits, backpressure, deduplication | Cyclic event flow, fan-out storm, repeated agent calls |
| Host/adapter/runtime vulnerability | Patching, supply-chain review, least privilege, layered isolation | Adapter validation bypass, unsafe pointer/length, unsafe cached code |
| Untrusted client result | Authoritative server validation and policy/state checks | Modified browser code, fabricated quote/identity/authorization result |

Wasm restricts guest access to memory/control flow and explicitly linked host interfaces. It does not make the host untrusted-proof, eliminate runtime/compiler bugs or side channels, or prevent source-language memory corruption inside guest linear memory. Imported/shared memories and tables require explicit isolation review. Native execution must establish its own process/OS isolation; a native adapter label does not inherit Wasm sandboxing.

The host is part of the trusted computing base. An allowed `http` import can still become SSRF; a permitted storage handle can still leak another tenant's data; a telemetry sink can still leak secrets. Reuse `security-architecture-patterns.md` and `iam-auth-architecture.md` for PEP/PDP, identity, credentials, reference-monitor completeness, and audit/key management.

Requested rights are not granted rights. Obtain grants from an authoritative policy over authenticated identity, tenant, action, resource, deployment, and current context. A self-declared `publisher`, `trustTier`, `verified`, or non-empty `checksum` is not authenticity/provenance verification. An SBOM inventories dependencies; a vulnerability scan and a compatibility test are different activities.

Fail closed for authorization, authenticity, protected data movement, and required isolation. An explicitly approved stale-policy/offline mode needs a bounded validity window, scoped authority, revocation risk assessment, and reconciliation. Never import a demo's default fail-open policy into production security decisions.

## Enforcement Limits By Host
| Control | Correct Interpretation | Residual Risk |
|---|---|---|
| Fuel | Bounded guest execution work under configured instrumentation | Not milliseconds, total CPU quota, or a bound on blocking host calls |
| Epoch/deadline interruption | Host-managed interruption of executing guest code | Timing varies; host I/O and cleanup need their own cancellation/deadlines |
| Linear-memory limiter | Limit on guest memories under the chosen embedding | Does not account for all host buffers, tables, instances, stacks, or process RSS |
| cgroup/process controls | OS-level resource containment on supported hosts | Shared process accounting, queueing, GPU memory, and downstream resources still matter |
| Browser Worker | Separates compute from the UI thread and permits lifecycle control | Suspension, startup, messages/copies, device scheduling, and no guaranteed hard deadline |
| Idle callback | Cooperative scheduling opportunity | Not security containment, a hard resource budget, or real-time scheduling proof |
| Network/filesystem grant | Explicit authority at the host boundary | Scope, redirects/DNS, handle lifetime, TOCTOU, and revocation must be enforced |

For Wasmtime, configure fuel/epoch and store limits deliberately, and test their actual behavior with the selected API/version. Avoid blanket preopens, inherited environment/secrets, unrestricted networking, or unsafe deserialization of untrusted precompiled artifacts. For every embedding, identify whether resource denial traps, yields, rejects, or kills the process and whether state can be safely reused afterward.

## Determinism Has A Scope
Distinguish:
- **Shape parity:** the result/event has the same types.
- **Semantic equivalence:** documented business invariants hold, possibly under an explicit tolerance/quality profile.
- **Exact replay:** the same captured inputs/context produce the same selected observable values.
- **Performance comparability:** workload and measurement conditions permit a meaningful comparison, not identical latency.

Exact replay requires artifact, contract, adapter/config, policy, state snapshot, external responses, clock/random inputs, event ordering, model/weights/preprocessing, and numerical behavior. Synchronize what the contract actually requires; do not normalize away business differences to obtain a matching hash.

Wasm is not universally deterministic by default. NaN representations, relaxed SIMD, memory/table growth, nondeterministic imports, and shared-memory scheduling require review. Native vs Wasm or GPU vs CPU can have different floating-point behavior. Specify exact integer/decimal units and rounding for financial/domain values; define tolerances and quality metrics only where the domain allows them.

A logical sequence counter orders one recorded scope, not all distributed events. Wall-clock timestamps do not establish causal/global order. Use monotonic clocks for durations and transport/domain-specific ordering mechanisms for state transitions. Canonicalized result hashes compare selected bytes; they do not prove universal semantic correctness, provenance, or secure delivery.

AI-generated summaries, classifications, or plans require model-quality and factual-grounding tests even when their schemas match. Stable toy fixtures or an extractive ranking example do not establish deterministic generative AI behavior. A reproducible approved plan can coexist with probabilistic outputs; record both honestly.

Replay external writes only through explicit safe simulation or an approved idempotent recovery protocol. Shadow execution must isolate credentials, storage, publications, payments, and tool effects; discarding the final response alone does not prevent duplicate effects.

## Verification Ladder
1. **Static contract/build review:** schema/IDL validity, semantic completeness, dependency/import inventory, permissions, features, version compatibility, license/provenance, debug-symbol policy.
2. **Binary validation and instantiation:** real artifact in each pinned runtime/browser/device profile; required imports denied by default and explicitly bound.
3. **Domain conformance:** golden vectors, property tests, fuzz/malformed/oversized input, boundaries, numeric/encoding behavior, structured errors, semantic output validation.
4. **Cross-host comparison:** same corpus/state/context through each implementation and actual adapters; distinguish exact, tolerated, or intentionally degraded outcomes.
5. **Security/adversarial checks:** denial, tampering, stale/revoked authority, tenant isolation, reentrancy, quota/cancellation, hostile host output handling.
6. **Distributed failure checks:** crash during commit, ACK loss, duplicate/reordered events, partition, disk full/eviction, offline expiry, backpressure, reconciliation.
7. **Performance/operational checks:** load/soak, weakest device, full envelope costs, trace/evidence completeness, canary, upgrade, rollback, support-window behavior.

Use `../templates/wasm-portability-validation-matrix.md`. Do not stop at a positive-path native unit test and label browser/edge targets verified.

Example commands, adapted to the project's pinned tooling and artifact:

```bash
rustc --edition 2021 --test examples/portable-quote/core.rs -o /tmp/portable-quote-tests
/tmp/portable-quote-tests
wasm-tools component wit examples/portable-quote/world.wit
wasm-tools validate path/to/capability.wasm
wasm-tools print path/to/capability.wasm
wasm-tools component wit path/to/component.wasm
```

Run from the skill directory for the bundled examples. Parsing WIT checks syntax, not an exported component. For Rust, use the chosen native `cargo build --locked --target ...` workflow and binding generator; do not assume an obsolete target name or a particular plugin generator is mandatory. Execute a command module or typed reactor through an appropriate host harness. A command runner cannot by itself exercise arbitrary component exports.

## Measure The Entire Cost
Record workload sizes/distribution, throughput and offered load, success/error rate, p50/p95/p99, queue wait, cold/warm download/compile/instantiate time, serialization/copies/host I/O, guest and total memory, sustained CPU/GPU, cancellation/cleanup, device energy/thermals, and distribution/egress/maintenance cost.

Keep host identity/version, hardware, concurrency, cache state, network/storage conditions, warmup, sampling/window, and measurement boundaries with results. Avoid coordinated omission in load tests. Four observations or an average cannot substantiate tail-latency/availability claims. Measure at expected and overload traffic and at relevant device constraints; use uncertainty rather than universal startup/memory/speed multipliers.

Budget decomposition should include queueing + setup + core + host I/O + serialization/network + validation + cleanup. A fast core may be irrelevant when GPU transfer, adapter calls, or registry lookups dominate. Optimize hot boundary crossings only after profiling; batching/fusing may be safer than adding more tiny capabilities.

## Release And Governance
- Bind source/build provenance, artifact digest, contract/world, adapter/config, policy, model/data, and state schema in the release record.
- Review consumer compatibility and graph diffs; a declaration of compatibility is not a test result.
- Recheck authority/freshness where caching would otherwise allow revoked publishers, permissions, or routes.
- Validate immutable artifact identity across load and invocation; record authorized exceptions with expiry and owners.
- Canary by contract/target profile with domain and SLO acceptance gates. Treat approved degraded outcomes separately from success.
- Roll back only to a compatible, non-revoked combination; restore/reconcile state separately when required.
- Monitor drift, denied/unevaluated constraints, model-quality changes, adapter failures, queue lag, resource rejection, policy age, and fleet versions. Avoid unbounded metric cardinality.
- Retain access-controlled, tamper-evident evidence where risk requires it. A local log is not automatically immutable or authoritative proof.

## Troubleshooting And Red Flags
| Symptom / Red Flag | First Evidence | Correction And Verification |
|---|---|---|
| "Works on Wasmtime, fails in browser" | Artifact kind, imports, JS binding/shim, browser feature support | Supply a supported boundary or restrict the target; run actual browser tests |
| "Portable" code branches on host globals | Core dependency/import map | Move host concerns into explicit ports; rerun behavior tests before changing semantics |
| Same schema, different result | Units, float precision, state/model/config versions, captured I/O | Fix the semantic contract and compare the same complete context |
| Policy field never evaluated | Enforcement trace and negative test | Implement its gate or label it unsupported; do not claim compliance |
| CPU limit but requests hang | Guest vs host-call timings, cancellation path | Bound host I/O/queue/cleanup separately; test blocked dependency and infinite loop |
| Sandbox within budget, host OOM | Process RSS, buffers, tables, instances, concurrency | Add total host/process limits and admission control; repeat sustained load |
| Duplicate effects on reconnect/replay | Idempotency key, commit/ACK order, durable inbox/outbox | Make effect and dedup atomic where possible; reconcile ambiguous external effects |
| Rollback breaks an old client | WIT/schema/semantic/permission changes, state format | Preserve tested compatibility or perform an explicit migration; test old fleet profiles |
| Unexplained provider/plan change | Registry snapshot, policy revision, selection/approval record | Pin resolution or reapprove a bounded plan; do not silently substitute authority/quality |

## Current Specification Checks
Verify mechanisms against [Wasmtime security](https://docs.wasmtime.dev/security.html), [interruption](https://docs.wasmtime.dev/examples-interrupting-wasm.html), [deterministic execution](https://docs.wasmtime.dev/examples-deterministic-wasm-execution.html), and [store limits](https://docs.wasmtime.dev/api/wasmtime/struct.StoreLimitsBuilder.html). Support and configuration are version-specific; production evidence belongs with the project, not a private literature directory.
