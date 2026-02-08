# AccessAble - Quick Start Guide

## 🚀 5-Minute Setup

### Step 1: Verify Requirements
```bash
python --version
# Should show Python 3.10 or higher
```

### Step 2: Run Setup Script
```bash
python setup.py
```

This will:
- ✓ Check Python version
- ✓ Verify project structure
- ✓ Check/install dependencies
- ✓ Confirm everything is ready

### Step 3: Launch Application
```bash
python main.py
```

---

## 🎯 First-Time User Guide

### Camera Setup
1. Position yourself **1-2 feet** from camera
2. Ensure **good lighting** (face a window or lamp)
3. Show **one hand** to the camera
4. Keep hand in **center of frame**

### Try Default Gestures

#### ✋ Open Palm (Pause)
- All fingers extended and spread
- Use to pause/rest without triggering actions

#### ✊ Fist (Left Click)
- All fingers curled into fist
- Hold for 1.5 seconds to click

#### ✌️ Peace Sign (Right Click)
- Index and middle finger extended
- Hold for 1.5 seconds to right-click

#### 👍 Thumbs Up (Scroll Up)
- Only thumb extended upward
- Other fingers curled
- Hold to scroll page up

#### 👎 Thumbs Down (Scroll Down)
- Thumb pointing downward
- Other fingers curled
- Hold to scroll page down

---

## ⌨️ Keyboard Controls

| Key | Action |
|-----|--------|
| `ESC` | Emergency pause/resume |
| `Space` | Toggle pause |
| `Q` | Quit application |

---

## 📊 Understanding the UI

### Info Panel (Top Left)
```
Status: ACTIVE/PAUSED
Gesture: [Current gesture name]
Confidence: [0-100%]
Action: [Action that will trigger]
```

### Progress Bar (Top Right)
- Shows dwell time progress
- Fills from 0% to 100%
- Action triggers at 100%

### Help Text (Bottom Left)
- Quick reference for controls

### FPS Counter (Bottom Right)
- Performance indicator
- Target: 25-30 FPS

---

## 🔧 Common Issues

### "Camera not found"
**Solution**: 
- Close other apps using camera (Zoom, Skype, etc.)
- Try different camera if multiple available
- Check camera permissions in system settings

### "Low FPS"
**Solution**:
- Close unnecessary applications
- Improve lighting (less processing needed)
- Reduce resolution in `config/constants.py`

### "Gestures not detecting"
**Solution**:
- Move closer to camera (1-2 feet optimal)
- Improve lighting
- Hold gestures more deliberately
- Ensure only one hand visible

### "Actions triggering too fast/slow"
**Solution**:
Edit `config/constants.py`:
```python
# Adjust dwell time
DWELL_TIME_SECONDS: float = 1.0  # Faster
DWELL_TIME_SECONDS: float = 2.0  # Slower
```

---

## 🎨 Customization

### Change Gesture Mappings

Edit `config/user_settings.json` (created after first run):
```json
{
  "gesture_mappings": {
    "fist": "scroll_down",
    "peace_sign": "left_click",
    "thumbs_up": "browser_forward"
  }
}
```

### Adjust Sensitivity

Edit `config/constants.py`:
```python
# Higher = more strict (fewer false positives)
GESTURE_CONFIDENCE_THRESHOLD: float = 0.85

# Higher = more stable (less jitter)
STABILIZATION_WINDOW: int = 7
```

---

## 📝 Tips for Best Experience

✅ **DO:**
- Start with open palm (pause gesture)
- Hold gestures steady for full dwell time
- Use smooth, deliberate movements
- Position hand in center of frame
- Ensure consistent lighting

❌ **AVOID:**
- Rapid hand movements
- Partial hand visibility
- Backlighting (window behind you)
- Cluttered background
- Multiple hands in frame

---

## 🆘 Emergency Stop

**If system becomes unresponsive:**
1. Press `ESC` key to pause
2. Move mouse to screen corner (PyAutoGUI failsafe)
3. Press `Q` to quit

---

## 📚 Next Steps

- Read [README.md](README.md) for full documentation
- See [TECHNICAL_DETAILS.md](TECHNICAL_DETAILS.md) for architecture
- Modify `config/constants.py` for your needs
- Experiment with gesture mappings

---

**Enjoy AccessAble! 🤲✨**
