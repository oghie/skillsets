# Tooling Matrix

## Placement Analysis
Tooling belongs in verification modules, not in the core driver model. Keep `SKILL.md` as the router, put tool selection here, and make `tasks/step-verify-workflow.md` call the tools at the correct engineering stage.

| Tool | Place In Workflow | Use For | Verify |
|---|---|---|---|
| `apt install build-essential linux-headers-$(uname -r)` | Environment setup for distro-host module builds | Compiler, make, libc headers, and matching running-kernel headers | `test -d /lib/modules/$(uname -r)/build` and a smoke module build |
| Elixir Bootlin | Design/reference before coding or during API lookup | Browse current and historical Linux source, examples, definitions, call sites | Cross-check against the local target kernel tree before final code |
| Smatch | Static analysis after first compiling driver | Kernel-oriented bug patterns: unchecked returns, NULL/ERR_PTR, locking, integer/user-copy issues | Review warnings manually; false positives are expected |
| Coccinelle | Semantic search, API migration, tree-wide refactor, bug-pattern audit | SmPL rules for structural C matches and transformations | Run with `MODE=report` before patching; review every generated diff |
| Syzkaller | Security/fuzzing stage for syscall/ioctl/netlink/USB/devfs reachable surfaces | Coverage-guided kernel fuzzing and reproducer generation | Run in disposable VM; minimize and replay reproducers |
| bpftrace | Runtime debugging after boot/probe works | Trace functions, kprobes, tracepoints, latency, arguments, return values | Keep probes narrow; compare output to expected call path |
| KGDB/KDB | Source-level debugging for crashes, hangs, early boot, complex races | Breakpoints, backtraces, memory/register inspection | Enable kernel configs and connect from separate host or QEMU GDB |
| QEMU | Isolation layer for builds, boot tests, fuzzing, KGDB, reproducers | Fast Linux boot, virtual hardware, crash-safe experiments | Boot kernel, load module, reproduce issue, preserve serial log |

## Tool Selection
- Start with compiler, `W=1`, local scanner, and `checkpatch.pl`.
- Add Smatch when the code compiles and has meaningful control/data flow.
- Add Coccinelle when searching for repeated API patterns or migrating across a kernel tree.
- Add bpftrace when the driver runs but behavior is unclear.
- Add KGDB when logs/traces cannot explain the crash, hang, or corruption.
- Add Syzkaller only after the ABI surface can be exercised in a VM or isolated target.
- Use QEMU for anything destructive, flaky, security-sensitive, or hard to reproduce on hardware.

## Setup Recipes
Debian/Ubuntu host for external module smoke builds:

```bash
sudo apt update
sudo apt install build-essential linux-headers-$(uname -r)
```

Kernel tree static checks:

```bash
make W=1 C=1 M=$PWD modules
scripts/checkpatch.pl --strict --file path/to/driver.c
make coccicheck MODE=report COCCI=scripts/coccinelle/<rule>.cocci
```

Runtime tracing examples:

```bash
sudo bpftrace -e 'kprobe:driver_probe_device { @[comm] = count(); }'
sudo bpftrace -e 'tracepoint:irq:irq_handler_entry { @[args->irq] = count(); }'
```

QEMU direct boot shape:

```bash
qemu-system-x86_64 -kernel arch/x86/boot/bzImage -append "console=ttyS0" -nographic
```

KGDB shape:

```bash
qemu-system-x86_64 -s -S -kernel arch/x86/boot/bzImage -append "console=ttyS0 nokaslr" -nographic
gdb vmlinux -ex "target remote :1234"
```

## Production Rule
Never install or run heavyweight tooling blindly on a user system. Ask what OS, kernel tree, target hardware, and isolation boundary are available; then propose commands scoped to that environment.

## External Tool Docs
- Elixir Bootlin: `https://elixir.bootlin.com/`
- Smatch: `https://github.com/error27/smatch`
- Coccinelle: `https://coccinelle.gitlabpages.inria.fr/website/`
- Syzkaller: `https://github.com/google/syzkaller`
- bpftrace: `https://bpftrace.org/`
- KGDB/KDB: `https://docs.kernel.org/process/debugging/kgdb.html`
- QEMU direct Linux boot: `https://www.qemu.org/docs/master/system/linuxboot.html`
