# Step Verify Workflow

Use this checklist to make driver work auditable. Each step must produce a concrete check before moving on.

1. Environment baseline -> verify: `uname -a`, compiler version, target kernel tree, `.config`, headers/build dir, and cross-compile variables are known.
2. Toolchain setup -> verify: external module smoke build or kernel `make W=1` reaches the target object without missing headers.
3. Hardware facts -> verify: datasheet/schematic/DT/log evidence names register map, bus address/chip-select, IRQ, clocks, resets, regulators, GPIOs, pinctrl, and DMA channels.
4. Subsystem choice -> verify: chosen framework is justified against standard ABIs and similar in-tree drivers.
5. Firmware model -> verify: DT/binding describes hardware resources, validates with schema tools where available, and does not encode Linux-private policy.
6. Skeleton and matching -> verify: Kconfig, Makefile, module metadata, match table, `MODULE_DEVICE_TABLE`, and `probe/remove` compile.
7. Probe resources -> verify: each resource acquisition has an error path, useful error log, and cleanup or `devm_*` lifetime.
8. Register access -> verify: one safe ID/status transaction succeeds; MMIO uses accessors, I2C/SPI uses sleepable context, regmap config matches width/endian/cache needs.
9. Concurrency design -> verify: every shared field has owner, lock, context, and teardown synchronization documented in code or review notes.
10. IRQ path -> verify: trigger type, polarity, status clear, mask/unmask, top half, threaded/work bottom half, and `/proc/interrupts` behavior match hardware.
11. Memory and DMA -> verify: allocation type, DMA mask, map/unmap direction, cache coherency, barriers, and completion/timeout handling are tested.
12. Userspace or framework ABI -> verify: sysfs/ioctl/read/write/poll/mmap/netdev/IIO/input/RTC/PWM/regulator behavior has a user-visible test.
13. Power management -> verify: clocks/regulators/resets/pinctrl/runtime PM/suspend/resume are balanced across probe, failure, remove, and resume paths.
14. Static analysis -> verify: compiler warnings, sparse/Smatch, Coccinelle reports, local scanner, and checkpatch findings are reviewed or justified.
15. Runtime tracing -> verify: `dmesg`, dynamic debug, ftrace/bpftrace, IRQ counters, bus traces, and subsystem state confirm the expected path.
16. Crash debugging -> verify: KGDB/KDB/QEMU or hardware console can capture backtrace, registers, module symbols, and reproduction steps.
17. Fuzz/security -> verify: reachable ABI surfaces have bounds/lifetime checks and, where practical, Syzkaller or targeted fuzz reproducers run in isolation.
18. Handoff -> verify: review checklist passes, residual risks are explicit, commands/results are recorded, and no debug-only ABI or noisy logs remain.
