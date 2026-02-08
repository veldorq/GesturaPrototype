# 🚀 Quick Reference Card - AccessAble CNN System

## ⚡ Installation (1 Minute)

```powershell
cd C:\Users\Souvik\Desktop\Project\ACESSABLE
pip install -r requirements.txt
python PROTOTYPE.PY
```

---

## 🎮 Runtime Keyboard Controls

| Key | Action |
|-----|--------|
| **'c'** | Toggle CNN on/off |
| **'q'** | Quit safely |
| **'s'** | Show statistics |
| **'h'** | Toggle advanced UI |
| **'b'** | Launch browser |

---

## 🤚 Supported Gestures (16 Total)

| Gesture | Action | CNN Support |
|---------|--------|-------------|
| Open Palm (4 fingers) | Scroll Down | ✅ |
| Closed Fist | Scroll Up | ✅ |
| Index Only | Pointer Move | MediaPipe |
| Peace Sign (2 fingers) | Left Click | Rule-based |
| Thumb Up | Right Click | Rule-based |
| Swipe Left | Browser Back | ✅ |
| Swipe Right | Browser Forward | ✅ |
| Pinch (Index+Thumb) | Zoom In/Out | ✅ (hybrid) |
| Thumb Down | Close Tab | ✅ |
| Pinky Only | Mute/Unmute | ✅ |
| 3 Fingers | Screenshot | Rule-based |
| 4 Fingers | Refresh | Rule-based |

---

## 🔧 CNN Configuration (Quick Access)

**File**: `PROTOTYPE.PY`  
**Lines**: 132-161

```python
# Toggle CNN on/off
ENABLE_CNN_CLASSIFIER = True

# Safety thresholds (DO NOT LOWER)
CNN_MIN_CONFIDENCE = 0.75        # 75% confidence minimum
CNN_VOTING_WINDOW = 5            # 5 frames must agree
CNN_VOTING_CONSISTENCY = 0.8     # 80% consistency required
```

---

## 📊 Quick Training (3 Commands)

### Option 1: Rule-Based (No Training)
```powershell
python PROTOTYPE.PY
```

### Option 2: CNN-Based (Best Accuracy)
```powershell
# Step 1: Collect data (30-40 min)
python collect_gesture_dataset.py

# Step 2: Train model (30-45 min CPU, 5-10 min GPU)
python train_gesture_model.py

# Step 3: Run with CNN
python PROTOTYPE.PY
```

---

## 🛡️ Safety Pipeline (4 Stages)

```
Raw CNN Prediction
    ↓
Stage 1: Confidence Filter (≥75%)
    ↓
Stage 2: Temporal Voting (5 frames, 80%)
    ↓
Stage 3: Gesture Stabilization (5-frame buffer)
    ↓
Stage 4: Debouncing (0.5s cooldown)
    ↓
Action Execution
```

---

## 📈 Expected Performance

| Metric | Target | Check |
|--------|--------|-------|
| **CNN Accuracy** | 90-95% | confusion_matrix.png |
| **Runtime FPS** | 25-30 | Video feed overlay |
| **False Positives** | <2% | Test during use |
| **Latency** | <50ms | Should feel instant |

---

## 🐛 Common Issues (Quick Fixes)

### CNN not loading?
```python
# PROTOTYPE.PY, line 141
ENABLE_CNN_CLASSIFIER = False  # Temporarily disable
```

### Too slow (FPS < 20)?
```python
# PROTOTYPE.PY, lines 48-49
FRAME_WIDTH = 960   # Lower resolution
FRAME_HEIGHT = 540
```

### Accidental triggers?
```python
# PROTOTYPE.PY, line 56
DEBOUNCE_TIME = 0.7  # Increase cooldown
```

### Low accuracy?
```python
# PROTOTYPE.PY, line 147
CNN_MIN_CONFIDENCE = 0.70  # Lower (carefully)
```

---

## 📂 File Structure (What to Keep)

```
ACESSABLE/
├── PROTOTYPE.PY                    # ⭐ Main system (run this)
├── collect_gesture_dataset.py      # Dataset collector
├── train_gesture_model.py          # CNN training
├── gesture_model_inference.py      # CNN inference
├── requirements.txt                # Dependencies
├── CNN_USAGE_GUIDE.md              # Full documentation
├── CNN_INTEGRATION_SUMMARY.md      # What was added
└── models/                         # ⭐ Trained models (critical!)
    ├── gesture_cnn_model.h5        # CNN model (~600 KB)
    └── label_encoder.pkl           # Gesture mapping
```

---

## 🎓 Key Configuration Sections

### Scroll Speed (Lines 63-68)
```python
SCROLL_SPEED_MULTIPLIER = 3.5  # Faster scroll
SCROLL_SMOOTH_STEPS = 4        # Smooth animation
SCROLL_DWELL_TIME = 0.25       # Quick response
```

### Browser Safety (Lines 99-113)
```python
# Browser navigation
BROWSER_NAV_DWELL_TIME = 0.8      # 0.8s deliberate hold
BROWSER_NAV_COOLDOWN = 1.5        # 1.5s between actions

# Close tab (MAX SAFETY)
CLOSE_TAB_DWELL_TIME = 1.2        # 1.2s hold required
CLOSE_TAB_COOLDOWN = 2.0          # 2s between closes
```

### Pointer Mode (Lines 72-77)
```python
MOUSE_SMOOTHING = 0.3              # Lower = more responsive
ENABLE_MODE_SEPARATION = True      # Separate POINTER/GESTURE
DISABLE_ZOOM_IN_POINTER_MODE = True  # Prevent interference
```

### Thumb Fix (Lines 93-95)
```python
THUMB_IGNORED_MODE = True          # Exclude from finger counting
THUMB_EXPLICIT_GESTURES_ONLY = True  # Only explicit thumb gestures
```

---

## 🔍 CNN Status Verification

### Startup Messages (Look for these)

**✅ Success:**
```
🤖 Initializing CNN Gesture Classifier...
✅ CNN model loaded successfully
   - Model: models/gesture_cnn_model.h5
   - Confidence threshold: 0.75
   - Voting window: 5 frames
   - Consistency required: 80.0%
```

**⚠️ Fallback (Expected if no model):**
```
⚠️ CNN model loading failed - falling back to rule-based recognition
```

**ℹ️ Disabled:**
```
ℹ️ CNN recognition disabled - using rule-based recognition
```

---

## 📝 Quick Tweaks (Most Common)

### Make scroll faster
```python
SCROLL_SPEED_MULTIPLIER = 4.5  # Was 3.5
```

### Make pointer more responsive
```python
MOUSE_SMOOTHING = 0.2  # Was 0.3 (lower = faster)
```

### Require more deliberate gestures
```python
GESTURE_BUFFER_SIZE = 7  # Was 5 (more stable)
```

### Make close tab even safer
```python
CLOSE_TAB_DWELL_TIME = 1.5  # Was 1.2
```

### Make CNN more strict
```python
CNN_MIN_CONFIDENCE = 0.80  # Was 0.75
CNN_VOTING_CONSISTENCY = 0.85  # Was 0.80
```

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| **CNN_USAGE_GUIDE.md** | Comprehensive CNN guide (500+ lines) |
| **CNN_INTEGRATION_SUMMARY.md** | What was added in Phase 4 |
| **QUICK_REFERENCE.md** | This file (quick lookup) |

---

## ✅ Pre-Flight Checklist

Before using for important work:

- [ ] Tested all gestures in good lighting
- [ ] Verified no accidental triggers during normal movement
- [ ] FPS ≥ 25 (check video feed)
- [ ] Close tab requires 1.2s hold (safety verified)
- [ ] Browser navigation requires 0.8s hold
- [ ] CNN toggle works (press 'c' key)
- [ ] Rule-based fallback works (disable CNN, still functions)

---

## 🎯 Success Indicators

You'll know everything is working when:

1. ✅ Video feed shows "🤖 CNN: ON" in cyan (top right)
2. ✅ FPS displays 25-30 (top left)
3. ✅ Gestures recognized within 200ms
4. ✅ No false positives during normal hand movement
5. ✅ Close tab requires deliberate 1.2s hold
6. ✅ Press 'c' key toggles "CNN: ON" ↔ "Rule-based"

---

## 🚑 Emergency Fallback

If CNN causes issues, instantly fall back:

```python
# PROTOTYPE.PY, line 141
ENABLE_CNN_CLASSIFIER = False
```

OR press **'c'** key during runtime to toggle off.

---

## 🎉 Quick Start Command

**Copy-paste this to get started immediately:**

```powershell
cd C:\Users\Souvik\Desktop\Project\ACESSABLE
pip install opencv-python mediapipe pyautogui numpy tensorflow scikit-learn matplotlib seaborn
python PROTOTYPE.PY
```

Press **'q'** to quit, **'c'** to toggle CNN, **'h'** for help.

---

**System Status**: ✅ Ready for use!

For detailed documentation, see `CNN_USAGE_GUIDE.md`.
