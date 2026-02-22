# Gestura Voice Assistant - Installation & Setup Guide

## Quick Install (10 minutes)

### Step 1: Install Python Dependencies

```bash
cd voice_assistant
pip install -r requirements.txt
```

**Platform-specific PyAudio installation:**

**Windows:**
```bash
pip install pipwin
pipwin install pyaudio
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install python3-pyaudio portaudio19-dev
pip install pyaudio
```

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

### Step 2: Download Vosk Model (Optional but Recommended)

**For offline recognition without internet:**

1. Download model: https://alphacephei.com/vosk/models
   - **Recommended**: `vosk-model-small-en-us-0.15.zip` (40 MB, fast)
   - Full accuracy: `vosk-model-en-us-0.22.zip` (1.8 GB)

2. Extract to models folder:
   ```bash
   mkdir -p ../models
   cd ../models
   # Extract the downloaded zip here
   unzip vosk-model-small-en-us-0.15.zip
   cd ../voice_assistant
   ```

3. Verify structure:
   ```
   SOuvikmeet/
   ├── models/
   │   └── vosk-model-small-en-us-0.15/
   │       ├── am/
   │       ├── conf/
   │       ├── graph/
   │       └── ivector/
   └── voice_assistant/
       ├── config.py
       └── ...
   ```

### Step 3: Test Installation

```bash
python main.py
```

**Expected output:**
```
✅ Voice controller initialized
✅ Voice command executor initialized
🎤 Calibrating microphone for ambient noise...
✅ Microphone calibrated
🎤 Voice listening started
📝 30+ commands available
```

**Try saying:**
- "show help" (lists all commands)
- "scroll up" / "scroll down"
- "new tab"
- "click"

### Step 4: Verify Components

```python
# test_voice.py
from voice_assistant import VoiceController, VoiceCommandExecutor, VoiceConfig

config = VoiceConfig()
print("✅ Config loaded")

executor = VoiceCommandExecutor(config)
print("✅ Executor initialized")

controller = VoiceController(config=config)
print("✅ Controller initialized")

print("\n✅ All components working!")
```

---

## Troubleshooting

### PyAudio Installation Fails

**Error:** "Failed building wheel for pyaudio"

**Solution:**
```bash
# Windows
pip install pipwin
pipwin install pyaudio

# Or use pre-compiled wheel
pip install https://download.lfd.uci.edu/pythonlibs/archived/pyaudio-0.2.11-cp310-cp310-win_amd64.whl
```

### No Microphone Detected

**Error:** "No microphone available"

**Solutions:**
1. Check mic permissions (Windows Settings → Privacy → Microphone)
2. List available mics:
   ```python
   import speech_recognition as sr
   print(sr.Microphone.list_microphone_names())
   ```
3. Select specific mic in config.py:
   ```python
   self.microphone = sr.Microphone(device_index=1)
   ```

### Vosk Model Not Found

**Error:** "Failed to load vosk model"

**Solution:**
1. Check path in `config.py`:
   ```python
   VOSK_MODEL_PATH = "models/vosk-model-small-en-us-0.15"
   ```
2. Use absolute path if needed:
   ```python
   import os
   VOSK_MODEL_PATH = os.path.join(os.getcwd(), "models", "vosk-model-small-en-us-0.15")
   ```

### Commands Not Recognized

**Issue:** Audio detected but no command executed

**Solutions:**
1. Speak **exact phrases** from command list (see README.md)
2. Adjust sensitivity in `config.py`:
   ```python
   ENERGY_THRESHOLD = 500  # Lower = more sensitive
   ```
3. Check backend:
   ```python
   stats = controller.get_statistics()
   print(f"Backend: {stats['backend']}")
   ```

---

## Verification Checklist

- [ ] Python 3.11+ installed
- [ ] All pip packages installed successfully
- [ ] PyAudio working (mic detected)
- [ ] Vosk model downloaded and extracted (optional)
- [ ] `python main.py` runs without errors
- [ ] Microphone calibration succeeds
- [ ] Voice commands recognized (try "show help")
- [ ] Actions execute (try "scroll up")

---

## Next Steps

1. **Test basic commands:**
   - "scroll up" / "scroll down"
   - "new tab" / "close tab"
   - "click"

2. **Integrate with your gesture system:**
   - See "Integration Guide" in README.md
   - Copy code from `main.py` into your existing system

3. **Customize commands:**
   - Edit `COMMAND_MAP` in config.py
   - Add action handlers in voice_commands.py

4. **Tune recognition:**
   - Adjust `ENERGY_THRESHOLD` for your environment
   - Modify `PAUSE_THRESHOLD` for faster/slower recognition

---

## Support

- **Documentation**: See README.md
- **Examples**: Check main.py
- **Issues**: Report on GitHub

**Installation complete! 🎉**
