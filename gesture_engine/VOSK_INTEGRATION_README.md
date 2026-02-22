# Gestura 3.0 - Vosk-Based Voice Control Integration

**Complete offline voice control system for Gestura**

## 📦 New Files Created

The Vosk-based voice control system consists of these files in `gesture_engine/`:

1. **`config.py`** (updated) - Added shared state variables and Vosk configuration
2. **`voice_commands.py`** (new) - Command registry and action definitions  
3. **`voice_controller.py`** (replaced) - Vosk-based speech recognition
4. **`main_vosk.py`** (new) - Integration example with concurrent gesture+voice

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
pip install vosk pyttsx3 pynput pyautogui sounddevice
```

### Step 2: Download Vosk Model

1. Visit: https://alphacephei.com/vosk/models
2. Download: **vosk-model-small-en-us-0.15.zip** (40 MB, recommended)
3. Extract to: `SOuvikmeet/models/vosk-model-small-en-us-0.15/`

**File structure should be:**
```
SOuvikmeet/
├── models/
│   └── vosk-model-small-en-us-0.15/
│       ├── am/
│       ├── conf/
│       ├── graph/
│       └── ivector/
└── gesture_engine/
    ├── config.py
    ├── voice_commands.py
    ├── voice_controller.py
    └── main_vosk.py
```

### Step 3: Run

```bash
# Test voice controller only
cd gesture_engine
python voice_controller.py

# Run full gesture + voice system
python main_vosk.py
```

## 🎤 Voice Commands

| Command | Action |
|---------|--------|
| **"click"** | Left mouse click |
| **"double click"** | Double click |
| **"scroll up"** | Scroll page up |
| **"scroll down"** | Scroll page down |
| **"new tab"** | Open new browser tab (Ctrl+T) |
| **"close tab"** | Close current tab (Ctrl+W) |
| **"go back"** | Browser back (Alt+Left) |
| **"go forward"** | Browser forward (Alt+Right) |
| **"refresh"** | Refresh page (F5) |
| **"zoom in"** | Zoom in (Ctrl++) |
| **"zoom out"** | Zoom out (Ctrl+-) |
| **"mute"** | Toggle mute |
| **"screenshot"** | Take screenshot |
| **"pause gestura"** | Pause gesture recognition |
| **"resume gestura"** | Resume gesture recognition |
| **"stop gestura"** | Stop entire system |

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│         MAIN THREAD                 │
│  - Gesture recognition (OpenCV)     │
│  - MediaPipe hand tracking          │
│  - UI rendering                     │
└─────────────────────────────────────┘
              ↕
    [Shared State - Thread-Safe]
    config.gesture_active
    config.running
              ↕
┌─────────────────────────────────────┐
│     BACKGROUND THREAD               │
│  - Continuous mic listening         │
│  - Vosk speech recognition          │
│  - Command dispatch                 │
└─────────────────────────────────────┘
```

## 📝 How It Works

### 1. Shared State (`config.py`)

```python
# Thread-safe shared state
state_lock = threading.Lock()
gesture_active = True  # Pause/resume gestures
running = True         # Shutdown signal
```

### 2. Command Registry (`voice_commands.py`)

```python
COMMAND_MAP = {
    "click": cmd_click,
    "scroll up": cmd_scroll_up,
    "pause gestura": cmd_pause_gestura,
    # ...
}

def dispatch(text):
    """Execute command if text matches"""
    handler = COMMAND_MAP.get(text.lower())
    if handler:
        handler()
        return True
    return False
```

### 3. Voice Controller (`voice_controller.py`)

```python
class VoiceController:
    def start(self):
        """Start background listening thread"""
        threading.Thread(target=self._listen_loop, daemon=True).start()
    
    def _listen_loop(self):
        """Continuous recognition with Vosk"""
        with sd.RawInputStream(...):
            while config.running:
                audio = queue.get()
                if recognizer.AcceptWaveform(audio):
                    text = result["text"]
                    dispatch(text)
```

### 4. Main Integration (`main_vosk.py`)

```python
def main():
    # Start voice (background)
    voice = VoiceController()
    voice.start()
    
    # Run gestures (main thread)
    while config.running:
        if not config.gesture_active:
            # Paused by voice command
            show_paused_message()
            continue
        
        # Process frame
        detect_gestures()
```

## 🔧 Adding Custom Commands

### Step 1: Add action function in `voice_commands.py`

```python
def cmd_copy() -> None:
    """Copy to clipboard."""
    pyautogui.hotkey('ctrl', 'c')
    print("[Voice Commands] Copy")
```

### Step 2: Register in COMMAND_MAP

```python
COMMAND_MAP = {
    # ... existing commands
    "copy": cmd_copy,
}
```

### Step 3: Test

```bash
python voice_controller.py
# Say "copy" into microphone
```

## 🐛 Troubleshooting

### Vosk Model Not Found

**Error:** `Failed to load Vosk model at 'models/vosk-model-small-en-us-0.15'`

**Solution:**
1. Download model from https://alphacephei.com/vosk/models
2. Extract completely (not just .zip)
3. Verify folder structure has `am/`, `conf/`, `graph/`, `ivector/`
4. Update path in `config.py` if needed:
   ```python
   VOSK_MODEL_PATH = "path/to/your/model"
   ```

### Microphone Not Working

**Error:** `Microphone unavailable`

**Solutions:**
- Check mic permissions (Windows: Settings → Privacy → Microphone)
- Close other apps using microphone (Discord, Skype, etc.)
- Test mic in other apps first
- Install PortAudio: `pip install sounddevice --upgrade`

### Commands Not Recognized

**Issue:** Speech detected but no commands executed

**Solutions:**
- **Speak exact phrases** from command list above
- Speak clearly at normal volume
- Reduce background noise
- Check recognized text in console: `[Voice] 🎤 Heard: 'your text'`
- Add similar phrases to COMMAND_MAP if needed

### TTS Not Speaking

**Issue:** No voice feedback

**Solutions:**
- Install pyttsx3: `pip install pyttsx3`
- Enable in config: `VOICE_FEEDBACK_ENABLED = True`
- Test separately:
  ```python
  import pyttsx3
  engine = pyttsx3.init()
  engine.say("test")
  engine.runAndWait()
  ```

## 🔄 Migrating from Old Voice System

If you're currently using the Google Speech API based system:

### Old System (voice_commands.py using speech_recognition)
```python
# Online, requires internet
recognizer.recognize_google(audio)
```

### New System (voice_controller.py using Vosk)
```python
# Offline, no internet needed
recognizer.AcceptWaveform(audio)
```

### Migration Steps:

1. **Backup old files:**
   ```bash
   cp gesture_engine/voice_controller.py gesture_engine/voice_controller_old.py
   ```

2. **Install new dependencies:**
   ```bash
   pip install vosk sounddevice
   ```

3. **Download Vosk model** (see Step 2 above)

4. **Test new system:**
   ```bash
   python gesture_engine/voice_controller.py
   ```

5. **Update main.py** to use new controller (or use `main_vosk.py`)

## 📊 Comparison: Old vs New

| Feature | Old (speech_recognition) | New (Vosk) |
|---------|-------------------------|------------|
| **Internet Required** | ✅ Yes (Google API) | ❌ No (offline) |
| **Speed** | 500-2000ms latency | <100ms latency |
| **Privacy** | Audio sent to Google | 100% local |
| **Reliability** | Depends on connection | Always works |
| **Setup Complexity** | Easy (pip only) | Medium (model download) |
| **Accuracy** | Excellent | Very good |
| **Model Size** | N/A | 40 MB - 1.8 GB |

## 📄 File Summary

### `config.py` (Updated)
- Added `state_lock`, `gesture_active`, `running` shared state variables
- Added `VOSK_MODEL_PATH`, `SAMPLE_RATE`, `AUDIO_BLOCK_SIZE` configuration
- Added `VOICE_FEEDBACK_ENABLED` toggle

### `voice_commands.py` (New, 210 lines)
- 16 command action functions (`cmd_click`, `cmd_scroll_up`, etc.)
- `COMMAND_MAP` registry (phrase → function)
- `dispatch(text)` function (command execution)
- `list_commands()` helper (print available commands)
- TTS feedback integration

### `voice_controller.py` (Replaced, 200 lines)
- `VoiceController` class with Vosk recognition
- Background thread listening (`_listen_loop`)
- Audio stream handling (`_audio_callback`)
- Command dispatch integration
- Graceful error handling

### `main_vosk.py` (New, 180 lines)
- `run_gesture_loop()` with pause/resume support
- `main()` entry point with voice initialization
- Status overlay (FPS, state)
- Keyboard controls ('q' to quit)
- Clean shutdown handling

## ✅ Verification Checklist

- [ ] Dependencies installed (`vosk`, `pyttsx3`, `sounddevice`, `pyautogui`)
- [ ] Vosk model downloaded and extracted
- [ ] Model path correct in `config.py`
- [ ] `python voice_controller.py` runs without errors
- [ ] Microphone detected and calibrated
- [ ] Voice commands recognized (check console output)
- [ ] Commands execute actions (test "scroll up")
- [ ] TTS feedback working (if enabled)

## 🎯 Next Steps

1. **Test standalone voice controller:**
   ```bash
   cd gesture_engine
   python voice_controller.py
   ```
   Speak commands and verify execution.

2. **Integrate with PROTOTYPE.PY:**
   - Import the new voice system
   - Replace old voice controller
   - Keep existing gesture pipeline

3. **Customize commands:**
   - Edit `COMMAND_MAP` in `voice_commands.py`
   - Add application-specific actions
   - Tune recognition parameters

## 📞 Support

- **Documentation:** This README
- **Example:** `main_vosk.py`
- **Test Script:** `voice_controller.py` (run standalone)
- **Command List:** Run `python voice_commands.py`

---

**Made with ❤️ for Gestura by the Development Team**
