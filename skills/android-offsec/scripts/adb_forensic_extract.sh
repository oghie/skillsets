#!/bin/bash
# adb_forensic_extract.sh — Automated Android forensic extraction
# Usage: bash adb_forensic_extract.sh <output_dir>

set -euo pipefail

OUTDIR="${1:?Usage: $0 <output_directory>}"
mkdir -p "$OUTDIR"/{data,media,system,databases,logs,evidence}

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
EVIDENCE_LOG="$OUTDIR/evidence_manifest.txt"
echo "Evidence Extraction started: $TIMESTAMP" > "$EVIDENCE_LOG"
echo "Device: $(adb devices | tail -1)" >> "$EVIDENCE_LOG"

hash_and_log() {
    local file="$1"
    local desc="$2"
    local sha256=$(shasum -a 256 "$file" | cut -d' ' -f1)
    echo "[$TIMESTAMP] $desc | $file | SHA256: $sha256" >> "$EVIDENCE_LOG"
}

echo "[*] Collecting device info..."
adb shell getprop ro.build.version.release > "$OUTDIR/device/android_version.txt"
adb shell getprop ro.build.version.security_patch > "$OUTDIR/device/security_patch.txt"
adb shell getprop ro.product.model > "$OUTDIR/device/model.txt"
adb shell getprop ro.product.manufacturer > "$OUTDIR/device/manufacturer.txt"
adb shell getprop ro.serialno > "$OUTDIR/device/serial.txt"
adb shell getprop ro.build.fingerprint > "$OUTDIR/device/fingerprint.txt"

echo "[*] Checking root status..."
adb shell su -c "id" > "$OUTDIR/device/root_check.txt" 2>/dev/null || echo "No root" > "$OUTDIR/device/root_check.txt"

ROOTED=$(grep -q "uid=0" "$OUTDIR/device/root_check.txt" && echo "yes" || echo "no")

if [ "$ROOTED" = "yes" ]; then
    echo "[*] Rooted device — pulling full /data partition..."
    adb pull /data/data/ "$OUTDIR/data/" 2>/dev/null || true
    adb pull /data/media/0/ "$OUTDIR/media/" 2>/dev/null || true
    adb pull /data/system/ "$OUTDIR/system/" 2>/dev/null || true
    adb pull /data/misc/ "$OUTDIR/misc/" 2>/dev/null || true

    echo "[*] Extracting system dumps..."
    adb shell su -c "dumpsys" > "$OUTDIR/logs/dumpsys.txt" 2>/dev/null || true
    adb shell su -c "bugreport" > "$OUTDIR/logs/bugreport.zip" 2>/dev/null || true
else
    echo "[*] Unrooted — using ADB backup..."
    adb backup -apk -shared -all -system -f "$OUTDIR/backup.ab" 2>/dev/null || echo "Backup may require device interaction"
    echo "[*] Extracting accessible databases..."
    adb pull /sdcard/ "$OUTDIR/media/" 2>/dev/null || true
fi

echo "[*] Extracting databases..."
for db in \
    /data/data/com.android.providers.telephony/databases/mmssms.db \
    /data/data/com.android.providers.contacts/databases/contacts2.db \
    /data/data/com.android.providers.calendar/databases/calendar.db \
    /data/data/com.google.android.gms/databases/ \
    /data/data/com.android.chrome/app_chrome/Default/History \
    /data/data/com.android.browser/databases/browser2.db \
    /data/data/com.whatsapp/databases/msgstore.db \
    /data/data/com.whatsapp/databases/wa.db \
    /data/data/org.telegram.messenger/files/cache4.db; do
    adb pull "$db" "$OUTDIR/databases/" 2>/dev/null || true
done

echo "[*] Extracting WhatsApp key..."
adb pull /data/data/com.whatsapp/files/key "$OUTDIR/databases/whatsapp.key" 2>/dev/null || true

echo "[*] Capturing screenshots..."
adb exec-out screencap -p > "$OUTDIR/evidence/screenshot.png"
hash_and_log "$OUTDIR/evidence/screenshot.png" "Device screenshot"

echo "[*] Extracting WiFi passwords..."
adb pull /data/misc/wifi/wpa_supplicant.conf "$OUTDIR/wpa_supplicant.conf" 2>/dev/null || true

echo "[*] Extracting logcat..."
adb logcat -d > "$OUTDIR/logs/logcat.txt" 2>/dev/null || true

echo "[*] Generating hashes for all extracted files..."
find "$OUTDIR" -type f ! -name "evidence_manifest.txt" | while read f; do
    hash_and_log "$f" "$(basename "$f")"
done

echo "[*] Searching for crypto evidence..."
grep -rE '(0x[a-fA-F0-9]{40}|[13][a-km-zA-HJ-NP-Z1-9]{25,34}|T[a-km-zA-HJ-NP-Z1-9]{33})' "$OUTDIR" > "$OUTDIR/crypto_addresses.txt" 2>/dev/null || true
grep -riE '(seed|mnemonic|recovery.phrase|private.key|wallet)' "$OUTDIR" > "$OUTDIR/crypto_keywords.txt" 2>/dev/null || true

echo ""
echo "[✓] Extraction complete: $OUTDIR"
echo "[✓] Evidence manifest: $EVIDENCE_LOG"
echo "[✓] Files extracted: $(find "$OUTDIR" -type f | wc -l)"
