# Phase 3: Post-Exploit Forensic Extraction

**When:** ADB shell access achieved (rooted or unrooted). Comprehensive evidence collection.

## Start Here

```bash
# Run the bundled automation script first — it handles complete extraction + hashing
bash scripts/adb_forensic_extract.sh /path/to/case/output
```

The script automates: full file pull, SHA-256 hashing per file, evidence manifest generation, database extraction, media dump, and system info collection.

## Manual Extraction (if script unavailable)

### Unrooted (limited)
```bash
adb backup -apk -shared -all -system -f backup.ab
adb backup -f app_data.ab com.target.app
```

### Rooted (full access)
```bash
adb pull /data/data/ /local/extraction/data/
adb pull /data/media/0/ /local/extraction/sdcard/
adb pull /data/system/ /local/extraction/system/
```

### Database Extraction
```bash
adb pull /data/data/com.android.providers.telephony/databases/mmssms.db
adb pull /data/data/com.android.providers.contacts/databases/contacts2.db
```

### Full Filesystem Dump
```bash
adb shell su -c "dd if=/dev/block/mmcblk0 of=/sdcard/full_dump.img bs=4096"
```

### Live Capture
```bash
adb exec-out screencap -p > device_screenshot.png
adb shell screenrecord /sdcard/live_recording.mp4
```

## Evidence Categories

Investigate ALL of these. Start broad → narrow based on findings.

### Communication

| App | Path | Notes |
|-----|------|-------|
| Call Logs | `content://call_log/calls` | Also `contacts2.db` |
| SMS/MMS | `content://sms/` | Recover deleted from SQLite free pages |
| WhatsApp | `/data/data/com.whatsapp/databases/msgstore.db` | Decrypt crypt14 with key from `/files/key` |
| Telegram | `/data/data/org.telegram.messenger/files/` | `cache4.db` |
| Signal | `/data/data/org.thoughtcrime.securesms/databases/` | Encrypted |
| Gmail | `/data/data/com.google.android.gm/databases/` | |
| WeChat | `/data/data/com.tencent.mm/` | EnMicroMsg.db |
| LINE | `/data/data/jp.naver.line.android/databases/` | |
| Viber | `/data/data/com.viber.voip/databases/viber_messages` | Key file in `/files/preferences/`; media in `/files/Media/` |
| KakaoTalk | `/data/data/com.kakao.talk/databases/KakaoTalk.db` | Multi-DB (KakaoTalk.db, KakaoTalk2.db per account); encrypted |
| Deleted messages | SQLite WAL + journal files + free page carving | |

### Financial

- **Wallet apps:** Binance, Trust Wallet, MetaMask, Coinbase, Exodus, BlueWallet, Samourai, Wasabi
- **Seed phrase search:** Scan all text for BIP39 word lists (2048-word dictionary)
- **Blockchain addresses:** Regex search for BTC (`[13][a-km-zA-HJ-NP-Z1-9]{25,34}`), ETH (`0x[a-fA-F0-9]{40}`), TRX, SOL
- **Banking apps:** Transaction history, beneficiary lists, account statements
- **Payment apps:** Google Pay, Samsung Pay, PayPal, Venmo, CashApp, GoPay, OVO, DANA
- **E-commerce:** Tokopedia, Shopee, Lazada — purchase history, shipping addresses
- **Hidden apps:** Calculator vault apps often hide financial records

### Multimedia

- Camera folder, screenshots (`/Pictures/Screenshots/`), downloads
- EXIF extraction on all images: GPS coordinates, timestamps, device model
- Deleted photos: file carving from `/data/media/` and external SD
- Thumbnail caches: `.thumbdata` — contains thumbnails of deleted images
- Screen recordings, voice recordings, CCTV/NVR apps

### Location

- Google Location History: `/data/data/com.google.android.gms/databases/`
- `CacheCellInfo` + `CacheWifiInfo` tables in Google Play Services
- App location caches: ride-hailing, food delivery, dating apps
- Geotagged photos (EXIF GPS)
- WiFi connection history → maps physical locations
- Bluetooth connection history → paired devices, timestamps
- Activity Recognition data

### App-Specific

- **Social:** Facebook, Instagram, Twitter/X, TikTok, Snapchat, Reddit, LinkedIn
- **Dating:** Tinder, Bumble, Badoo, OkCupid
- **Encrypted chat:** Threema, Wire, Session, Status
- **Ride-hailing:** Uber, Grab, Gojek, Lyft
- **Browsers:** Chrome, Firefox, Samsung Internet, Brave, Opera, UC
- **Saved passwords:** Chrome password manager, Samsung Pass
- **Autofill:** Addresses, credit cards, personal info
- **Keyboard cache:** Gboard/SwiftKey personal dictionary (learned words = names, addresses)
- **Clipboard:** Android 10+ clipboard access logs
- **Cloud:** Google Drive, Dropbox, OneDrive, Mega
- **VPN/Proxy apps:** OPSEC awareness indicator
- **Burner phone apps:** TextNow, 2ndLine, Hushed
- **Encrypted notes:** Standard Notes, Joplin, Obsidian

### System

- `/data/system/` — accounts DB, locksettings, app usage stats, notification history
- `dumpsys` full dump — running services, battery exemptions
- `logcat` — app crashes, intents, debug output
- `/data/anr/` — ANR traces with sensitive stack data
- `bugreport` — comprehensive device snapshot
- MAC times: modified, accessed, changed
- USB connection history
- `/data/system_ce/0/` — credential-encrypted per-user storage
- `/data/misc/` — WiFi passwords (plaintext `wpa_supplicant.conf`), BT pairings, VPN configs

## Chain of Custody

For every evidence artifact:
1. Record extraction timestamp (UTC)
2. Generate SHA-256 hash immediately
3. Document exact command used, device state, operator ID
4. Never modify original files — work on copies
5. Maintain evidence log: file → hash → forensic significance

The automated extraction script (`scripts/adb_forensic_extract.sh`) handles steps 1-2 automatically.
