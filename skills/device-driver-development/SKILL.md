---
name: device-driver-development
description: Use when developing, reviewing, debugging, porting, or engineering Linux kernel device drivers, kernel modules, device tree bindings, bus clients, subsystem drivers, DMA/IRQ/memory paths, userspace interfaces, or hardware bring-up plans.
---

# Device Driver Development

## Core Rule
Treat every driver task as hardware contract engineering: identify the kernel version, hardware bus, subsystem owner, execution context, lifetime model, and userspace ABI before writing code.

## Knowledge Grounding
- Use `references/knowledge-map.md` for the driver domain map and conceptual model.
- Treat API details as version-sensitive; verify callback signatures, helpers, and bindings against the active kernel tree or current kernel docs.

## First Pass
1. Classify the device: char, platform, I2C, SPI, regmap, IIO, GPIO, IRQ controller, input, RTC, PWM, regulator, framebuffer, or NIC.
2. Identify interface surfaces: `/dev`, sysfs, debugfs, ioctl, mmap, netdev, IIO buffers, input events, DT binding, or kernel consumer API.
3. Choose probe/remove lifetime: prefer `devm_*`, explicit unwind only when ordering or shared state requires it.
4. Decide concurrency boundaries: process context, atomic context, IRQ top half, threaded IRQ, workqueue, timer, DMA callback.
5. Define evidence needed: datasheet registers, bus transaction examples, DT node, logs, scope/logic-analyzer traces, and test plan.

## Required Reads By Task
- New driver or hardware bring-up: `tasks/bringup-workflow.md`.
- Implementing subsystem callbacks: `tasks/implementation-patterns.md` and `references/subsystem-matrix.md`.
- Memory, MMIO, mmap, DMA, IRQ, locking: `references/kernel-engineering-principles.md`.
- Debugging, validation, or intermittent behavior: `tasks/debugging-testing.md`.
- Toolchain, QEMU, KGDB, bpftrace, Smatch, Coccinelle, Syzkaller, Bootlin: `references/tooling-matrix.md`.
- Auditable engineering flow: `tasks/step-verify-workflow.md`.
- Upstream-ready patches or long-term maintenance: `tasks/upstream-maintenance.md`.
- Final review before handoff: `references/review-checklist.md`.

## Design Heuristics
- Prefer an existing kernel subsystem over a private char driver when the device matches a framework.
- Keep policy in userspace and mechanism in kernel; avoid inventing ABI without necessity.
- Never sleep in atomic context; never hold spinlocks across bus calls that may sleep.
- Use `copy_{to,from}_user()` only at ABI boundaries and handle partial copy/error paths.
- For MMIO use `devm_ioremap_resource()` plus accessor APIs; do not dereference `__iomem`.
- For register devices on I2C/SPI, consider regmap before custom read/write helpers.
- For DT, model hardware, not Linux driver internals; document compatibles and supplies/clocks/IRQs/GPIOs.

## Script Helpers
- Run `scripts/driver_static_scan.py <path>` for heuristic review of C, Kconfig, Makefile, DTS, and binding files.
- Run `scripts/module_smoke_build.sh <module-dir> [kernel-build-dir]` for out-of-tree build smoke checks.
- Run `scripts/tooling_probe.sh` to inspect local build, static-analysis, tracing, fuzzing, QEMU, and KGDB tool availability.

## Verification Gate
- Build with warnings enabled and, when available, `sparse`, Smatch, Coccinelle, `checkpatch.pl`, `dt_binding_check`, and subsystem selftests.
- Test load/unload, probe/remove failure paths, hot/unplug or unbind where applicable, suspend/resume if resources are power-managed.
- Capture runtime evidence: `dmesg`, `/proc/interrupts`, sysfs state, tracepoints/ftrace/bpftrace, bus transactions, and userspace API results.
- Use QEMU/KGDB for isolated crash reproduction and Syzkaller for fuzzable ABI surfaces when practical.
- Do not claim correctness from compilation alone; tie each claim to a code path, runtime observation, or documented subsystem contract.

## Output Standard
When answering, name assumptions, selected subsystem, key APIs, file layout, validation commands, and residual hardware risks. If source evidence is missing, say what must be measured or read next.
