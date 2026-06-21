# Subsystem Matrix

| Subsystem | Use When | Core Objects/APIs | User/Kernel Surface | Key Risks |
|---|---|---|---|---|
| Module only | Learning, glue, simple kernel service | `module_init`, `module_exit`, params | `modprobe`, `sysfs/module`, `dmesg` | No real device lifetime, unload races |
| Character device | No standard subsystem fits | `dev_t`, `cdev`, `class`, `device`, `file_operations` | `/dev`, `read`, `write`, `poll`, `ioctl`, `mmap` | ABI design, user copy, blocking semantics |
| Platform | Non-discoverable SoC/peripheral | `platform_driver`, resources, `probe/remove` | DT/ACPI/platform data | Matching, resource order, power sequencing |
| Device tree | Hardware description | `of_match_table`, `of_property_*`, resources | `.dts`, `.yaml` bindings | Binding stability, wrong hardware model |
| I2C client | Device on I2C bus | `i2c_driver`, `i2c_client`, SMBus/I2C funcs | DT node, bus transactions | Sleepable bus, address/probe side effects |
| SPI device | Device on SPI controller | `spi_driver`, `spi_device`, `spi_message`, `spi_transfer` | DT node, mode/speed/chip-select | CPOL/CPHA, word size, transfer ordering |
| Regmap | Register device on I2C/SPI/MMIO | `regmap_config`, `devm_regmap_init_*` | Driver-internal API | Endian/width/cache/volatile mistakes |
| IIO | Sensors, ADCs, DACs | `iio_dev`, `iio_info`, channels, buffers, triggers | sysfs, `/dev/iio:deviceX` | Scale/offset ABI, buffer scan layout |
| GPIO consumer | Driver uses GPIO lines | `gpiod_get`, `gpiod_set_value*`, `gpiod_to_irq` | DT GPIO properties | Sleepable GPIO ops, polarity naming |
| GPIO controller | Chip exports GPIO lines | `gpio_chip`, optional irqchip | gpiolib, sysfs/char GPIO ABI | `can_sleep`, IRQ mapping, base numbering |
| IRQ controller | Device multiplexes interrupts | `irq_chip`, domains, chained/nested handlers | `/proc/interrupts`, child IRQs | Flow type, masking, storm handling |
| Input | Keys, touch, relative/absolute events | `input_dev`, event bits, report/sync | `/dev/input/event*` | Wrong event type/range, missing sync |
| RTC | Hardware clock/alarm | `rtc_device`, `rtc_class_ops` | `/dev/rtc*`, sysfs, `hwclock` | Time conversion, alarm IRQ, wakeup |
| PWM | PWM producer/consumer | `pwm_chip`, `pwm_ops`, `pwm_get/apply` | PWM core, sysfs in old flows | Period/duty polarity, sleepability |
| Regulator | PMIC rails and consumers | `regulator_desc`, `regulator_ops`, `regulator_get` | regulator API, DT supplies | Constraints, enable counts, voltage tables |
| Framebuffer | Simple display memory driver | `fb_info`, `fb_ops`, video timings | `/dev/fb*`, mmap | Legacy interface, timings, memory mapping |
| NIC | Network interface controller | `net_device`, `net_device_ops`, `sk_buff`, ethtool | netdev, socket stack, ethtool | skb lifetime, TX flow control, NAPI/IRQ |
| DMAengine client | Device uses DMA controller | `dma_request_chan`, slave config, descriptors | Driver-internal transfer API | Mapping, completion, channel DT binding |

## Selection Rules
- If userspace already has a standard tool for the class, use that subsystem.
- If hardware is only a register block behind a bus, start with platform/I2C/SPI plus regmap.
- If data is sampled, timestamped, buffered, or triggered, consider IIO before char devices.
- If the device controls power, pins, clocks, resets, or GPIOs for other drivers, expose a provider framework rather than private hooks.
- If the driver only needs board wiring, fix DT/binding before adding code.
