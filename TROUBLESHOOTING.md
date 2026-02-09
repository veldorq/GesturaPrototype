"""
TROUBLESHOOTING GUIDE - Gesture System Not Responding
======================================================
Date: February 9, 2026

PROBLEMS FIXED:
===============
✅ "does not support assignment" error - FIXED (protobuf landmark assignment)
✅ TensorFlow protobuf compatibility - FIXED (protobuf 6.33.5 installed)
✅ CNN disabled by default - CHANGED (no trained model yet)

CURRENT STATUS:
===============
✓ TensorFlow: Working (2.20.0)
✓ MediaPipe: Working (0.10.9)  
✓ CNN Recognition: DISABLED (enable after training model)
✓ Rule-based Recognition: ACTIVE
✓ Smoothing Pipeline: ACTIVE

WHY GESTURES MIGHT NOT BE DETECTED:
====================================

1. GESTURE CONFIRMATION DELAY (Most Common)
   ------------------------------------------
   The system requires you to HOLD each gesture for ~166ms (5 frames)
   before it executes the action. This is a SAFETY FEATURE to prevent
   accidental triggers.
   
   ✅ SOLUTION: Hold gestures steadily for at least 0.2 seconds
   
   Example:
   - Open palm → HOLD → wait 0.2s → scroll down executes
   - Closed fist → HOLD → wait 0.2s → scroll up executes

2. COOLDOWN PERIOD
   ------------------------------------------
   After each action, there's a 0.6 second cooldown where NEW gestures
   are ignored. This prevents rapid-fire accidental actions.
   
   ✅ SOLUTION: Wait about 1 second between gestures

3. HAND NOT DETECTED
   ------------------------------------------
   MediaPipe might not be detecting your hand due to:
   - Poor lighting
   - Hand too close/far from camera
   - Cluttered background
   - Camera blocked
   
   ✅ SOLUTION: Run the diagnostic test (see below)

4. CAMERA PERMISSION OR ACCESS ISSUES
   ------------------------------------------
   Another application might be using your camera
   
   ✅ SOLUTION: Close other camera apps (Zoom, Skype, etc.)

DIAGNOSTIC STEPS:
=================

STEP 1: Test Camera and Hand Detection
---------------------------------------
Run this test script:

    python test_gesture_detection.py

This will show you:
- If camera is working
- If hand is detected
- How many fingers are extended
- Real-time gesture feedback

Expected result:
- You should see "Hand detected! Fingers extended: X"
- Green overlay on your hand
- gestures detected when you change finger positions

STEP 2: Run Main System with Debug Output
------------------------------------------
Run the main system:

    python PROTOTYPE.PY

Watch the console output:
- Should say "[INFO] CNN recognition disabled - using rule-based recognition"
- Should NOT say "TensorFlow not available"
- Should show FPS counter in video window

STEP 3: Test Individual Gestures
---------------------------------
Try each gesture one at a time, HOLD for 1 full second:

1. OPEN PALM (all 5 fingers extended)
   → Should scroll DOWN after ~0.2s
   
2. CLOSED FIST (all fingers folded)
   → Should scroll UP after ~0.2s
   
3. INDEX FINGER ONLY (1 finger)
   → Should move mouse cursor
   
4. PEACE SIGN (index + middle fingers)
   → Should LEFT CLICK after ~0.2s

IMPORTANT: You must HOLD each gesture steady!

KEYBOARD CONTROLS WHILE RUNNING:
=================================
q - Quit
s - Show statistics
h - Toggle advanced UI
c - Toggle CNN mode (currently disabled)
b - Launch browser

COMMON MISTAKES:
================

❌ Moving gesture too quickly
   ✅ Hold gesture steady for at least 0.3 seconds

❌ Trying gestures too fast (< 1 second apart)
   ✅ Wait  full second between gestures

❌ Hand partially out of frame
   ✅ Keep entire hand visible in camera

❌ Poor lighting
   ✅ Face a window or turn on lights

❌ Expecting instant response
   ✅ System has deliberate delay for safety

SYSTEM CONFIGURATION:
=====================

Current settings (in PROTOTYPE.PY Config class):

GESTURE_BUFFER_SIZE = 5              # Frames needed to confirm (166ms @ 30fps)
DEBOUNCE_TIME = 0.5                  # Seconds between repeated actions
CANDIDATE_CONFIRMATION_FRAMES = 5    # State machine confirmation frames
COOLDOWN_DURATION = 0.6              # Seconds after action before new gesture

These are INTENTIONALLY conservative for accessibility and safety.

IF STILL NO GESTURES DETECTED:
===============================

1. Check Python environment:
   
   python -c "import cv2, mediapipe, pyautogui; print('All imports OK')"

2. Verify camera index (might not be 0):
   
   In PROTOTYPE.PY, try changing:
   CAMERA_INDEX = 0  →  CAMERA_INDEX = 1

3. Check for errors in console output

4. Try reducing confirmation frames (less safe, faster response):
   
   In PROTOTYPE.PY, change:
   CANDIDATE_CONFIRMATION_FRAMES = 5  →  CANDIDATE_CONFIRMATION_FRAMES = 3

EXPECTED BEHAVIOR:
==================

When system is working correctly:

1. Window opens showing camera feed
2. Green skeleton overlaid on detected hand
3. FPS counter in top-left (~25-30 FPS)
4. Gesture name displayed when recognized
5. Buffer counter shows how many frames detected
6. Actions execute after brief hold (~0.2s)
7. Console shows no errors

CNN WARNINGS (IGNORE THESE - NORMAL):
======================================

✓ "INFO: CNN recognition disabled - using rule-based recognition"
   → This is EXPECTED - CNN is disabled because no model is trained

✓ "WARNING: CNN model loading failed - falling back to rule-based"
   → This is EXPECTED if you try to enable CNN without a trained model

✓ "AttributeError: 'MessageFactory' object has no attribute 'GetPrototype'"
   → This is a harmless protobuf/MediaPipe compatibility warning

TRAINING CNN MODEL (OPTIONAL):
===============================

If you want to enable CNN recognition:

1. Collect gesture dataset:
   python collect_gesture_dataset.py

2. Train model:
   python train_gesture_model.py

3. Enable CNN in PROTOTYPE.PY:
   ENABLE_CNN_CLASSIFIER = True

STILL HAVING ISSUES?
====================

Run the diagnostic and share the output:

1. python test_gesture_detection.py
   - Shows hand detection status
   
2. python PROTOTYPE.PY
   - Check console for error messages
   - Test if window opens
   - Test if hand is detected (green overlay)

Issue checklist:
☐ Camera opens?
☐ Hand detected (green skeleton)?
☐ Holding gesture for 0.3+ seconds?
☐ Waiting 1 second between gestures?
☐ Good lighting?
☐ No console errors?

"""