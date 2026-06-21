# Kernel Engineering Principles

## Context First
Every callback has a context. Before choosing an API, answer whether it can sleep, whether interrupts are disabled, whether locks are held, and whether the function may run concurrently with remove, suspend, sysfs, userspace I/O, or another interrupt.

## Lifetime Model
- Store per-device state with `dev_set_drvdata()`, subsystem private data, `file->private_data`, or framework-owned private memory only after defining who frees it.
- Work items, timers, IRQ handlers, DMA callbacks, sysfs attributes, and open file handles can outlive simple assumptions. Cancel or synchronize them before freeing state.
- Prefer managed resources for simple probe-owned objects. Use explicit unwind when ordering must differ from reverse allocation order.

## Locking and Sleepability
- Use mutexes for process context and operations that can sleep.
- Use spinlocks for short atomic sections, IRQ state, and data shared with hard IRQ paths.
- Do not hold spinlocks across I2C/SPI/regmap operations that may sleep.
- Never call sleeping APIs from hard IRQ, timer callback, or atomic context.
- Use wait queues for condition-based blocking and wake the exact condition changed by the producer.

## Interrupt Design
- Keep hard IRQ top halves minimal: acknowledge, capture status, mask if needed, and schedule sleepable work.
- Use threaded IRQs when the device needs bus access, mutexes, or longer processing.
- Use chained/nested IRQ handling only for interrupt controllers and GPIO irqchips that fan in child IRQs.
- Always verify IRQ trigger type, polarity, sharing, and wakeup behavior from hardware and DT.

## Memory and I/O
- Use `GFP_KERNEL` only where sleeping is allowed; use atomic allocation sparingly and design away from it when possible.
- Use `kmalloc` for small physically contiguous buffers, `vmalloc` for larger virtually contiguous kernel memory, and DMA APIs for device-visible memory.
- Use `devm_ioremap_resource()` and `readb/readw/readl` or `writeb/writew/writel` for MMIO; do not directly dereference `__iomem`.
- For mmap, validate VMA length/flags, choose `remap_pfn_range()` or `io_remap_pfn_range()` according to memory type, and document caching behavior.

## DMA
- Pick coherent DMA for shared control rings/descriptors and streaming DMA for transient buffers.
- Map/unmap streaming DMA on the correct direction and lifetime.
- Handle cache coherency, alignment, DMA mask, IOMMU constraints, and scatter/gather limits.
- Treat DMA callbacks like interrupt-adjacent code: synchronize state, complete waiters, and avoid freeing buffers before the device is done.

## Bus and Register Access
- Platform drivers model non-discoverable devices and collect resources from DT/ACPI/platform data.
- I2C/SPI client drivers should store device-specific state, validate adapter/controller capabilities, and use regmap for register devices when suitable.
- Regmap centralizes endian, width, cache, volatile/readable/writeable registers, and update-bit logic.
- Do not assume register reset values; read datasheet and confirm on hardware if silicon revisions differ.

## Userspace ABI
- Char devices expose byte streams and control operations. Use them when no subsystem ABI fits.
- Prefer standard subsystem ABI: IIO channels/buffers, input events, RTC, PWM, regulator, netdev, GPIO consumer/controller, framebuffer.
- Validate all user pointers, sizes, offsets, and integer arithmetic before copy or mmap.
- Sysfs attributes should be one value per file, stable, and non-policy-heavy. Debugfs is not ABI.

## Device Tree
- DT describes hardware topology and electrical/resource wiring, not Linux implementation details.
- Name compatibles, registers, interrupts, clocks, resets, supplies, GPIOs, pinctrl states, DMA channels, and child nodes according to binding rules.
- Bindings must validate real hardware variations and preserve compatibility for old DTBs.
