# AccessAble - Conflict-Free Edition - Quick Start

## 🚀 Running the Conflict-Free Version

### Launch Command

```bash
python main_conflict_free.py
```

---

## 🎯 What's Different?

The conflict-free edition guarantees **ONE gesture = ONE action** through:

1. **Mutually Exclusive Classification** - Only highest confidence gesture selected
2. **State Machine** - NONE → CANDIDATE → CONFIRMED → COOLDOWN lifecycle
3. **Dwell Time** - Hold gesture 1.5 seconds before triggering
4. **Action Cooldown** - 0.5 second block after each action
5. **Stability Checks** - 80% consistency across 5 frames

---

## 🤲 Supported Gestures

| Gesture | Criteria | Confidence | Action (Default) |
|---------|----------|------------|------------------|
| **Open Palm** | All 5 fingers extended & spread | 0.90-0.95 | Pause (none) |
| **Fist** | All fingers curled, none extended | 0.90-0.95 | Left Click |
| **Thumbs Up** | Only thumb extended, pointing up | 0.70-0.95 | Scroll Up |
| **Thumbs Down** | Only thumb extended, pointing down | 0.70-0.95 | Scroll Down |
| **Peace Sign** | Index + middle extended only | 0.90 | Right Click |
| **Pointing** | Only index extended | 0.85 | (Reserved) |

---

## 📊 Understanding the UI

### Top Left Panel

```
Status: ACTIVE | CANDIDATE
Gesture: Thumbs Up
Confidence: 87%
Action: Scroll Up
Actions: 5
```

- **Status**: Shows system and state machine state
  - `ACTIVE` = System running
  - `PAUSED` = System paused
  - `NONE` = No gesture
  - `CANDIDATE` = Checking stability
  - `CONFIRMED` = Action triggered
  - `COOLDOWN` = Blocking gestures

- **Gesture**: Current detected gesture
- **Confidence**: Classification confidence (0-100%)
- **Action**: What will execute
- **Actions**: Total actions triggered this session

### Top Right Progress Bar

**During CANDIDATE State**:
- Shows dwell time progress (0-100%)
- Green when ready to trigger
- Must reach 100% for action

**During COOLDOWN State**:
- Shows cooldown progress (0-100%)
- Red color indicates blocking
- Gestures ignored until 100%

---

## 🎮 Controls

| Key | Action |
|-----|--------|
| `ESC` | Emergency pause/resume |
| `Q` | Quit application |
| `Space` | Toggle pause |
| `D` | Debug info (console) |

---

## 🔍 How It Works

### Example: Triggering Left Click with Fist

```
Time  | Hand Pose | Classifier | State      | Progress | Action
------|-----------|------------|------------|----------|--------
0.0s  | Fist      | fist (0.9) | CANDIDATE  | 0%       | -
0.2s  | Fist      | fist (0.91)| CANDIDATE  | 13%      | -
0.4s  | Fist      | fist (0.89)| CANDIDATE  | 27%      | -
0.6s  | Fist      | fist (0.92)| CANDIDATE  | 40%      | -
0.8s  | Fist      | fist (0.9) | CANDIDATE  | 53%      | -
1.0s  | Fist      | fist (0.91)| CANDIDATE  | 67%      | -
1.2s  | Fist      | fist (0.9) | CANDIDATE  | 80%      | -
1.4s  | Fist      | fist (0.91)| CANDIDATE  | 93%      | -
1.5s  | Fist      | fist (0.9) | CONFIRMED  | 100%     | LEFT_CLICK ✓
1.5s  | Fist      | fist (0.9) | COOLDOWN   | -        | (blocked)
1.7s  | Fist      | fist (0.9) | COOLDOWN   | -        | (blocked)
1.9s  | Fist      | fist (0.9) | COOLDOWN   | -        | (blocked)
2.0s  | Fist      | fist (0.9) | NONE       | -        | -
```

**Key Points**:
- Gesture must be **held steadily** for 1.5 seconds
- Action triggers at 100% dwell progress
- System immediately blocks for 0.5 seconds
- Must release and re-do gesture for second click

---

## ⚠️ Troubleshooting

### "Gesture not triggering"

**Check**:
1. Confidence display - Is it above 75%?
2. Progress bar - Does it reach 100%?
3. State - Are you in COOLDOWN? (wait 0.5s)

**Solution**:
- Hold gesture more deliberately
- Ensure only intended fingers extended
- Wait for cooldown to expire

---

### "Wrong action triggered"

**This should NOT happen** in conflict-free mode!

If it does:
1. Press `D` to see debug info
2. Check which gesture was detected
3. Verify your hand matches gesture criteria

**Report**: This indicates a logic error - please report with:
- Gesture you showed
- Action that triggered
- Debug info from console

---

### "Multiple actions from one gesture"

**This is IMPOSSIBLE** in conflict-free mode due to:
- State machine COOLDOWN blocking
- Only one gesture detected per frame
- Explicit action cooldown

If you experience this:
1. Check console for duplicate action logs
2. Verify you're running `main_conflict_free.py`
3. Report as bug with timestamps

---

## 🎯 Best Practices

### For Reliable Detection

✅ **DO**:
- Start with open palm (neutral)
- Transition smoothly between gestures
- Hold gestures steady until progress = 100%
- Wait for cooldown to complete
- Use consistent hand shapes

❌ **DON'T**:
- Make rapid hand movements
- Change gestures mid-dwell
- Expect instant response (dwell time is intentional)
- Force ambiguous hand poses

---

### For Accessibility

**Adjust timing** in `config/constants.py`:

```python
# Faster response (less stable)
STABILIZATION_WINDOW: int = 3       # Default: 5
DWELL_TIME_SECONDS: float = 1.0     # Default: 1.5
DEBOUNCE_COOLDOWN_SECONDS: float = 0.3  # Default: 0.5

# Slower response (more stable)
STABILIZATION_WINDOW: int = 7       # More frames
DWELL_TIME_SECONDS: float = 2.0     # Longer hold
DEBOUNCE_COOLDOWN_SECONDS: float = 1.0  # Longer cooldown
```

**Adjust confidence** for sensitivity:

```python
# More lenient (detects easier, more false positives)
GESTURE_CONFIDENCE_THRESHOLD: float = 0.6  # Default: 0.75

# Stricter (requires clearer gestures, fewer false positives)
GESTURE_CONFIDENCE_THRESHOLD: float = 0.85
```

---

## 📈 Performance

### Expected Metrics

- **FPS**: 25-30 (real-time)
- **Gesture Detection**: <5ms per frame
- **Classification**: <2ms per frame
- **State Machine**: <1ms per frame
- **Total Latency**: <10ms (perception threshold ~16ms)

### Minimum Action Interval

```
Dwell Time (1.5s) + Cooldown (0.5s) = 2.0s minimum
```

**Why intentional**:
- Prevents accidental double-triggers
- Allows users to rest between actions
- Ensures deliberate interaction

---

## 🧪 Testing Your Setup

### Test 1: Single Gesture

1. Show **fist** to camera
2. Hold steady
3. Watch progress bar fill
4. Action should trigger at 100%
5. **Goal**: ONE left click, then cooldown

---

### Test 2: Gesture Change

1. Show **fist**
2. Hold for 0.5 seconds (not full dwell)
3. Switch to **peace sign**
4. Hold peace sign for 1.5 seconds
5. **Goal**: Only peace sign (right click) triggers, NOT fist

---

### Test 3: Rapid Attempts

1. Show **fist** until action triggers
2. **Immediately** show fist again
3. **Goal**: Second attempt blocked by cooldown
4. Must wait for cooldown, then start new dwell cycle

---

## 📚 Additional Resources

- **[CONFLICT_FREE_DESIGN.md](CONFLICT_FREE_DESIGN.md)** - Full technical explanation
- **[TECHNICAL_DETAILS.md](TECHNICAL_DETAILS.md)** - Architecture deep-dive
- **[README.md](README.md)** - General documentation

---

## 🆘 Getting Help

### Debug Mode

Press `D` during runtime to see:
```
DEBUG INFO
state: candidate
current_gesture: fist
dwell_progress: 0.67
cooldown_progress: 1.0
buffer_fill: 1.0
action_count: 3
```

### Console Logging

Actions are logged as:
```
✓ [fist] → left_click
✓ [peace_sign] → right_click
✗ [thumbs_up] → scroll_up FAILED
```

---

**Enjoy conflict-free gesture control!** 🤲✨
