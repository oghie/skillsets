# Portable Capability Decisions And Trade-Offs

## Mental Model
Reason about **behavior before location**, but never ignore location's constraints. A capability has an outcome, a quality tier, and a resource budget. Its contract captures intent; its core implements business behavior; its envelope binds that behavior to an actual host.

These are independent questions:
- **Business boundary:** which invariant, owner, state, and reason to change belong together?
- **Implementation boundary:** which domain computation can remain independent of host APIs?
- **Execution boundary:** which module/component/native artifact and host actually run it?
- **Deployment boundary:** is this an in-process plugin, service, container, function, or device application?
- **Authority boundary:** who may approve, invoke, persist, or trust its result?

Do not turn every capability into a microservice. Do not equate one contract with one process: a service may expose several cohesive contracts, and one contract may have multiple implementations with distinct declared quality profiles.

UMA is an architectural model for portable, contract-described capabilities. It is not an industry-wide conformance standard, a WASI release, or the Unified Architecture Process. Adopt its useful constraints selectively; reject unsupported universal guarantees.

## Suitability Decision
| Option | Strong Fit | Main Liability | Evidence Needed |
|---|---|---|---|
| Local module/shared source | One ecosystem or predictable build targets | Compile-time/framework coupling, divergent forks | Dependency direction, characterization and target tests |
| Native library/shared SDK | Controlled callers need platform integration | ABI/allocator/OS compatibility, privileged execution | ABI contract, supported triples, safe wrappers, release tests |
| Remote API | Central data and authoritative decisions dominate | Network availability, latency, egress, backend capacity | SLO under network failure, auth, rate limits, offline policy |
| Core Wasm module | Portable compute or a small sandboxed plugin with explicit imports | Low-level ABI, host glue, optional feature support | Actual imports/exports, memory protocol, engine tests |
| WASI module | Existing command/module ecosystem needs system interfaces | API subset and runtime/version assumptions | Exact WASI imports, preopens/grants, executable target tests |
| Component Model | Typed cross-language plugin/component composition matters | Bindings/tooling/version/host support | WIT world, compiled component validation, host integration tests |
| Hybrid Wasm/native/GPU | One semantic operation benefits from specialized implementations | Quality/numeric drift, data copying, larger attack surface | Explicit profile selection and semantic/performance comparison |

Prefer portable compute when duplicated rules demonstrably drift across products, offline execution is required, or untrusted extensions need a controlled host boundary. Good candidates include parsers, validators, transforms, policy calculations, feature evaluation, codecs, and bounded inference kernels. These still need artifact and host verification.

Prefer centralized authority for secrets, settlement, credential issuance, durable shared state, and system-wide coordination. A local rule evaluation may improve responsiveness without becoming the trusted source of authorization.

Defer Wasm when one runtime suffices, the useful work is mostly platform I/O, native dependencies dominate, serialization/copy cost defeats locality, safety certification is unresolved, or fleet/tooling complexity exceeds demonstrated benefits.

## Boundary Critique
Ask these questions before splitting:
1. Can the outcome be described without listing implementation steps?
2. Can it finish meaningfully without undocumented coordination?
3. Which transaction and invariant must remain atomic?
4. Do owner, change cadence, state scope, failure domain, latency class, or trust domain materially differ?
5. Do observed call/event patterns show chatty fragments or independently useful behavior?
6. Is the proposed reuse conceptual, or merely similar-looking code with different business meanings?

Merge fragments that always travel together and add only routing/serialization cost. Split only when independent semantics, evolution, authority, or deployment needs justify the coordination. A single-sentence description is a clarity check, not sufficient proof of a correct boundary. No universal hop-count, subscriber-count, service-size, or "90 percent portable" threshold establishes quality.

## Placement Is Constrained Optimization
Evaluate hard constraints before ranking eligible providers by soft preferences.

| Dimension | Questions That Change Placement |
|---|---|
| Authority | Is this host controlled? Can clients forge inputs/results? Where is final approval? |
| Data | Where is the authoritative snapshot? Are locality, privacy, classification, and freshness satisfied? |
| Latency | What are end-to-end p95/p99, cold-start/download cost, host-call cost, and queueing delay? |
| Resources | Are memory, sustained CPU/GPU, battery, thermals, and concurrency sufficient? |
| Connectivity | What happens offline, during partitions, and after reconnect with stale policies/state? |
| Economics | Include distribution, egress, device energy, adapter maintenance, support, telemetry, and security patching |
| Operations | Who owns updates, crash recovery, key rotation, revocation, rollback, and heterogeneous client versions? |

Client placement removes some network hops, not all latency or security risk. Edge placement may improve locality, not guarantee connectivity or strong trust. Cloud placement provides controllable infrastructure, not inherently correct authorization or unlimited capacity. Mobile browser execution and a native mobile embedding are different targets.

If placement changes dynamically, specify eligible target profiles, selection owner, tie-breaks, telemetry freshness, hysteresis, rate limits on movement, and state-transfer prerequisites. Otherwise adaptive routing can oscillate, amplify overload, or send protected data to an ineligible host. A metadata field cannot provision capacity or implement a scheduler by itself.

## Sector Forces
Use these as questions, not predefined compliance or product guarantees.

| Context | Useful Portable Behavior | Boundary That Must Remain Explicit |
|---|---|---|
| Banking/payments/insurance | Local quote, validation, feature/risk hint | Trusted authorization, settlement, fraud control, freshness, reconciliation; offline approval needs explicit delegated authority and limits |
| Energy/manufacturing/oil and gas | Local transforms, inspection, diagnostics | Safety/control deadlines, WCET, fail-safe state, native drivers, and certification evidence |
| Healthcare | Local redaction, image preprocessing, assisted analysis | Patient privacy, clinical quality, model/version traceability, human oversight, and approved degradation |
| Logistics/agriculture | Offline capture, route hints, sensor aggregation | Conflict resolution, ordering scope, data loss, device storage quotas, location privacy |
| Government/defense | Restricted-domain processing and portable tooling | Offline trust roots, air-gap updates, residency, signed artifacts, explicit authority |
| Education/non-profit | Low-connectivity validation and learning transforms | Low-end devices, download budget, accessibility, equitable fallback, support capacity |
| Media/technology | Codecs, filters, sandboxed extensions | SIMD/GPU support, host-copy cost, untrusted content, licensing, quality differences |
| Enterprise/FMCG/consulting | Shared business rules across integrations | Existing ERP/SOA contracts, ownership, legacy semantics, update windows, migration cost |

Route deadline/scheduling proofs to `../../realtime-systems-coding/SKILL.md`, state/CDC/data migration to `../../data-architect-engineering/SKILL.md`, and UI/browser interaction/accessibility to `../../uiux-frontend-engineering/SKILL.md`. Keep this skill responsible for the architecture decision. Do not recursively bounce ownership between skills.

## Brownfield Adoption
1. Inventory deployed behaviors, consumers, implicit contracts, incidents, and governed/ungoverned paths.
2. Characterize observed legacy semantics, including error, timing, side-effect, and state behavior.
3. Put a versioned facade/anti-corruption boundary around one high-value capability. Retain the legacy implementation.
4. Add observability and contract testing; use observe-only policy evaluation only where it cannot weaken existing security controls.
5. Extract a portable core and bind one target-specific envelope at a time.
6. Compare with isolated shadow execution: no real writes, payments, messages, or other side effects from the shadow path.
7. Canary compatible traffic, reconcile state, and keep explicit rollback and fleet support windows.
8. Expand only if measured correctness, cost, maintainability, and operational results justify it.

Do not declare compatibility merely by adding `backward_compatible_from`. Verify actual consumers, serializers, semantics, permissions, and side effects. Keep data/state migrations separate from contract routing changes. Full rewrites are not automatically wrong, but require evidence that staged boundary repair cannot meet the constraints.

## Decision Record
Record outcome and invariant; alternatives; component/service boundary rationale; target matrix; authority/state owners; enforced vs aspirational constraints; measured workload; costs; failure/degraded behavior; implementation evidence; rollout/rollback; and revisit trigger. Select the smallest model that can be implemented and operated, not the most universal diagram.
