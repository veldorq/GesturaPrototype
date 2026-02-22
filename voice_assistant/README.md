# Gestura Voice Assistant Module

**Production-ready offline voice control system for gesture-based computer interaction**

Version: 3.0.0  
Author: Gestura Development Team  
License: MIT

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Quick Start](#quick-start)
5. [Architecture](#architecture)
6. [Configuration](#configuration)
7. [Voice Commands](#voice-commands)
8. [Integration Guide](#integration-guide)
9. [Troubleshooting](#troubleshooting)
10. [API Reference](#api-reference)

---

## 🎯 Overview

The Gestura Voice Assistant is a modular, production-ready voice control system that enables hands-free computer interaction alongside existing gesture recognition. It runs completely **offline** with no cloud dependencies, using local speech recognition models.

### Key Capabilities

- ✅ **Offline-first recognition** (vosk, sphinx)
- ✅ **Continuous background listening** (non-blocking)
- ✅ **Thread-safe command execution**
- ✅ **Gesture system integration** (pause/resume via voice)
- ✅ **Optional TTS feedback** (pyttsx3)
- ✅ **30+ voice commands** out of the box
- ✅ **Graceful error handling** (mic unavailable, recognition errors)

---

## ✨ Features

### Recognition Backends

**Priority order:**
1. **Vosk** (offline, fast, 100% local)
2. **CMU Sphinx** (offline, included with speech_recognition)
3. **Google Speech API** (online fallback)

### Command Categories

- **Mouse Control**: click, double click, right click
- **Scrolling**: scroll up/down, page up/down
- **Browser Navigation**: back, forward, new tab, close tab, refresh
- **Zoom**: zoom in, zoom out, reset zoom
- **Media**: mute, volume up/down
- **Screenshot**: take screenshot
- **System Control**: pause/resume gestures, stop system

### Threading Architecture

```
┌─────────────────────────────────────────────┐
│           MAIN THREAD                       │
│  - Gesture recognition (OpenCV loop)        │
│  - UI rendering                             │
│  - Command execution                        │
└─────────────────────────────────────────────┘
                  ↕
         [Shared State - Thread-Safe]
                  ↕
┌─────────────────────────────────────────────┐
│      BACKGROUND THREAD                      │
│  - Continuous mic listening                 │
│  - Speech recognition                       │
│  - Command queue population                 │
└─────────────────────────────────────────────┘
```

---

## 📦 Installation

### Required Dependencies

```bash
# Core speech recognition (required)
pip install SpeechRecognition

# Audio input (required for microphone)
pip install pyaudio

# System control (required for command execution)
pip install pyautogui pynput

# Offline recognition with vosk (recommended)
pip install vosk

# Alternative: sounddevice for audio
pip install sounddevice

# Optional: Text-to-speech feedback
pip install pyttsx3
```

### One-Line Install

```bash
pip install SpeechRecognition pyaudio pyautogui pynput vosk pyttsx3 sounddevice
```

### Vosk Model Setup (Offline Recognition)

1. Download a vosk model from https://alphacephei.com/vosk/models
   - Recommended: `vosk-model-small-en-us-0.15` (40 MB)
   - Full accuracy: `vosk-model-en-us-0.22` (1.8 GB)

2. Extract the model:
   ```bash
   mkdir -p models
   cd models
   # Extract downloaded zip here
   unzip vosk-model-small-en-us-0.15.zip
   ```

3. Update path in `config.py`:
   ```python
   VOSK_MODEL_PATH = "models/vosk-model-small-en-us-0.15"
   ```

### Platform-Specific Notes

**Windows:**
```bash
# PyAudio binary wheel
pip install pipwin
pipwin install pyaudio
```

**Linux:**
```bash
# ALSA development libraries
sudo apt-get install python3-pyaudio portaudio19-dev
pip install pyaudio
```

**macOS:**
```bash
# PortAudio via homebrew
brew install portaudio
pip install pyaudio
```

---

## 🚀 Quick Start

### Minimal Example

```python
from voice_assistant import VoiceController, VoiceCommandExecutor, VoiceConfig

# Initialize
config = VoiceConfig()
executor = VoiceCommandExecutor(config)

def on_command(action, phrase):
    executor.execute(action, phrase)

controller = VoiceController(command_callback=on_command, config=config)

# Start listening
controller.start_listening()

# Your main loop here
try:
    while config.is_system_running():
        # Process commands
        command = controller.get_command(timeout=None)
        if command:
            action, phrase = command
            # Already executed by callback
        
        # Your gesture recognition code here
        time.sleep(0.03)

finally:
    controller.stop_listening()
```

### Full Application

```bash
cd voice_assistant
python main.py
```

**Voice commands to try:**
- "scroll up" / "scroll down"
- "new tab" / "close tab"
- "click" / "double click"
- "pause gestura" / "resume gestura"
- "show help"

---

## 🏗️ Architecture

### File Structure

```
voice_assistant/
├── __init__.py              # Module exports
├── config.py               # Configuration & shared state
├── voice_controller.py     # Speech recognition & listening
├── voice_commands.py       # Command execution & actions
├── main.py                 # Integration example
└── README.md               # This file

models/                      # Vosk models (download separately)
└── vosk-model-small-en-us-0.15/
```

### Component Responsibilities

**config.py:**
- Voice recognition settings (thresholds, timeouts)
- Command mapping (phrase → action)
- Thread-safe shared state (gesture_active, system_running)
- TTS configuration

**voice_controller.py:**
- Microphone input management
- Speech recognition (vosk/sphinx/google)
- Continuous background listening
- Command queue management
- Thread-safe command dispatch

**voice_commands.py:**
- Action execution (pyautogui/pynput)
- Mouse control
- Keyboard shortcuts
- Browser actions
- System state control
- Optional TTS feedback

**main.py:**
- Integration example
- Concurrent gesture + voice execution
- Shared state coordination
- Clean shutdown

---

## ⚙️ Configuration

### Basic Settings

Edit `voice_assistant/config.py`:

```python
class VoiceConfig:
    # Recognition
    USE_OFFLINE_RECOGNITION = True  # Use vosk/sphinx (no internet)
    LANGUAGE = "en-US"              # Recognition language
    ENERGY_THRESHOLD = 1000         # Mic sensitivity (300-4000)
    PAUSE_THRESHOLD = 0.8           # Phrase completion delay (seconds)
    PHRASE_TIMEOUT = 5.0            # Max listening time (seconds)
    
    # TTS Feedback
    VOICE_FEEDBACK_ENABLED = True   # Speak confirmations
    TTS_RATE = 180                  # Speech rate (WPM)
    TTS_VOLUME = 0.8                # Volume (0.0-1.0)
    
    # Vosk Model
    VOSK_MODEL_PATH = "models/vosk-model-small-en-us-0.15"
```

### Adding Custom Commands

1. Add phrase to command map:
   ```python
   COMMAND_MAP: Dict[str, str] = {
       "copy text": "copy",
       "paste text": "paste",
       # ...
   }
   ```

2. Add action handler in `voice_commands.py`:
   ```python
   def action_copy(self) -> None:
       """Copy to clipboard."""
       if PYAUTOGUI_AVAILABLE:
           pyautogui.hotkey('ctrl', 'c')
       print("📋 Copy")
   
   # Register in action_map
   self.action_map = {
       "copy": self.action_copy,
       # ...
   }
   ```

3. Optional: Add feedback message:
   ```python
   FEEDBACK_MESSAGES: Dict[str, str] = {
       "copy": "Text copied",
       # ...
   }
   ```

---

## 🎤 Voice Commands

### Complete Command List

| Category | Command | Action |
|----------|---------|--------|
| **Mouse** | "click" | Left click |
| | "double click" | Double click |
| | "right click" | Right click |
| **Scrolling** | "scroll up" | Scroll up |
| | "scroll down" | Scroll down |
| | "page up" | Page up |
| | "page down" | Page down |
| **Browser** | "go back" | Browser back |
| | "go forward" | Browser forward |
| | "new tab" | Open new tab (Ctrl+T) |
| | "close tab" | Close tab (Ctrl+W) |
| | "refresh" / "refresh page" | Refresh (F5) |
| **Zoom** | "zoom in" | Zoom in (Ctrl++) |
| | "zoom out" | Zoom out (Ctrl+-) |
| | "reset zoom" | Reset zoom (Ctrl+0) |
| **Media** | "mute" / "unmute" | Toggle mute |
| | "volume up" | Increase volume |
| | "volume down" | Decrease volume |
| **Screenshot** | "screenshot" / "take screenshot" | Take screenshot |
| **System** | "pause gestura" | Pause gesture recognition |
| | "resume gestura" | Resume gesture recognition |
| | "stop gestura" | Stop entire system |
| | "show help" | List all commands |

### Usage Tips

- **Speak clearly** at normal volume
- **Wait for recognition** (small delay is normal)
- **Use exact phrases** from the table above
- **Background noise**: Adjust `ENERGY_THRESHOLD` if needed
- **Internet**: Not required if using vosk/sphinx

---

## 🔌 Integration Guide

### Integrating with Existing Gesture System

**Step 1: Import voice assistant**

```python
from voice_assistant import VoiceController, VoiceCommandExecutor, VoiceConfig
```

**Step 2: Initialize in your main file**

```python
class YourGestureSystem:
    def __init__(self):
        # Your existing code
        self.camera = cv2.VideoCapture(0)
        # ...
        
        # Add voice assistant
        self.voice_config = VoiceConfig()
        self.voice_executor = VoiceCommandExecutor(self.voice_config)
        self.voice_controller = VoiceController(
            command_callback=self.on_voice_command,
            config=self.voice_config
        )
        
        # Start voice listening
        self.voice_controller.start_listening()
    
    def on_voice_command(self, action, phrase):
        """Handle voice commands."""
        self.voice_executor.execute(action, phrase)
```

**Step 3: Check shared state in gesture loop**

```python
def process_gestures(self):
    while True:
        # Check if system should stop
        if not self.voice_config.is_system_running():
            break
        
        # Check if gestures are paused by voice
        if not self.voice_config.is_gesture_active():
            # Skip gesture recognition, show "PAUSED" UI
            continue
        
        # Your gesture recognition code
        # ...
```

**Step 4: Clean shutdown**

```python
def shutdown(self):
    self.voice_controller.stop_listening()
    self.camera.release()
    cv2.destroyAllWindows()
```

### Thread Safety

**Shared state access (thread-safe):**

```python
# Check if gestures active (from any thread)
if config.is_gesture_active():
    # Do gesture recognition

# Pause gestures (from any thread)
config.set_gesture_active(False)

# Check if system running (from any thread)
if config.is_system_running():
    # Continue main loop

# Stop system (from any thread)
config.stop_system()
```

**Never directly access internal flags:**
```python
# ❌ WRONG - not thread-safe
if config._gesture_active:

# ✅ CORRECT - thread-safe
if config.is_gesture_active():
```

---

## 🔧 Troubleshooting

### Microphone Not Working

**Problem:** "Failed to initialize microphone"

**Solutions:**
1. Check mic permissions (Windows: Settings → Privacy → Microphone)
2. Test mic in other apps (Audacity, Voice Recorder)
3. Try different mic input:
   ```python
   # List available mics
   import speech_recognition as sr
   print(sr.Microphone.list_microphone_names())
   
   # Use specific mic
   self.microphone = sr.Microphone(device_index=1)
   ```
4. Install/reinstall PyAudio:
   ```bash
   pip uninstall pyaudio
   pip install pyaudio
   ```

### Recognition Not Working

**Problem:** Audio detected but no commands recognized

**Solutions:**
1. **Speak exact phrases** from command list
2. **Adjust energy threshold:**
   ```python
   ENERGY_THRESHOLD = 500  # More sensitive
   # or
   ENERGY_THRESHOLD = 2000  # Less sensitive
   ```
3. **Check background noise:**
   - Calibrate in quieter environment
   - Use headset mic instead of laptop mic
4. **Verify recognition backend:**
   ```python
   stats = controller.get_statistics()
   print(f"Backend: {stats['backend']}")
   ```

### Vosk Not Loading

**Problem:** "Failed to load vosk model"

**Solutions:**
1. **Verify model path:**
   ```bash
   ls models/vosk-model-small-en-us-0.15
   # Should show: am/ conf/ graph/ ivector/
   ```
2. **Download correct model:**
   - Get from https://alphacephei.com/vosk/models
   - Extract completely (not just .zip)
3. **Use absolute path:**
   ```python
   VOSK_MODEL_PATH = r"C:\Users\...\models\vosk-model-small-en-us-0.15"
   ```

### Commands Lag/Slow

**Problem:** Long delay between speech and action

**Solutions:**
1. **Use smaller vosk model:**
   - `vosk-model-small-en-us-0.15` (40 MB) is fastest
2. **Reduce pause threshold:**
   ```python
   PAUSE_THRESHOLD = 0.5  # Faster response
   ```
3. **Check CPU usage:**
   - Close other applications
   - Use offline recognition (no network latency)

### TTS Not Speaking

**Problem:** No voice feedback

**Solutions:**
1. **Check TTS enabled:**
   ```python
   VOICE_FEEDBACK_ENABLED = True
   ```
2. **Install pyttsx3:**
   ```bash
   pip install pyttsx3
   ```
3. **Test TTS separately:**
   ```python
   import pyttsx3
   engine = pyttsx3.init()
   engine.say("Test")
   engine.runAndWait()
   ```

---

## 📚 API Reference

### VoiceController

**Constructor:**
```python
VoiceController(
    command_callback: Optional[Callable[[str, str], None]] = None,
    config: Optional[VoiceConfig] = None
)
```

**Methods:**
- `start_listening() -> bool` - Start background listening
- `stop_listening() -> None` - Stop listening and cleanup
- `get_command(timeout=None) -> Optional[tuple]` - Get next command from queue
- `clear_queue() -> int` - Clear all pending commands
- `get_statistics() -> dict` - Get recognition stats

**Attributes:**
- `is_listening: bool` - Whether actively listening
- `commands_recognized: int` - Total commands recognized
- `use_vosk: bool` - Whether using vosk backend

### VoiceCommandExecutor

**Constructor:**
```python
VoiceCommandExecutor(config: Optional[VoiceConfig] = None)
```

**Methods:**
- `execute(action: str, phrase: str = "") -> bool` - Execute command action
- `speak(text: str) -> None` - TTS text (if enabled)

**Action Methods:**
All action methods are callable directly:
- `action_click()`, `action_double_click()`, `action_right_click()`
- `action_scroll_up()`, `action_scroll_down()`
- `action_new_tab()`, `action_close_tab()`, `action_refresh()`
- `action_zoom_in()`, `action_zoom_out()`, `action_reset_zoom()`
- `action_pause_gestures()`, `action_resume_gestures()`
- `action_stop_system()`, `action_show_help()`

### VoiceConfig

**Class Methods (Thread-Safe):**
- `is_gesture_active() -> bool` - Check if gestures active
- `set_gesture_active(active: bool) -> None` - Pause/resume gestures
- `is_voice_active() -> bool` - Check if voice active
- `set_voice_active(active: bool) -> None` - Pause/resume voice
- `is_system_running() -> bool` - Check if system running
- `stop_system() -> None` - Stop entire system

**Configuration Attributes:**
- `USE_OFFLINE_RECOGNITION: bool`
- `LANGUAGE: str`
- `ENERGY_THRESHOLD: int`
- `PAUSE_THRESHOLD: float`
- `PHRASE_TIMEOUT: float`
- `VOSK_MODEL_PATH: str`
- `VOICE_FEEDBACK_ENABLED: bool`
- `TTS_RATE: int`
- `TTS_VOLUME: float`
- `COMMAND_MAP: Dict[str, str]`
- `FEEDBACK_MESSAGES: Dict[str, str]`

---

## 📄 License

MIT License - See LICENSE file for details

## 👨‍💻 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch
3. Add tests for new features
4. Submit pull request

## 📞 Support

- Issues: GitHub Issues
- Documentation: This README
- Examples: `main.py`

---

**Made with ❤️ by Gestura Development Team**
