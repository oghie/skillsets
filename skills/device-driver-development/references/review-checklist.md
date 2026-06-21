# Driver Review Checklist

## Architecture
- [ ] Kernel version, target architecture, bus, device class, and subsystem are explicit.
- [ ] The chosen subsystem is justified against existing kernel ABI/frameworks.
- [ ] Datasheet register map, reset values, timing, IRQ behavior, and power sequencing are referenced or marked unknown.
- [ ] DT binding models hardware resources and includes compatible, `reg`, interrupts, clocks, resets, supplies, GPIOs, pinctrl, DMA, and child nodes as applicable.

## Probe and Teardown
- [ ] `probe()` validates hardware identity and required resources before exposing user/kernel interfaces.
- [ ] Resource acquisition order is clear; `devm_*` or cleanup labels cover every failure path.
- [ ] `remove()`/unbind/suspend cancels work, disables IRQ/DMA/timers, and prevents use-after-free.
- [ ] Runtime PM, wake IRQ, regulator, clock, reset, and pinctrl state transitions are balanced.

## Concurrency
- [ ] Each shared field has an owner and locking rule.
- [ ] Atomic and sleepable contexts are separated.
- [ ] Mutexes are not used in IRQ/timer/atomic paths.
- [ ] Spinlocks are short and do not wrap sleeping bus calls.
- [ ] Wait queues, completions, and poll conditions are updated before wakeups.

## Memory and I/O
- [ ] MMIO uses `__iomem` accessors and mapping helpers.
- [ ] DMA buffers use the DMA API, correct direction, correct mask, and mapped lifetime.
- [ ] Endianness, alignment, register width, and barriers are addressed.
- [ ] `mmap` validates VMA size/offset/protection and documents cache attributes.

## ABI and Security
- [ ] User input sizes, offsets, enum values, and ioctl commands are validated.
- [ ] `copy_to_user()` and `copy_from_user()` return values are handled.
- [ ] No kernel pointers, uninitialized bytes, stale buffers, or device secrets leak to userspace.
- [ ] sysfs files are stable, minimal, one-value-per-file, and not debug-only.
- [ ] debugfs content is optional and never required for normal operation.

## Build and Runtime Evidence
- [ ] Builds with `W=1` and no relevant warnings.
- [ ] `sparse`, Smatch, Coccinelle, `checkpatch.pl`, `dt_binding_check`, or local equivalents were run when available.
- [ ] QEMU/KGDB crash-debug path exists for unsafe or hard-to-reproduce failures.
- [ ] bpftrace/ftrace/dynamic-debug evidence exists for runtime paths that cannot be proven by logs alone.
- [ ] Syzkaller or targeted fuzzing is considered for every externally reachable ABI surface.
- [ ] Load/unload, probe failure, unbind/rebind, suspend/resume, and userspace API tests are covered as applicable.
- [ ] Logs include driver name, device identity, relevant errors, and no noisy success spam.
- [ ] Hardware evidence exists for IRQ count, bus transactions, register reads/writes, DMA completion, and visible output/events.
