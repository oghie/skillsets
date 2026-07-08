# Phase 2: Locked Device Bypass

**When:** Physical possession, but device locked (PIN/password/pattern/biometric).

## Step 0: Faraday Isolation (MANDATORY — Do This First)

Before ANY interaction with a seized device, isolate it from all radio signals. A single remote command can wipe the device, lock it permanently, or alert the target's associates.

### Why
- **Remote wipe:** Find My Device / Samsung Find / Xiaomi Cloud can erase the device remotely
- **Remote lock:** Device can be locked with a new PIN remotely → adds additional barrier
- **Cellular tracking:** Device continuously reports location via cellular triangulation
- **WiFi/BT:** Device may auto-connect to known networks and receive wipe/lock commands
- **Evidence integrity:** Radio isolation must be documented as part of chain of custody

### Equipment
- **Faraday bag:** Commercial RF-shielded pouch (Mission Darkness, SLNT, Silent Pocket)
- **Faraday cage/box:** Metal enclosure with conductive gasket (lab-grade)
- **RF-shielded container:** Aluminum foil wrap layered 3+ times (field expedient)
- **Verification:** Place a phone inside and call it — no ring = effective isolation

### Procedure
1. **Before removing from crime scene:** Place device in Faraday bag while still in situ
2. **Document:** Timestamp when device entered isolation (for chain of custody log)
3. **Transport:** Device stays in Faraday bag throughout transport to lab
4. **Lab arrival:** If device is ON, keep bagged until power analysis complete
5. **During extraction:** If ADB over USB is used, the wired connection does not break isolation
6. **Removal risks:** Only remove from isolation when ready to perform bypass/extraction; every second outside isolation is a second the device could receive a remote command

### Edge Cases
- **Airplane mode:** Do not trust airplane mode — baseband may still be active for emergency services
- **No SIM:** Still isolate — WiFi and Bluetooth radios remain active
- **Powered off:** Still isolate during transport — prevents accidental power-on and cellular registration
- **Battery removal:** If battery is removable, remove it as additional assurance; still keep bagged

### Chain of Custody Entry
```
[UTC Timestamp] Device placed in Faraday bag #FB-001. Verified isolation:
cellular signal 0 bars, WiFi networks 0, Bluetooth devices 0.
Battery: [XX]%. Device state: [ON/OFF/Screen locked].
```

## Step 1: Triage

Determine before attempting bypass:
- Device model (recovery/bootloader screen)
- Android version and patch level
- Security patch date (critical — exploits patched monthly)
- Lock type (PIN/password/pattern/fingerprint/face)
- OEM unlock status (bootloader)
- FRP (Factory Reset Protection) status
- USB debugging: enabled or not?

## Step 2: Version-Specific Bypass

### Android 4.x – 6.x (Legacy)
- Emergency call screen bypasses (dialer codes, character overflow)
- Lockscreen media player intent hijacking
- Camera intent bypass → settings access
- ADB from recovery with custom binary (no auth prompt on old versions)

### Android 7.x – 9.x
- Split-screen / multi-window bypasses
- Google Assistant / Voice Match bypass to settings
- SIM PIN → emergency dialer → settings chain
- Password reset via linked account (if target's email compromised)

### Android 10 – 13
- EDL (Emergency Download Mode) for Qualcomm devices
- Bootrom exploits (amonet, firehose) per chipset
- CVE-based lockscreen bypass — search Android Security Bulletin
- Secure USB debugging auth via TEE token extraction (hardware-level)
- ISP / JTAG extraction (chip-off forensics)

### Android 14 – 17 (Modern)
- Check CVE database for lockscreen bypass CVEs → `references/cve-feed.md`
- Bootloader unlock via OEM unlocking (rare)
- Commercial forensic tools: Cellebrite UFED, Oxygen, XRY
- ADB pairing bypass (wireless debugging pairing code vulnerabilities)
- TEE/TrustZone exploitation for key extraction
- Secure Element attacks for biometric template extraction
- MTE bypass research on Android 15+

### Universal Techniques
- Dictionary/rainbow table for common PINs (0000, 1234, birth years)
- Smudge attack (screen smudge pattern analysis)
- Thermal imaging (recent touch heat signature)
- Shoulder surfing (CCTV or direct observation)
- Biometric spoofing (fingerprint lift, 3D face for older face unlock)

## Step 3: ADB Enablement

If USB debugging is NOT enabled:

- Recovery mode ADB sideload (limited, can push packages)
- EDL/Firehose → flash custom recovery with ADB enabled
- Bootloader unlock → flash custom boot image with ADB defaults + root
- **Samsung:** Odin/Heimdall flash engineering bootloader
- **MTK devices:** SP Flash Tool with scatter file + preloader bypass
- **Qualcomm:** QFIL/QPST with programmer file (firehose)

## Step 4: FRP (Factory Reset Protection) Bypass

FRP activates after a factory reset — the device demands the last synced Google account credentials before completing setup. This is encountered when a target resets their device before seizure or when a device is found in post-reset state.

### FRP Architecture
- Tied to Google account that was active before the reset
- Persists across factory resets — stored in a protected partition (frp/regulatory)
- Triggers during Setup Wizard after first WiFi connection
- Bypass = reach any setting that lets you add a new Google account or open a browser

### Version-Specific Techniques

**Android 5.x – 7.x (Easiest):**
- Accessibility menu chain: TalkBack → Help & Feedback → YouTube → Chrome → download APK → Settings
- Emergency dialer → code to open settings → enable USB debugging
- OTG cable with keyboard → Windows key shortcuts → access settings
- Samsung: Real-time text (RTT) → Samsung keyboard settings → Samsung Browser → download FRP bypass app

**Android 8.x – 9.x:**
- TalkBack → draw L gesture → TalkBack settings → Help → YouTube → Chrome
- Samsung Keyboard: Settings → Language → Samsung Browser → download APK
- Emergency call → Share location → Maps → Chrome
- Google Assistant: "Open Settings" (patched on newer Google Play Services)

**Android 10 – 11:**
- TalkBack + Samsung keyboard multi-step chains still work on Samsung devices
- Accessibility Suite → gesture navigation → tutorial → YouTube → Chrome
- OTG mouse/keyboard methods becoming harder (restricted USB during setup)
- Xiaomi: Mi Account → "Forgot Password" → SMS → back gesture (race condition)
- Huawei: Emergency backup → HiSuite → file manager → install APK

**Android 12 – 13 (Harder):**
- Accessibility menu paths largely patched
- Samsung: Still sometimes possible via specific keyboard → Samsung Browser chains (varies by One UI version)
- Most success requires commercial tools at this version

**Android 14+ (Very Hard):**
- Google has aggressively hardened FRP
- Commercial tools (SamFw, iToolab UnlockGo, Tenorshare 4uKey) are the primary path
- Most manual methods patched within weeks of discovery

### Tools

| Tool | Type | Platform |
|------|------|----------|
| SamFw FRP Tool | Free, Samsung-focused | Windows |
| iToolab UnlockGo | Paid, multi-brand | Windows/Mac |
| Tenorshare 4uKey | Paid, multi-brand | Windows/Mac |
| DroidKit | Paid, multi-brand | Windows/Mac |

### OEM-Specific FRP Patterns

**Samsung:** The most targeted. Chains exploit Samsung's custom Setup Wizard keyboard → Samsung Browser path. Test Mode (dial *#0*#) sometimes bypassable. Combination firmware (engineering boot) can skip FRP entirely.

**Xiaomi:** Mi Account lock. If the device uses Mi Account instead of Google, the attack surface shifts to Xiaomi's cloud infrastructure. Browser-based bypasses via Mi Browser in setup.

**Huawei:** Huawei ID lock. EMUI setup has fewer accessibility bypass paths than Samsung but more cloud-based recovery options.

**Oppo/Realme:** ColorOS FRP is relatively new. Security research is thinner. Test TalkBack chains first, fall back to commercial tools.

### Post-Bypass Steps
1. Immediately enable USB debugging after bypass
2. Disable automatic updates (prevent Google Play Services from patching the bypass method)
3. Add a new Google account (the bypassed device will work normally)
4. Document the FRP bypass method used in chain of custody

## Decision Matrix

| Chipset | Primary Path | Fallback |
|---------|-------------|----------|
| MediaTek | MTK BROM → mtkclient | ISP/chip-off |
| Qualcomm | EDL → firehose | ISP/JTAG |
| Exynos | Commercial tool (UFED) | Chip-off |
| Tensor | Commercial tool (UFED/GrayKey) | National agency |
| Unisoc | SPD Flash Tool | ISP |
