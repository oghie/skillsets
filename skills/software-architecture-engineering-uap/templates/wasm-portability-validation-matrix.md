# Portable Capability Validation Matrix

## Decision And Contract
- Capability/outcome and owner:
- Business invariants, state authority, and trusted decision boundary:
- Portability need and rejected simpler alternatives:
- Contract/world/version/digest; artifact/build provenance:
- Semantic input/output, units, encoding, errors, permitted degraded profiles:
- Workload and quality/SLO scenarios; budget units:
- Consumers, compatibility rules, and supported fleet window:
- Current unknowns: `This needs verification.` where applicable.

## Target Evidence
Create one row per concrete target/version/profile, not one vague row for all browsers or edges.

| Target / CPU / OS / Engine / Version | Artifact / ABI / WASI / WIT | Required Features And Imports | Adapter / Config / Policy Versions | Core And Adapter Conformance | Negative Security / Budget Tests | Load / Offline / Recovery Evidence | Status / Owner / Date |
|---|---|---|---|---|---|---|---|
| Actual browser/device profile | | | | | | | |
| Actual edge profile | | | | | | | |
| Actual cloud embedding | | | | | | | |
| Native alternative, if selected | | | | | | | |

Status is `declared`, `implemented`, `verified`, `unsupported`, or `blocked`. Attach commands, exit codes, fixture/workload IDs, artifact hashes, traces, and reports. "Verified" must name its scope; absent evidence is not a pass.

## Enforcement Map
| Contract Requirement | Authority / Enforcement Point | Mechanism And Configuration | Denial / Failure Test | Observed Result | Gap / Owner |
|---|---|---|---|---|---|
| Publisher/artifact authenticity | | | | | |
| Caller/tenant/resource authorization | | | | | |
| Required imports and placement | | | | | |
| Input/output semantic bounds | | | | | |
| Guest and total host memory | | | | | |
| Guest execution and host-call deadline | | | | | |
| Concurrency / queue / output limits | | | | | |
| State transition and deduplication | | | | | |
| Policy freshness / revocation | | | | | |
| Privacy / telemetry / audit | | | | | |

## Comparison And Operations
- Comparison scope: shape, semantic equivalence, exact replay, or quality tolerance; name any excluded telemetry fields without excluding business values.
- Captured inputs/state/config/model/I/O/time/random context:
- Cold/warm latency, p50/p95/p99 window/sample size, offered load, errors, queueing, setup, copies/host I/O, guest/host memory, CPU/GPU, mobile energy:
- Transport semantics, required graph dependencies, resolution/fan-out, cycle limits, declared/resolved/observed topology diff:
- Agent decision/approval/effect evidence and bounded budgets, only if agents are selected:
- Permitted fallback/degraded outcomes and rejection conditions:
- Canary gates, owners, alerts, support and deprecation window:
- Rollback artifact/contract/adapter/policy combination, state recovery, revocation and offline-client behavior:
- Decision: proceed / limited pilot / defer / reject; residual risks and revisit trigger:
