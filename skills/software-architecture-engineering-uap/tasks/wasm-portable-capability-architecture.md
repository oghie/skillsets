# Task: Wasm And Portable Capability Architecture

## Goal
Design, implement, review, troubleshoot, or evolve reusable behavior across heterogeneous hosts without confusing a portable binary with a portable system. Use the Unified Architecture Process for traceability; UMA-inspired capability modeling is an optional design technique within it.

## Load By Need
- Suitability, boundaries, placement, sector forces, or brownfield migration: `../references/wasm-portability-decisions.md`.
- Core/envelope separation, WIT/ABI, capability contracts, state, or adapter implementation: `../references/wasm-contracts-and-runtime-boundaries.md`.
- Security, determinism, performance, testing, release, or troubleshooting: `../references/wasm-runtime-security-and-verification.md`.
- Event catalogs, service graphs, MCP, or agent composition: `../references/capability-graphs-and-governed-agents.md`.
- Distributed transactions and delivery: reuse `microservices-pattern-architecture-design.md`; Rust API/FFI/features: reuse `rust-library-design-review-and-testing.md`.

## Required Inputs
- User-visible outcome, business invariant, current behavior evidence, owner, consumers, and non-goals.
- Actual targets: CPU/OS, browser engine or embedding runtime/version, device class, connectivity, deployment lifecycle, and update cadence.
- Required host I/O, state authority, data classification/locality, authorization authority, and external integrations.
- Quality scenarios and workload: correctness/accuracy, freshness, availability, latency, concurrency, memory, energy, cost, and failure tolerance.
- Existing contracts, build artifacts, imports/exports, adapter code, policy enforcement, tests, traces, incidents, and release constraints.

If targets or enforcement mechanisms are unknown, say `This needs verification.` and identify the smallest executable spike. Do not fill a target matrix with invented support.

## Workflow
1. **Challenge the premise.** State why portability might be unnecessary. Compare native/shared code, a remote API, and a portable component; do not introduce microservices, brokers, MCP, or a custom runtime by default.
   - Verify: at least one measured pain or mandatory constraint justifies the added build, adapter, security, and fleet-maintenance cost.
2. **Define the capability boundary.** Specify outcome, quality tier, resource budget, invariants, state ownership, trust/failure domain, and change cadence. A capability may be one module inside a larger bounded context.
   - Verify: it is operationally meaningful, not a pass-through technical layer; split/merge decisions consider transaction, latency, and team ownership.
3. **Define the contract before the new implementation.** Capture semantic inputs/outputs, units, errors, events, degraded outcomes, version compatibility, permissions requested, policy references, and telemetry. For legacy work, characterize actual behavior before declaring a replacement contract.
   - Verify: shape validation, semantic tests, policy checks, and statistical quality measurements are distinct gates with named owners.
4. **Separate core and envelope.** Extract domain computation from file/network/UI/storage/GPU/clock/random/runtime concerns. Define explicit host ports and the adapter binding order.
   - Verify: inspect source dependencies and compiled imports; hidden I/O and state cannot bypass the governed boundary.
5. **Choose artifact and target profiles.** Decide core Wasm module, WASI module, Component Model component, native alternative, or hybrid. Pin WIT/interface versions, features, bindings generator, runtime, and adapters.
   - Verify: validate/instantiate the actual artifact in each intended profile. Browser Wasm support is not native WASI/component support; a shim/transpilation path requires its own evidence.
6. **Implement enforcement, not labels.** Bind authoritative grants, schema/semantic validation, memory and execution controls, host-call limits, cancellation, output limits, and audit behavior. Reject unsupported required capabilities before side effects.
   - Verify: a denied import, tampered artifact, stale/revoked policy, oversized payload, or runaway guest cannot silently reach privileged execution.
7. **Design composition and failure semantics.** Decide direct calls vs events vs durable orchestration. Define persistence, deduplication, ordering scope, retries, backpressure, reconciliation, and permitted fallback. Add discovery or agents only when those solve a separate evidenced problem.
   - Verify: process/network interruption and stale state cannot create duplicate business effects, unauthorized fallback, or an unbounded event/agent loop.
8. **Implement one vertical slice.** Start with a representative pure operation plus the hardest host interaction, on the weakest and strongest relevant targets. Keep unfinished adapters explicitly unsupported.
   - Verify: the same contract suite exercises both nominal and failure paths; fixture parity is not treated as proof of universal equivalence.
9. **Build target-specific evidence.** Run differential/property/fuzz tests, denial tests, load/soak tests, offline recovery, and upgrade/rollback checks. Measure end-to-end behavior, including host and distribution costs.
   - Verify: complete `../templates/wasm-portability-validation-matrix.md`; mark each result declared, implemented, verified, unsupported, or blocked.
10. **Release and maintain coherence.** Bind contract/artifact/adapter/policy/state versions, review topology diffs, canary incrementally, preserve compatible consumers, monitor drift, and deprecate with an explicit support window.
    - Verify: rollback remains valid after state changes; registry loss, offline devices, key rotation, and revocation have tested operational procedures.

## Mode-Specific Work
| Mode | Additional Requirement |
|---|---|
| Greenfield | Begin with one capability and real targets; avoid speculative universal platforms |
| Refactor/migrate | Characterization tests -> governed facade -> isolated core -> side-effect-safe comparison -> phased cutover |
| Review | Lead with severity, evidence, impact, correction, and target-specific verification; distinguish proposed mechanisms from implemented code |
| Troubleshoot | Capture artifact/import/adapter/policy/fixture/state identities; reproduce on the failing target before changing logic |
| Remove/decommission | Find live and offline consumers, remove grants/bindings, reconcile state/events, retain required audit history, and prove safe rejection |

## Stop Conditions
- Stop rollout when required runtime support, authorization, budget enforcement, data semantics, or rollback is unverified.
- Do not weaken security or silently change quality to make a demo pass.
- Do not classify a device-side hint, local validator, or agent proposal as an authoritative decision.
- Do not promise hard real-time behavior from a fuel limit, browser idle callback, or an average benchmark.

## Output
Deliver an architecture judgment, alternatives, capability/contract map, core-envelope boundaries, target matrix, enforcement map, diagrams, implementation tasks, test commands, release/rollback plan, and residual uncertainty. Use `../templates/mermaid-portable-capability-flow.mmd`; add `../templates/mermaid-governed-capability-execution.mmd` only for governed planner execution.
