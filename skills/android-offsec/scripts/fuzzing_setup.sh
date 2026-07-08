#!/bin/bash
# fuzzing_setup.sh — Setup fuzzing and exploit development environment for Android targets
# Usage: bash fuzzing_setup.sh [--light|--full]

set -euo pipefail

MODE="${1:---full}"

echo "[*] Installing fuzzing and exploit development toolchain..."

# Base dependencies
echo "[*] Installing base dependencies..."
if command -v apt-get &>/dev/null; then
    sudo apt-get update -qq
    sudo apt-get install -y -qq \
        build-essential cmake autoconf automake libtool \
        python3 python3-pip python3-dev \
        git wget curl unzip \
        gdb gdb-multiarch lldb \
        libssl-dev libffi-dev \
        pkg-config bison flex \
        libglib2.0-dev libpixman-1-dev \
        qemu-system-aarch64 qemu-user-static \
        clang llvm lld \
        2>/dev/null || true
elif command -v brew &>/dev/null; then
    brew install cmake python3 gdb llvm qemu binutils 2>/dev/null || true
fi

# Python exploit dev tools
echo "[*] Installing Python exploit development toolkit..."
pip3 install --quiet pwntools ropgadget ropper capstone unicorn keystone-engine 2>/dev/null || true

# GDB plugins
echo "[*] Setting up GDB plugins..."
if [ ! -d ~/.local/share/gef ]; then
    git clone -q https://github.com/hugsy/gef ~/.local/share/gef 2>/dev/null || true
    echo "source ~/.local/share/gef/gef.py" >> ~/.gdbinit 2>/dev/null || true
fi

if [ "$MODE" = "--light" ]; then
    echo "[✓] Light setup complete (pwntools + debugging tools only)"
    exit 0
fi

# Full setup: fuzzing frameworks

# AFL++
echo "[*] Installing AFL++..."
if [ ! -d /tmp/aflplusplus ]; then
    git clone -q --depth 1 https://github.com/AFLplusplus/AFLplusplus /tmp/aflplusplus 2>/dev/null || true
    cd /tmp/aflplusplus && make -j$(nproc) && sudo make install 2>/dev/null || true
fi

# Honggfuzz (alternative coverage-guided fuzzer)
echo "[*] Installing Honggfuzz..."
if [ ! -d /tmp/honggfuzz ]; then
    git clone -q --depth 1 https://github.com/google/honggfuzz /tmp/honggfuzz 2>/dev/null || true
    cd /tmp/honggfuzz && make -j$(nproc) && sudo make install 2>/dev/null || true
fi

# Radamsa (mutation-based fuzzer for quick testing)
echo "[*] Installing Radamsa..."
if command -v apt-get &>/dev/null; then
    sudo apt-get install -y -qq radamsa 2>/dev/null || true
elif command -v brew &>/dev/null; then
    brew install radamsa 2>/dev/null || true
fi

# Android NDK (for cross-compiling fuzz harnesses)
echo "[*] Installing Android NDK..."
NDK_VERSION="r27b"
if [ ! -d "$HOME/android-ndk-$NDK_VERSION" ]; then
    if [[ "$(uname)" == "Darwin" ]]; then
        wget -q "https://dl.google.com/android/repository/android-ndk-$NDK_VERSION-darwin.zip" -O /tmp/ndk.zip 2>/dev/null || true
    else
        wget -q "https://dl.google.com/android/repository/android-ndk-$NDK_VERSION-linux.zip" -O /tmp/ndk.zip 2>/dev/null || true
    fi
    unzip -q /tmp/ndk.zip -d "$HOME" 2>/dev/null || true
    echo "[*] NDK installed at $HOME/android-ndk-$NDK_VERSION"
fi

# syzkaller (kernel fuzzer)
echo "[*] Installing syzkaller..."
if [ ! -d /tmp/syzkaller ]; then
    git clone -q --depth 1 https://github.com/google/syzkaller /tmp/syzkaller 2>/dev/null || true
    cd /tmp/syzkaller && make -j$(nproc) 2>/dev/null || true
    echo "[*] syzkaller built at /tmp/syzkaller"
fi

echo ""
echo "============================================"
echo " Fuzzing environment ready"
echo ""
echo " Fuzzers:    AFL++, Honggfuzz, Radamsa"
echo " Kernel:     syzkaller (/tmp/syzkaller)"
echo " Debugging:  GDB+GEF, lldb, pwntools"
echo " NDK:        $HOME/android-ndk-$NDK_VERSION (if downloaded)"
echo "============================================"
echo ""
echo "Quick start:"
echo "  AFL++:    afl-fuzz -i corpus/ -o findings/ ./harness @@"
echo "  syzkaller: cd /tmp/syzkaller && ./bin/syz-manager -config=my.cfg"
echo "  GDB:      gdb-multiarch -ex 'target remote :1234'"
echo "  pwntools: python3 -c 'from pwn import *; print(asm(\"ret\", arch=\"aarch64\"))'"
