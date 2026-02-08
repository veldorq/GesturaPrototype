# AccessAble - Gesture-Based Web Navigation

**A production-quality assistive technology system for touchless web navigation using hand gestures.**

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## 🎯 Overview

AccessAble is a modular Python application that enables **gesture-based, touchless web navigation** using a standard webcam. Designed specifically for users with **partial motor impairments**, it prioritizes:

- **Reliability** - Stable detection with tremor compensation
- **Low Physical Effort** - Single hand, limited motion gestures
- **Customization** - User-recordable gestures and mappings
- **Accessibility** - Dwell-based activation, visual feedback, emergency controls

---

## ✨ Key Features

### 🤲 Gesture Detection
- Real-time single-hand detection at ~30 FPS
- Landmark-based recognition (no background assumptions)
- Support for limited-motion and single-hand usage

### 🧠 Smart Gesture Handling
- **Gesture abstraction layer** - gestures ≠ actions
- **Custom gesture recording** - personalize to your needs
- **Persistent configuration** - saved to JSON files

### ⚡ Robust Interaction
- **Dwell-based activation** - hold gesture to trigger
- **Stabilization system** - smoothing, confidence thresholds, debounce
- **Tremor compensation** - multi-frame averaging
- **Emergency controls** - ESC to pause, failsafe mechanisms

### 🎨 Visual Feedback
Real-time overlay displays:
- Detected gesture name
- Mapped action preview
- Dwell-time progress bar
- System status indicators

### 🌐 Browser Actions
- Scroll up / down
- Left click / Right click
- Browser back / forward
- Easily extensible for more actions

---

## 🛠️ Technical Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.10+ |
| Camera Input | OpenCV (`opencv-python`) |
| Hand Tracking | MediaPipe Hands |
| Automation | PyAutoGUI |
| Math | NumPy |

---

## 📦 Installation

### Prerequisites
- Python 3.10 or higher
- Webcam (built-in or external)
- Windows / macOS / Linux

### Step 1: Clone or Download the Project

```bash
cd c:\Users\Souvik\Desktop\Project\ACESSABLE
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `opencv-python` - Camera capture and image processing
- `mediapipe` - Hand landmark detection
- `pyautogui` - System automation
- `numpy` - Numerical operations

---

## 🚀 Usage

### Quick Start

1. **Activate virtual environment** (if created):
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

2. **Run the application**:
   ```bash
   python main.py
   ```

3. **Position yourself**:
   - Sit 1-2 feet from the camera
   - Ensure good lighting
   - Show one hand to the camera

4. **Try default gestures**:
   - **Open Palm** → Pause (neutral)
   - **Fist** → Left Click
   - **Peace Sign** → Right Click
   - **Thumbs Up** → Scroll Up
   - **Thumbs Down** → Scroll Down

### Controls

| Key | Action |
|-----|--------|
| `ESC` | Emergency stop (pause/resume) |
| `Space` | Toggle pause |
| `Q` | Quit application |

### Tips for Best Experience

✅ **DO:**
- Use consistent lighting
- Keep hand in frame center
- Hold gestures steady for dwell time
- Start with default gestures

❌ **AVOID:**
- Rapid gesture changes
- Complex multi-hand poses
- Backlighting (light behind you)
- Moving camera during use

---

## 🏗️ Architecture

The project follows **clean architecture principles** with strong separation of concerns:

```
AccessAble/
├── camera/              # Webcam capture and frame management
│   ├── __init__.py
│   └── webcam.py        # Webcam class with resource management
│
├── hand_tracking/       # MediaPipe hand detection
│   ├── __init__.py
│   └── detector.py      # HandDetector and HandLandmarks classes
│
├── gestures/            # Gesture recognition system
│   ├── __init__.py
│   ├── gesture.py       # Gesture and GestureLibrary classes
│   ├── recognizer.py    # GestureRecognizer with stabilization
│   └── recorder.py      # GestureRecorder for custom gestures
│
├── actions/             # Action execution
│   ├── __init__.py
│   └── browser_actions.py  # BrowserActions using PyAutoGUI
│
├── ui/                  # Visual feedback
│   ├── __init__.py
│   └── overlay.py       # OverlayRenderer for on-screen info
│
├── config/              # Configuration management
│   ├── __init__.py
│   ├── constants.py     # Constants dataclass (no magic values)
│   └── settings.py      # Settings class for persistence
│
├── main.py              # Application entry point and orchestrator
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

### Module Responsibilities

#### 📷 `camera` - Frame Acquisition
- Opens/releases webcam
- Captures frames with error handling
- Mirrors frame for intuitive UX

#### 👁️ `hand_tracking` - Landmark Detection
- Wraps MediaPipe Hands API
- Extracts 21 3D hand landmarks
- Provides high-level landmark accessors

#### ✋ `gestures` - Gesture Recognition
- **`gesture.py`** - Defines gesture data structures
- **`recognizer.py`** - Feature extraction and matching
- **`recorder.py`** - Custom gesture capture

#### 🎬 `actions` - Automation
- Maps action names to PyAutoGUI commands
- Executes browser and system actions
- Extensible action registry

#### 🖼️ `ui` - Visual Feedback
- Renders info panels and progress bars
- Provides real-time user feedback
- Notification system

#### ⚙️ `config` - Configuration
- Centralized constants (no magic numbers)
- User preference persistence (JSON)
- Gesture-to-action mappings

---

## 🧪 How It Works: Gesture Recognition

AccessAble uses **geometric features** derived from hand landmarks, not raw positions. This makes the system **invariant to**:
- Hand size
- Distance from camera
- Position in frame

### Feature Extraction Process

1. **MediaPipe detects 21 hand landmarks** (wrist, finger joints, tips)

2. **Normalize by palm size** to handle distance variations

3. **Extract geometric features**:
   - **Finger extension** - Is each finger extended or curled?
   - **Finger spread** - Distance between adjacent fingertips
   - **Thumb angle** - Orientation relative to palm
   - **Finger curl** - Overall hand openness

4. **Compare to gesture library** using normalized Euclidean distance

5. **Stabilize** over multiple frames to reduce noise

### Stabilization Pipeline

```
Raw Landmarks
    ↓
Feature Extraction
    ↓
Gesture Matching
    ↓
[ History Buffer (5 frames) ]
    ↓
Consistency Check (60% threshold)
    ↓
Confidence Threshold (75%)
    ↓
Dwell Time (1.5 seconds)
    ↓
Debounce (0.5 seconds)
    ↓
ACTION TRIGGERED
```

This multi-stage approach ensures:
- **No false positives** from hand tremors
- **Deliberate activation** via dwell time
- **Stable tracking** across frames

---

## 🎨 Customization

### Adjusting Sensitivity

Edit [`config/constants.py`](config/constants.py):

```python
# Require higher confidence for activation
MIN_DETECTION_CONFIDENCE: float = 0.8  # Default: 0.7

# Shorter dwell time for faster interaction
DWELL_TIME_SECONDS: float = 1.0  # Default: 1.5

# More aggressive stabilization
STABILIZATION_WINDOW: int = 7  # Default: 5
```

### Custom Gesture Mapping

Edit [`config/settings.py`](config/settings.py) or modify `config/gestures_config.json`:

```json
{
  "fist": "scroll_down",
  "peace_sign": "left_click",
  "thumbs_up": "browser_forward"
}
```

### Recording New Gestures

The `GestureRecorder` class in [`gestures/recorder.py`](gestures/recorder.py) enables custom gesture capture. Integration into the main UI is left for future enhancement, but the core functionality is complete.

### Adding New Actions

Edit [`actions/browser_actions.py`](actions/browser_actions.py):

```python
def refresh_page(self) -> None:
    """Refresh current browser page."""
    pyautogui.hotkey('ctrl', 'r')  # or 'cmd', 'r' on Mac
    print("Action: Refresh Page")

# Register in __init__
self.action_map['refresh'] = self.refresh_page
```

---

## 🔧 Troubleshooting

### Camera Not Detected
- Ensure no other app is using the webcam
- Try changing `CAMERA_INDEX` in [`config/constants.py`](config/constants.py)
- Check camera permissions in system settings

### Poor Gesture Recognition
- **Improve lighting** - face a window or use desk lamp
- **Increase confidence threshold** in [`config/constants.py`](config/constants.py)
- **Move closer to camera** (1-2 feet optimal)
- **Use slower, more deliberate gestures**

### Low FPS (< 20)
- Close other applications
- Reduce `FRAME_WIDTH/HEIGHT` in [`config/constants.py`](config/constants.py)
- Ensure GPU acceleration (if available)

### Actions Not Triggering
- Check dwell time progress bar reaches 100%
- Verify gesture-to-action mapping in [`config/gestures_config.json`](config/gestures_config.json)
- Ensure application has accessibility permissions (macOS)

---

## 🔒 Privacy & Safety

- **All processing is local** - no data sent to cloud
- **No recording or storage** of camera feed
- **Emergency stop** via ESC key
- **PyAutoGUI failsafe** - move mouse to screen corner to abort

---

## 🛣️ Future Enhancements

Potential improvements for contributors:

- [ ] GUI for gesture recording and mapping
- [ ] Multi-language support
- [ ] Sound/haptic feedback options
- [ ] Head-tracking for cursor movement
- [ ] Gesture macros (sequences)
- [ ] Eye-gaze integration
- [ ] Mobile device support
- [ ] Cloud profile sync

---

## 📚 Technical Reference

### MediaPipe Hand Landmarks

MediaPipe provides 21 landmarks per hand:

```
0:  Wrist
1-4:  Thumb  (CMC, MCP, IP, Tip)
5-8:  Index  (MCP, PIP, DIP, Tip)
9-12: Middle (MCP, PIP, DIP, Tip)
13-16: Ring  (MCP, PIP, DIP, Tip)
17-20: Pinky (MCP, PIP, DIP, Tip)
```

Each landmark has `(x, y, z)` coordinates normalized to [0, 1].

### Configuration Files

- **`config/gestures_config.json`** - Gesture definitions
- **`config/user_settings.json`** - User preferences
- Generated automatically on first run

---

## 📄 License

This project is provided as-is for educational and assistive technology purposes.

---

## 🙏 Acknowledgments

Built with:
- [OpenCV](https://opencv.org/) - Computer vision library
- [MediaPipe](https://google.github.io/mediapipe/) - Google's ML solutions
- [PyAutoGUI](https://pyautogui.readthedocs.io/) - GUI automation

---

## 📧 Support

For issues or questions:
1. Check the [Troubleshooting](#-troubleshooting) section
2. Review code comments for implementation details
3. Adjust constants in [`config/constants.py`](config/constants.py)

---

**AccessAble** - Empowering accessible web navigation through gesture control. 🤲✨
