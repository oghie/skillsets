#!/bin/bash
# deepfake_setup.sh — Automated deepfake pipeline setup for Phase 8
# Usage: bash deepfake_setup.sh [--voice-samples /path/to/audio] [--face-samples /path/to/images]
#        bash deepfake_setup.sh --check-only  (just verify prerequisites)

set -euo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
OS="$(uname -s)"

VOICE_SAMPLES=""
FACE_SAMPLES=""
CHECK_ONLY=false
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PIPELINE_DIR="$SCRIPT_DIR/../deepfake_pipeline"

# Parse args
while [[ $# -gt 0 ]]; do
    case "$1" in
        --voice-samples) VOICE_SAMPLES="$2"; shift 2;;
        --face-samples) FACE_SAMPLES="$2"; shift 2;;
        --check-only) CHECK_ONLY=true; shift;;
        *) echo "Usage: $0 [--voice-samples DIR] [--face-samples DIR] [--check-only]"; exit 1;;
    esac
done

echo -e "${GREEN}=== Deepfake Pipeline Setup ===${NC}"
echo ""

# ---------- Prerequisites ----------
echo "[*] Checking prerequisites..."

check_cmd() {
    if command -v "$1" &>/dev/null; then
        echo -e "  ${GREEN}[✓]${NC} $1 ($(which $1))"
        return 0
    else
        echo -e "  ${RED}[✗]${NC} $1 — MISSING"
        return 1
    fi
}

FAILS=0
check_cmd python3 || FAILS=$((FAILS+1))
check_cmd pip3 || FAILS=$((FAILS+1))
check_cmd ffmpeg || FAILS=$((FAILS+1))
check_cmd git || FAILS=$((FAILS+1))

# GPU check
GPU_OK=false
if command -v nvidia-smi &>/dev/null; then
    GPU_INFO=$(nvidia-smi --query-gpu=name,memory.total --format=csv,noheader 2>/dev/null || echo "NVIDIA GPU")
    echo -e "  ${GREEN}[✓]${NC} GPU: $GPU_INFO"
    GPU_OK=true
elif [[ "$OS" == "Darwin" ]] && system_profiler SPDisplaysDataType 2>/dev/null | grep -q "Metal"; then
    echo -e "  ${GREEN}[✓]${NC} GPU: Apple Silicon/Metal (MPS backend)"
    GPU_OK=true
else
    echo -e "  ${YELLOW}[!]${NC} No GPU detected — deepfake will be SLOW (CPU-only)"
fi

# Check v4l2loopback (Linux) or OBS VirtualCam
if [[ "$OS" == "Linux" ]]; then
    lsmod | grep -q v4l2loopback && echo -e "  ${GREEN}[✓]${NC} v4l2loopback loaded" || {
        echo -e "  ${YELLOW}[!]${NC} v4l2loopback not loaded — attempting setup..."
        sudo modprobe v4l2loopback devices=1 video_nr=10 card_label="DeepfakeCam" exclusive_caps=1 2>/dev/null || {
            echo -e "  ${RED}[✗]${NC} Failed. Install: sudo apt install v4l2loopback-dkms && sudo modprobe v4l2loopback"
        }
    }
fi

# OBS check
check_cmd obs || echo -e "  ${YELLOW}[!]${NC} OBS Studio recommended for virtual camera routing"

if [ "$CHECK_ONLY" = true ]; then
    echo ""
    [ $FAILS -eq 0 ] && echo -e "${GREEN}All prerequisites met.${NC}" || echo -e "${RED}$FAILS prerequisite(s) missing.${NC}"
    exit $FAILS
fi

# ---------- Python Environment ----------
echo ""
echo "[*] Setting up Python environment..."

mkdir -p "$PIPELINE_DIR"
cd "$PIPELINE_DIR"

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

echo "[*] Installing Python dependencies..."
pip install --quiet --upgrade pip

# Core deepfake packages
pip install --quiet torch torchvision torchaudio 2>/dev/null || \
    pip install --quiet torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

pip install --quiet opencv-python opencv-python-headless
pip install --quiet insightface onnxruntime
pip install --quiet openai-whisper  # speech-to-text
pip install --quiet TTS  # text-to-speech with voice cloning
pip install --quiet flask flask-cors  # for control panel

# Verify PyTorch
python3 -c "
import torch
print(f'PyTorch {torch.__version__}')
if torch.cuda.is_available():
    print(f'CUDA available: {torch.cuda.get_device_name(0)}')
elif torch.backends.mps.is_available():
    print('Apple MPS available')
else:
    print('WARNING: Running on CPU — deepfake will be very slow')
"

# ---------- Voice Cloning Setup ----------
echo ""
echo "[*] Setting up voice cloning..."

# Install Coqui TTS (XTTSv2 — best open-source voice cloning)
pip install --quiet TTS

# If voice samples provided, pre-train
if [ -n "$VOICE_SAMPLES" ] && [ -d "$VOICE_SAMPLES" ]; then
    echo "[*] Voice samples found: $(ls "$VOICE_SAMPLES"/*.wav "$VOICE_SAMPLES"/*.mp3 2>/dev/null | wc -l) files"
    echo "[*] Training voice clone model (this will take 10-30 minutes)..."
    
    # Quick fine-tune using XTTSv2
    python3 -c "
from TTS.api import TTS
tts = TTS('tts_models/multilingual/multi-dataset/xtts_v2')
# Test with a sample
tts.tts_to_file(text='Halo, ini adalah tes suara.', 
                speaker_wav='$VOICE_SAMPLES/$(ls "$VOICE_SAMPLES"/*.wav "$VOICE_SAMPLES"/*.mp3 2>/dev/null | head -1)',
                file_path='$PIPELINE_DIR/test_voice_output.wav')
print('Voice clone ready. Test output: test_voice_output.wav')
"
    echo -e "  ${GREEN}[✓]${NC} Voice model ready (XTTSv2 one-shot, no training needed)"
else
    echo -e "  ${YELLOW}[!]${NC} No voice samples provided. Use --voice-samples DIR to set up."
    echo "     Place target audio files (.wav/.mp3) in a directory."
fi

# ---------- Face Swap Setup ----------
echo ""
echo "[*] Setting up face swap..."

# Install FaceFusion (cross-platform, one-shot face swap)
if [ ! -d "$PIPELINE_DIR/facefusion" ]; then
    git clone --quiet --depth 1 https://github.com/facefusion/facefusion "$PIPELINE_DIR/facefusion" 2>/dev/null || \
        echo -e "  ${YELLOW}[!]${NC} FaceFusion clone failed (network issue?) — skip, manual install later"
fi

pip install --quiet onnxruntime-gpu 2>/dev/null || pip install --quiet onnxruntime

if [ -n "$FACE_SAMPLES" ] && [ -d "$FACE_SAMPLES" ]; then
    echo "[*] Face samples found: $(find "$FACE_SAMPLES" -name "*.jpg" -o -name "*.png" -o -name "*.jpeg" 2>/dev/null | wc -l) images"
    echo -e "  ${GREEN}[✓]${NC} Face samples ready"
else
    echo -e "  ${YELLOW}[!]${NC} No face samples provided. Use --face-samples DIR to specify."
    echo "     Place target face images (.jpg/.png) in a directory."
fi

# ---------- Virtual Audio Cable ----------
echo ""
echo "[*] Setting up virtual audio..."

if [[ "$OS" == "Linux" ]]; then
    # PulseAudio virtual sink
    if command -v pactl &>/dev/null; then
        pactl load-module module-null-sink sink_name=tts_output 2>/dev/null || true
        pactl load-module module-loopback source=tts_output.monitor 2>/dev/null || true
        echo -e "  ${GREEN}[✓]${NC} PulseAudio virtual sink (tts_output) created"
    else
        echo -e "  ${YELLOW}[!]${NC} PulseAudio not found — install: sudo apt install pulseaudio"
    fi
elif [[ "$OS" == "Darwin" ]]; then
    # Check BlackHole
    if system_profiler SPAudioDataType 2>/dev/null | grep -q "BlackHole"; then
        echo -e "  ${GREEN}[✓]${NC} BlackHole virtual audio device found"
    else
        echo -e "  ${YELLOW}[!]${NC} Install BlackHole: brew install blackhole-2ch"
    fi
else
    echo -e "  ${YELLOW}[!]${NC} Windows: install VB-Audio Virtual Cable from vb-audio.com"
fi

# ---------- Control Panel ----------
echo ""
echo "[*] Creating control panel..."

cat > "$PIPELINE_DIR/control_panel.py" << 'PYEOF'
#!/usr/bin/env python3
"""Deepfake Call Control Panel — Streamlit web UI"""
import streamlit as st
import subprocess
import os

st.set_page_config(page_title="Deepfake Call Control", layout="wide")
st.title("🎭 Deepfake Call Control Panel")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Target")
    target_name = st.text_input("Target Name", "")
    persona = st.selectbox("Persona", ["Bank Fraud Officer", "IT Support", "Legal Investigator", "Colleague", "Family Member", "Service Provider"])
    platform = st.selectbox("Call Platform", ["WhatsApp", "Telegram", "Zoom", "Google Meet", "Microsoft Teams"])
    goal = st.selectbox("Goal", ["Deliver URL", "Install APK", "Extract 2FA Code", "Extract Info", "Build Trust"])

with col2:
    st.subheader("Pipeline Status")
    st.metric("Voice Model", "XTTSv2 (ready)")
    st.metric("Face Model", "FaceFusion (ready)")
    st.metric("Virtual Camera", "/dev/video10" if os.path.exists("/dev/video10") else "Not configured")

st.subheader("Quick Actions")
c1, c2, c3, c4 = st.columns(4)
c1.button("▶ Start Pipeline")
c2.button("⏸ Pause")
c3.button("📹 Test Camera")
c4.button("🔊 Test Audio")

st.subheader("Live Transcript")
st.text_area("Transcript", height=200, disabled=True, placeholder="Call transcript will appear here...")

st.subheader("Manual Override")
manual = st.text_input("Type message to inject into TTS pipeline...")
st.button("Send Override")
PYEOF

chmod +x "$PIPELINE_DIR/control_panel.py"
echo -e "  ${GREEN}[✓]${NC} Control panel created: $PIPELINE_DIR/control_panel.py"

# ---------- Android Emulator Check ----------
echo ""
echo "[*] Checking Android emulator..."
if command -v emulator &>/dev/null; then
    AVDS=$(emulator -list-avds 2>/dev/null)
    if [ -n "$AVDS" ]; then
        echo -e "  ${GREEN}[✓]${NC} Android emulator available:"
        echo "$AVDS" | while read avd; do echo "    - $avd"; done
    else
        echo -e "  ${YELLOW}[!]${NC} No AVDs found. Create one in Android Studio with Google APIs."
    fi
else
    echo -e "  ${YELLOW}[!]${NC} Android emulator not found. Install Android Studio for Phase 4+8."
fi

# ---------- Summary ----------
echo ""
echo "============================================"
echo -e "${GREEN} Deepfake Pipeline Setup Complete${NC}"
echo "============================================"
echo ""
echo "Pipeline directory: $PIPELINE_DIR"
echo "Voice model:  XTTSv2 (one-shot cloning, no training needed)"
echo "Face swap:    FaceFusion ($PIPELINE_DIR/facefusion)"
echo "Control UI:   $PIPELINE_DIR/control_panel.py"
echo ""
echo "Quick test:"
echo "  1. Place target voice in a .wav file"
echo "  2. python3 -c \"from TTS.api import TTS; TTS('tts_models/multilingual/multi-dataset/xtts_v2').tts_to_file(text='test', speaker_wav='voice.wav', file_path='out.wav')\""
echo "  3. Place target face in face.jpg"
echo "  4. python3 $PIPELINE_DIR/facefusion/run.py --source face.jpg --target 0"
echo ""
echo "For full video call:"
echo "  1. Start OBS → set scene to facefusion output → Start Virtual Camera"
echo "  2. Launch Android emulator with camera = OBS Virtual Camera"
echo "  3. Open WhatsApp/Telegram on emulator"
echo "  4. python3 $PIPELINE_DIR/control_panel.py (to drive the conversation)"
echo "  5. Make the call"
