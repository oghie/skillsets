# Upstream and Maintenance

## Patch Shape
- Keep patches reviewable: bindings first, subsystem driver second, board DT last when possible.
- One logical change per patch. Avoid mixing refactors, formatting, and behavior.
- Follow local subsystem style by reading nearby drivers and maintainer expectations.
- Include `MODULE_LICENSE`, useful `MODULE_DESCRIPTION`, match tables, and Kconfig help.

## Version Awareness
- Check the active kernel tree for changed APIs, renamed callbacks, managed helpers, new subsystem ABI, or deprecated interfaces.
- Prefer modern descriptor APIs and YAML bindings where the current kernel expects them.
- Note when a pattern is intentionally legacy because the target vendor tree is old.

## Documentation
- DT bindings describe hardware. Include constraints, required/optional properties, examples, and compatible fallback strategy.
- User ABI must be documented if it is new or non-obvious.
- Keep debugfs out of required workflows.
- Explain hardware-specific delays, reset order, IRQ clear sequence, and register quirks in comments or commit text.

## Review Preparation
- Run build and static checks.
- Run runtime smoke tests and capture evidence.
- Run `git grep` for similar drivers to compare naming, callback signatures, and error handling.
- Confirm maintainers with `scripts/get_maintainer.pl` when in a kernel tree.
- State residual risks: missing hardware, untested suspend, unavailable analyzer trace, or vendor-tree API difference.

## Long-Term Maintainability
- Minimize private framework code.
- Avoid global state unless hardware truly is singleton.
- Keep ABI extensible with reserved fields or versioning when structures cross userspace.
- Do not expose register poking as ABI except debug-only paths.
- Keep power management and error recovery close to runtime paths, not as an afterthought.
