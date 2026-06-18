# Driver Knowledge Map

## Core Domains
| Domain | What To Know | Use When |
|---|---|---|
| Kernel/module basics | Module lifecycle, build integration, params, logging, errors | Any module or driver skeleton |
| Kernel facilities | `container_of`, lists, wait queues, timers, mutex/spinlock, workqueues, IRQs | Shared state, async events, deferred work |
| Character devices | `cdev`, major/minor, `file_operations`, read/write/poll/ioctl/mmap | No standard subsystem ABI fits |
| Platform model | Non-discoverable devices, resources, bus matching, `probe/remove` | SoC blocks and board-wired peripherals |
| Firmware description | Device tree nodes, bindings, resources, clocks, resets, regulators, GPIOs, IRQs, DMA | Hardware topology and board integration |
| I2C/SPI clients | Client registration, bus transactions, probe/remove, mode/addressing | External register devices on serial buses |
| Regmap | Register width, endian, cache, volatile/readable/writeable maps, update bits | I2C/SPI/MMIO register abstractions |
| IIO | Channels, raw/scale/offset, triggers, buffers, scan layout | Sensors, ADCs, DACs, sampled data |
| Memory/MMIO | Virtual memory, allocators, `__iomem`, mmap, devres | Device registers, buffers, userspace mapping |
| DMA | Coherent/streaming mappings, DMAengine, completions, cache coherency | Device-visible memory transfers |
| Device model/sysfs | bus/device/driver, kobject, attributes, classes | User-visible state and framework integration |
| Pinctrl/GPIO | Pinmux, descriptor GPIO, GPIO IRQ mapping, `gpio_chip` | Board pins, GPIO expanders/controllers |
| IRQ controllers | Chained/nested IRQs, irqchip, flow handlers, demultiplexing | Devices that fan out interrupts |
| Input/RTC/PWM/regulator | Framework provider/consumer APIs and standard userspace ABI | Buttons, clocks, waveforms, power rails |
| Framebuffer/netdev | Display memory/timings, `sk_buff`, `net_device`, TX/RX, ethtool | Graphics memory and NIC drivers |

## Conceptual Diagrams To Reconstruct Mentally
- User space interacts through syscalls/VFS/subsystem ABI; the driver sits in kernel space and mediates hardware.
- Bus matching is a table lookup between device descriptors and registered drivers; platform devices need firmware/board description.
- Regmap inserts one register abstraction between bus-specific I/O and driver logic.
- IIO separates application/sysfs/char-device access from IIO core, bus driver, and hardware.
- Virtual addresses, VMAs, page tables, allocators, MMIO mappings, and DMA mappings are different contracts.
- IRQ design is a flow: hardware line, interrupt controller, Linux IRQ descriptor, top half, bottom half/thread/work.
- Provider frameworks expose resources to other drivers; consumer drivers request named resources and respect enable/disable balance.

## Version-Sensitive Rule
Use this map for reasoning, but verify callback signatures, helper names, binding format, and deprecation status against the active kernel tree and current kernel documentation.
