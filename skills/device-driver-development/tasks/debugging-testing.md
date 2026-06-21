# Debugging and Testing

## First Triage
- Collect exact kernel version, config, hardware revision, DTB, module params, full `dmesg`, and reproduction command.
- Classify failure: build, modpost, probe, resource acquisition, bus transaction, IRQ storm, DMA timeout, userspace ABI, suspend/resume, teardown, or data corruption.
- Identify the first bad observable event, not the final symptom.

## Build and Static Checks
- Build with `W=1`; use `C=1` for sparse when available.
- Run `scripts/driver_static_scan.py <path>` for local heuristic issues.
- Run Smatch after the driver compiles to catch kernel-specific data-flow and error-path bugs.
- Run Coccinelle in report mode for semantic bug patterns, API migration, and repeated callback mistakes.
- Run `scripts/checkpatch.pl --strict` from a kernel tree for upstream style review.
- Run `make dt_binding_check` for bindings and `dtbs_check` for board nodes when applicable.
- Use `pahole`, `objdump`, or `nm` only when layout, symbol export, or module section behavior matters.

## Runtime Signals
- `dmesg -w` for probe/runtime logs.
- `/proc/interrupts` for IRQ counts and storms.
- `/sys/bus/*/devices`, `/sys/class/*`, and `/sys/kernel/debug` for framework state.
- `trace-cmd`, ftrace, dynamic debug, or tracepoints for timing and call paths.
- `bpftrace` for narrow kprobe/tracepoint questions when runtime state is unclear and the target permits eBPF tracing.
- `i2cdetect`, `i2ctransfer`, `spidev_test`, `evtest`, `iio_info`, `hwclock`, `ethtool`, `ip`, and framebuffer tools only when safe for the bus/device.

## Kernel Debug Features
- Enable lockdep for locking inversions.
- Enable KASAN/KFENCE for memory bugs.
- Enable KCSAN for data races.
- Enable UBSAN for undefined behavior.
- Enable dynamic debug for controlled driver logging.
- Use fault injection to verify probe unwind if the kernel config supports it.
- Use KGDB/KDB when traces are insufficient for a crash, hang, or early-boot fault.
- Use QEMU for destructive reproducers, KGDB sessions, and Syzkaller fuzzing where virtual hardware is sufficient.
- Use Syzkaller for fuzzable syscall/ioctl/netlink/devfs surfaces after basic ABI tests pass.

## Hardware Evidence
- For I2C/SPI, compare driver transactions to datasheet timing and analyzer captures.
- For IRQ, verify electrical polarity, trigger mode, masking, status clear order, and deglitch behavior.
- For DMA, confirm descriptor addresses, cache coherency, completion interrupt, and residue.
- For power/reset, verify rails, delays, clocks, pinctrl states, and reset line transitions.

## Failure Pattern Guide
- Probe returns `-EPROBE_DEFER`: inspect supplier clocks, regulators, GPIOs, resets, pinctrl, and parent devices.
- IRQ fires once then stops: check status clear, mask/unmask, threaded handler return, and trigger type.
- IRQ storm: check level interrupt status clear, wrong polarity, shared IRQ return value, and unmasked child sources.
- Data is stale or corrupted: inspect endian, register width, DMA sync, cache attributes, buffer lifetime, and locking.
- Remove crashes: cancel work/timers, disable IRQ, stop DMA, unregister user-visible interface before freeing private state.
- Userspace hangs: review wait queue condition, wakeup ordering, nonblocking behavior, and poll mask.
