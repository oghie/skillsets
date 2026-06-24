# Rust Library Architecture

Use this reference when the architecture work is a Rust library, crate, SDK, parser, client, data structure, async crate, macro crate, FFI wrapper, `no_std` crate, or reusable internal library.

## Core Position

A Rust library is an architecture contract, not just a package of code. Every public item is part of the contract: `pub` modules, functions, structs, fields, enum variants, traits, associated types, generic bounds, feature flags, error variants, re-exports, MSRV policy, docs, examples, and observed auto-traits such as `Send`, `Sync`, and `Unpin`.

The default posture is conservative:
- Promise less in the public API than the implementation can do.
- Encode misuse-resistant rules in types when the rules are stable.
- Keep internals private so the implementation can evolve.
- Treat feature flags, dependencies, `unsafe`, FFI, `no_std`, and macros as architecture decisions with compatibility cost.
- Test the public contract across versions, features, targets, invalid inputs, docs, and downstream-style usage.

## Architecture Map

| Architecture Concern | Rust Library Translation | Evidence To Inspect |
|---|---|---|
| System boundary | Public crate API, re-exports, feature-gated modules, FFI ABI, generated macros | `src/lib.rs`, public docs, `Cargo.toml`, exported symbols |
| Component view | Modules, subcrates, workspaces, hidden/internal modules, facade/prelude | module tree, workspace members, dependency graph |
| Information view | Public structs/enums, ownership model, lifetimes, error types, opaque handles | type definitions, trait bounds, constructors |
| Behavior view | Builder flows, state transitions, async/runtime behavior, drop/cleanup, retries | examples, tests, state-machine types, cancellation paths |
| Deployment view | `std`/`no_std`, target triples, linker/build scripts, `cdylib`/`staticlib`, allocator needs | Cargo config, `build.rs`, CI target matrix |
| NFRs | Compatibility, safety, portability, performance, compile time, security, binary size | SemVer policy, MSRV, Miri/fuzz/bench, cargo tree |

## Public API Contract

Start by drawing the contract surface:
- `pub` modules, items, fields, enum variants, trait methods, associated types, and constants.
- `pub(crate)` or private modules that are reachable through macros or generated code.
- re-exported foreign types or trait implementations.
- public generic bounds and return types, including `impl Trait` and `dyn Trait`.
- public feature names and default features.
- documented panic, error, async, blocking, thread-safety, and allocation behavior.

Reductive rule: if a downstream crate can compile against it, pattern-match it, import it, rely on it, implement it, or observe it through docs/examples, treat it as contract.

### Contract Stability Tactics

| Risk | Prefer |
|---|---|
| Public field or tuple struct constrains future layout | Private fields plus constructors/getters; `#[non_exhaustive]` when evolution is expected |
| Exhaustive public enum blocks future variants | `#[non_exhaustive]` for error/domain enums likely to grow |
| Exposed dependency type makes dependency upgrade breaking | Newtype wrapper, owned DTO, or `impl Trait` return when sufficient |
| Public trait will need new methods | Default methods, sealed trait if downstream implementation is not intended |
| Auto-traits accidentally change | Compile-time tests for `Send`, `Sync`, `Unpin`, size, and alignment where contract-relevant |
| Hidden macro support API leaks | `#[doc(hidden)]` plus clear internal-contract docs and tests |

## Interface Design

Use four filters for every public interface.

### Unsurprising
- Use established names with established semantics: `new`, `try_new`, `from_*`, `into_*`, `as_*`, `iter`, `into_inner`, `Error`.
- Implement expected traits when semantically valid: `Debug`, `Clone`, `Default`, `PartialEq`, `Eq`, `Hash`, `Ord`, `From`, `TryFrom`, `Display`, `Error`.
- Document why a common trait is intentionally absent, especially `Send`, `Sync`, `Clone`, or `Debug`.
- Implement `IntoIterator` for owned and borrowed forms when collection-like usage is expected.
- Avoid `Copy` unless the type is very likely to stay trivially copyable; removing `Copy` is a breaking change.

### Flexible
- Accept borrowed data when ownership is not needed: `&str`, `&[u8]`, `&Path`, `impl AsRef<Path>`.
- Use `impl Into<String>` only when the function stores an owned `String`.
- Prefer `Cow<'_, T>` only when the caller benefits from either borrowed or owned return values.
- Do not over-genericize every argument; use generics where callers reasonably have multiple useful input types.
- Be explicit when choosing dynamic dispatch: caller cannot opt out of `dyn Trait` overhead if the API requires it.

### Obvious
- Replace multiple `bool` arguments with semantic enums or option structs.
- Use newtypes for units, identifiers, capabilities, and validated strings.
- Use type-state or marker types when call order or state transitions are critical.
- Add `#[must_use]` to builder/config/result-like values where ignoring the value is likely a bug.
- Make fallible operations return `Result`; do not hide recoverable errors behind panics.

Example type-state shape:

```rust
pub struct Client<State = Unauthenticated> {
    endpoint: String,
    state: std::marker::PhantomData<State>,
}

pub struct Unauthenticated;
pub struct Authenticated;

impl Client<Unauthenticated> {
    pub fn login(self, token: Token) -> Result<Client<Authenticated>, Error> {
        validate_token(&token)?;
        Ok(Client { endpoint: self.endpoint, state: std::marker::PhantomData })
    }
}

impl Client<Authenticated> {
    pub fn send(&self, request: Request) -> Result<Response, Error> {
        send_authenticated(&self.endpoint, request)
    }
}
```

### Constrained
- Keep internal modules private by default.
- Avoid public constructors that prevent future private fields.
- Use builders for configuration with many optional fields, validation, or future expansion.
- Avoid exposing data structures that encode incidental implementation detail.
- Design `Drop` carefully. Destructors cannot return errors and should not block unexpectedly; provide explicit `close`, `flush`, or `shutdown` when failure or blocking matters.

## Errors And Panics

Error design is part of API design.

Use structured errors when callers can act differently:

```rust
#[derive(Debug)]
#[non_exhaustive]
pub enum Error {
    InvalidInput { field: &'static str },
    Io(std::io::Error),
}

impl std::fmt::Display for Error {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Error::InvalidInput { field } => write!(f, "invalid input: {field}"),
            Error::Io(err) => write!(f, "io error: {err}"),
        }
    }
}

impl std::error::Error for Error {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            Error::Io(err) => Some(err),
            _ => None,
        }
    }
}
```

Use opaque errors when callers only need display/logging and the library must preserve internal evolution. Do not leak vendor or parser internals through the public error type unless that dependency is deliberately part of the contract.

Document:
- `# Errors` for fallible public functions.
- `# Panics` for documented panics.
- `# Safety` for every `unsafe fn` and every unsafe trait.
- cancellation, timeout, retry, and cleanup semantics for async or IO-heavy APIs.

Panic policy:
- Panic only for programmer bugs, impossible states, or explicit infallible APIs whose preconditions are documented.
- Prefer `try_` methods for allocation, parsing, IO, and external input.
- In `no_std`, kernel, embedded, or host-plugin contexts, panics can be operationally unacceptable; provide fallible variants where possible.

## Cargo, Features, And Dependencies

Feature flags are architecture controls. They must be additive unless there is a carefully documented incompatibility.

Rules:
- Features may add modules, trait implementations, optional dependencies, integrations, or richer APIs.
- Features should not remove public APIs, replace signatures, or make previously compiling downstream combinations fail.
- Avoid mutually exclusive features. If unavoidable, add explicit compile errors and document the incompatibility.
- Prefer a `std` feature that enables standard-library support over a `no_std` feature that disables it.
- Test `default`, `--no-default-features`, `--all-features`, and feature powersets for public crates.
- Use `#[doc(cfg(...))]` for feature-gated public APIs when available in the chosen toolchain.

Dependency decisions:
- Every dependency adds compile time, feature unification risk, MSRV pressure, license/security review, and transitive compatibility exposure.
- Optional dependencies should be feature-gated and absent by default unless most users need them.
- Avoid re-exporting dependency types unless the dependency is intentionally part of the API contract.
- Audit the graph for duplicate major versions, vulnerabilities, license policy, unused dependencies, and feature activation paths.
- Pin or bound dependency versions only when MSRV, audit, compatibility, or reproducibility requires it.

MSRV and SemVer:
- Declare an MSRV policy when users may depend on stable old toolchains.
- Check MSRV in CI with a concrete toolchain command.
- Treat MSRV changes as user-visible; at minimum document them and usually bump minor version.
- Run a SemVer review before release: public fields, variants, trait methods, bounds, feature defaults, re-exports, auto-traits, and dependency type exposure can all break downstream code.

## Async And Runtime Contract

Async libraries must state their runtime assumptions.

Decide and document:
- runtime-specific vs runtime-agnostic API;
- sync API, async API, or both;
- blocking behavior inside async functions;
- cancellation safety and drop behavior for futures;
- spawned tasks, background workers, shutdown hooks, and resource cleanup;
- `Send` requirements on futures and handles;
- timeout and retry ownership.

Avoid hidden runtime capture. A library that silently starts tasks, blocks a runtime worker, or requires one runtime while pretending to be generic creates architecture coupling for every consumer.

## Unsafe, FFI, And Low-Level Boundaries

Use `unsafe` only to encode invariants the compiler cannot verify. It is not a shortcut around Rust rules.

Unsafe discipline:
- Encapsulate unsafety behind a small private module or crate with a safe public interface when possible.
- Keep unsafe blocks small, but audit at the privacy boundary that can affect the invariant.
- Add a `SAFETY:` comment immediately before each unsafe block explaining why every required invariant holds.
- Keep `unsafe fn` unsafe if the caller must uphold invariants, even for internal APIs.
- Use assertions or `debug_assert!` to defend invariants before undefined behavior is possible.
- Run Miri and sanitizer/fuzz/stress tests when unsafe code is material.

Example review target:

```rust
// SAFETY: `idx` is checked against `items.len()` immediately above, and no
// mutation of `items` occurs between the check and unchecked access.
let item = unsafe { items.get_unchecked(idx) };
```

FFI design:
- Prefer safe Rust wrappers over raw FFI bindings.
- Use `repr(C)` or `repr(transparent)` only when layout compatibility is required and understood.
- Do not pass Rust `String`, `Vec`, trait objects, or non-FFI-safe enums directly across C ABI boundaries.
- Pair allocation and deallocation on the same side of the boundary or expose explicit free/destroy functions.
- Avoid panics crossing FFI boundaries; translate panics and errors into ABI-safe error codes or handles.
- Model pointer lifetimes and mutability in safe wrappers; use distinct opaque pointer types to prevent confusion.
- Isolate `*-sys` crates from ergonomic wrapper crates when binding large native libraries.

`no_std` design:
- Use `#![no_std]` for compatibility only when tested against a target that lacks `std`.
- Use `alloc` only when an allocator is available and acceptable.
- Provide fallible allocation paths for constrained environments.
- Define panic, out-of-memory, volatile memory access, and target-specific behavior when the library touches low-level runtime constraints.
- Use type-state and ownership to make hardware or resource states impossible to misuse.

## Macros

Macro APIs are public APIs.

Use macros when they remove real user burden that ordinary functions, traits, builders, or derives cannot handle cleanly. Avoid macros as syntax decoration.

Review:
- Is generated code visible enough through docs and examples?
- Does `cargo expand` output remain understandable?
- Are spans and diagnostics helpful?
- Does the macro crate pull heavy dependencies into default builds?
- Are compile-fail tests present for bad input?
- Are hidden support items documented and versioned as part of the macro contract where their effects leak?
- Is compile-time cost measured or at least estimated with a resource-usage signal before adding heavy procedural macro dependencies?

## Testing Strategy

A senior Rust library test plan is a risk matrix, not a list of unit tests.

| Risk | Test/Evidence |
|---|---|
| Public contract | Integration tests in `tests/`, doctests, examples, downstream-style smoke crate |
| Error semantics | Expected variants, `Display`, source chain, no panic on recoverable input |
| Boundary/edge inputs | Empty, max size, invalid UTF-8, malformed bytes, huge input, duplicate operations |
| Algebraic behavior | Property-based tests for invariants, round-trips, idempotence, ordering, monotonicity |
| Parser/decoder robustness | Fuzz targets and corpus regression tests |
| Optimized implementation | Differential tests against simple reference implementation |
| Operation sequences | Generated sequences over stateful APIs |
| Docs as contract | `cargo test --doc`; examples compile and are not misleading |
| Compile-time guarantees | `compile_fail` doctests, `trybuild`, static assertions |
| Feature flags | `--no-default-features`, `--all-features`, and feature-powerset checks |
| MSRV | `cargo +<msrv> check/test` on supported targets |
| SemVer | downstream compatibility check or public API diff review |
| Unsafe | Miri, sanitizer, assertions, fuzz/stress, invariant comments |
| Concurrency | `Send`/`Sync` assertions, stress tests, loom/model checks for low-level sync |
| FFI | ABI smoke tests, allocation/free pairing, panic boundary tests, generated header review |
| Performance | Criterion or workload benchmarks with regression thresholds |
| Packaging | `cargo package`, docs build, examples, license/readme/include checks |

Baseline commands to consider:

```bash
cargo fmt --all -- --check
cargo clippy --workspace --all-targets --all-features -- -D warnings
cargo test --workspace
cargo test --workspace --all-features
cargo test --workspace --no-default-features
cargo test --workspace --doc
cargo doc --workspace --all-features --no-deps
cargo package
```

Optional checks when the project uses the relevant risk:

```bash
cargo hack test --feature-powerset
cargo +<msrv> check --workspace --all-targets
cargo +nightly miri test
cargo fuzz run <target>
cargo bench
cargo tree -e features
cargo tree -i <crate>
```

Tool names and flags are version-sensitive. If a command is material to a current production release, verify the installed toolchain behavior before relying on it.

## Library Type Decision Matrix

| Library Type | Primary Architecture Risk | Extra Checks |
|---|---|---|
| Parser/decoder | malformed input, ambiguous errors, unbounded memory | fuzzing, property tests, invalid corpus, allocation limits |
| Serializer/formatter | non-roundtripping output, compatibility drift | round-trip, golden files, versioned schema tests |
| Client/SDK | API stability, retries, auth propagation, runtime coupling | contract tests, fake server, timeout/cancellation tests |
| Data structure | invariant corruption, perf regression, unsafe shortcuts | model comparison, operation sequences, Miri, benchmarks |
| Async crate | runtime coupling, cancellation, blocking | runtime matrix, cancellation tests, `Send` future assertions |
| FFI wrapper | ABI, lifetime, allocator, panic boundary | safe wrapper tests, header/bindings review, sanitizer |
| Macro crate | poor diagnostics, compile-time cost, generated API drift | `trybuild`, `cargo expand`, compile-time tracking |
| `no_std` crate | accidental `std`, allocation/panic assumptions | target build, `alloc` feature matrix, fallible APIs |
| Security/crypto-adjacent | misuse, side channels, dependency posture | threat model, constant-time review, vetted primitives, fuzzing |

## Release Gate

Before publishing or tagging:
1. Confirm scope, MSRV, supported targets, feature policy, and breaking-change classification.
2. Run formatting, linting, tests, doctests, docs, package, and feature matrix checks.
3. Run risk-specific checks: Miri/loom/fuzz/bench/FFI/target builds.
4. Review public API diff, re-exports, dependency updates, feature defaults, and auto-traits.
5. Verify package metadata: license, readme, repository/homepage, keywords/categories, include/exclude.
6. Update changelog with migration notes and MSRV changes.
7. Document residual risk and the next compatibility trigger.

When compile-time cost, binary size, benchmark runtime, or maintainer effort drives a decision, include a lightweight estimate, resource-usage observation, or benchmark trend instead of treating "cost" as a vague complaint.

## Cross-Skill Mapping

- Use clean-code guidance for naming, function shape, error paths, module cohesion, tests, and refactoring.
- Use architecture-as-code guidance for workspace dependency rules, public API gates, feature matrix CI, and SemVer checks.
- Use security patterns when the crate handles auth, secrets, crypto-adjacent code, untrusted input, or policy enforcement.
- Use realtime/concurrency guidance when the crate implements synchronization, lock-free code, DPDK/XDP/RDMA bindings, or performance-sensitive concurrent runtime behavior.
- Use data architecture guidance when the crate is a DB client, storage engine, query planner, serialization layer, or migration tool.

## Red Flags

- Public API chosen before caller workflows and compatibility policy are known.
- `pub` fields, tuple structs, or enums exposed because it is faster to code.
- Public trait with no decision on downstream implementation and evolution.
- Dependency type appears in public API without deliberate commitment.
- Feature flags are mutually exclusive or change signatures silently.
- `unsafe` block lacks a `SAFETY:` explanation.
- `unsafe fn` lacks a `# Safety` doc contract.
- Async API hides blocking work, runtime requirement, task spawning, or cancellation behavior.
- `no_std` claim is not tested on a target without `std`.
- FFI wrapper lets panics, allocator ownership, or raw opaque pointers leak unsafely.
- Tests only cover happy-path unit behavior, not public contract, feature matrix, docs, invalid input, or downstream usage.
- Release plan lacks SemVer, MSRV, changelog, package, and public API review.

## Prompt Templates

### Rust Library Design

```markdown
Design this Rust library as an architecture contract.
Separate Facts, Inferences, Assumptions, and Questions.
Map the public API surface, caller workflows, error model, feature flags, MSRV/SemVer policy, dependencies, async/runtime assumptions, unsafe/FFI/no_std risks, and test matrix.
Recommend the smallest API that preserves future evolution.
```

### Rust Library Review

```markdown
Review this Rust crate for library architecture risk.
Prioritize public API compatibility, feature flag behavior, dependency exposure, error/panic contracts, unsafe invariants, async/runtime coupling, concurrency guarantees, docs, tests, and release readiness.
For each finding: cite file/line, contract risk, downstream impact, recommended fix, and verification.
```

### Rust Library Testing Plan

```markdown
Create a senior QA test plan for this Rust library.
Classify the crate type, then define tests for public contract, edge cases, errors, properties, fuzz/differential/metamorphic behavior, docs, compile-fail, feature matrix, MSRV, unsafe/Miri, concurrency, performance, packaging, and downstream compatibility.
Name exact commands where possible and mark version-sensitive tools for verification.
```
