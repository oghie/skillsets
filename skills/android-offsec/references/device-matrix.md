# Device-Specific Exploitation Matrix

When targeting a non-Pixel Android device, adaption requires mapping: **Device Model → Chipset → GPU → Exploit Family → Firmware Offsets**. This reference teaches the agent how to auto-detect and adapt.

## Decision Tree: What Exploit to Use

```
Device Model identified
    ↓
Chipset?
├── Qualcomm Snapdragon → GPU: Adreno → Use: Adreno patterns (CVE-2022-25664 info leak)
│   ├── SD 888, 8 Gen 1/2/3 → Adreno 6xx/7xx → kgsl-3d0
│   ├── US Samsung S21-S24 → Snapdragon → same path
│   ├── OnePlus 9/10/11/12 → Snapdragon → same path
│   ├── Xiaomi Mi/Poco F → Snapdragon → same path
│   └── Sony Xperia → Snapdragon → same path
│
├── Samsung Exynos → GPU: Mali (Valhall) → Use: Mali CSF patterns (CVE-2025-0072)
│   ├── International S21/S22 → Exynos 2100/2200 → Mali-G78/G78MP14
│   ├── International S23/S24 → Exynos 2300/2400 → Mali-G710/Xclipse
│   └── Older S series → Exynos 990/9820 → Mali-G77/G76
│
├── MediaTek (Dimensity/Helio) → GPU: Mali → Use: Mali JM/CSF patterns
│   ├── Dimensity 700/720/800/810 → Mali-G57 MC2 → kmalloc-256 (JM)
│   ├── Dimensity 900/920/1100/1200 → Mali-G77/G78 → CSF
│   ├── Dimensity 9000/9200/9300 → Mali-G710/G720 → CSF
│   ├── Oppo Reno → Dimensity → Mali
│   ├── Realme Narzo/GT → Dimensity → Mali
│   ├── Redmi Note → Dimensity/Helio → Mali
│   └── Vivo V/Y → Dimensity → Mali
│
├── Google Tensor → GPU: Mali → Use: Mali CSF patterns (CVE-2025-0072)
│   ├── Tensor G1 (Pixel 6) → Mali-G78 MP20 → JM (CVE-2022-38181)
│   ├── Tensor G2 (Pixel 7) → Mali-G710 MP7 → CSF (CVE-2023-6241)
│   ├── Tensor G3 (Pixel 8) → Mali-G715 MP7 → CSF (CVE-2025-0072)
│   └── Tensor G4 (Pixel 9) → Mali-G715 MP7 → CSF
│
├── Huawei Kirin → GPU: Mali → Use: Mali patterns (check kernel version)
│   └── No Google services → different attack surface (Huawei AppGallery)
│
└── Unisoc (Spreadtrum) → GPU: Mali → Use: Mali JM patterns (usually older)
    └── Budget devices → often older kernel (4.x/5.x) → easier exploitation
```

## Chipset Auto-Detection

### From ADB (if available)
```bash
adb shell getprop ro.board.platform         # e.g., "lahaina" (SD 888), "taro" (SD 8 Gen 1)
adb shell getprop ro.hardware               # e.g., "qcom", "exynos9820", "mt6781"
adb shell getprop ro.soc.model              # e.g., "Snapdragon 8 Gen 2"
adb shell cat /proc/cpuinfo | grep Hardware # e.g., "Qualcomm Technologies, Inc SM8450"
```

### From Device Model (without ADB)
```
Model → Chipset mapping (auto-detected):
Samsung SM-S901B → Exynos 2200 → Mali-G78 MP14
Samsung SM-S901U → Snapdragon 8 Gen 1 → Adreno 730
Samsung SM-S908B → Exynos 2200 → Mali-G78
Samsung SM-G998B → Exynos 2100 → Mali-G78 MP14
Samsung SM-G998U → Snapdragon 888 → Adreno 660
Oppo CPH2389 (Reno 8T) → Dimensity 700 → Mali-G57 MC2
Oppo CPH2449 (Find N2 Flip) → Dimensity 9000+ → Mali-G710 MC10
Realme RMX3686 (Narzo 50 Pro) → Dimensity 700 → Mali-G57 MC2
Realme RMX3560 (GT Neo 3) → Dimensity 8100 → Mali-G610 MC6
Xiaomi 22071212AG (Redmi Note 12 Pro) → Dimensity 1080 → Mali-G68 MC4
Xiaomi 2210132G (Mi 13) → Snapdragon 8 Gen 2 → Adreno 740
OnePlus CPH2413 (Nord 2T) → Dimensity 1300 → Mali-G77 MC9
OnePlus LE2113 (9 Pro) → Snapdragon 888 → Adreno 660
Pixel 6 (oriole) → Tensor G1 → Mali-G78 MP20
Pixel 8 (shiba) → Tensor G3 → Mali-G715 MP7
```

### GPU Model Detection
```bash
adb shell cat /sys/class/kgsl/kgsl-3d0/gpu_model        # Adreno GPU model
adb shell dmesg | grep -i mali                           # Mali GPU version
adb shell cat /proc/mali/version                         # Mali driver version
adb shell getprop ro.gpu.name                            # Sometimes available
```

## Exploit Family Selection by GPU Architecture

### Mali JM (Job Manager) — Pixel 6, older MediaTek, older Exynos
- **CVEs applicable:** CVE-2022-38181 (JIT UAF), CVE-2022-22706, CVE-2022-33917
- **ioctl surface:** `KBASE_IOCTL_JOB_SUBMIT`, `KBASE_IOCTL_MEM_FLAGS_CHANGE`
- **Key objects:** `kbase_va_region` (kmalloc-256), JIT memory (3-list lifecycle)
- **Exploit primitive:** PGD reuse from kmalloc-256 UAF → physical R/W

### Mali CSF (Command Stream Frontend) — Pixel 7/8/9, newer Exynos, newer Dimensity
- **CVEs applicable:** CVE-2025-0072 (queue rebind UAF), CVE-2023-6241
- **ioctl surface:** `KBASE_IOCTL_CS_QUEUE_REGISTER` + `BIND` + `TERMINATE`
- **Key objects:** `kbase_queue`, `kbase_queue_group`, `queue->phys[]` pages
- **Exploit primitive:** Page-level UAF → PGD reuse → physical R/W
- **OpenCL path:** Use `libGLES_mali.so` for GPU command execution

### Adreno — Qualcomm Snapdragon devices
- **CVEs applicable:** CVE-2022-25664 (cache coherency info leak)
- **ioctl surface:** `IOCTL_KGSL_MAP_USER_MEM`, `IOCTL_KGSL_GPU_COMMAND`
- **Key insight:** ARM64 `flush_anon_page` is NO-OP → CPU-GPU cache coherency bugs
- **Exploit primitive:** Info leak (not R/W) → KASLR bypass → combine with other exploit

## OEM-Specific Security Layers

### Samsung Knox
- **Real-time kernel protection (RKP):** Monitors kernel page tables and critical data structures
- **Defeat:** RKP only protects specific memory regions — kernel code patching outside those regions still works
- **DM-Verity:** Verified boot — prevents persistent kernel modifications
- **Defeat:** Runtime-only exploitation (no persistent modification needed)
- **Knox warranty bit:** Hardware fuse tripped on custom firmware — forensic indicator
- **Secure Folder:** Encrypted workspace — separate from main user's key hierarchy
- **Samsung-specific kernel configs:** `CONFIG_SEC_RESTRICT_ROOTING`, `CONFIG_RKP_KDP`

### Xiaomi MIUI / HyperOS
- **MIUI security app:** Monitors root access, SELinux status
- **Xiaomi Account lock:** Similar to FRP but Xiaomi-specific (Mi Cloud binding)
- **Bootloader unlock:** Requires Mi Unlock tool, wait period (72h-168h), SIM binding
- **EDL mode:** Sometimes locked via Xiaomi auth (requires authorized account)
- **Defeat:** EDL auth bypass for older devices; preloader exploits for newer

### Oppo/Realme ColorOS / RealmeUI
- **Hardware-level bootloader lock:** Very difficult to unlock
- **Deep testing APK:** Required for bootloader unlock on some models
- **EDL auth:** Oppo-specific, requires authorized service account
- **MTK BROM bypass:** Most Oppo/Realme use MediaTek — MTK BROM is often accessible
- **Defeat:** MTK BROM → mtkclient → boot image modification → root

### OnePlus OxygenOS
- **Bootloader unlock:** Relatively easy — fastboot oem unlock (with toggle in developer settings)
- **EDL:** Typically accessible via test points (9008 mode)
- **Qualcomm devices:** Use firehose programmer for EDL extraction
- **Least-restrictive OEM for security research**

### Vivo Funtouch OS / OriginOS
- **Bootloader:** Locked, no official unlock for most models
- **MTK/Unisoc devices:** BROM mode often accessible
- **Defeat:** Same as Oppo/Realme — chipset-level bypass

### Huawei EMUI / HarmonyOS
- **No Google services:** Attack surface shifts to Huawei AppGallery, Petal Search, HMS
- **Bootloader:** Locked since 2018, no official unlock
- **Kirin chipset:** Less researched → harder to find chipset-specific exploits
- **Defeat:** Hardware-level attacks (ISP/JTAG), commercial forensic tools

## Kernel Version → Exploit Difficulty Mapping

| Kernel Version | Year | Available Mitigations | Difficulty |
|---------------|------|----------------------|------------|
| 4.4 / 4.9 | 2016-2018 | KASLR, limited CFI | Easy |
| 4.14 / 4.19 | 2018-2021 | +SLAB_FREELIST_RANDOM, hardened usercopy | Moderate |
| 5.4 | 2020-2022 | +CFI, improved RANDOM | Moderate-Hard |
| 5.10 | 2021-2023 | +PAC (ARMv8.3+), KFENCE | Hard |
| 5.15 | 2022-2024 | +MTE (ARMv8.5+, optional) | Hard |
| 6.1 | 2023+ | All mitigations + MTE on by default | Very Hard |

## Firmware Offset Discovery Workflow

For each new device/firmware combination, discover kernel symbol offsets:

### Method 1: Extract from factory image
```bash
# Download firmware
# Extract system/vendor images
# Find kernel: boot.img or vendor_boot.img
# Unpack: unpack_bootimg.py or magiskboot
# Decompress kernel (gz/lz4/xz)
# Find symbols: strings Image | grep "commit_creds\|init_cred"
# Calculate offsets from kernel base (usually 0xffffffc008000000 or 0x80000000)
```

### Method 2: From /proc/kallsyms (rooted device)
```bash
adb shell cat /proc/kallsyms | grep -E "(avc_denied|sel_read_enforce|commit_creds|init_cred|selinux_enforcing)"
```

### Method 3: From kernel source (open-source kernels)
```bash
# Many OEMs publish kernel source (required by GPL)
# Samsung: https://opensource.samsung.com
# Xiaomi: https://github.com/MiCode
# OnePlus: https://github.com/OnePlusOSS
# Extract Symbol.map or System.map from build artifacts
```

### Method 4: Pattern matching (binary analysis)
```python
# For Mali exploits: find avc_denied by pattern
# Pattern: strb wzr, [x0]; mov x0, #0; ret
# ARM64 encoding: 0x3900001f 0xd2800000 0xd65f03c0
# Search kernel .text section for these bytes

# For commit_creds calling pattern:
# Pattern: adrp x0, init_cred; add x0, x0, #offset; bl commit_creds
# The offsets in adrp/add instructions reveal the firmware-specific values
```

### Auto-Discovery Script Pattern
```bash
# Extract kernel, search for shellcode landing points
python3 << EOF
import struct
kernel = open("Image", "rb").read()

# Search for "strb wzr, [x0]; mov x0, #0; ret" (avc_denied patch site)
avc_patch = b'\x1f\x00\x00\x39\x00\x00\x80\xd2\xc0\x03\x5f\xd6'
offset = kernel.find(avc_patch)
if offset >= 0:
    print(f"avc_denied patch site: 0x{offset:x}")
EOF
```

## Regional Variant Awareness

| Device Line | US/China Variant | International Variant | GPU Diff |
|-------------|-----------------|----------------------|----------|
| Samsung S21 | SD 888 (Adreno) | Exynos 2100 (Mali) | Different exploit family |
| Samsung S22 | SD 8 Gen 1 (Adreno) | Exynos 2200 (Mali) | Different exploit family |
| Samsung S23/S24 | All SD 8 Gen 2/3 | All SD 8 Gen 2/3 | Same! (Samsung stopped Exynos) |
| Xiaomi Mi | SD (Adreno) | SD (Adreno) | Same |
| Pixel 6/7/8/9 | Tensor (Mali) | Tensor (Mali) | Same (Google uses Tensor globally) |
| OnePlus | SD (Adreno) | SD (Adreno) | Same |

**Key rule:** Always check the specific model number (e.g., SM-S901B vs SM-S901U). The "B" suffix means Exynos; "U" suffix means Snapdragon.

## Agentic Self-Improvement Loop for Device Adaptation

```
Device model identified
    ↓
1. LOOKUP: model → chipset → GPU → kernel version
    ↓ (use public databases: GSMArena, DeviceSpecifications, kernel sources)
2. MAP: GPU type → exploit family (Mali JM / Mali CSF / Adreno)
    ↓
3. CHECK: Driver version? (Mali rXXp0, Adreno kgsl version)
    ↓ (get from /proc/mali/version or kgsl sysfs)
4. MATCH: Driver version → known CVEs
    ↓ (cross-reference Mali/Adreno vulnerability list)
5. DISCOVER: Are firmware offsets known? 
    ↓ NO → download firmware, extract kernel, pattern-match symbols
    ↓ YES → use existing offsets
6. ADAPT: Compile exploit with target offsets
    ↓
7. DELIVER: Choose delivery path
    ├── Browser exploit URL? → Path A (browser_exploit.html + kernel exploit)
    ├── APK delivery? → Path B (apk_patcher.sh + C2)
    ├── Physical access? → Phase 2/3 (Faraday → bypass → extract)
    └── Network access? → Phase 1 (evil twin → captive portal)
    ↓
8. EXECUTE: Run exploit → gain root → extract evidence → produce reports
```

## Quick Reference: Device → Exploit Path

| Device | Chipset | GPU | Architecture | Best Exploit Family |
|--------|---------|-----|-------------|-------------------|
| Samsung S21 (Intl) | Exynos 2100 | Mali-G78 | JM | CVE-2022-38181 patterns |
| Samsung S22 (Intl) | Exynos 2200 | Mali-G78 | JM/CSF | CVE-2022-38181 or CVE-2025-0072 |
| Samsung S21 (US) | SD 888 | Adreno 660 | - | CVE-2022-25664 patterns |
| Samsung S22 (US) | SD 8 Gen 1 | Adreno 730 | - | CVE-2022-25664 patterns |
| Pixel 6 | Tensor G1 | Mali-G78 | JM | CVE-2022-38181 |
| Pixel 7 | Tensor G2 | Mali-G710 | CSF | CVE-2023-6241 patterns |
| Pixel 8 | Tensor G3 | Mali-G715 | CSF | CVE-2025-0072 |
| Oppo Reno 8T | Dimensity 700 | Mali-G57 | JM | CVE-2022-38181 patterns |
| Realme Narzo 50 | Dimensity 700 | Mali-G57 | JM | CVE-2022-38181 patterns |
| Redmi Note 12 | Dimensity 1080 | Mali-G68 | CSF | CVE-2025-0072 patterns |
| Xiaomi Mi 13 | SD 8 Gen 2 | Adreno 740 | - | CVE-2022-25664 patterns |
| OnePlus 9 Pro | SD 888 | Adreno 660 | - | CVE-2022-25664 patterns |
| Oppo Find N2 | Dimensity 9000+ | Mali-G710 | CSF | CVE-2025-0072 patterns |
