# Phase 4: Mobile App Offensive Analysis

**When:** Analyzing a specific APK for vulnerabilities — deeplink exploits, account takeover, data extraction.

## Static Analysis Workflow

### 1. Decompile
```bash
apktool d target.apk -o decompiled/
jadx target.apk -d jadx_output/
```

### 2. Manifest Analysis
- **Exported components:** Activities, Services, Receivers, Providers with `android:exported="true"`
- **Permissions:** Custom permissions, dangerous permissions requested
- **Deeplink intent filters:** All `<intent-filter>` with `android.intent.action.VIEW` + `data android:scheme`

### 3. Secrets Hunt
Search decompiled code for:
```
"key", "secret", "token", "password", "api_key", "auth"
"BEGIN PRIVATE KEY", "BEGIN RSA PRIVATE KEY"
"googleapis.com", "firebaseio.com", ".cloudfunctions.net"
"https://" (hardcoded URLs with credentials)
```

### 4. WebView Audit
- `setJavaScriptEnabled(true)` — XSS surface
- `onReceivedSslError` with empty override — SSL bypass
- `setAllowFileAccess(true)` — local file access
- `addJavascriptInterface` — JS bridge exploitation surface

### 5. Native Libraries
- Check `.so` files for hardcoded strings: `strings lib/*.so | grep -E "(key|secret|token|http)"`
- Weak crypto: custom AES/RSA implementations, hardcoded IVs

### 6. Protection Assessment
- **Cert pinning:** Custom TrustManager, OkHttp CertificatePinner, network_security_config.xml
- **Root detection:** Check for `su`, `Magisk`, `Superuser.apk`, test-keys build tag
- **Emulator detection:** Check Build.FINGERPRINT, Build.MODEL, QEMU pipes
- **Obfuscation:** ProGuard/DexGuard mapping, string encryption

## Dynamic Analysis

### Environment Setup
```bash
# Frida server on device
adb push frida-server-<arch> /data/local/tmp/
adb shell chmod 755 /data/local/tmp/frida-server-<arch>
adb shell /data/local/tmp/frida-server-<arch> &

# Objection
pip install objection
objection -g com.target.app explore
```

### Frida Hooks
```bash
# Bypass root detection
frida -U -l bypass_root.js com.target.app

# SSL pinning bypass
objection -g com.target.app explore
# > android sslpinning disable

# Trace crypto
frida-trace -U -i "Cipher*" com.target.app
```

### Xposed + Inspeckage (Automated Runtime Hooking)

When you need comprehensive, always-on hooks without writing individual Frida scripts, use Xposed Framework with Inspeckage module:

**Setup:**
```bash
# 1. Install Xposed Framework on rooted device/emulator
# Download from: https://forum.xda-developers.com/xposed

# 2. Install Inspeckage Xposed module
# Download APK from: https://github.com/ac-pm/Inspeckage/releases
adb install Inspeckage.apk

# 3. Enable Inspeckage in Xposed Installer → reboot

# 4. Start Inspeckage, select target app, enable hooks
# Inspeckage runs a WebSocket server on port 8008

# 5. Forward port to desktop
adb forward tcp:8008 tcp:8008

# 6. Open Inspeckage web UI
open http://localhost:8008
```

**Key Inspeckage Hooks (zero code required):**

| Category | What It Hooks | Investigation Value |
|----------|--------------|-------------------|
| **Crypto** | Cipher.doFinal, MAC, MessageDigest, SecureRandom | Reveals encryption keys, IVs, and algorithms |
| **Intents** | startActivity, sendBroadcast, startService, bindService | Maps all IPC interactions and deeplink flows |
| **File System** | File, FileInputStream, FileOutputStream, SharedPreferences | Reveals what files the app reads/writes |
| **Network** | HttpURLConnection, OkHttp, WebView URL loads | Dumps all HTTP/HTTPS URLs and headers |
| **SQLite** | SQLiteDatabase.execSQL, rawQuery, insert, update, delete | Captures all database operations |
| **WebView** | loadUrl, addJavascriptInterface, WebViewClient callbacks | Maps all WebView interactions and JS bridges |
| **Clipboard** | ClipboardManager.setPrimaryClip | Captures clipboard changes |
| **Reflection** | Method.invoke, Class.forName | Detects obfuscation bypass and hidden API use |
| **Hooks** | PackageManager, Process, Runtime.exec | Detects security checks and shell commands |

**Integration with Static Analysis:**
1. Run static analysis first (JADX) → identify suspicious code paths
2. Enable Inspeckage hooks for those specific categories
3. Trigger the suspicious code (deeplink, button press, network call)
4. Inspeckage output confirms/reveals actual runtime behavior
5. Cross-reference: JADX shows what code *can* do; Inspeckage shows what it *actually does*

### Traffic Interception
1. Configure Burp Suite as upstream proxy
2. Install Burp CA on device (system cert store for Android 7+)
3. Bypass SSL pinning with Frida/objection
4. Monitor HTTP/HTTPS, WebSocket, gRPC

### Key Targets
- Authentication flow (JWT, OAuth, session cookies)
- API endpoints — test IDOR, parameter pollution
- Deeplink handling — test all intent filter paths
- WebView JS bridges — XSS → code execution?
- FileProvider — directory traversal?
- IPC endpoints — unauthorized access?

## Deeplink Exploitation

### Map Handlers
```bash
grep -r "android.intent.action.VIEW" decompiled/
grep -r "data android:scheme" decompiled/
grep -r "data android:host" decompiled/
```

Use `scripts/deeplink_fuzzer.py` for automated enumeration and testing.

### Test Payloads
```bash
adb shell am start -W -a android.intent.action.VIEW \
  -d "scheme://host/path?param=test" com.target.app
```

### Attack Patterns
1. **Open redirect:** deeplink → WebView → redirect to attacker → JS execution
2. **Parameter injection:** `?return_url=http://evil.com` → token leaked via Referer
3. **Path traversal:** `?file=../../../../data/data/com.target.app/shared_prefs/auth.xml`
4. **Account takeover:** deeplink auto-fills OTP/resets password with attacker-controlled params
5. **WebView JS bridge:** deeplink param lands in WebView → `javascript:` URI → native function invocation

## Account Takeover Methodology

1. Identify recovery/reset flows in decompiled code
2. Test for weak OTP generation (predictable, TOTP without secret)
3. Check session tokens: valid across devices? reusable?
4. Test rate limiting on login/OTP endpoints
5. Check deeplinks with auto-login params (`myapp://login?token=xyz` where `xyz` is guessable)
