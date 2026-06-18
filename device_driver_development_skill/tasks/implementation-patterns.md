# Implementation Patterns

## Platform Skeleton
Use platform drivers for non-discoverable devices. Core pattern: match table, `probe()`, resource acquisition, hardware init, framework registration, and remove/suspend teardown.

```c
static const struct of_device_id foo_of_match[] = {
	{ .compatible = "vendor,foo" },
	{ }
};
MODULE_DEVICE_TABLE(of, foo_of_match);

static struct platform_driver foo_driver = {
	.probe = foo_probe,
	.remove = foo_remove,
	.driver = {
		.name = "foo",
		.of_match_table = foo_of_match,
	},
};
module_platform_driver(foo_driver);
```

## Character Device
- Use only when standard frameworks do not fit.
- Use `alloc_chrdev_region()`, `cdev_init()`, `cdev_add()`, `class_create()`, `device_create()` or local equivalents.
- Use `file->private_data` for open instance state and define blocking/nonblocking semantics.
- Pair `poll()` wait queues with the same conditions used by `read()`/`write()`.
- Design ioctl numbers and structures as stable ABI; validate `_IOC_TYPE`, `_IOC_NR`, `_IOC_SIZE`, direction, and user buffer size.

## I2C/SPI Register Device
- Store state with `i2c_set_clientdata()` or `spi_set_drvdata()`.
- Use regmap when registers are regular enough for `reg_bits`, `val_bits`, volatile tables, and cache policy.
- Confirm bus operation sleepability; never perform I2C/SPI in a hard IRQ top half.
- SPI-specific: verify CPOL/CPHA, max speed, bits per word, chip-select polarity, and transfer grouping.

## IIO Sensor
- Allocate `iio_dev` with private state.
- Define channels, info callbacks, scale/offset/raw semantics, and buffer scan layout.
- Use triggers and buffers for sampled streams; use direct mode for one-shot reads.
- Verify sysfs naming follows IIO channel conventions.

## GPIO and IRQ
- Consumer drivers use descriptor GPIO APIs.
- GPIO controllers implement `gpio_chip`; set `can_sleep` correctly for expander chips on I2C/SPI.
- GPIO irqchips need child IRQ mapping, mask/unmask, type setting, and interrupt-status demultiplexing.
- Use threaded IRQ or nested threaded IRQ for sleepable expander access.

## DMA
- Use DMAengine for slave transfers when a controller channel is described by DT.
- Configure direction, address width, burst size, residue behavior, and completion callback.
- For streaming DMA, map before handing buffers to device and unmap after device completion.
- Use completions or wait queues for transaction completion, with timeout and abort handling.

## Networking
- Allocate `net_device` with private data, fill `net_device_ops`, register only after hardware is ready.
- TX path owns `skb` until consumed or dropped; stop/wake queue around resource pressure.
- RX path allocates skb, reserves alignment, copies or maps packet data, sets protocol, and submits to stack.
- Prefer NAPI for real high-throughput hardware even when a simpler IRQ flow is enough for a toy driver.
