# AccessAble - Technical Architecture Document

## Overview

This document provides an in-depth technical explanation of how AccessAble derives gestures from hand landmarks and recognizes them with high reliability.

---

## 1. Hand Landmark Detection (MediaPipe)

### 1.1 Raw Input
MediaPipe Hands provides **21 3D landmarks** per detected hand:

```
Landmark Structure:
├── 0: Wrist (base reference point)
├── Thumb Chain (1-4)
│   ├── 1: CMC (Carpometacarpal)
│   ├── 2: MCP (Metacarpophalangeal)
│   ├── 3: IP (Interphalangeal)
│   └── 4: Tip
├── Index Finger (5-8)
│   ├── 5: MCP, 6: PIP, 7: DIP, 8: Tip
├── Middle Finger (9-12)
│   ├── 9: MCP, 10: PIP, 11: DIP, 12: Tip
├── Ring Finger (13-16)
│   ├── 13: MCP, 14: PIP, 15: DIP, 16: Tip
└── Pinky (17-20)
    ├── 17: MCP, 18: PIP, 19: DIP, 20: Tip
```

Each landmark `(x, y, z)`:
- `x, y`: Normalized to [0, 1] relative to image dimensions
- `z`: Depth relative to wrist (negative = closer to camera)

### 1.2 Challenge: Position Invariance

**Problem**: Raw landmark positions vary with:
- Hand size (child vs adult)
- Distance from camera
- Position in frame (left/right/up/down)

**Solution**: Extract **geometric features** that are invariant to these factors.

---

## 2. Feature Extraction (`GestureRecognizer.extract_features`)

### 2.1 Normalization Strategy

All measurements are normalized by **palm size** to create scale-invariant features:

```python
# Calculate palm size (reference scale)
wrist = landmarks[0]
middle_base = landmarks[9]
palm_size = distance(wrist, middle_base)

# Now all measurements are divided by palm_size
```

This makes the system work regardless of:
- How far the hand is from the camera
- Whether it's a small or large hand

### 2.2 Core Features

#### Feature 1: Finger Extension
**What it measures**: Is each finger extended (straight) or curled?

**Algorithm**:
```python
for each finger:
    tip_distance = distance(wrist, finger_tip)
    base_distance = distance(wrist, finger_base)
    
    # Normalize by palm size
    extension = (tip_distance - base_distance) / palm_size
    
    # Threshold
    is_extended = extension > 0.3
```

**Result**: Binary flags for each finger + total count
- `thumb_extended`: {0.0, 1.0}
- `index_extended`: {0.0, 1.0}
- `middle_extended`: {0.0, 1.0}
- `ring_extended`: {0.0, 1.0}
- `pinky_extended`: {0.0, 1.0}
- `fingers_extended`: {0.0, 1.0, 2.0, 3.0, 4.0, 5.0}

**Gestures distinguished**:
- Fist (0 extended) vs Open Palm (5 extended)
- Peace Sign (2 extended) vs Thumbs Up (1 extended)

#### Feature 2: Finger Curl
**What it measures**: Overall "openness" of the hand

**Algorithm**:
```python
# Inverse of extension for 4 main fingers (excluding thumb)
curl = average(1.0 - extension for each finger)
```

**Result**: Continuous value [0, 1]
- 0.0 = All fingers extended
- 1.0 = All fingers curled (fist)

**Use case**: Distinguishes tight fist from relaxed fist

#### Feature 3: Finger Spread
**What it measures**: How far apart the fingers are

**Algorithm**:
```python
# Distances between adjacent fingertips
spreads = [
    distance(index_tip, middle_tip),
    distance(middle_tip, ring_tip),
    distance(ring_tip, pinky_tip)
]

# Normalize and average
finger_spread = average(spreads) / palm_size
```

**Result**: Continuous value ~[0, 1]
- Low value = Fingers together (pointing)
- High value = Fingers spread (open palm, stop sign)

**Gestures distinguished**:
- Open Palm (spread) vs Pointing (not spread)

#### Feature 4: Thumb Angle
**What it measures**: Thumb orientation relative to palm

**Algorithm**:
```python
# Palm direction vector
palm_vector = normalize(middle_base - wrist)

# Thumb direction vector
thumb_vector = normalize(thumb_tip - thumb_base)

# Dot product = cosine of angle
thumb_angle = dot(palm_vector, thumb_vector)
```

**Result**: Continuous value [-1, 1]
- `+1.0` = Thumb pointing same direction as palm (thumbs up)
- `-1.0` = Thumb pointing opposite direction (thumbs down)
- `0.0` = Thumb perpendicular to palm

**Gestures distinguished**:
- Thumbs Up (+0.9) vs Thumbs Down (-0.9) vs Side Thumb (0.0)

---

## 3. Gesture Matching (`compute_similarity`)

### 3.1 Similarity Metric

Given:
- `current_features`: Features extracted from current hand
- `gesture.features`: Features defining a known gesture

**Algorithm**: Normalized Euclidean distance with exponential decay

```python
# Only compare common features
common = set(current_features) & set(gesture.features)

# Calculate squared differences
distances = [
    (current_features[f] - gesture.features[f])**2
    for f in common
]

# Root mean square distance
distance = sqrt(mean(distances))

# Convert to similarity score
similarity = exp(-distance * 3.0)
```

**Interpretation**:
- `similarity = 1.0` → Perfect match (distance = 0)
- `similarity = 0.5` → Moderate match
- `similarity < 0.3` → Poor match

**Why exponential decay?**
- Emphasizes close matches over near-misses
- Smooth falloff for UI confidence display
- Tunable via scale factor (3.0)

### 3.2 Example: Fist Detection

**Fist gesture features**:
```python
{
    'fingers_extended': 0.0,
    'finger_curl': 0.9,
    'thumb_angle': 0.2
}
```

**Test Case 1: Perfect Fist**
```python
current = {
    'fingers_extended': 0.0,
    'finger_curl': 0.9,
    'thumb_angle': 0.2
}
distance = sqrt(0 + 0 + 0) = 0.0
similarity = exp(0) = 1.0  ✓ MATCH
```

**Test Case 2: Peace Sign (should NOT match)**
```python
current = {
    'fingers_extended': 2.0,
    'finger_curl': 0.3,
    'thumb_angle': 0.1
}
distance = sqrt((2-0)² + (0.3-0.9)² + (0.1-0.2)²)
        = sqrt(4 + 0.36 + 0.01) = 2.09
similarity = exp(-2.09 * 3) = 0.002  ✗ NO MATCH
```

---

## 4. Stabilization System

### 4.1 Multi-Stage Filtering

**Stage 1: Confidence Threshold**
```python
if similarity < 0.75:
    reject  # Not confident enough
```

**Stage 2: Temporal Consistency**
```python
# Ring buffer of last 5 detections
history = ["fist", "fist", "peace", "fist", "fist"]

# Most common gesture
counts = Counter(history)
most_common, count = counts.most_common(1)[0]

# Require 60% consistency
if count >= 3:  # 3 out of 5
    gesture = most_common  # Stable
```

**Stage 3: Dwell Time**
```python
if gesture == current_gesture:
    elapsed = time.time() - gesture_start_time
    
    if elapsed >= 1.5:  # Default dwell time
        TRIGGER ACTION
```

**Stage 4: Debounce**
```python
time_since_last = time.time() - last_activation_time

if time_since_last < 0.5:  # Cooldown period
    ignore  # Prevent double-triggering
```

### 4.2 Why This Works for Tremors

**Problem**: Hand tremors cause rapid feature changes

**Solution**: Multi-frame voting system

Example with tremor:
```
Frame:    1    2    3    4    5    6    7
Gesture:  fist fist open fist fist fist open
                 ^               ^
                tremor          tremor

History Buffer (last 5):
[fist, fist, open, fist, fist]

Vote: fist=4, open=1  → Output: fist ✓
```

The system "filters out" occasional tremor frames by requiring consistency.

---

## 5. Dwell-Based Activation

### 5.1 Rationale

**Why not instant activation?**
- Prevents accidental triggers during transitions
- Gives users time to cancel unintended gestures
- Reduces cognitive load (deliberate actions only)

### 5.2 Implementation

```python
class GestureRecognizer:
    def recognize(self, landmarks, current_time):
        # ... feature extraction and matching ...
        
        if gesture != previous_gesture:
            # New gesture - start timer
            gesture_start_time = current_time
            should_activate = False
        else:
            # Same gesture - check dwell
            elapsed = current_time - gesture_start_time
            
            if elapsed >= DWELL_TIME:
                should_activate = True
        
        return gesture, confidence, should_activate
```

### 5.3 Visual Feedback Loop

```
User shows gesture
       ↓
UI shows progress bar (0%)
       ↓
User holds steady
       ↓
Progress bar fills (50%)
       ↓
User maintains pose
       ↓
Progress bar complete (100%)
       ↓
ACTION TRIGGERED
       ↓
Visual confirmation
```

This creates a **predictable feedback loop** essential for accessibility.

---

## 6. Performance Optimizations

### 6.1 Frame Rate Targets

**Goal**: 30 FPS (~33ms per frame)

**Budget Breakdown**:
```
Camera capture:         ~5ms
MediaPipe detection:    ~15ms
Feature extraction:     ~2ms
Gesture matching:       ~1ms
UI rendering:           ~8ms
----------------------------------
Total:                  ~31ms ✓
```

### 6.2 Efficiency Techniques

**1. Single Hand Only**
```python
max_num_hands=1  # Skip multi-hand processing
```

**2. Video Stream Mode**
```python
static_image_mode=False  # Enables tracking optimization
```

**3. NumPy Vectorization**
```python
# Vectorized distance calculation
distances = np.linalg.norm(tips - bases, axis=1)
# vs loop
for tip, base in zip(tips, bases):
    distance = sqrt((tip[0]-base[0])**2 + ...)
```

**4. Feature Caching**
- Gesture library features computed once at load
- Only current frame features recomputed each iteration

---

## 7. Customization Architecture

### 7.1 Gesture Recording Pipeline

```python
# 1. User triggers recording mode
recorder.start_recording("my_gesture")

# 2. System captures samples over 2 seconds
for _ in range(30):  # 30 frames
    features = extract_features(current_hand)
    recorder.add_sample(features)

# 3. System averages features (robust to noise)
averaged_features = {
    'fingers_extended': median([0, 1, 0, 0, 1, ...]),
    'finger_curl': median([0.8, 0.9, 0.7, ...]),
    # ...
}

# 4. Create and save gesture
gesture = Gesture("my_gesture", averaged_features)
library.add_gesture(gesture)
library.save_to_file()
```

**Why median instead of mean?**
- Outlier resistance (few bad frames don't corrupt gesture)
- Better handles discrete features (e.g., finger counts)

### 7.2 Action Mapping

**Abstraction Layer**:
```
Gesture → [Mapping] → Action
```

Example:
```python
# User can remap without changing code
settings.map_gesture_to_action('fist', 'scroll_down')
settings.map_gesture_to_action('peace_sign', 'browser_back')
```

**Stored in JSON**:
```json
{
    "fist": "scroll_down",
    "peace_sign": "browser_back"
}
```

This allows:
- Per-user customization
- A/B testing different mappings
- Quick reconfiguration without code changes

---

## 8. Error Handling & Edge Cases

### 8.1 No Hand Detected

```python
if hand_landmarks is None:
    # Reset state to prevent stale activations
    gesture_recognizer.reset()
    # Show "No hand detected" in UI
```

### 8.2 Low Confidence

```python
if confidence < threshold:
    # Continue tracking but don't activate
    # Useful for ambiguous hand positions
```

### 8.3 Camera Failure

```python
success, frame = camera.read_frame()
if not success:
    log_warning()
    continue  # Skip this frame, try next
```

### 8.4 PyAutoGUI Safeguards

```python
pyautogui.FAILSAFE = True  
# Moving mouse to corner aborts all operations
```

---

## 9. Accessibility Considerations

### 9.1 Low Physical Effort

✅ **Single hand only** - no coordination required  
✅ **Stateless gestures** - no complex sequences  
✅ **Dwell activation** - no rapid movements needed  
✅ **Tremor compensation** - stabilization filters noise

### 9.2 Customization for Individual Needs

**User A** (severe tremor):
```python
STABILIZATION_WINDOW = 10  # More frames
DWELL_TIME = 2.5  # Longer hold time
CONFIDENCE_THRESHOLD = 0.65  # More lenient
```

**User B** (good control, wants speed):
```python
STABILIZATION_WINDOW = 3  # Fewer frames
DWELL_TIME = 0.8  # Shorter hold time
CONFIDENCE_THRESHOLD = 0.85  # More strict
```

### 9.3 Visual Feedback

**Why critical?**
- Users need to know system state
- Predictable behavior builds trust
- Clear progress indication ("Am I doing this right?")

**What's shown**:
- Detected gesture name
- Action that will trigger
- Dwell progress bar (0-100%)
- FPS (performance indicator)

---

## 10. Future Improvements

### 10.1 Machine Learning Enhancements

**Current**: Hand-crafted features (geometric)  
**Future**: Learned features via neural network

Benefits:
- Adapt to individual hand anatomy
- Discover optimal features automatically
- Handle more complex gestures

### 10.2 Multi-Modal Input

**Combine with**:
- Eye tracking (cursor positioning)
- Voice commands (gesture + speech)
- Head pose (additional control channel)

### 10.3 Adaptive Thresholds

```python
# Learn user's typical confidence scores
user_history = [0.82, 0.85, 0.79, ...]
adaptive_threshold = percentile(user_history, 25)
```

---

## Conclusion

AccessAble achieves reliable gesture recognition through:

1. **Position-invariant features** → Works regardless of hand placement
2. **Multi-stage stabilization** → Filters tremors and noise
3. **Dwell-based activation** → Prevents accidental triggers
4. **Clear separation of concerns** → Gesture ≠ Action
5. **Strong visual feedback** → Predictable user experience

The system prioritizes **accessibility over novelty**, ensuring users with partial motor impairments can navigate the web with minimal physical effort and maximum reliability.
