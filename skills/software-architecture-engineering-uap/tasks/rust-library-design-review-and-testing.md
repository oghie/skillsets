# Rust Library Design, Review, And Testing

Use this task when a user asks to create, design, write, review, refactor, test, publish, or troubleshoot a Rust library, crate, SDK, parser, data structure, macro crate, FFI wrapper, async library, `no_std` crate, or reusable internal crate.

## Inputs

Scope the work before judging the crate: define the goal, non-goals, target caller workflows, acceptance criteria, and which contracts are allowed to change. This prevents the review from drifting into generic Rust style advice.

Collect only what is needed:
- Library purpose, caller personas, and the workflows the public API must support.
- Requirements, use cases, stakeholders, and quality attributes that drive the public API.
- Existing repository, `Cargo.toml`, module tree, examples, docs, tests, CI, and release history.
- Target users: internal team, public crates.io users, enterprise users pinned to older toolchains, embedded users, FFI consumers, or generated-code users.
- Compatibility expectations: SemVer strictness, MSRV policy, supported targets, feature flags, default features, and deprecation tolerance.
- Risk surface: untrusted input, unsafe code, FFI, async runtime, concurrency, `no_std`, allocation limits, security/crypto-adjacent behavior, performance-critical loops.
- Verification budget and available tools.

If evidence is missing, state exactly which contract cannot be judged yet and why it matters.

## Classification

Classify before designing:

| Crate Type | Architectural Bias |
|---|---|
| Small internal helper | Minimize public surface; optimize for clarity and tests, not generic extensibility. |
| Public library | Treat API, docs, feature flags, MSRV, and SemVer as first-class architecture. |
| SDK/client | Prioritize error semantics, timeout/cancellation, credential or claim propagation, retries, token/session handling where applicable, versioned contracts, and fake-server tests. |
| Parser/decoder | Prioritize invalid input, fuzzing, allocation limits, streaming boundaries, and precise errors. |
| Data structure | Prioritize invariants, operation sequences, model comparisons, unsafe boundaries, and performance regression. |
| Async crate | Prioritize runtime contract, cancellation safety, `Send` futures, blocking work, and shutdown. |
| Macro crate | Prioritize diagnostics, generated API stability, compile-fail tests, and compile-time cost. |
| FFI wrapper | Prioritize ABI, allocator ownership, lifetimes, safe wrapper, panic boundary, and build scripts. |
| `no_std` crate | Prioritize accidental `std`, allocator policy, target matrix, panic/OOM behavior, and fallible APIs. |

## Design Workflow

1. State `Fact`, `Inference`, `Assumption`, and `Question`.
2. Record key decisions, rationale, rejected alternatives, trade-offs, and verification before implementation.
3. Define the contract:
   - public modules and re-exports;
   - types, fields, enum variants, traits, functions, builders;
   - feature flags and default features;
   - error, panic, async, blocking, allocation, thread-safety, and target behavior.
4. Choose the smallest stable API:
   - private fields over public fields;
   - constructors/builders over struct literals when evolution is expected;
   - `#[non_exhaustive]` where downstream exhaustive matching should not be promised;
   - newtypes/enums/type-state for misuse-resistant states;
   - wrappers over exposed dependency types unless dependency exposure is deliberate.
5. Decide trait strategy:
   - expected common traits and why;
   - `Send`/`Sync`/`Unpin` guarantees;
   - public trait implementation policy;
   - sealed traits when downstream implementation is not intended;
   - default methods for future evolution.
6. Decide Cargo architecture:
   - workspace/subcrate split;
   - feature names and additive behavior;
   - optional dependencies and default features;
   - MSRV policy;
   - supported targets;
   - package metadata and publish policy.
7. Decide risk-specific boundaries:
   - unsafe encapsulation and `SAFETY:` comments;
   - FFI safe wrapper and allocation/free ownership;
   - `no_std`/`alloc`/panic/OOM policy;
   - async runtime and cancellation model;
   - concurrency model and synchronization verification;
   - macro diagnostics and generated-code visibility.
8. Convert decisions into tests, CI checks, examples, docs, and release gates.

Apply modularity principles explicitly: name coupling, cohesion, dependency direction, and the volatile decision each module or subcrate hides. If compile time, binary size, benchmark runtime, or maintainer effort drives a split, include a lightweight estimate, resource-usage observation, or benchmark trend.

## Review Workflow

Lead with findings, ordered by impact.

For each finding, include:
- Location.
- Contract affected.
- Downstream/user impact.
- Evidence.
- Recommended smallest fix.
- Verification.

Review in this order:
1. Public API compatibility and caller ergonomics.
2. Error/panic contracts and documented safety.
3. Cargo features, dependencies, MSRV, target support, and package metadata.
4. Unsafe/FFI/`no_std`/async/concurrency risks.
5. Test matrix and CI gaps.
6. Performance, compile time, and operational/release risks.
7. Documentation and examples as executable contract.

Do not mistake private implementation cleanliness for public API readiness. A clean implementation with a careless public contract is still a bad library.

## Testing Workflow

Build the test matrix from risks:

1. Contract tests:
   - integration tests in `tests/`;
   - doctests and examples;
   - downstream-style smoke crate when public compatibility matters.
2. Correctness tests:
   - unit tests for internal algorithms;
   - edge and invalid input cases;
   - golden/regression tests where output compatibility matters.
3. Generated tests:
   - property-based tests for invariants;
   - fuzzing for parsers/decoders/untrusted input;
   - differential tests against a simple reference implementation;
   - metamorphic tests for behavior relationships.
4. Compile-time tests:
   - `compile_fail` doctests or `trybuild`;
   - static assertions for auto-traits, size, alignment, and type-state guarantees.
5. Matrix tests:
   - `default`, `--all-features`, `--no-default-features`;
   - feature powerset when public feature combinations matter;
   - MSRV toolchain;
   - supported targets.
6. Risk-specific tests:
   - Miri/sanitizer for unsafe code;
   - loom/stress for concurrency;
   - ABI/header smoke tests for FFI;
   - target build for `no_std`;
   - cancellation/runtime tests for async;
   - `cargo expand` and compile-fail diagnostics for macros.
7. Release checks:
   - docs, package, changelog, SemVer review, dependency audit, benchmark regression where relevant.

## Command Menu

Use only commands that fit the project and installed tools:

```bash
cargo fmt --all -- --check
cargo clippy --workspace --all-targets --all-features -- -D warnings
cargo test --workspace
cargo test --workspace --all-features
cargo test --workspace --no-default-features
cargo test --workspace --doc
cargo doc --workspace --all-features --no-deps
cargo package
cargo tree -e features
```

Optional risk checks:

```bash
cargo hack test --feature-powerset
cargo +<msrv> check --workspace --all-targets
cargo +nightly miri test
cargo fuzz run <target>
cargo bench
```

Tool availability, flags, and current Rust behavior are version-sensitive. Verify current local tool behavior before treating a command as authoritative.

## Handoff Output

```markdown
## Rust Library Architecture
- Facts:
- Inferences:
- Assumptions:
- Questions:
- Crate type:
- Public contract:
- API design:
- Error/panic model:
- Feature/dependency/MSRV policy:
- Unsafe/FFI/no_std/async/concurrency risks:
- Test matrix:
- Release gate:
- Residual risk:
```

## Review Output

```markdown
## Findings
- Severity:
  Location:
  Contract risk:
  Downstream impact:
  Evidence:
  Recommended fix:
  Verification:

## Open Questions
## Residual Risk
## Suggested Release Gate
```
