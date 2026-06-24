# Rust Library Contract Matrix

Use this matrix during Rust crate design, review, release planning, or SemVer audit.

| Contract Area | Decision | Public Surface | Compatibility Risk | Verification | Owner |
|---|---|---|---|---|---|
| Crate purpose |  | README, crate docs | Wrong abstraction or caller mismatch | Usage scenario review |  |
| Supported callers |  | Examples, docs | Missing workflow or over-general API | Downstream-style smoke crate |  |
| Modules/re-exports |  | `pub mod`, `pub use` | Dependency type becomes API | Public API diff |  |
| Types |  | structs, enums, newtypes | Field/variant evolution blocked | Compile checks, SemVer review |  |
| Traits |  | public traits, blanket impls | Downstream impl breakage | Sealed/default-method review |  |
| Auto-traits |  | `Send`, `Sync`, `Unpin` | Hidden breaking change | Static assertions |  |
| Errors |  | error enum/opaque error | Caller cannot recover or API leaks internals | Error contract tests |  |
| Panics |  | docs, infallible APIs | Runtime crash on recoverable input | Panic/invalid-input tests |  |
| Features |  | `Cargo.toml` features | Non-additive or conflicting combos | Feature matrix checks |  |
| Dependencies |  | public types, optional deps | MSRV/license/security/compile-time risk | `cargo tree`, audit tools |  |
| MSRV |  | `rust-version`, policy | Enterprise/toolchain breakage | `cargo +<msrv> check` |  |
| Async/runtime |  | async API, spawned tasks | Hidden runtime coupling | Runtime/cancellation tests |  |
| Unsafe |  | unsafe fn/traits, safe wrappers | Undefined behavior | Miri, `SAFETY:` review |  |
| FFI |  | ABI, headers, raw handles | allocator/lifetime/panic bugs | ABI smoke tests |  |
| `no_std` |  | crate attrs, `std` feature | false portability claim | target build |  |
| Macros |  | derives, attributes, generated code | bad diagnostics/API drift | `trybuild`, `cargo expand` |  |
| Performance |  | algorithms, hot paths | regression or compile-time bloat | criterion/workload bench |  |
| Packaging |  | metadata, include/exclude | bad release artifact | `cargo package` |  |
