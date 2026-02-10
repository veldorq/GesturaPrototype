# Hand Gesture Control System - User Guide

## 🚀 Quick Start

### First Time Setup
1. **Install Python** (if not already installed):
   - Download Python 3.10+ from [python.org](https://www.python.org/downloads/)
   - ✅ Check "Add Python to PATH" during installation

2. **Run Installation**:
   - Double-click `INSTALL.bat`
   - Wait for dependencies to install (takes 2-3 minutes)

3. **Start Application**:
   - Double-click `RUN.bat`
   - Allow camera access when prompted

---

## 🎮 Gesture Controls

### Scrolling
- **Open Palm** (5 fingers) → Scroll Down (fast)
- **Closed Fist** (0 fingers) → Scroll Up

### Mouse Control
- **Index Finger Only** → Move Cursor (pointer mode)
- **Three Fingers** (index + middle + ring) → Left Click
- **Peace Sign** ✌️ (index + middle) → Left Click (alternative)

### Navigation
- **Swipe Left** 👈 → Browser Back
- **Swipe Right** 👉 → Browser Forward

### Page Actions
- **Four Fingers** (without thumb) → Refresh Page
- **Thumb Up** 👍 → Zoom In
- **Pinky Only** → Mute/Unmute

### Clipboard
- **OK Sign** 👌 (thumb + index circle) → Paste

### System Control
- **Rock Sign** 🤘 (index + pinky) + **HOLD 1.5s** → Exit Program
- **Call Me** 🤙 (thumb + pinky) + **HOLD 1.5s** → Close Browser

---

## ⌨️ Keyboard Shortcuts
- **Q** → Quit program
- **H** → Toggle camera view
- **S** → Show statistics
- **B** → Launch browser

---

## ⚙️ System Requirements

### Minimum
- Windows 10/11
- Python 3.10+
- Webcam (built-in or USB)
- 4GB RAM
- Dual-core processor

### Recommended
- Windows 11
- Python 3.11+
- HD Webcam
- 8GB RAM
- Quad-core processor

---

## 🐛 Troubleshooting

### Camera Not Working
- **Check permissions**: Settings → Privacy → Camera → Allow apps to access camera
- **Close other apps** using camera (Zoom, Teams, etc.)
- Try different camera index in settings

### Gestures Not Detecting
- **Lighting**: Ensure good lighting (avoid backlighting)
- **Distance**: Keep hand 1-2 feet from camera
- **Background**: Use plain background for best results
- **Fingers**: Make clear, deliberate gestures

### Slow Performance
- Close unnecessary browser tabs
- Reduce background applications
- Check Task Manager for high CPU usage
- Try lowering camera resolution in config

### Installation Errors
```powershell
# If pip install fails, try:
python -m pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt
```

---

## 📝 Tips for Best Experience

1. **Hand Position**: Keep entire hand in frame, palm facing camera
2. **Deliberate Gestures**: Hold gestures for 0.5s for recognition
3. **Lighting**: Bright, even lighting works best
4. **Background**: Plain walls reduce false positives
5. **Practice**: Spend 2-3 minutes practicing gestures

---

## 🔧 Advanced Configuration

Edit `PROTOTYPE.PY` to customize:
- Scroll sensitivity (line ~96): `SCROLL_SENSITIVITY = "high"`
- Pointer smoothness (line ~83): `MOUSE_SMOOTHING = 0.35`
- Camera index (line ~71): `CAMERA_INDEX = 0`
- Recognition confidence (line ~74): `MIN_DETECTION_CONFIDENCE = 0.7`

---

## 📞 Support

For issues or questions:
1. Check troubleshooting section above
2. Review gesture examples in camera preview
3. Contact: [Your contact info]

---

## 📄 License & Credits

Created by: [Your Name]
Version: 1.0
Date: February 2026

Uses:
- MediaPipe (Google)
- OpenCV
- PyAutoGUI
