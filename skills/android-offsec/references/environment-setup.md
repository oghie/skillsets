# Environment Pre-Flight: Investigator Workstation Setup

Before ANY offensive Android operation, verify the investigator's environment. This is **Step 0** — mandatory before phase selection.

## OS Detection

```bash
# Auto-detect OS and architecture
case "$(uname -s)" in
    Linux*)     OS="linux";;
    Darwin*)    OS="macos";;
    CYGWIN*|MINGW*|MSYS*) OS="windows";;
    *)          OS="unknown";;
esac
ARCH=$(uname -m)
echo "OS: $OS, Arch: $ARCH"
```

## Mandatory Tools Checklist

### Tier 1: Always Required

| Tool | Purpose | Linux | macOS | Windows | Verify Command |
|------|---------|-------|-------|---------|---------------|
| **ADB** | Android device interaction | `apt install adb` | `brew install android-platform-tools` | [Android SDK Platform Tools](https://developer.android.com/studio/releases/platform-tools) | `adb version` |
| **Python 3.10+** | Scripts, exploit dev, C2 server | `apt install python3` | `brew install python@3.11` | `choco install python` | `python3 --version` |
| **pip3** | Python package management | Included with Python | Included with Python | Included with Python | `pip3 --version` |
| **git** | Repository cloning | `apt install git` | `brew install git` | `choco install git` | `git --version` |
| **curl / wget** | File downloads | `apt install curl` | Built-in | Built-in | `curl --version` |
| **OpenSSL** | SSL certs, hashing | `apt install openssl` | Built-in | `choco install openssl` | `openssl version` |

### Tier 2: Phase-Dependent

| Tool | Needed For | Linux | macOS | Verify |
|------|-----------|-------|-------|--------|
| **Docker** | Container isolation, fuzzing, C2 | `apt install docker.io` | `brew install docker` | `docker --version` |
| **Android SDK** | APK building, emulator | `apt install android-sdk` | `brew install android-sdk` | `sdkmanager --list` |
| **Android Emulator** | App testing, camera injection | Via Android Studio | Via Android Studio | `emulator -list-avds` |
| **APKTool** | APK decompilation | `apt install apktool` | `brew install apktool` | `apktool --version` |
| **JADX** | DEX→Java decompilation | `apt install jadx` | `brew install jadx` | `jadx --version` |
| **Frida** | Dynamic instrumentation | `pip3 install frida-tools` | `pip3 install frida-tools` | `frida --version` |
| **Burp Suite** | Traffic interception | Download from portswigger.net | Download from portswigger.net | `java -jar burpsuite.jar` |
| **Wireshark / tcpdump** | Network capture | `apt install wireshark` | `brew install wireshark` | `tshark --version` |
| **Aircrack-ng** | WiFi attacks | `apt install aircrack-ng` | `brew install aircrack-ng` | `aircrack-ng --help` |
| **Bettercap** | Network MITM | `apt install bettercap` | `brew install bettercap` | `bettercap --version` |
| **Metasploit** | Exploit framework | `curl https://raw.../msfinstall > msfinstall` | Same | `msfconsole --version` |
| **GDB-multiarch** | ARM debugging | `apt install gdb-multiarch` | `brew install gdb` | `gdb-multiarch --version` |
| **pwntools** | Exploit development | `pip3 install pwntools` | `pip3 install pwntools` | `python3 -c "from pwn import *"` |
| **OpenCL** | Mali CSF exploits | `apt install ocl-icd-opencl-dev` | Built-in | `clinfo` |
| **GPU Drivers** | Deepfake, fuzzing | `apt install nvidia-driver` or ROCm | Built-in (Metal) | `nvidia-smi` or `system_profiler SPDisplaysDataType` |

### Tier 3: Deepfake-Specific (Phase 8)

| Tool | Linux | macOS | Windows | Verify |
|------|-------|-------|---------|--------|
| **OBS Studio** | `apt install obs-studio` | `brew install obs` | obsproject.com | `obs --version` |
| **v4l2loopback** | `modprobe v4l2loopback` | N/A (use OBS VirtualCam) | N/A (use OBS VirtualCam) | `lsmod | grep v4l2` |
| **FFmpeg** | `apt install ffmpeg` | `brew install ffmpeg` | `choco install ffmpeg` | `ffmpeg -version` |
| **CUDA / ROCm** | `apt install nvidia-cuda-toolkit` | N/A (use MPS) | `choco install cuda` | `nvcc --version` |
| **PyTorch** | `pip3 install torch` | `pip3 install torch` | `pip3 install torch` | `python3 -c "import torch; print(torch.cuda.is_available())"` |
| **OpenCV** | `pip3 install opencv-python` | `pip3 install opencv-python` | `pip3 install opencv-python` | `python3 -c "import cv2"` |

## Environment Pre-Flight Script

Run this before any operation:

```bash
#!/bin/bash
# preflight.sh — verify investigator environment
set -e

echo "=== Android Offsec Environment Pre-Flight ==="
echo ""

# OS Detection
OS="$(uname -s)"
ARCH="$(uname -m)"
echo "[*] OS: $OS / $ARCH"

# Tier 1: Always Required
echo ""
echo "[*] Tier 1 — Mandatory Tools:"
for tool in adb python3 pip3 git curl openssl; do
    if command -v $tool &>/dev/null; then
        echo "  [✓] $tool ($(which $tool))"
    else
        echo "  [✗] $tool — MISSING"
    fi
done

# Python packages
echo ""
echo "[*] Python packages:"
for pkg in frida-tools pwntools flask requests; do
    if python3 -c "import ${pkg/-/_}" 2>/dev/null; then
        echo "  [✓] $pkg"
    else
        echo "  [✗] $pkg — MISSING (pip3 install $pkg)"
    fi
done

# ADB devices
echo ""
echo "[*] Connected devices:"
adb devices 2>/dev/null || echo "  [!] ADB not available or no devices"

# Docker
echo ""
echo "[*] Docker:"
if command -v docker &>/dev/null; then
    echo "  [✓] Docker $(docker --version)"
    docker ps 2>/dev/null && echo "  [✓] Docker daemon running" || echo "  [!] Docker daemon not running"
else
    echo "  [✗] Docker not installed"
fi

# Android SDK / Emulator
echo ""
echo "[*] Android SDK:"
if command -v emulator &>/dev/null; then
    echo "  [✓] Emulator available"
    emulator -list-avds 2>/dev/null | head -5
else
    echo "  [!] No Android emulator found (needed for Phase 4 dynamic analysis + Phase 8 camera injection)"
fi

# GPU for deepfake/fuzzing
echo ""
echo "[*] GPU:"
if command -v nvidia-smi &>/dev/null; then
    nvidia-smi --query-gpu=name,memory.total --format=csv,noheader 2>/dev/null
elif [[ "$OS" == "Darwin" ]]; then
    system_profiler SPDisplaysDataType 2>/dev/null | grep "Chipset Model" | head -1
else
    echo "  [!] No dedicated GPU detected"
fi

# Disk space
echo ""
echo "[*] Disk space:"
df -h . | tail -1 | awk '{print "  Available: " $4 " / " $2}'

# Internet
echo ""
echo "[*] Internet connectivity:"
curl -s --max-time 5 https://google.com >/dev/null && echo "  [✓] Connected" || echo "  [✗] No internet"

# Summary
echo ""
echo "=== Pre-flight Complete ==="
echo "Fix any [✗] items before starting operations."
```

## Tool Installation Quick Reference

### Linux (Ubuntu/Debian) — Full Install
```bash
# Tier 1
sudo apt update && sudo apt install -y adb android-sdk-platform-tools python3 python3-pip git curl openssl

# Tier 2
sudo apt install -y docker.io apktool jadx aircrack-ng bettercap gdb-multiarch ffmpeg obs-studio
sudo apt install -y ocl-icd-opencl-dev nvidia-cuda-toolkit  # GPU
pip3 install frida-tools objection pwntools flask requests opencv-python torch

# Enable Docker
sudo usermod -aG docker $USER && newgrp docker

# v4l2loopback
sudo apt install -y v4l2loopback-dkms && sudo modprobe v4l2loopback devices=1
```

### macOS — Full Install
```bash
# Homebrew first
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Tier 1
brew install android-platform-tools python@3.11 git curl openssl

# Tier 2
brew install --cask docker android-studio
brew install apktool jadx aircrack-ng bettercap gdb ffmpeg obs

# Python
pip3 install frida-tools objection pwntools flask requests opencv-python torch
```

### Windows — Full Install (via Chocolatey)
```powershell
# Chocolatey first
Set-ExecutionPolicy Bypass -Scope Process
iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

# Install all
choco install adb python git curl openssl docker-desktop androidstudio
choco install apktool jadx aircrack-ng wireshark gdb ffmpeg obs-studio
choco install cuda

# Python
pip3 install frida-tools objection pwntools flask requests opencv-python torch
```

## Agent Self-Check Protocol

When invoked, the agent MUST run this mental checklist before any technique:

```
□ 1. What OS is the investigator using? → Adapt all commands to this OS
□ 2. Is ADB installed? → If not, guide installation first
□ 3. Are any Android devices connected? → Check with "adb devices"
□ 4. Does the investigator have root/sudo? → Some tools require it
□ 5. Is Docker available? → Needed for C2, fuzzing, isolated env
□ 6. Is GPU available? → Needed for deepfake (Phase 8), fuzzing (Phase 6)
□ 7. Disk space sufficient? → Forensic extraction needs 10GB+ per device
□ 8. Internet connectivity? → CVE research, tool downloads, C2 hosting
□ 9. What's the investigator's skill level? → Adapt explanation depth
□ 10. Any legal/operational constraints? → Chain of custody, time limits
```

If any mandatory tool is missing, guide the investigator to install it before proceeding.
