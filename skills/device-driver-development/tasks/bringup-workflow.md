# Bring-Up Workflow

## 1. Establish Facts
- Identify kernel version, target board, architecture, boot method, compiler, config, and whether the driver is in-tree or out-of-tree.
- Gather datasheet, schematic, board manual, DT source, boot log, existing vendor driver, and any logic-analyzer/scope captures.
- Record power rails, clocks, reset lines, pinmux, interrupts, bus address/chip-select, DMA channels, and external dependencies.

## 2. Choose the Kernel Surface
- Map the device to the closest subsystem using `references/subsystem-matrix.md`.
- Avoid a custom char device unless no standard ABI fits.
- Decide whether the driver is a provider, consumer, or both. Examples: regulator provider, PWM consumer, GPIO irqchip, IIO sensor using regulator/IRQ/GPIO.

## 3. Model Hardware in DT or Platform Data
- Define `compatible`, `reg`, interrupts, clocks, resets, supplies, pinctrl states, GPIOs, DMA, and child nodes.
- Validate electrical polarity in property names: active-low GPIOs, IRQ trigger type, reset semantics, enable GPIOs.
- For bindings, write the schema before relying on the node in code.

## 4. Create Minimal Probe
- Add Kconfig and Makefile entries.
- Add match table and `MODULE_DEVICE_TABLE()`.
- Allocate per-device state with `devm_kzalloc()`.
- Acquire resources in dependency order: memory/registers, regmap, clocks, resets, regulators, GPIOs, pinctrl, IRQs, DMA.
- Keep external interfaces disabled until the hardware has been identified and initialized.

## 5. Prove One Hardware Transaction
- Read a stable ID/status register or perform the safest no-side-effect operation.
- For I2C/SPI, verify address/chip-select/mode/speed with bus tools or analyzer when possible.
- For MMIO, confirm resource range and use accessors, not pointer dereferences.
- Log failures with actionable resource names.

## 6. Add Functional Paths Incrementally
- Add one callback path at a time: read, write, event, buffer, IRQ, DMA, power, or user ABI.
- Add locking at the same time as shared state.
- Add teardown synchronization as soon as work/IRQ/timer/DMA/sysfs/open file state is introduced.

## 7. Validate on Hardware
- Build, boot, insert, bind, exercise one path, unbind, reload, and reboot.
- Capture `dmesg`, `/proc/interrupts`, relevant sysfs/debugfs state, bus traces, and userspace command results.
- Test failure paths by missing DT resources or simulated allocation/probe failures when practical.

## 8. Harden for Maintenance
- Remove debug-only ABI, noisy logs, dead code, and board-specific policy.
- Run static tools and review checklist.
- Document assumptions that remain hardware-dependent.
