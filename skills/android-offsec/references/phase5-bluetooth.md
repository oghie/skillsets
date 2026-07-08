# Phase 5: Bluetooth Offensive

## Reconnaissance

```bash
# Classic Bluetooth scan
hcitool scan
hcitool inq --flush

# Device info
hcitool info <BD_ADDR>

# Service enumeration
sdptool browse <BD_ADDR>

# BLE scanning
hcitool lescan

# BlueZ interactive
bluetoothctl
[bluetooth]# scan on
[bluetooth]# devices
[bluetooth]# info <MAC>
```

### Via Android ADB
```bash
adb shell am start -a android.bluetooth.adapter.action.REQUEST_DISCOVERABLE
adb shell settings get global bluetooth_on
```

## Exploitation Catalog

### BlueBorne (CVE-2017-0781/0782/0783)
- **Affects:** Android 4.4 – 7.x
- **Type:** RCE without pairing
- **Vector:** Bluetooth stack memory corruption
- **Value:** High — fully remote, no user interaction

### BlueFrag (CVE-2020-0022)
- **Affects:** Android 8.0 – 9.0
- **Type:** RCE via Bluetooth daemon
- **Vector:** Malformed L2CAP packet
- **Value:** High — remote, adjacent network

### BleedingTooth (CVE-2020-24490)
- **Affects:** BlueZ 5.x < 5.55 (Linux kernel)
- **Type:** Heap overflow
- **Note:** Affects Android devices using BlueZ stack

### KNOB Attack (CVE-2019-9506)
- **Type:** BR/EDR key negotiation downgrade
- **Result:** Force 1-byte encryption entropy → eavesdrop on any Bluetooth traffic
- **Value:** Universal for Bluetooth Classic

### BIAS Attack (CVE-2020-10135)
- **Type:** Bluetooth Impersonation
- **Result:** Impersonate previously paired device without long-term key
- **Value:** High for persistent access

### BLE Spoofing
- Spoof legitimate BLE peripherals to trigger app behavior
- Many apps trust BLE peripheral identity without challenge-response
- Targets: fitness trackers, smart locks, car keys

### Bluetooth Keyboard Injection
- If device has paired Bluetooth keyboard
- Spoof keyboard → inject keystrokes
- May bypass lock screen if "Unlock with Bluetooth keyboard" enabled

## Post-Exploitation via Bluetooth

Once you have Bluetooth-level access:
- Extract paired device list + link keys (for impersonation)
- **PBAP** (Phone Book Access Profile) → contacts
- **MAP** (Message Access Profile) → SMS/MMS/email
- **OBEX** file transfer → file system access
- **HID spoofing** → input injection
