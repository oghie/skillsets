# Phase 8: Deepfake Social Engineering — Real-Time Video/Voice Impersonation

**When:** Target is sophisticated, resistant to text-based phishing. Need real-time interactive deception via video call (WhatsApp, Telegram) or conference call (Google Meet, Teams, Zoom) to deliver payloads, extract information, or establish trust for subsequent operations.

## Strategic Overview

The chain: **Target Profile → Voice/Video Sample Collection → Model Training → Pipeline Setup → Scenario Crafting → Live Call → Deliver Payload/Extract Info**

This is an agentic operation. The AI agent orchestrates the entire pipeline from sample collection through live execution, potentially driving the conversation itself via LLM + TTS + face animation.

## Step 1: Target Profiling & Sample Collection

### Voice Sample Collection
```
Sources (ranked by quality):
1. Target's social media videos (TikTok, Instagram Reels, YouTube) → highest quality
2. Voice notes from WhatsApp/Telegram (if already intercepted via Phase 1/7)
3. Recorded phone calls (via SS7 intercept, SIM swap, or legal wiretap)
4. Conference call recordings (Zoom, Teams, Meet — if target has public talks)
5. Podcast interviews, radio appearances
6. Voicemail greetings
7. Casual conversation recordings (from surveillance)

Minimum needed: 3-5 minutes of clean speech for basic cloning
Optimal: 15-30 minutes for high-quality cloning
```

### Target Person Voice Mapping
- **Language:** What language(s) does target speak? Accent? Dialect?
- **Speech patterns:** Speed, filler words ("uh", "like", "ya kan"), catchphrases
- **Vocabulary level:** Formal vs casual, technical vs layperson
- **Emotional range:** Angry, persuasive, friendly, authoritative tones
- **Background noise profile:** Office, outdoor, car — for authenticity

### Face/Video Sample Collection
```
Sources:
1. Social media photos (Instagram, Facebook, LinkedIn profile pics)
2. Video calls you've recorded (if intercepted)
3. Public videos (YouTube, TikTok, company website)
4. Surveillance footage
5. ID photos (KTP, passport — from OSINT/breach databases)

Minimum needed: 10-20 high-quality face images from different angles
Optimal: 50+ images + short video clips for expression reference
```

### Digital Persona Construction
Build a complete profile of the impersonation target:
- Full name, title, company
- Common phrases, signature sign-offs
- Relationship to the real target (how do they know each other?)
- Recent shared context (events, projects, mutual contacts)
- Device they normally call from (phone model, camera quality for matching)

## Step 2: Technical Pipeline Setup

### Architecture Overview
```
┌─────────────────────────────────────────────────┐
│                 OPERATOR / AI AGENT              │
│  ┌─────────┐  ┌──────────┐  ┌────────────────┐  │
│  │ LLM     │→ │ TTS       │→ │ Face Animator  │  │
│  │ (GPT-4) │  │ (cloned)  │  │ (Wav2Lip/etc)  │  │
│  └─────────┘  └──────────┘  └───────┬────────┘  │
│                                      ↓           │
│                              ┌────────────────┐  │
│                              │ Virtual Camera  │  │
│                              │ (OBS/v4l2loop)  │  │
│                              └───────┬────────┘  │
│                                      ↓           │
│                              ┌────────────────┐  │
│                              │ Android Emulator│  │
│                              │ or Physical     │  │
│                              │ Device w/ Cam   │  │
│                              │ Injection       │  │
│                              └───────┬────────┘  │
│                                      ↓           │
│                              ┌────────────────┐  │
│                              │ WhatsApp / TG / │  │
│                              │ Meet / Zoom     │  │
│                              │ Video Call      │  │
│                              └────────────────┘  │
└─────────────────────────────────────────────────┘
```

### Voice Cloning Pipeline

**Option A: RVC (Retrieval-based Voice Conversion) — Best Quality, Real-time**
```bash
# Setup RVC WebUI
git clone https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI
cd Retrieval-based-Voice-Conversion-WebUI
pip install -r requirements.txt

# Train on target voice samples
# 1. Place target audio in datasets/target_name/
# 2. Run training (50-200 epochs depending on quality needed)
python train.py --name target_voice --epochs 100

# Real-time conversion
python realtime_inference.py --model target_voice --input mic --output virtual_cable
```

**Option B: ElevenLabs API — Best Quality, Cloud-based**
```python
# Requires internet. Faster setup, better quality for English.
# api_key obtained from elevenlabs.io
import elevenlabs
elevenlabs.set_api_key("sk-...")
voice = elevenlabs.clone(
    name="target_voice",
    files=["./samples/target_audio_1.mp3", "./samples/target_audio_2.mp3"]
)
# Generate speech
audio = elevenlabs.generate(text="Hello, this is a test", voice=voice)
```

**Option C: OpenVoice — Open Source, Multi-Language**
```bash
git clone https://github.com/myshell-ai/OpenVoice
cd OpenVoice
pip install -r requirements.txt
# Downloads base model + provides voice cloning from short samples
```

**Option D: Coqui TTS + XTTS — Offline, Fine-tuning**
```bash
pip install TTS
# Fine-tune XTTSv2 on target voice
tts --model_name tts_models/multilingual/multi-dataset/xtts_v2 \
    --train_dataset_path /data/target_voice/ \
    --output_path ./target_model/
```

### Face Swapping / Deepfake Pipeline

**Option A: DeepFaceLive — Real-time, Production Quality**
```bash
# Windows primarily, best real-time face swap
# Download from: https://github.com/iperov/DeepFaceLive
# Train DFM model on target face images
# Output: virtual camera with swapped face in real-time
```

**Option B: FaceFusion — Cross-platform, One-shot**
```bash
git clone https://github.com/facefusion/facefusion
cd facefusion
python install.py
# One image → face swap on video stream
python run.py --source target_face.jpg --target webcam --output virtual_camera
```

**Option C: Wav2Lip — Audio-Driven Lip Sync**
```bash
git clone https://github.com/Rudrabha/Wav2Lip
cd Wav2Lip
# Combines: face video + cloned audio → lip-synced video
python inference.py --checkpoint wav2lip_gan.pth \
    --face target_face_video.mp4 --audio cloned_speech.wav \
    --outfile output.mp4
```

**Option D: SadTalker — Audio-Driven Head Animation**
```bash
git clone https://github.com/OpenTalker/SadTalker
cd SadTalker
# Single image + audio → talking head video
python inference.py --driven_audio cloned_speech.wav \
    --source_image target_face.jpg --result_dir ./output/
```

### Virtual Camera Setup

**Linux:**
```bash
# v4l2loopback — create virtual camera device
sudo modprobe v4l2loopback devices=1 video_nr=10 card_label="VirtualCam" exclusive_caps=1

# OBS Studio — route deepfake output to virtual camera
obs --startvirtualcam

# Pipe deepfake output to v4l2 device
ffmpeg -i deepfake_output.mp4 -f v4l2 /dev/video10
```

**macOS:**
```bash
# OBS Virtual Camera plugin (built into OBS 26+)
# Or CamTwist for older setups
```

**Windows:**
```bash
# OBS Virtual Camera (built-in since OBS 26)
# Or ManyCam
```

### Audio Routing (Virtual Audio Cable)

**Linux (PulseAudio):**
```bash
# Create virtual sink for TTS output
pactl load-module module-null-sink sink_name=tts_output
# Route TTS output to virtual microphone
pactl load-module module-loopback source=tts_output.monitor sink=microphone_input
```

**All platforms:**
- **VB-Audio Virtual Cable** (Windows/macOS)
- **BlackHole** (macOS)
- **PulseAudio null-sink** (Linux)

## Step 3: Call Infrastructure

### Android Emulator Setup (for WhatsApp/Telegram calls)
```bash
# Android Studio AVD with Google APIs + Play Store
# Install WhatsApp/Telegram/Meet/Zoom on emulator
# Configure emulator camera to use virtual camera device:
#   AVD Manager → Edit → Advanced → Camera → Webcam0 → VirtualCam

# For WhatsApp: register with a burner number (Phase 7 SIM swap or virtual number)
# For Telegram: register with burner number
```

### Physical Device Setup
```bash
# Rooted Android with camera injection
# Use: manycam or ipcam to feed virtual camera as device camera
adb shell am start -a android.media.action.VIDEO_CAPTURE
# Or use scrcpy with camera forwarding
scrcpy --camera-facing=front --video-source=camera --camera-id=0
```

### Alternative: Browser-Based (Google Meet, Zoom, Teams)
```bash
# Easier — use desktop browser with virtual camera
# Chrome/Edge: Settings → Privacy → Site Settings → Camera → select VirtualCam
# Firefox: about:preferences → Camera → select VirtualCam

# Google Meet: meet.google.com → join meeting → select VirtualCam
# Zoom: zoom.us → join → select VirtualCam in settings
# Teams: teams.microsoft.com → join → device settings → VirtualCam
```

## Step 4: Scenario Crafting & Script Generation

### Persona Templates for Video Call

**Financial/Banking:**
```
Persona: [BANK NAME] Fraud Department Officer
Pretext: "Mr/Ms [TARGET], we detected unusual transactions on your account.
         For security verification, we need you to confirm your identity
         via video call. This is now mandatory per OJK regulation."
Call setup: Video call via WhatsApp Business (verified business account)
Payload delivery: "Please open this link to verify your device: [URL]"
                 → Browser exploit Page A
```

**Legal/Government:**
```
Persona: [AGENCY NAME] Investigator
Pretext: "This is regarding case number [X] filed against your identity.
         We need to verify your identity via video statement."
Call setup: WhatsApp video call or Google Meet
Goal: Extract additional personal information, or deliver URL for "e-filing"
```

**Corporate/IT Support:**
```
Persona: [COMPANY] IT Security Team
Pretext: "We detected your account was accessed from an unknown device.
         I need to walk you through the security verification process."
Call setup: Zoom or Teams (looks more corporate)
Goal: Screen share → guide target to install "security tool" (APK) or visit URL
```

**Personal/Relationship:**
```
Persona: Friend/colleague known to target
Pretext: "Hey! I got a new number. My old phone broke. Can you help me 
         with something? I need you to check this link [URL]"
Call setup: WhatsApp video call
Goal: Build trust via familiar face, then deliver payload
```

### LLM-Driven Conversation Script

The AI agent can be the active participant in the call:

```python
# Agentic conversation loop
import openai

conversation_context = """
You are impersonating [PERSONA NAME], [TITLE] at [ORGANIZATION].
You are on a video call with [TARGET NAME].
Your goal: [OBJECTIVE — deliver URL, extract info, etc.]

Target profile:
- Name: [TARGET NAME]
- Age: [AGE]
- Occupation: [OCCUPATION]
- Recent events: [CONTEXT FROM OSINT]
- Known apps: [APPS FROM PHASE 1 OSINT]
- Personality: [TRAITS FROM PROFILING]

Your persona:
- Speech style: [VOICE PROFILE — speed, accent, filler words]
- Signature phrases: [PHRASES]
- Relationship to target: [HOW THEY KNOW EACH OTHER]

Rules:
1. Stay in character at all times
2. Use the target's language (Indonesian/English/etc.)
3. Build rapport before making the ask
4. If questioned, have a plausible escalation path
5. Never mention the real operation
"""

def generate_response(target_said, context):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": f"Target said: {target_said}\n\nRespond as {PERSONA_NAME}:"}
        ]
    )
    text = response.choices[0].message.content
    return text

# Full agentic loop
while call_active:
    target_speech = listen_to_target()        # speech-to-text
    agent_response = generate_response(target_speech, conversation_context)
    cloned_audio = tts(agent_response, voice_model)  # text-to-speech with cloned voice
    animated_face = lip_sync(cloned_audio, target_face_model)  # face animation
    output_to_virtual_camera(animated_face)    # send to call
```

### Common Pretext Scenarios (with Deepfake)

| Goal | Persona | Platform | Visual Requirement |
|------|---------|----------|-------------------|
| Deliver browser exploit URL | Bank fraud officer | WhatsApp VC | Professional attire, bank backdrop |
| Install APK | IT support | Zoom/Meet | Corporate background, lanyard |
| Extract 2FA code | Service provider | WhatsApp VC | Uniform, ID badge visible |
| Confirm transaction | Target's boss/colleague | WhatsApp VC | Office background, familiar face |
| Reset password | Platform support | Meet/Zoom | Corporate branding on screen |
| Extract crypto wallet seed | "Exchange security team" | Telegram VC | Professional backdrop |

## Step 5: Execution Workflow

### Pre-Call Checklist
```
□ Voice samples collected and model trained (test on known samples)
□ Face model trained (test on different expressions/angles)
□ Virtual camera pipeline tested (OBS + v4l2loopback)
□ Audio routing tested (TTS → virtual mic)
□ Android emulator/device configured with camera injection
□ WhatsApp/Telegram/Meet/Zoom installed and working
□ Burner number registered (cannot trace back to operator)
□ Call script generated (LLM prompt loaded with context)
□ Fallback scenario prepared (what if target asks unexpected questions?)
□ Recording system active (for operational record and evidence)
```

### Call Execution
```
1. Send initial message (text) to establish contact:
   "Mr/Ms [TARGET], this is [PERSONA] from [ORG]. 
    We need to speak with you urgently regarding [MATTER].
    Can you take a video call now?"

2. Initiate video call on target's preferred platform

3. [AI AGENT LOOP BEGINS]
   - Target speaks → STT (whisper/GCP STT)
   - Transcript → LLM generates response
   - Response → TTS with cloned voice
   - Audio + face model → lip-synced video
   - Video → virtual camera → call output
   - LOOP back to listen

4. During call: deliver payload (URL, file, request action)
   - "Please open this link to verify: [URL]"
   - "I'm sending you a security update, please install: [APK]"
   - "Can you read me the code you just received?" (2FA intercept)

5. After payload delivery: maintain cover, end call naturally

6. Post-call: check C2 for implant registration, extract collected data
```

### Latency Budget (for Real-time)
```
Microphone input:             10-30ms
Speech-to-text (Whisper):    200-500ms (depends on GPU)
LLM response generation:     500-2000ms (GPT-4 API latency)
Text-to-speech (cloned):     100-300ms (RVC real-time mode)
Face animation + render:      50-100ms
Virtual camera output:        10-30ms
─────────────────────────────────────────
Total latency:               ~1-3 seconds

Acceptable for video call (normal network latency is 200-500ms).
Target may notice slight delay; attribute to "poor connection."
```

## Step 6: Tools & Infrastructure

### Hardware Requirements
```
Minimum:
- GPU: NVIDIA RTX 3060 (12GB VRAM) or better
- CPU: 8+ cores
- RAM: 32GB
- Storage: 50GB free (for models + samples)

Optimal:
- GPU: NVIDIA RTX 4090 (24GB VRAM)
- CPU: 16+ cores
- RAM: 64GB
- Secondary GPU for dedicated face rendering

Cloud alternative:
- RunPod.io / Lambda Labs: rent GPU instances on demand
- ~$1-2/hour for RTX 4090 instances
```

### Software Stack
```bash
# Core deepfake pipeline
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install opencv-python face-recognition insightface
pip install TTS coqui-tts elevenlabs openai-whisper
pip install flask streamlit  # for control panel

# Virtual camera + audio
# Linux: v4l2loopback + OBS + PulseAudio
# macOS: OBS + BlackHole
# Windows: OBS + VB-Cable

# Android emulator
# Android Studio with Google APIs system image
# Or physical device with scrcpy camera forwarding

# Optional: Voice activity detection
pip install silero-vad webrtcvad
```

### Agent Control Panel (Web UI)
```python
# streamlit_control.py — agent control dashboard
import streamlit as st

st.title("Deepfake Call Control Panel")

# Session config
target_name = st.text_input("Target Name")
persona_name = st.text_input("Impersonating")
call_platform = st.selectbox("Platform", ["WhatsApp", "Telegram", "Zoom", "Google Meet", "Teams"])
goal_type = st.selectbox("Goal", ["Deliver URL", "Install APK", "Extract Info", "Build Trust Only"])

# Pipeline status
st.metric("Voice Model", "Ready (23 min samples)")
st.metric("Face Model", "Ready (45 images)")
st.metric("Pipeline Latency", "1.8s avg")

# Call controls
if st.button("Start Call"):
    # Initialize pipeline, connect to Android device, initiate call
    pass

# Live transcript
st.subheader("Live Transcript")
transcript = st.empty()
# Update transcript in real-time during call

# Agent override (manual intervention)
st.subheader("Manual Override")
manual_text = st.text_input("Send custom message to TTS")
if st.button("Send"):
    # Override LLM, send manual text to TTS pipeline
    pass
```

## Step 7: Counter-Detection & OpSec

### Anti-Deepfake Detection Awareness
Modern platforms increasingly deploy deepfake detection:
- **WhatsApp/Telegram:** No server-side detection currently (2026)
- **Zoom:** Has announced interest but not deployed
- **Google Meet:** May flag unusual video patterns
- **Microsoft Teams:** Similar to Meet

**Countermeasures:**
1. **Add subtle noise:** Gaussian blur (0.5-1px), slight compression artifacts
2. **Match camera quality:** If target uses phone front camera, degrade output to 720p
3. **Random micro-movements:** Slight head tilt, occasional blink pattern variation
4. **Background consistency:** Use real background, not green-screen
5. **Lighting variation:** Slight auto-exposure fluctuations (natural phone camera behavior)
6. **Audio artifacts:** Add subtle background noise matching target's environment

### Operational Security
```
□ Burner phone/SIM for WhatsApp registration (not traceable to operator)
□ VPN/proxy chain for all network traffic during call
□ Virtual camera output NEVER saved to disk (RAM-only pipeline)
□ Session recording encrypted at rest
□ Call platform account created with burner email
□ No metadata linking back to investigative agency
□ Dispose of burner SIM after operation
```

## Integration with Other Phases

```
Phase 1 (OSINT) → Gather voice/video samples, target profiling
Phase 7 (Text SE) → Initial contact via SMS/WA to set up video call
Phase 8 (Deepfake Call) → Execute interactive deception
    ↓
Phase 7 Path A → Deliver browser exploit URL during call
Phase 7 Path B → Convince target to install APK during call
Phase 3 → After compromise, extract all communication evidence
```

## Quick Start: Minimal Pipeline in 10 Minutes

```bash
#!/bin/bash
# quick_deepfake_setup.sh — minimal pipeline for testing

# 1. Install dependencies
pip install openai-whisper TTS opencv-python insightface

# 2. Clone voice from sample (using Coqui TTS)
tts --model_name tts_models/multilingual/multi-dataset/xtts_v2 \
    --text "Hello, this is a test of the cloned voice." \
    --speaker_wav /path/to/target_audio.wav \
    --out_path test_output.wav

# 3. Face swap on webcam (FaceFusion)
python run.py --source target_face.jpg --target 0 --output /dev/video10

# 4. Setup virtual camera (Linux)
sudo modprobe v4l2loopback devices=1 video_nr=10
obs --startvirtualcam &

# 5. Open WhatsApp on Android emulator with camera = /dev/video10
emulator -avd Pixel_6_API_34 -camera-back webcam0 -camera-front webcam1

echo "Pipeline ready. Open WhatsApp on emulator and make a video call."
```
