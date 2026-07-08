# Phase 6: Zero-Day Discovery & Exploit Development

**When:** All known CVEs, techniques, and tools in Phases 1-5 have been exhausted. No public exploit exists for the target version/configuration. You must find and weaponize a new vulnerability.

## Two Parallel Tracks

### Track A: Userspace Fuzzing (quicker, for delivery)
Target app-level and library-level bugs. Proceed to sections below (Fuzzing Infrastructure through Crash Triage).

### Track B: Kernel Exploit Development (deeper, for privilege escalation) 
**For full kernel exploitation methodology** — futex PI race, pipe buffer corruption, arbitrary physical R/W, KASLR bypass, fops hijack, credential patching, SELinux bypass, root persistence — **read `references/kernel-exploit-methodology.md`**.

This is the definitive reference derived from CVE-2026-43499 (IonStack) by NebuSec. It covers: Android ARM64 memory layout, key kernel structures (task_struct, cred, pipe_buffer, file_operations, mm_struct), exploit primitives ladder, heap feng shui, race condition engineering patterns, KASLR bypass techniques, credential patching code patterns, and mitigation bypass strategies.

## Mindset Shift

Phase 6 is different. You are no longer applying known techniques — you are researching, fuzzing, and developing original exploits. This requires:

1. **Patience.** Fuzzing campaigns run for hours or days. Set them up, let them run, analyze crashes.
2. **Systematic approach.** Don't randomly mutate inputs. Understand the attack surface, prioritize high-value targets, build targeted harnesses.
3. **Root-cause analysis.** Every crash is a clue. Triage, minimize, determine exploitability, build primitives.
4. **Chain thinking.** A single crash rarely gives full RCE. Build a chain: info leak → arbitrary read → arbitrary write → code execution.

## Attack Surface Prioritization

On Android, the most promising attack surfaces for zero-day discovery, ranked by value:

### Tier 1: Remote, No Interaction (Highest Value)
| Target | Protocol | Attack Surface | Tools |
|--------|----------|---------------|-------|
| Baseband/Modem | GSM/LTE/5G/NR | SMS parser, RIL, NAS/AS layers | srsRAN, OpenBTS, QEMU modem |
| Bluetooth Daemon | L2CAP, RFCOMM, SDP, GATT | Packet parsers, pairing state machine | InternalBlue, BtleJuice, custom fuzzer |
| WiFi Firmware | 802.11 management frames | Beacon, probe response, association parsers | Nexmon, custom firmware fuzzer |
| NFC Stack | NCI, NDEF, ISO-DEP | Tag parsing, NDEF record handling | libnfc, Proxmark3, custom harness |

### Tier 2: Remote, User Interaction
| Target | Protocol | Attack Surface | Tools |
|--------|----------|---------------|-------|
| Browser Engine | HTML/CSS/JS | DOM, CSS parser, JS JIT, WebGL | Domato, Fuzzilli, Browser fuzzing harness |
| Media Codecs | MP4, AAC, H.264/5, VP9 | Stagefright, OMX, Codec2 | AFL++ with custom decoder harness |
| Image Parsers | JPEG, PNG, GIF, WebP, HEIF, AVIF | libjpeg, libpng, Skia, libheif | AFL++, libFuzzer with image corpus |
| Font Parsing | TTF, OTF | FreeType, HarfBuzz, Minikin | AFL++, FontFuzz |
| WebView / Chromium | JS bridges, IPC | addJavascriptInterface, Mojo IPC | Frida hooks + custom fuzzer |

### Tier 3: Local, Privilege Escalation
| Target | Component | Attack Surface | Tools |
|--------|-----------|---------------|-------|
| Binder Driver | Kernel | ioctl handlers, transaction parsing | syzkaller with binder descriptions |
| GPU Driver | Kernel | Mali/Adreno ioctl, command stream parsing | syzkaller, custom harness |
| ION/DMA-BUF | Kernel | Memory allocator ioctl | syzkaller |
| System Services | Userspace | Parcel deserialization, intents | AFL++, intent fuzzer |
| TEE/TrustZone | Secure world | Trusted app loading, shared memory | QEMU TEE emulation, hardware glitching |

## Fuzzing Infrastructure

### Quick Setup
```bash
bash scripts/fuzzing_setup.sh
```

This installs and configures AFL++, libFuzzer, syzkaller, and common fuzzing dependencies.

### AFL++ (Coverage-Guided Fuzzing)
```bash
# Compile target with AFL instrumentation
afl-clang-fast -o harness target_harness.c -ltargetlib

# Run fuzzer with corpus
afl-fuzz -i corpus/ -o findings/ -- ./harness @@

# Parallel fuzzing (N cores)
for i in $(seq 1 $(nproc)); do
    afl-fuzz -i corpus/ -o findings/ -S fuzzer$i -- ./harness @@ &
done
```

### libFuzzer (In-Process, Fast)
```c
// harness.c — compile: clang -g -fsanitize=fuzzer,address harness.c -o harness
int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    target_parse_function(data, size);
    return 0;
}
```

### syzkaller (Kernel Fuzzing)
```bash
# Build syzkaller
git clone https://github.com/google/syzkaller
cd syzkaller && make

# Configure for Android kernel
# Edit config: target = "linux/arm64", kernel_obj = "/path/to/kernel"
# Add Android-specific syscall descriptions for binder, ashmem, ion

./bin/syz-manager -config=android.cfg
```

### Honggfuzz (Hardware-Assisted Fuzzing)

Prefer Honggfuzz over AFL++ when fuzzing **binary-only targets** (no source code for recompilation) or when hardware-assisted coverage (Intel PT / BTS) can provide better feedback:

```bash
# Install
git clone https://github.com/google/honggfuzz && cd honggfuzz && make

# Compile target with honggfuzz (if source available)
hfuzz-clang -o harness target_harness.c -ltargetlib

# Binary-only mode (no recompilation needed)
honggfuzz -i corpus/ -o findings/ -- ./binary_target ___FILE___

# Persistent mode (fastest — requires source modification)
honggfuzz -P -i corpus/ -o findings/ -- ./harness
```

**When to use:** Binary-only targets (pre-built APK native libs, vendor blobs), targets without AFL-compatible compiler, or when Intel PT hardware coverage is available (significantly faster than software instrumentation for certain workloads).

### Radamsa (Black-Box Mutation)

Quick-and-dirty mutation fuzzing before investing in coverage-guided harnesses. Good for initial triage of an unknown binary:

```bash
# Install
apt-get install radamsa  # or brew install radamsa

# Single mutation
radamsa seed_input > mutated_output

# Batch fuzzing loop with crash detection
for i in $(seq 1 10000); do
    radamsa seed_input > mutated
    ./target_binary mutated 2>/dev/null
    [ $? -gt 127 ] && cp mutated crash_$(date +%s).bin
done
```

**Use cases:** Testing an APK's native library against malformed assets (images, audio, fonts), quick smoke test before writing AFL++ harnesses, testing closed-source protocol parsers. **Graduate to AFL++/libFuzzer** when the target proves interesting — Radamsa is a scout, not a siege weapon.

### Android-Specific Fuzzing Targets

**Intent Fuzzer:**
```python
# Fuzz exported activities/services/receivers with malformed intents
from scripts.deeplink_fuzzer import generate_payloads
# Extend with: oversized extras, malformed URIs, type confusion payloads
```

**Binder Fuzzer:**
```bash
# Fuzz Binder transactions via custom client
# Target: system services with large attack surface
# Use: service call, custom binder client with AFL++ harness
```

**Stagefright/Media Fuzzer:**
```bash
# Fuzz media codecs via stagefright command-line tool
# Compile stagefright with AFL instrumentation
# Corpus: collection of malformed media files
```

## Crash Triage & Exploitability

When a crash is found, determine exploitability:

### Triage Steps
1. **ASAN/UBSAN report:** Read the sanitizer output. What type of bug? (heap-buffer-overflow, use-after-free, double-free, integer overflow)
2. **Minimize reproducer:** Reduce the crashing input to the minimum that triggers the bug
3. **Control analysis:** Can you control the overflowing data? The freed object? The integer operands?
4. **Primitive mapping:**
   - Heap overflow → potential arbitrary write
   - Use-after-free → potential type confusion / vtable hijack
   - Integer overflow → potential buffer size bypass
   - Uninitialized memory → potential info leak
5. **Mitigation check:** What mitigations are active?
   - ASLR (always on Android 5+)
   - PIE (mandatory since Android 7)
   - NX/DEP
   - Stack canaries
   - CFI (Control Flow Integrity, Android 9+)
   - PAC (Pointer Authentication, ARMv8.3+, Android 12+)
   - MTE (Memory Tagging Extension, ARMv8.5+, Android 15+)

### Debugging Setup
```bash
# GDB with GEF for exploit development
gdb-multiarch -q -ex "target remote :1234" -ex "gef config gef.debug 1"

# lldb for Android native debugging
lldb -o "platform select remote-android" -o "platform connect connect://localhost:1234"

# Kernel debugging via QEMU
qemu-system-aarch64 -kernel Image -initrd ramdisk.img \
  -append "console=ttyAMA0" -nographic -s -S
```

## Exploit Development Workflow

### 1. Build Primitives
```
Crash → Info Leak (defeat ASLR) → Arbitrary Read → Arbitrary Write → Code Execution
```

Toolkit:
- **pwntools:** `from pwn import *` — exploit development framework
- **ROPgadget:** Find ROP gadgets in target binary: `ROPgadget --binary libc.so`
- **one_gadget:** Find execve("/bin/sh") gadgets in libc
- **ropper:** Alternative ROP gadget finder

### 2. Defeat Mitigations

| Mitigation | Technique |
|-----------|-----------|
| ASLR | Info leak (pointer read), partial overwrite, side-channel |
| PIE | Same as ASLR — leak PIE base from stack/heap |
| Stack Canary | Info leak, brute-force (fork server), overwrite canary from adjacent buffer |
| CFI | Reuse allowed call targets, COOP/JOP attacks |
| PAC | PAC forgery via signing gadget abuse, PAC brute-force (limited entropy) |
| MTE | Probabilistic bypass, tag prediction, uninitialized tag leak |
| SELinux | Escalate from untrusted_app to platform_app via service vulnerability, then kernel |

### 3. Real-World Chain References

Study these full-chain exploits for technique patterns:

**CVE-2026-43499 — Firefox → Android RCE (IonStack)**
- **Repo:** `https://github.com/NebuSec/CyberMeowfia/tree/main/IonStack/CVE-2026-43499`
- **Chain:** Browser JavaScript → IPC sandbox escape → privilege escalation → full device compromise
- **Key insight:** Firefox's Android IPC implementation had a use-after-free in GeckoView's content process boundary

**CVE-2026-10702 — Firefox < v151.0.2 Full Chain**
- **Chain:** Browser-to-kernel with two 0-day vulnerabilities
- **Components:** Renderer process RCE + kernel privilege escalation via GPU driver
- **Key insight:** GPU command buffer parsing vulnerability provided kernel arbitrary write from a sandboxed renderer

**CVE-2023-24033 — Samsung Exynos Baseband RCE**
- **Chain:** Malformed SMS → baseband heap overflow → modem processor code execution → application processor access
- **Key insight:** Baseband and application processor share memory regions; compromising the modem gives AP access

**CVE-2024-0044 — Android System LPE**
- **Chain:** Any app → run-as privilege bypass → system-level code execution
- **Key insight:** PackageManager's origin check for `run-as` could be bypassed via shell identity confusion

### 4. Reporting

When a zero-day is discovered:
1. Document the full chain with CVE-level detail
2. Create a minimal PoC that demonstrates exploitation
3. Map the exploit to the operational goal (device access, data extraction)
4. Integrate into the broader investigation report

## Quick Command Reference

```bash
# Fuzzing
afl-fuzz -i in/ -o out/ ./harness @@
./libfuzzer_harness -max_len=65536 corpus/

# Kernel fuzzing
./bin/syz-manager -config=android.cfg

# Crash triage
c++filt <mangled_symbol>
addr2line -e binary -f -C <address>
llvm-symbolizer -obj=binary <address>

# Exploit dev
python3 -c "from pwn import *; print(asm('mov x0, 0; ret', arch='aarch64'))"
ROPgadget --binary libc.so | grep "ldr x0"
checksec --file=binary  # Show mitigations

# Debugging
gdb-multiarch -ex "target remote :1234"
adb forward tcp:1234 tcp:1234
gdbserver :1234 --attach $(pidof com.target.app)
```

## Important: Scope and Ethics

Zero-day discovery is a last resort. Exhaust all known techniques (Phases 1-5, CVE database, commercial tools) before initiating Phase 6. When a zero-day is discovered:

1. **Document the vulnerability** with clear root cause analysis
2. **Develop in an isolated environment** — never test exploits on live evidence devices
3. **Preserve forensic integrity** — the zero-day itself becomes part of the chain of custody
4. **Disclose responsibly** — if the vulnerability affects widely deployed devices, coordinate disclosure with the vendor after the investigation concludes
