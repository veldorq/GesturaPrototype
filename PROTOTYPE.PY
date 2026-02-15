"""
Real-Time Hand Gesture Control System for Web Browsers
========================================================
Author: Expert Python CV Engineer
Date: February 8, 2026
Platform: Windows
Python: 3.10+

Description:
    This system enables touchless browser control using hand gestures detected
    via webcam. Uses MediaPipe for hand tracking and PyAutoGUI for browser automation.

Gestures Supported:
    - Open Palm → Scroll Down
    - Closed Fist → Scroll Up
    - Index Finger Only → Mouse Move
    - Index + Middle Finger → Left Click
    - Thumb Up → Right Click
    - Swipe Left → Browser Back
    - Swipe Right → Browser Forward

INSTALLATION:
    pip install opencv-python mediapipe pyautogui numpy

USAGE:
    python test.py
    Press 'q' to quit safely
"""

import cv2
import mediapipe as mp
import pyautogui
import time
import subprocess
import platform
import math
from collections import deque
from enum import Enum

# CNN Gesture Recognition (optional import - graceful degradation if not available)
try:
    from gesture_model_inference import CNNGestureClassifier
    CNN_AVAILABLE = True
except ImportError:
    CNN_AVAILABLE = False
    print("Warning: CNN gesture recognition module not found. Using rule-based recognition only.")

# Smoothing pipeline for stability improvements (optional, graceful degradation)
try:
    from smoothing_pipeline import GestureSmoothingPipeline  # type: ignore
    SMOOTHING_AVAILABLE = True
except ImportError:
    SMOOTHING_AVAILABLE = False
    GestureSmoothingPipeline = None  # type: ignore
    print("WARNING: Smoothing pipeline not available - install filterpy/scipy for better stability")
    print("   pip install filterpy scipy")


# ============================================================================
# CONFIGURATION & CONSTANTS
# ============================================================================

class Config:
    """System configuration parameters"""
    # Video settings
    CAMERA_INDEX = 0
    FRAME_WIDTH = 1280
    FRAME_HEIGHT = 720
    FPS_TARGET = 30
    
    # Screen settings
    SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
    
    # Hand detection settings
    MIN_DETECTION_CONFIDENCE = 0.7
    MIN_TRACKING_CONFIDENCE = 0.7
    MAX_NUM_HANDS = 1
    
    # Gesture stabilization - HACKATHON STABLE (prioritize reliability over speed)
    GESTURE_BUFFER_SIZE = 5  # Frames to buffer - STABLE (was 3, too fast for clean demo)
    DEBOUNCE_TIME = 0.4  # Seconds between repeated actions - STABLE (prevents accidental double-trigger)
    CONFIDENCE_THRESHOLD = 0.6  # Minimum confidence - STABLE (reduces false positives)
    
    # Movement settings - ULTRA SMOOTH pointer control
    MOUSE_SMOOTHING = 0.35  # 0=instant, 1=no movement (increased for silky smooth tracking)
    MOUSE_ACCELERATION = 1.5  # Speed multiplier for large movements (gentler acceleration)
    MOUSE_DEAD_ZONE = 0.004  # Ignore movements smaller than this (reduced jitter)
    MOUSE_EDGE_PADDING = 50  # Pixels from edge where movement slows down
    
    # POINTER SMOOTHNESS: Advanced filtering
    POINTER_VELOCITY_BUFFER = 3  # Frames to average velocity (smoother transitions)
    POINTER_INTERPOLATION_STEPS = 2  # Sub-steps for ultra-smooth movement
    POINTER_MIN_MOVEMENT = 2  # Minimum pixels to move (prevents micro-stuttering)
    
    # POINTER PRECISION: Dual-zone sensitivity for fine control
    POINTER_PRECISION_MODE = True  # Enable center-area precision zone
    POINTER_PRECISION_ZONE = 0.3  # Center 30% of screen = precision zone (0.0-1.0)
    POINTER_PRECISION_MULTIPLIER = 0.5  # In precision zone, movements are 50% slower for accuracy
    POINTER_EDGE_BOOST = 1.3  # Boost speed near edges to reach corners easily
    
    # SCROLL: Configurable sensitivity (3 levels)
    SCROLL_SENSITIVITY = "high"  # Options: "low" (gentle), "medium" (balanced), "high" (fast)
    # Scroll profiles (amount, smoothness, delay)
    SCROLL_PROFILES = {
        "low": {"base": 15, "multiplier": 2.0, "steps": 4, "delay": 0.015},     # Gentle, very smooth
        "medium": {"base": 20, "multiplier": 2.5, "steps": 3, "delay": 0.012}, # Balanced (default)
        "high": {"base": 30, "multiplier": 3.0, "steps": 2, "delay": 0.008}    # Fast, responsive
    }
    SCROLL_BASE_AMOUNT = SCROLL_PROFILES[SCROLL_SENSITIVITY]["base"]
    SCROLL_SPEED_MULTIPLIER = SCROLL_PROFILES[SCROLL_SENSITIVITY]["multiplier"]
    SCROLL_SMOOTH_STEPS = SCROLL_PROFILES[SCROLL_SENSITIVITY]["steps"]
    SCROLL_STEP_DELAY = SCROLL_PROFILES[SCROLL_SENSITIVITY]["delay"]
    SCROLL_DWELL_TIME = 0.4  # STABLE - hold gesture 0.4s before scrolling
    SCROLL_CONTINUOUS_DELAY = 0.3  # STABLE - 0.3s between scroll actions
    
    # SWIPE: Clear intentional movements only (browser navigation safety)
    SWIPE_THRESHOLD = 0.12  # Minimum movement - DELIBERATE (prevents drift detection)
    SWIPE_VERTICAL_THRESHOLD = 0.12  # For up/down swipes - CONSISTENT
    SWIPE_DIRECTION_DOMINANCE_RATIO = 2.0  # Required ratio - STRICT (swipe must be clearly directional)
    SWIPE_CONFIRMATION_FRAMES = 4  # Frames needed - STABLE (prevents single-frame glitches)
    SWIPE_VELOCITY_MIN = 0.05  # Minimum velocity - MODERATE (intentional swipe, not drift)
    
    # BROWSER NAVIGATION: High-stakes action (back/forward affects user state)
    BROWSER_NAV_DWELL_TIME = 0.5  # DELIBERATE - hold 0.5s (prevents accidental navigation)
    BROWSER_NAV_COOLDOWN = 0.8  # SAFE - 0.8s cooldown between nav actions
    
    # CLOSE BROWSER: CRITICAL action - requires longer dwell time
    CLOSE_BROWSER_DWELL_TIME = 1.5  # VERY DELIBERATE - hold 1.5s (prevents accidental close)
    CLOSE_BROWSER_COOLDOWN = 2.0  # EXTRA SAFE - 2s cooldown
    
    # Distance-based gestures
    ENABLE_ZOOM_GESTURES = False  # DISABLED BY DEFAULT - too easy to trigger accidentally
    PINCH_THRESHOLD = 0.04  # Max distance for pinch (VERY CLOSE - strict)
    SPREAD_THRESHOLD = 0.20  # Min distance for spread (VERY WIDE - much stricter than before)
    PINCH_DISTANCE_THRESHOLD = 0.08  # Threshold for pinch verification
    
    # Finger extension detection - STRICT (correctness over sensitivity)
    FINGER_EXTENSION_THRESHOLD = 0.020  # Y-axis threshold (STRICT - clear extension required)
    FINGER_CURL_THRESHOLD = 0.015  # Threshold for detecting curled fingers (strict)
    
    # REFINEMENT #4: Pinch zoom - smooth and isolated
    ZOOM_SMOOTH_STEPS = 2  # Number of incremental zoom steps for smoothness
    ZOOM_STEP_DELAY = 0.02  # Delay between zoom steps (creates smooth animation)
    ZOOM_GESTURE_ISOLATION = True  # Disable other gestures during active zoom
    ZOOM_COOLDOWN = 0.3  # Cooldown after zoom completes
    
    # ISSUE #2 FIX: Mode separation to prevent zoom/pointer interference
    ENABLE_MODE_SEPARATION = True  # Separate POINTER_MODE from GESTURE_MODE
    MODE_SWITCH_DEBOUNCE = 1.0  # Seconds before allowing mode switch
    DISABLE_ZOOM_IN_POINTER_MODE = True  # Disable pinch/spread when pointer active
    
    # ISSUE #5 FIX: Thumb interference prevention
    THUMB_IGNORED_MODE = True  # Exclude thumb from most gesture detection (accessibility feature)
    THUMB_EXPLICIT_GESTURES_ONLY = True  # Only detect thumb in gestures that explicitly require it
    
    # ISSUE #2 FIX: Pointer coordinate mapping
    POINTER_INVERT_X = False  # Set to False for natural left/right movement (was causing inverted feeling)
    POINTER_INVERT_Y = False  # Set to False for natural up/down movement
    
    # CLOSE TAB: REMOVED - too risky for hackathon demo (choose MUTE instead)
    # Accidentally closing tabs during demo = bad UX. Gestura favors MUTE for accessibility.
    CLOSE_TAB_ENABLED = False  # DISABLED - use MUTE as the destructive action alternative
    CLOSE_TAB_DWELL_TIME = 0.5  # (legacy)
    CLOSE_TAB_COOLDOWN = 0.8  # (legacy)
    CLOSE_TAB_REQUIRE_STABILITY = True  # (legacy)
    
    # MUTE TOGGLE: Key accessibility feature (replaces close tab)
    MUTE_TOGGLE_DWELL_TIME = 0.4  # STABLE - intentional hold (prevents accidental mute)
    MUTE_TOGGLE_COOLDOWN = 0.6  # STABLE - prevents rapid toggle spam
    
    # REFINEMENT #6: Browser launch keyboard shortcut
    BROWSER_LAUNCH_KEY = 'ctrl+shift+b'  # Configurable keyboard shortcut
    BROWSER_LAUNCH_TARGET = 'chrome'  # Options: 'chrome', 'edge', 'firefox', 'default'
    BROWSER_LAUNCH_ENABLED = True  # Enable/disable keyboard shortcut feature
    
    # DEBUG MODE: Enable detailed gesture detection logging
    DEBUG_GESTURE_DETECTION = False  # Print what gestures are being detected
    
    # ========================================================================
    # CNN GESTURE RECOGNITION (DataFlair-based integration)
    # ========================================================================
    
    # CNN Model Configuration
    ENABLE_CNN_CLASSIFIER = False  # DISABLED BY DEFAULT - Enable after training model
    CNN_MODEL_PATH = "models/gesture_cnn_model.h5"
    CNN_LABEL_ENCODER_PATH = "models/label_encoder.pkl"
    
    # CNN Confidence Thresholding (CRITICAL for anti-glitch)
    CNN_MIN_CONFIDENCE = 0.75  # Ignore CNN predictions below 75% confidence
    CNN_HIGH_CONFIDENCE = 0.85  # Strong confidence for immediate acceptance
    
    # CNN Temporal Voting (CRITICAL for stability)
    CNN_VOTING_WINDOW = 5  # Last 5 frames must agree
    CNN_VOTING_CONSISTENCY = 0.8  # 80% of frames must show same gesture
    
    # Hybrid System Configuration
    # CNN handles: scroll_up, scroll_down, swipe_left, swipe_right, pinch_zoom, thumb_down_close, mute_toggle
    # MediaPipe handles: pointer movement (INDEX_ONLY), pinch distance measurement
    USE_HYBRID_MODE = True  # Use CNN + MediaPipe hybrid (recommended)
    
    # CNN Integration Safety (NON-NEGOTIABLE)
    CNN_MUST_PASS_THROUGH_STATE_MACHINE = True  # CNN output NEVER directly triggers actions
    CNN_CONFIDENCE_FILTER_REQUIRED = True  # Must filter low-confidence predictions
    CNN_TEMPORAL_VOTING_REQUIRED = True  # Must require frame consistency
    
    # Advanced features
    ENABLE_SOUND_FEEDBACK = False  # Audio confirmation
    ENABLE_GESTURE_HISTORY = True  # Log gestures
    ENABLE_LEARNING_MODE = True    # Adaptive thresholds
    ENABLE_VISUAL_TRAILS = True    # Show hand trails
    
    # Mutable UI setting (not frozen)
    @staticmethod
    def toggle_advanced_ui():
        """Toggle advanced UI display"""
        Config._SHOW_ADVANCED_UI = not getattr(Config, '_SHOW_ADVANCED_UI', True)
    
    @staticmethod
    def is_advanced_ui_enabled():
        """Check if advanced UI is enabled"""
        return getattr(Config, '_SHOW_ADVANCED_UI', True)
    
    _SHOW_ADVANCED_UI = True  # Internal mutable state
    
    # Performance
    HISTORY_SIZE = 100  # Gesture history buffer
    AUTOSAVE_INTERVAL = 60  # Seconds between stats save
    
    # Safety
    PYAUTOGUI_FAILSAFE = True


class GestureType(Enum):
    """Enumeration of all recognized gestures - HACKATHON SIMPLIFIED (9 core gestures)"""
    NONE = 0
    
    # === ESSENTIAL BROWSER GESTURES (9 total) ===
    # Scrolling (2 gestures)
    OPEN_PALM = 1        # Scroll down - all 5 fingers spread
    CLOSED_FIST = 2      # Scroll up - all fingers folded
    
    # Pointing & Clicking (2 gestures)
    INDEX_ONLY = 3       # Mouse move - pointer mode
    PEACE_SIGN = 11      # Left click - index + middle extended
    
    # Navigation (2 gestures)
    SWIPE_LEFT = 6       # Browser back
    SWIPE_RIGHT = 7      # Browser forward
    
    # Zoom (1 gesture - simple)
    THUMB_UP = 5         # Zoom in (thumb-up gesture)
    
    # Page Actions (1 gesture)
    FOUR_FINGERS = 9     # Refresh page - 4 fingers without thumb
    
    # Click gesture (1 gesture)
    THREE_FINGERS = 8    # Left click - index, middle, ring extended
    
    # Accessibility (1 gesture)
    PINKY_ONLY = 10      # Mute toggle (pinky extended)
    
    # System Control (2 gestures)
    ROCK_SIGN = 12       # Exit program - index + pinky extended (rock on) - HOLD 1.5s
    CALL_ME = 14         # Close browser - thumb + pinky ONLY (call me gesture) - HOLD 1.5s
    
    # Clipboard (1 gesture)
    OKAY_SIGN = 13       # Paste - thumb + index circle, others extended
    
    # === REMOVED/DISABLED GESTURES (not demo-ready) ===
    # These caused conflicts, instability, or were too risky for hackathon:
    # - THUMB_DOWN / Close tab: Too risky (accidental tab closure)
    # - FOUR_FINGERS / Refresh: Conflicts with OPEN_PALM
    # - THREE_FINGERS / Screenshot: Not essential browser action
    # - PINCH/SPREAD: Disabled by default, conflicts with other poses
    # - SWIPE_UP/DOWN: Conflicts with vertical hand movement
    # - OK_SIGN, ROCK_SIGN, CALL_SIGN: Experimental, not essential
    # - INDEX_MIDDLE: Reserved, never implemented


# ============================================================================
# GESTURE STATE MACHINE (CRITICAL FOR STABILITY)
# ============================================================================

class GestureState(Enum):
    """Gesture lifecycle states for anti-glitch enforcement"""
    NONE = 0        # No gesture detected
    CANDIDATE = 1   # Gesture detected but not confirmed
    CONFIRMED = 2   # Gesture confirmed and ready for action
    COOLDOWN = 3    # Action executed, blocking new gestures


class GestureStateMachine:
    """
    Enforces strict state transitions: NONE → CANDIDATE → CONFIRMED → COOLDOWN → NONE
    
    Purpose:
        - Prevents single-frame glitches from triggering actions
        - Enforces temporal confirmation before execution
        - Blocks mid-action gesture switching
        - Ensures one gesture → one intent → one action
    
    DataFlair Pattern:
        - CANDIDATE requires N consecutive detections
        - CONFIRMED requires confidence + stability
        - COOLDOWN prevents rapid re-triggering
    """
    
    def __init__(self):
        """Initialize state machine"""
        self.state = GestureState.NONE
        self.current_gesture = GestureType.NONE
        self.candidate_gesture = GestureType.NONE
        self.candidate_start_time = 0.0
        self.candidate_frame_count = 0
        self.confirmed_start_time = 0.0
        self.cooldown_start_time = 0.0
        
        # Tuning parameters - HACKATHON STABLE (one gesture → one intent → one action)
        self.CANDIDATE_CONFIRMATION_FRAMES = 5  # STABLE - 5 frames @ 30fps = 167ms (prevents flicker)
        self.CANDIDATE_TIMEOUT = 1.5  # GENEROUS - allows natural gesture formation
        self.COOLDOWN_DURATION = 0.4  # STABLE - clear separation between gestures
        
        # DWELL TIMES: Gestures require holding after confirmation (prevents false triggers)
        # HACKATHON PRINCIPLE: Calm, predictable gestures > frantic responsiveness
        self.DWELL_GESTURES = {
            GestureType.OPEN_PALM: 0.4,      # Scroll down - STABLE hold
            GestureType.CLOSED_FIST: 0.4,    # Scroll up - STABLE hold
            GestureType.PINKY_ONLY: 0.4,     # Mute toggle - STABLE (key accessibility feature)
            GestureType.SWIPE_LEFT: 0.5,     # Browser back - DELIBERATE (high-stakes navigation)
            GestureType.SWIPE_RIGHT: 0.5,    # Browser forward - DELIBERATE
        }
        
        # FIX #1: Continuous gestures that don't need confirmation
        self.CONTINUOUS_GESTURES = {GestureType.INDEX_ONLY}  # Pointer mode
        
        # Track if action was executed this confirmation cycle
        self.action_executed_this_cycle = False
    
    def update(self, detected_gesture, current_time):
        """
        Update state machine with new gesture detection.
        
        FIX #1: Consolidated timing logic - handles both frame confirmation AND dwell time.
        Now returns (should_execute, stable_gesture, is_first_confirmation) tuple.
        
        Args:
            detected_gesture: GestureType from recognizer
            current_time: Current timestamp
        
        Returns:
            tuple: (should_execute, stable_gesture, is_first_confirmation)
                  is_first_confirmation: True on first frame of CONFIRMED state
        """
        # State: NONE - waiting for gesture
        if self.state == GestureState.NONE:
            if detected_gesture != GestureType.NONE:
                # FIX #1: Skip confirmation for continuous gestures (INDEX_ONLY)
                if detected_gesture in self.CONTINUOUS_GESTURES:
                    self.state = GestureState.CONFIRMED
                    self.current_gesture = detected_gesture
                    self.confirmed_start_time = current_time
                    self.action_executed_this_cycle = False
                    return True, self.current_gesture, True  # Execute immediately
                
                # Transition NONE → CANDIDATE
                self.state = GestureState.CANDIDATE
                self.candidate_gesture = detected_gesture
                self.candidate_start_time = current_time
                self.candidate_frame_count = 1
            return False, GestureType.NONE, False
        
        # State: CANDIDATE - accumulating confirmation
        elif self.state == GestureState.CANDIDATE:
            # Check timeout
            if current_time - self.candidate_start_time > self.CANDIDATE_TIMEOUT:
                self.reset()
                return False, GestureType.NONE, False
            
            # Check consistency
            if detected_gesture == self.candidate_gesture:
                self.candidate_frame_count += 1
                
                # Check if confirmed
                if self.candidate_frame_count >= self.CANDIDATE_CONFIRMATION_FRAMES:
                    # Transition CANDIDATE → CONFIRMED
                    self.state = GestureState.CONFIRMED
                    self.current_gesture = self.candidate_gesture
                    self.confirmed_start_time = current_time
                    self.action_executed_this_cycle = False
                    
                    # FIX #1: Check if dwell required
                    if self.current_gesture in self.DWELL_GESTURES:
                        # Dwell-based: stay in CONFIRMED, execute after dwell time
                        return False, self.current_gesture, True  # is_first_confirmation=True
                    else:
                        # Instant action: execute immediately
                        return True, self.current_gesture, True  # Execute now
            else:
                # Gesture changed - reset
                self.reset()
            
            return False, GestureType.NONE, False
        
        # State: CONFIRMED - holding gesture (for dwell-based actions)
        elif self.state == GestureState.CONFIRMED:
            # FIX #1: Check if gesture still maintained
            if detected_gesture != self.current_gesture:
                # Gesture changed while in CONFIRMED - reset
                self.reset()
                return False, GestureType.NONE, False
            
            # FIX #1: For dwell-based gestures, check if dwell time elapsed
            if self.current_gesture in self.DWELL_GESTURES:
                dwell_required = self.DWELL_GESTURES[self.current_gesture]
                if not self.action_executed_this_cycle and (current_time - self.confirmed_start_time >= dwell_required):
                    self.action_executed_this_cycle = True
                    return True, self.current_gesture, False  # Execute action
            
            # FIX #1: For continuous gestures (INDEX_ONLY), keep executing
            if self.current_gesture in self.CONTINUOUS_GESTURES:
                return True, self.current_gesture, False  # Continuous execution
            
            return False, self.current_gesture, False
        
        # State: COOLDOWN - blocking new gestures
        elif self.state == GestureState.COOLDOWN:
            if current_time - self.cooldown_start_time >= self.COOLDOWN_DURATION:
                # Transition COOLDOWN → NONE
                self.reset()
            return False, GestureType.NONE, False
        
        # Safety fallback: Should never reach here, but ensures method always returns tuple
        return False, GestureType.NONE, False
    
    def trigger_cooldown(self, current_time, duration=None):
        """Move to COOLDOWN after action execution"""
        self.state = GestureState.COOLDOWN
        self.cooldown_start_time = current_time
        if duration is not None:
            self.COOLDOWN_DURATION = duration
    
    def reset(self):
        """Reset to NONE state"""
        self.state = GestureState.NONE
        self.current_gesture = GestureType.NONE
        self.candidate_gesture = GestureType.NONE
        self.candidate_frame_count = 0
    
    def get_state_info(self):
        """Get current state for debugging"""
        return {
            'state': self.state.name,
            'current_gesture': self.current_gesture.name if self.current_gesture != GestureType.NONE else 'NONE',
            'candidate_frames': self.candidate_frame_count
        }


# ============================================================================
# GESTURE RECOGNITION ENGINE
# ============================================================================

class HandGestureRecognizer:
    """
    Recognizes hand gestures using MediaPipe hand landmarks.
    
    MediaPipe Hand Landmarks (21 points):
        0: Wrist
        1-4: Thumb (CMC, MCP, IP, TIP)
        5-8: Index (MCP, PIP, DIP, TIP)
        9-12: Middle (MCP, PIP, DIP, TIP)
        13-16: Ring (MCP, PIP, DIP, TIP)
        17-20: Pinky (MCP, PIP, DIP, TIP)
    """
    
    # Landmark indices for easier reference
    WRIST = 0
    THUMB_TIP = 4
    THUMB_IP = 3
    INDEX_TIP = 8
    INDEX_DIP = 7
    INDEX_PIP = 6
    INDEX_MCP = 5
    MIDDLE_TIP = 12
    MIDDLE_DIP = 11
    MIDDLE_PIP = 10
    MIDDLE_MCP = 9
    RING_TIP = 16
    RING_DIP = 15
    RING_MCP = 13
    PINKY_TIP = 20
    PINKY_DIP = 19
    PINKY_MCP = 17
    
    def __init__(self):
        """Initialize the gesture recognizer"""
        # Swipe detection state
        self.previous_wrist_x = None
        self.previous_wrist_y = None
        self.previous_index_x = None  # ISSUE #3 FIX: Track index finger for better swipe detection
        self.previous_index_y = None
        self.swipe_start_time = None
        self.swipe_confirmation_buffer = []  # ISSUE #4 FIX: Multi-frame swipe validation
        # Persist confirmed swipes so dwell-based actions can complete
        self.active_horizontal_swipe = GestureType.NONE
        self.active_horizontal_swipe_start = 0.0
        self.active_vertical_swipe = GestureType.NONE
        self.active_vertical_swipe_start = 0.0
        
        # Scroll gesture state (ISSUE #1 FIX: Dwell time tracking)
        self.scroll_gesture_start_time = 0.0  # Changed from None to 0.0
        self.scroll_last_gesture = GestureType.NONE  # Changed from None
        self.scroll_last_action_time = 0.0  # REFINEMENT #1: Track last scroll for continuous delay
        
        # REFINEMENT #2: Browser navigation safety timing
        self.browser_nav_gesture_start_time = 0.0  # Changed from None to 0.0
        self.browser_nav_last_gesture = GestureType.NONE  # Changed from None
        self.browser_nav_last_action_time = 0.0
        
        # Close browser safety timing (CRITICAL - requires long dwell)
        self.close_browser_gesture_start_time = 0.0
        self.close_browser_last_gesture = GestureType.NONE
        self.close_browser_last_action_time = 0.0
        
        # REFINEMENT #3: Close tab safety timing
        self.close_tab_gesture_start_time = 0.0  # Changed from None to 0.0
        self.close_tab_gesture_stable = False
        self.close_tab_last_action_time = 0.0
        self.close_tab_last_progress_printed = -1  # BUG FIX: Track last printed progress to prevent spam
        
        # REFINEMENT #4: Zoom gesture isolation
        self.zoom_active = False
        self.zoom_last_action_time = 0.0
        
        # REFINEMENT #5: Mute toggle timing
        self.mute_gesture_start_time = 0.0  # Changed from None to 0.0
        self.mute_last_action_time = 0.0
        
        # Mode state (ISSUE #2 FIX: Mode separation)
        self.current_mode = 'GESTURE'  # 'GESTURE' or 'POINTER'
        self.mode_switch_time = 0.0
        
        self.hand_size_baseline = None  # For auto-calibration
        
        # CNN Gesture Recognition Integration (PHASE 4: ML Integration)
        # CRITICAL: CNN must ALWAYS use temporal voting (no single-frame predictions)
        self.cnn_classifier = None
        self.cnn_enabled = Config.ENABLE_CNN_CLASSIFIER and CNN_AVAILABLE
        
        if self.cnn_enabled:
            try:
                print("Initializing CNN Gesture Classifier...")
                # Import from gesture_model_inference.py
                from gesture_model_inference import CNNGestureClassifier
                self.cnn_classifier = CNNGestureClassifier()
                
                # Load model (no parameters - uses config paths internally)
                if self.cnn_classifier.load_model():
                    print("[SUCCESS] CNN model loaded with temporal voting enabled")
                    print(f"   - Confidence threshold: ≥80%")
                    print(f"   - Voting window: 7 frames (233ms @ 30fps)")
                    print(f"   - Consistency required: 85%")
                else:
                    print("WARNING: CNN model loading failed - falling back to rule-based")
                    self.cnn_enabled = False
                    self.cnn_classifier = None
            except Exception as e:
                print(f"WARNING: CNN initialization error: {e}")
                print("   Falling back to rule-based recognition")
                self.cnn_enabled = False
                self.cnn_classifier = None
        else:
            if Config.ENABLE_CNN_CLASSIFIER and not CNN_AVAILABLE:
                print("WARNING: CNN recognition enabled but module not found")
                print("   Using rule-based recognition only")
            else:
                print("[INFO] CNN recognition disabled - using rule-based recognition")
        
        # CNN to GestureType Mapping (5 CNN gestures → GestureType enum)
        # HACKATHON SIMPLIFIED: Only map gestures that are still active
        self.cnn_to_gesture_map = {
            'scroll_up': GestureType.CLOSED_FIST,
            'scroll_down': GestureType.OPEN_PALM,
            'swipe_left': GestureType.SWIPE_LEFT,
            'swipe_right': GestureType.SWIPE_RIGHT,
            'mute_toggle': GestureType.PINKY_ONLY,
            # Removed: 'pinch_zoom' (PINCH disabled), 'thumb_down_close' (THUMB_DOWN removed)
        }
        
        # PERFORMANCE IMPROVEMENT: Initialize smoothing pipeline
        # Post-CNN smoothing (after prediction, before state machine)
        self.smoothing_pipeline = None
        if SMOOTHING_AVAILABLE and GestureSmoothingPipeline is not None:
            try:
                self.smoothing_pipeline = GestureSmoothingPipeline()  # type: ignore
                print("[SUCCESS] Smoothing pipeline active (filterpy + scipy)")
            except Exception as e:
                print(f"WARNING: Smoothing pipeline initialization error: {e}")
                self.smoothing_pipeline = None
    
    def is_finger_extended(self, landmarks, finger_tip, finger_dip, finger_mcp):
        """
        STRICT: Determines if a finger is CLEARLY extended.
        
        WHY OVERLAPS OCCURRED BEFORE:
        - Threshold was 0.005 (0.5% of screen) - allowed partial extension
        - No angle or distance verification - accepted ambiguous poses
        
        WHY THIS PREVENTS OVERLAP:
        - Threshold is 0.020 (2% of screen) - requires clear extension
        - Both joints must show progressive extension (tip > dip > mcp)
        - Stricter threshold means partial curls won't trigger false positives
        
        Logic:
            Finger is EXTENDED only if TIP is clearly higher than DIP,
            and DIP is clearly higher than MCP (progressive extension).
            In image coordinates, y increases downward (smaller y = higher).
        
        Args:
            landmarks: List of hand landmarks
            finger_tip: Index of fingertip landmark
            finger_dip: Index of DIP joint landmark  
            finger_mcp: Index of MCP joint landmark
            
        Returns:
            bool: True if finger is CLEARLY extended (not ambiguous)
        """
        tip_y = landmarks[finger_tip].y
        dip_y = landmarks[finger_dip].y
        mcp_y = landmarks[finger_mcp].y
        
        # STRICT: Require CLEAR progressive extension with proper threshold
        # Old threshold (0.005) allowed partial extension - NEW (0.020) requires clear extension
        is_tip_above_dip = (tip_y + Config.FINGER_EXTENSION_THRESHOLD) < dip_y
        is_dip_above_mcp = (dip_y + Config.FINGER_EXTENSION_THRESHOLD) < mcp_y
        
        return is_tip_above_dip and is_dip_above_mcp
    
    def is_finger_curled(self, landmarks, finger_tip, finger_dip, finger_mcp):
        """
        STRICT: Determines if a finger is CLEARLY curled (folded).
        
        WHY THIS IS CRITICAL:
        - Previous code only checked if NOT extended, but didn't verify actually curled
        - Ambiguous positions (half-curled) could trigger wrong gestures
        
        WHY THIS PREVENTS OVERLAP:
        - Explicitly verifies finger is curled (tip below or near dip)
        - Closed Fist requires ALL fingers pass this test
        - Pinky-Only requires all OTHER fingers pass this test
        
        Logic:
            Finger is CURLED if TIP is NOT significantly above DIP.
            This is the inverse of is_finger_extended with a buffer zone.
        
        Args:
            landmarks: List of hand landmarks
            finger_tip: Index of fingertip landmark
            finger_dip: Index of DIP joint landmark
            finger_mcp: Index of MCP joint landmark
            
        Returns:
            bool: True if finger is CLEARLY curled (not extended or ambiguous)
        """
        tip_y = landmarks[finger_tip].y
        dip_y = landmarks[finger_dip].y
        
        # Finger is curled if tip is NOT clearly above dip
        # Using curl threshold (slightly smaller than extension) for buffer zone
        is_curled = tip_y >= (dip_y - Config.FINGER_CURL_THRESHOLD)
        
        return is_curled
    
    def is_thumb_extended(self, landmarks):
        """
        Checks if thumb is extended (spread away from palm).
        
        STRICT: Made strict to distinguish between tucked thumb vs extended thumb.
        This is critical for differentiating FOUR_FINGERS (thumb tucked) from OPEN_PALM (thumb spread).
        
        Logic:
            Thumb extends horizontally. It's extended if the TIP is
            clearly farther from the wrist with progressive joint distances.
        
        Returns:
            bool: True if thumb is clearly extended (not tucked)
        """
        thumb_tip = landmarks[self.THUMB_TIP]
        thumb_ip = landmarks[self.THUMB_IP]
        thumb_mcp = landmarks[2]  # Thumb MCP joint
        wrist = landmarks[self.WRIST]
        index_mcp = landmarks[self.INDEX_MCP]
        
        # Calculate distance from wrist for tip and ip
        tip_dist = ((thumb_tip.x - wrist.x)**2 + (thumb_tip.y - wrist.y)**2) ** 0.5
        ip_dist = ((thumb_ip.x - wrist.x)**2 + (thumb_ip.y - wrist.y)**2) ** 0.5
        mcp_dist = ((thumb_mcp.x - wrist.x)**2 + (thumb_mcp.y - wrist.y)**2) ** 0.5
        
        # STRICT: Require clear progressive extension
        is_progressive = tip_dist > ip_dist and ip_dist > mcp_dist * 0.95
        
        # STRICT: Thumb must be reasonably far from wrist
        is_clearly_away = tip_dist > 0.10
        
        # ADDITIONAL CHECK: Thumb should be away from index finger base (not tucked alongside)
        thumb_index_dist = ((thumb_tip.x - index_mcp.x)**2 + (thumb_tip.y - index_mcp.y)**2) ** 0.5
        is_away_from_index = thumb_index_dist > 0.08
        
        return is_progressive and is_clearly_away and is_away_from_index
    
    def count_extended_fingers(self, landmarks, ignore_thumb=None):
        """
        Counts how many fingers are extended.
        
        ISSUE #5 FIX: Added thumb-ignored mode for accessibility.
        When ignore_thumb=True, thumb is excluded from count (reduces false positives).
        
        Args:
            landmarks: Hand landmarks
            ignore_thumb: Override for thumb detection (None = use Config setting)
        
        Returns:
            dict: Contains count and which specific fingers are extended
        """
        # ISSUE #5 FIX: Apply thumb-ignored mode if enabled
        if ignore_thumb is None:
            ignore_thumb = Config.THUMB_IGNORED_MODE
        
        fingers = {
            'thumb': False if ignore_thumb else self.is_thumb_extended(landmarks),
            'index': self.is_finger_extended(landmarks, self.INDEX_TIP, 
                                            self.INDEX_DIP, self.INDEX_MCP),
            'middle': self.is_finger_extended(landmarks, self.MIDDLE_TIP,
                                             self.MIDDLE_DIP, self.MIDDLE_MCP),
            'ring': self.is_finger_extended(landmarks, self.RING_TIP,
                                           self.RING_DIP, self.RING_MCP),
            'pinky': self.is_finger_extended(landmarks, self.PINKY_TIP,
                                            self.PINKY_DIP, self.PINKY_MCP)
        }
        
        count = sum(fingers.values())
        return count, fingers
    
    def detect_thumb_up(self, landmarks):
        """
        Detects thumbs-up gesture - IMPROVED DISTINCTNESS.
        
        Logic:
            Thumb extended upward (tip.y < ip.y) while all other fingers folded.
            Additional angle check to ensure thumb is vertical and clearly pointing up.
        
        Returns:
            bool: True if thumbs-up detected
        """
        count, fingers = self.count_extended_fingers(landmarks, ignore_thumb=False)
        
        # Only thumb should be extended, all others folded
        if fingers['thumb'] and not fingers['index'] and not fingers['middle'] and not fingers['ring'] and not fingers['pinky']:
            thumb_tip_y = landmarks[self.THUMB_TIP].y
            thumb_ip_y = landmarks[self.THUMB_IP].y
            thumb_mcp_y = landmarks[2].y  # Thumb MCP
            wrist_y = landmarks[self.WRIST].y
            
            # Thumb pointing up: tip above ip above mcp
            vertical_alignment = thumb_tip_y < thumb_ip_y < thumb_mcp_y
            
            # STRICT: Thumb must be significantly above wrist (not just tucked to side)
            thumb_elevated = thumb_tip_y < wrist_y - 0.15  # INCREASED threshold
            
            # STRICT: Thumb tip should be higher than all other fingertips (confirm it's pointing UP not sideways)
            index_tip_y = landmarks[self.INDEX_TIP].y
            middle_tip_y = landmarks[self.MIDDLE_TIP].y
            ring_tip_y = landmarks[self.RING_TIP].y
            pinky_tip_y = landmarks[self.PINKY_TIP].y
            thumb_is_highest = (thumb_tip_y < index_tip_y and thumb_tip_y < middle_tip_y and 
                               thumb_tip_y < ring_tip_y and thumb_tip_y < pinky_tip_y)
            
            return vertical_alignment and thumb_elevated and thumb_is_highest
        
        return False
    
    def detect_swipe(self, landmarks):
        """
        Detects horizontal swipe gestures (left or right).
        
        ISSUE #3 FIX: Uses wrist + index finger for detection (ignores thumb).
        ISSUE #3 FIX: Enforces direction dominance (horizontal >> vertical).
        ISSUE #4 FIX: Multi-frame confirmation to prevent false positives.
        
        Logic:
            Tracks wrist + index finger position. Requires:
            1. Significant horizontal movement (exceeds threshold)
            2. Horizontal movement >> vertical movement (direction dominance)
            3. Consistent direction across multiple frames
        
        Returns:
            GestureType: SWIPE_LEFT, SWIPE_RIGHT, or NONE
        """
        current_wrist_x = landmarks[self.WRIST].x
        current_wrist_y = landmarks[self.WRIST].y
        current_index_x = landmarks[self.INDEX_TIP].x

        # If a horizontal swipe was recently confirmed, persist it for a short window
        if (self.active_horizontal_swipe != GestureType.NONE and
            time.time() - self.active_horizontal_swipe_start < Config.BROWSER_NAV_DWELL_TIME):
            return self.active_horizontal_swipe
        else:
            # expire active swipe
            if time.time() - self.active_horizontal_swipe_start >= Config.BROWSER_NAV_DWELL_TIME:
                self.active_horizontal_swipe = GestureType.NONE
        
        if self.previous_wrist_x is None or self.previous_index_x is None:
            self.previous_wrist_x = current_wrist_x
            self.previous_wrist_y = current_wrist_y
            self.previous_index_x = current_index_x
            return GestureType.NONE
        
        # ISSUE #3 FIX: Calculate movement using wrist + index (thumb-independent)
        delta_x = (current_wrist_x - self.previous_wrist_x + 
                   current_index_x - self.previous_index_x) / 2.0
        delta_y = current_wrist_y - self.previous_wrist_y
        
        # ISSUE #3 FIX: Enforce direction dominance (horizontal >> vertical)
        horizontal_movement = abs(delta_x)
        vertical_movement = abs(delta_y)
        
        # FIX #5: Add velocity threshold to prevent accidental swipes from slow drifts
        # Check if movement exceeds threshold AND has minimum velocity AND has direction dominance
        if horizontal_movement > Config.SWIPE_THRESHOLD and horizontal_movement > Config.SWIPE_VELOCITY_MIN:
            # ISSUE #3 FIX: Require horizontal dominance
            if vertical_movement > 0 and (horizontal_movement / vertical_movement) < Config.SWIPE_DIRECTION_DOMINANCE_RATIO:
                # Too much vertical movement - reject as horizontal swipe
                self.previous_wrist_x = current_wrist_x
                self.previous_wrist_y = current_wrist_y
                self.previous_index_x = current_index_x
                return GestureType.NONE
            
            # Determine direction
            swipe_direction = GestureType.SWIPE_LEFT if delta_x < 0 else GestureType.SWIPE_RIGHT
            
            # ISSUE #4 FIX: Multi-frame confirmation
            self.swipe_confirmation_buffer.append(swipe_direction)
            if len(self.swipe_confirmation_buffer) > Config.SWIPE_CONFIRMATION_FRAMES:
                self.swipe_confirmation_buffer.pop(0)
            
            # Check if last N frames agree on direction
            if len(self.swipe_confirmation_buffer) == Config.SWIPE_CONFIRMATION_FRAMES:
                if all(d == swipe_direction for d in self.swipe_confirmation_buffer):
                    # Persist confirmed swipe so execute_gesture_action can observe it across frames
                    self.active_horizontal_swipe = swipe_direction
                    self.active_horizontal_swipe_start = time.time()
                    self.swipe_confirmation_buffer.clear()
                    self.previous_wrist_x = current_wrist_x
                    self.previous_wrist_y = current_wrist_y
                    self.previous_index_x = current_index_x
                    return swipe_direction
        
        self.previous_wrist_x = current_wrist_x
        self.previous_wrist_y = current_wrist_y
        self.previous_index_x = current_index_x
        return GestureType.NONE
    
    def detect_vertical_swipe(self, landmarks):
        """
        REMOVED: Vertical swipes disabled for hackathon (conflicts with hand movement).
        
        Vertical swipes (SWIPE_UP/SWIPE_DOWN) were removed because:
        - Conflict with natural vertical hand positioning
        - Not essential for browser control (tab switching not critical)
        - Simplifies gesture set to 8 core actions
        
        Returns:
            GestureType.NONE (always - function disabled)
        """
        # DISABLED FOR HACKATHON STABILITY
        return GestureType.NONE
    
    def calculate_hand_size(self, landmarks):
        """
        Calculate hand size for auto-calibration.
        
        Returns:
            float: Distance between wrist and middle finger tip
        """
        wrist = landmarks[self.WRIST]
        middle_tip = landmarks[self.MIDDLE_TIP]
        
        distance = ((middle_tip.x - wrist.x)**2 + 
                   (middle_tip.y - wrist.y)**2) ** 0.5
        return distance
    
    def calculate_pinch_distance(self, landmarks):
        """
        Calculate distance between thumb and index finger tips.
        
        Returns:
            float: Normalized distance between thumb and index tips
        """
        thumb_tip = landmarks[self.THUMB_TIP]
        index_tip = landmarks[self.INDEX_TIP]
        
        distance = ((thumb_tip.x - index_tip.x)**2 + 
                   (thumb_tip.y - index_tip.y)**2) ** 0.5
        return distance
    
    def detect_pinch_spread(self, landmarks):
        """
        DISABLED: Pinch/spread gestures removed for hackathon (conflict-prone).
        
        Pinch/spread (zoom) gestures were removed because:
        - Conflict with other two-finger poses (peace sign)
        - Accidental triggers during hand positioning
        - THUMB_UP provides simpler zoom-in alternative
        - Zoom-out not essential for browser demos
        
        Returns:
            GestureType.NONE (always - function disabled)
        """
        # DISABLED FOR HACKATHON STABILITY
        # Config.ENABLE_ZOOM_GESTURES = False by default
        return GestureType.NONE
    
    def detect_special_gestures(self, landmarks, fingers):
        """
        DISABLED: Special hand signs removed for hackathon (not essential).
        
        Special gestures (OK_SIGN, ROCK_SIGN, CALL_SIGN) were removed because:
        - Not essential for browser control
        - Require complex finger configurations (unreliable detection)
        - Simplifies gesture set to 8 core actions
        - Reduces cognitive load for judges
        
        Returns:
            GestureType.NONE (always - function disabled)
        """
        # DISABLED FOR HACKATHON STABILITY
        return GestureType.NONE
    
    def detect_thumb_down(self, landmarks):
        """
        DISABLED: Thumbs-down gesture removed for hackathon (close tab too risky).
        
        THUMB_DOWN (close tab) was removed because:
        - High-stakes action (accidental tab closure)  
        - Too risky for live demos
        - Replaced with PINKY_ONLY for mute (safer alternative)
        
        Returns:
            False (always - function disabled)
        """
        # DISABLED FOR HACKATHON SAFETY
        return False
    
    def recognize_gesture_hybrid(self, hand_landmarks, frame):
        """
        Hybrid CNN + Rule-based Gesture Recognition (PHASE 4: ML Integration)
        
        This method combines CNN-based classification with rule-based fallback for maximum
        accuracy and safety. The CNN handles static gestures while MediaPipe continues
        to handle pointer movement and dynamic gesture validation.
        
        DataFlair-based Safety Pipeline (NON-NEGOTIABLE):
            1. CNN Raw Prediction → Confidence Filter (≥80%) → Temporal Voting (7 frames, 85%)
            2. CNN output NEVER directly triggers actions (goes through state machine)
            3. Falls back to rule-based if CNN disabled or prediction rejected
            4. Single-frame predictions are NEVER propagated (temporal voting mandatory)
        
        Args:
            hand_landmarks: MediaPipe hand landmarks object
            frame: Current video frame (for ROI extraction if CNN enabled)
            
        Returns:
            GestureType: The detected gesture (CNN or rule-based)
        """
        if not hand_landmarks:
            return GestureType.NONE
        
        # Special case: INDEX_ONLY is ALWAYS handled by MediaPipe (pointer mode)
        # CNN does NOT classify pointer gestures - only action gestures
        landmarks = hand_landmarks.landmark
        count, fingers = self.count_extended_fingers(landmarks)
        if count == 1 and fingers['index']:
            return GestureType.INDEX_ONLY  # Skip CNN for pointer mode
        
        # Attempt CNN classification if enabled and model loaded
        if self.cnn_enabled and self.cnn_classifier and frame is not None:
            try:
                # Extract hand ROI using SAME method as dataset collector (consistency critical)
                hand_roi = self.extract_hand_roi_for_cnn(frame, landmarks)
                
                if hand_roi is not None:
                    # CNN Classification with MANDATORY temporal voting
                    # The classify() method enforces: confidence filter + 7-frame voting + 85% consistency
                    cnn_label, cnn_confidence = self.cnn_classifier.classify(hand_roi)
                    
                    # PERFORMANCE IMPROVEMENT: Apply smoothing to confidence
                    # Post-CNN smoothing reduces oscillation (e.g., 0.78→0.82→0.79...)
                    # Pipeline: Raw confidence → Kalman → Savitzky-Golay → Smoothed
                    if self.smoothing_pipeline is not None and cnn_confidence is not None:
                        cnn_confidence_smoothed = self.smoothing_pipeline.smooth_confidence(cnn_confidence)
                        # Use smoothed confidence but keep original label (smoothing doesn't change classification)
                        cnn_confidence = cnn_confidence_smoothed
                    
                    # If CNN returned valid prediction (passed all safety filters)
                    if cnn_label is not None and cnn_label in self.cnn_to_gesture_map:
                        gesture_type = self.cnn_to_gesture_map[cnn_label]
                        
                        # CNN prediction accepted (PINCH gesture verification removed - zoom disabled)
                        return gesture_type
                
                # CNN rejected prediction (low confidence or voting failed)
                # Fall back to rule-based recognition
                
            except Exception as e:
                # CNN processing error - gracefully fall back to rule-based
                print(f"WARNING: CNN processing error: {e}")
        
        # Fallback: Use existing rule-based recognition
        return self.recognize_gesture(hand_landmarks)
    
    def extract_hand_roi_for_cnn(self, frame, landmarks):
        """
        Extract hand ROI for CNN inference.
        
        CRITICAL: Must match collect_gesture_dataset.py preprocessing EXACTLY.
        OPTIMIZED: Single-pass coordinate extraction, early validation checks
        
        Args:
            frame: Current video frame
            landmarks: MediaPipe hand landmarks
        
        Returns:
            Preprocessed hand ROI (64x64 grayscale) or None
        """
        h, w = frame.shape[:2]
        
        # OPTIMIZATION: Single-pass min/max calculation (avoid list allocations)
        x_min = y_min = float('inf')
        x_max = y_max = float('-inf')
        
        for lm in landmarks:
            x = lm.x * w
            y = lm.y * h
            x_min = min(x_min, x)
            x_max = max(x_max, x)
            y_min = min(y_min, y)
            y_max = max(y_max, y)
        
        # Convert to int
        x_min, x_max = int(x_min), int(x_max)
        y_min, y_max = int(y_min), int(y_max)
        
        # Early validation: Check if bounding box is valid
        if x_max <= x_min or y_max <= y_min:
            return None
        
        # Add padding (20%) - MUST match collector
        padding_x = int((x_max - x_min) * 0.2)
        padding_y = int((y_max - y_min) * 0.2)
        
        x_min = max(0, x_min - padding_x)
        y_min = max(0, y_min - padding_y)
        x_max = min(w, x_max + padding_x)
        y_max = min(h, y_max + padding_y)
        
        # Extract ROI
        hand_roi = frame[y_min:y_max, x_min:x_max]
        
        # Validate ROI size
        if hand_roi.size == 0:
            return None
        
        # OPTIMIZATION: In-place conversion when possible
        # Convert to grayscale - MUST match collector
        if len(hand_roi.shape) == 3:
            hand_gray = cv2.cvtColor(hand_roi, cv2.COLOR_BGR2GRAY)
        else:
            hand_gray = hand_roi
        
        # Normalize lighting (histogram equalization) - MUST match collector
        hand_normalized = cv2.equalizeHist(hand_gray)
        
        # Resize to target size (64x64) - MUST match collector
        # OPTIMIZATION: Use INTER_AREA for downsampling (faster than INTER_LINEAR)
        hand_resized = cv2.resize(hand_normalized, (64, 64), interpolation=cv2.INTER_AREA)
        
        return hand_resized
    
    def recognize_gesture(self, hand_landmarks):
        """
        Main gesture recognition function with STRICT EXCLUSIVITY ENFORCEMENT.
        
        DataFlair Anti-Conflict Pattern:
            - Collect ALL candidate gestures with confidence scores
            - Apply strict exclusivity rules (only ONE gesture can be active)
            - Select highest-confidence gesture only when multiple candidates exist
            - Use mutually exclusive priority ordering to prevent overlap
        
        CONFLICT EXAMPLE (BEFORE FIX):
            "Swipe-right and PEACE_SIGN (index+middle extended) can overlap when hand
            moves slowly rightward with two fingers up, causing CNN to alternate labels."
        
        CONFLICT FIX (AFTER):
            "Swipes require wrist+index movement AND multi-frame confirmation AND no
            static finger pose detection during movement. PEACE_SIGN requires static
            pose (no movement) AND exact 2-finger count AND all others folded.
            Movement gestures are checked BEFORE static poses, eliminating overlap."
        
        Analyzes hand landmarks and returns the detected gesture type.
        
        Args:
            hand_landmarks: MediaPipe hand landmarks object
            
        Returns:
            GestureType: The detected gesture (strictly one only)
        """
        if not hand_landmarks:
            return GestureType.NONE
        
        landmarks = hand_landmarks.landmark
        
        # OPTIMIZATION: Single finger count call - cache result for entire method
        # ISSUE #5 FIX: Count fingers with thumb-ignored mode applied
        count, fingers = self.count_extended_fingers(landmarks)
        
        # OPTIMIZATION: Initialize variables for lazy evaluation (prevents unbound errors)
        count_with_thumb = None  # Will be computed when needed
        fingers_with_thumb = None  # Will be computed when needed
        count_full = None  # Will be computed when needed
        fingers_full = None  # Will be computed when needed
        
        # Debug output for finger detection (only when advanced UI enabled)
        if Config.is_advanced_ui_enabled() and hasattr(self, '_debug_frame_counter'):
            self._debug_frame_counter = getattr(self, '_debug_frame_counter', 0) + 1
            # Print every 15 frames to avoid spam (2x per second at 30fps)
            if self._debug_frame_counter % 15 == 0:
                print(f"[DEBUG] Fingers: {count} | Extended: {[k for k, v in fingers.items() if v]}")
        
        # Auto-calibrate hand size on first detection
        if self.hand_size_baseline is None and Config.ENABLE_LEARNING_MODE:
            self.hand_size_baseline = self.calculate_hand_size(landmarks)
        
        # MUTUALLY EXCLUSIVE PRIORITY ORDER (8 essential gestures only)
        # HACKATHON PRINCIPLE: Movement gestures FIRST, then static poses (prevents overlap)
        # Collect candidates with confidence for conflict resolution
        candidates = []  # List of (gesture, confidence, reason) tuples
        
        # PRIORITY 1: Movement-based gestures (swipes) - CHECK FIRST
        # CRITICAL: Movement detection BEFORE static poses prevents "swipe + peace" conflicts
        # Swipes require sustained motion AND direction dominance AND multi-frame confirmation
        swipe_h = self.detect_swipe(landmarks)
        if swipe_h != GestureType.NONE:
            candidates.append((swipe_h, 0.95, 'Horizontal swipe detected'))
        
        # STRICT EXCLUSIVITY: If movement detected, BLOCK all static pose detection
        # This is the key anti-conflict measure for hackathon demos
        if candidates:
            best = max(candidates, key=lambda x: x[1])
            if Config.DEBUG_GESTURE_DETECTION:
                print(f"\n[DETECTED] {best[0].name}: {best[2]}")
            return best[0]
        
        # PRIORITY 2: Thumb gestures (explicit thumb-only poses)
        # Only THUMB_UP supported (THUMB_DOWN removed - too risky for demo)
        if self.detect_thumb_up(landmarks):
            if Config.DEBUG_GESTURE_DETECTION:
                print("\n[DETECTED] THUMB_UP (zoom in)")
            return GestureType.THUMB_UP
        
        # ============================================================================
        # GESTURE REGISTRY: STRICT, MUTUALLY EXCLUSIVE DEFINITIONS
        # ============================================================================
        # Each gesture requires ALL fingers in EXPLICIT states (extended OR curled)
        # NO ambiguous states allowed - partial extension = NO MATCH
        
        # WHY THIS PREVENTS OVERLAPS:
        # 1. Each gesture explicitly checks ALL 5 fingers (thumb, index, middle, ring, pinky)
        # 2. Uses both is_finger_extended() AND is_finger_curled() for verification
        # 3. Strict elif chain - only ONE gesture can match
        # 4. Ambiguous poses (partial extension) rejected by strict thresholds
        
        # PRIORITY 3: Finger-count based gestures (static poses)
        # STRICT elif chain ensures mutual exclusivity (only ONE gesture can match)
        
        # ========================================
        # GESTURE 1: CLOSED_FIST (0 fingers extended)
        # ========================================
        # DEFINITION: ALL fingers must be clearly curled (not extended)
        # WHY STRICT: Prevents partial fist from triggering scroll up
        if count == 0:
            # OPTIMIZATION: Lazy compute count_with_thumb only when needed
            # STRICT VALIDATION: Verify ALL fingers are actually curled, not just "not extended"
            if count_with_thumb is None:
                count_with_thumb, fingers_with_thumb = self.count_extended_fingers(landmarks, ignore_thumb=False)
            
            # Double-check: Verify fingers are curled using explicit curl detection
            all_curled = (
                self.is_finger_curled(landmarks, self.INDEX_TIP, self.INDEX_DIP, self.INDEX_MCP) and
                self.is_finger_curled(landmarks, self.MIDDLE_TIP, self.MIDDLE_DIP, self.MIDDLE_MCP) and
                self.is_finger_curled(landmarks, self.RING_TIP, self.RING_DIP, self.RING_MCP) and
                self.is_finger_curled(landmarks, self.PINKY_TIP, self.PINKY_DIP, self.PINKY_MCP)
            )
            
            if count_with_thumb == 0 and all_curled:
                if Config.DEBUG_GESTURE_DETECTION:
                    print("\n[DETECTED] CLOSED_FIST (scroll up - all fingers curled)")
                return GestureType.CLOSED_FIST
        
        # ========================================
        # GESTURE 2: FOUR_FINGERS (4 fingers, thumb curled)
        # ========================================
        # DEFINITION: Exactly 4 fingers (index, middle, ring, pinky) extended + thumb NOT extended
        # WHY FIRST: Check before OPEN_PALM to prevent conflict
        # This must come BEFORE OPEN_PALM in priority
        elif count == 4:
            # OPTIMIZATION: Lazy compute count_with_thumb only when needed
            if count_with_thumb is None:
                count_with_thumb, fingers_with_thumb = self.count_extended_fingers(landmarks, ignore_thumb=False)
            
            # Debug output (fingers_with_thumb is now guaranteed to be initialized)
            if Config.DEBUG_GESTURE_DETECTION and fingers_with_thumb is not None:
                print(f"\n[DEBUG] 4 fingers detected: count_with_thumb={count_with_thumb}, thumb={fingers_with_thumb.get('thumb', False)}")
            
            # FOUR_FINGERS: Exactly 4 fingers extended, thumb NOT extended
            if fingers_with_thumb is not None and count_with_thumb == 4 and not fingers_with_thumb.get('thumb', False):
                # STRICT VALIDATION: Verify exactly index, middle, ring, pinky extended
                four_fingers_extended = (
                    fingers_with_thumb.get('index', False) and
                    fingers_with_thumb.get('middle', False) and
                    fingers_with_thumb.get('ring', False) and
                    fingers_with_thumb.get('pinky', False)
                )
                
                if four_fingers_extended:
                    if Config.DEBUG_GESTURE_DETECTION:
                        print("\n[DETECTED] FOUR_FINGERS (refresh page - 4 fingers, thumb not extended)")
                    return GestureType.FOUR_FINGERS
            
            # If we have 5 fingers including thumb, might be OPEN_PALM - continue checking
            # Fall through to next gesture check
        
        # ========================================
        # GESTURE 3: OPEN_PALM (5 fingers extended)
        # ========================================
        # DEFINITION: ALL 5 fingers (including thumb) must be CLEARLY extended
        # WHY STRICT: Prevents 4-finger poses or partial spreads from triggering scroll down
        # CONFLICT PREVENTION: Most common overlap was Open Palm vs Pinky-Only (partial extension)
        if count == 4 or count == 5:  # Could be 4 fingers without thumb OR 5 fingers with thumb
            # OPTIMIZATION: Compute full count only when in this range
            if count_with_thumb is None:
                count_with_thumb, fingers_with_thumb = self.count_extended_fingers(landmarks, ignore_thumb=False)
            
            # STRICT VALIDATION: Require exactly 5 fingers AND explicit verification of each
            if fingers_with_thumb is not None and count_with_thumb == 5:
                # Verify ALL fingers are extended (no ambiguous states)
                all_extended = (
                    fingers_with_thumb.get('thumb', False) and
                    fingers_with_thumb.get('index', False) and
                    fingers_with_thumb.get('middle', False) and
                    fingers_with_thumb.get('ring', False) and
                    fingers_with_thumb.get('pinky', False)
                )
                
                # Additional strictness: Verify fingers are NOT curled
                none_curled = not (
                    self.is_finger_curled(landmarks, self.INDEX_TIP, self.INDEX_DIP, self.INDEX_MCP) or
                    self.is_finger_curled(landmarks, self.MIDDLE_TIP, self.MIDDLE_DIP, self.MIDDLE_MCP) or
                    self.is_finger_curled(landmarks, self.RING_TIP, self.RING_DIP, self.RING_MCP) or
                    self.is_finger_curled(landmarks, self.PINKY_TIP, self.PINKY_DIP, self.PINKY_MCP)
                )
                
                if all_extended and none_curled:
                    if Config.DEBUG_GESTURE_DETECTION:
                        print("\n[DETECTED] OPEN_PALM (scroll down - all 5 fingers extended)")
                    return GestureType.OPEN_PALM
        
        # ========================================  
        # GESTURE 4: PEACE_SIGN (2 fingers: index + middle)
        # ========================================
        # DEFINITION: ONLY index and middle extended, ring and pinky MUST be curled
        # WHY STRICT: Prevents 3-finger or partial poses from triggering click
        if count == 2:
            # Verify ONLY index and middle extended
            if fingers['index'] and fingers['middle'] and not fingers['ring'] and not fingers['pinky']:
                # STRICT: Verify ring and pinky are actually curled (not just "not extended")
                ring_curled = self.is_finger_curled(landmarks, self.RING_TIP, self.RING_DIP, self.RING_MCP)
                pinky_curled = self.is_finger_curled(landmarks, self.PINKY_TIP, self.PINKY_DIP, self.PINKY_MCP)
                
                if ring_curled and pinky_curled:
                    if Config.DEBUG_GESTURE_DETECTION:
                        print("\n[DETECTED] PEACE_SIGN (left click - index+middle only)")
                    return GestureType.PEACE_SIGN
        
        # ========================================
        # GESTURE 5A: INDEX_ONLY (1 finger: index only - POINTER MODE)
        # ========================================
        # DEFINITION: ONLY index extended, ALL others curled
        # WHY STRICT: Prevents partial finger extension from triggering pointer mode
        # OPTIMIZATION: Compute full count only when needed for this gesture
        if count_full is None:
            count_full, fingers_full = self.count_extended_fingers(landmarks, ignore_thumb=False)
        if count_full == 1 and fingers_full is not None:
            # Verify ONLY index extended, all others NOT extended
            if fingers_full['index'] and not fingers_full['middle'] and not fingers_full['ring'] and not fingers_full['pinky'] and not fingers_full['thumb']:
                # STRICT: Verify other fingers are actually curled
                others_curled = (
                    self.is_finger_curled(landmarks, self.MIDDLE_TIP, self.MIDDLE_DIP, self.MIDDLE_MCP) and
                    self.is_finger_curled(landmarks, self.RING_TIP, self.RING_DIP, self.RING_MCP) and
                    self.is_finger_curled(landmarks, self.PINKY_TIP, self.PINKY_DIP, self.PINKY_MCP)
                )
                
                if others_curled:
                    if Config.DEBUG_GESTURE_DETECTION:
                        print("\n[DETECTED] INDEX_ONLY (pointer mode - index only)") 
                    return GestureType.INDEX_ONLY
        
        # ========================================
        # GESTURE 5B: THREE_FINGERS (click gesture - index, middle, ring)
        # ========================================
        # DEFINITION: Index, middle, and ring extended (thumb and pinky curled)
        # WHY: Easy to do from pointer mode - just extend 2 more fingers
        # NO INTERFERENCE: Different from all other gestures, natural click motion
        if count == 3:
            # Check if it's index, middle, ring (NOT including thumb or pinky)
            if fingers['index'] and fingers['middle'] and fingers['ring'] and not fingers['pinky']:
                # OPTIMIZATION: Compute full count only when needed
                if count_full is None:
                    count_full, fingers_full = self.count_extended_fingers(landmarks, ignore_thumb=False)
                # Verify pinky is curled and thumb is not extended  
                pinky_curled = self.is_finger_curled(landmarks, self.PINKY_TIP, self.PINKY_DIP, self.PINKY_MCP)
                thumb_not_extended = not fingers_full.get('thumb', False) if fingers_full is not None else True
                
                if pinky_curled and thumb_not_extended:
                    if Config.DEBUG_GESTURE_DETECTION:
                        print("\n[DETECTED] THREE_FINGERS (click - index, middle, ring extended)")
                    return GestureType.THREE_FINGERS
        
        # ========================================
        # GESTURE 6A: ROCK_SIGN (2 fingers: index + pinky - "rock on")
        # ========================================
        # DEFINITION: Index and pinky extended, middle and ring curled, thumb NOT extended
        # WHY: Natural "rock on" hand shape - EXIT PROGRAM (critical action)
        # MUST COME BEFORE PINKY_ONLY to prevent conflict
        if count == 2:
            # Check if it's index + pinky (not peace sign which is index + middle)
            if fingers['index'] and fingers['pinky'] and not fingers['middle'] and not fingers['ring']:
                # OPTIMIZATION: Compute full count only when needed
                if count_full is None:
                    count_full, fingers_full = self.count_extended_fingers(landmarks, ignore_thumb=False)
                # Verify middle and ring are curled, thumb not extended
                middle_curled = self.is_finger_curled(landmarks, self.MIDDLE_TIP, self.MIDDLE_DIP, self.MIDDLE_MCP)
                ring_curled = self.is_finger_curled(landmarks, self.RING_TIP, self.RING_DIP, self.RING_MCP)
                thumb_not_extended = not fingers_full.get('thumb', False) if fingers_full is not None else True
                
                if middle_curled and ring_curled and thumb_not_extended:
                    if Config.DEBUG_GESTURE_DETECTION:
                        print("\n[DETECTED] ROCK_SIGN (exit program - index + pinky extended)")
                    return GestureType.ROCK_SIGN
        
        # ========================================
        # GESTURE 6B: CALL_ME (2 fingers: thumb + pinky - "call me" gesture)
        # ========================================
        # DEFINITION: Thumb and pinky extended, index/middle/ring curled
        # WHY: Natural "call me" gesture - comfortable, unique, prevents accidental browser close
        # CRITICAL: This is for closing browser (high-stakes action)
        # Different from: Rock sign (index+pinky), Thumb up (thumb only), Pinky only (pinky only)
        # MUST CHECK: count_with_thumb for accurate detection since thumb is involved
        # OPTIMIZATION: Compute with thumb only when needed for this gesture
        if count_with_thumb is None:
            count_with_thumb, fingers_with_thumb = self.count_extended_fingers(landmarks, ignore_thumb=False)
        if count_with_thumb == 2 and fingers_with_thumb is not None:
            # Check if it's thumb + pinky ONLY (index, middle, ring must be curled)
            if fingers_with_thumb.get('thumb', False) and fingers_with_thumb.get('pinky', False):
                # Verify index, middle, ring are NOT extended
                if not fingers_with_thumb.get('index', False) and not fingers_with_thumb.get('middle', False) and not fingers_with_thumb.get('ring', False):
                    # STRICT VERIFICATION: Index, middle, ring MUST be curled
                    index_curled = self.is_finger_curled(landmarks, self.INDEX_TIP, self.INDEX_DIP, self.INDEX_MCP)
                    middle_curled = self.is_finger_curled(landmarks, self.MIDDLE_TIP, self.MIDDLE_DIP, self.MIDDLE_MCP)
                    ring_curled = self.is_finger_curled(landmarks, self.RING_TIP, self.RING_DIP, self.RING_MCP)
                    
                    if index_curled and middle_curled and ring_curled:
                        if Config.DEBUG_GESTURE_DETECTION:
                            print("\n[DETECTED] CALL_ME (close browser - thumb + pinky extended)")
                        return GestureType.CALL_ME
        
        # ========================================
        # GESTURE 7: OKAY_SIGN (thumb + index circle, 3 others extended)
        # ========================================
        # DEFINITION: Thumb tip and index tip close together (circle), middle/ring/pinky extended
        # WHY: Natural "OK" hand shape for paste gesture
        # Check if middle, ring, pinky are extended
        if count == 3:
            if fingers['middle'] and fingers['ring'] and fingers['pinky'] and not fingers['index']:
                # OPTIMIZATION: Compute full count only when needed for thumb check
                if count_full is None:
                    count_full, fingers_full = self.count_extended_fingers(landmarks, ignore_thumb=False)
                
                # Check if thumb and index tips are close together (forming circle)
                thumb_tip = landmarks[self.THUMB_TIP]
                index_tip = landmarks[self.INDEX_TIP]
                
                # Calculate distance between thumb and index tips
                distance = math.sqrt(
                    (thumb_tip.x - index_tip.x) ** 2 +
                    (thumb_tip.y - index_tip.y) ** 2
                )
                
                # Verify thumb is extended (for OK sign, thumb comes forward)
                thumb_extended = fingers_full.get('thumb', False) if fingers_full is not None else False
                
                # If tips are close together (< 0.06 normalized distance) = OK sign
                if distance < 0.06 and thumb_extended:
                    if Config.DEBUG_GESTURE_DETECTION:
                        print("\n[DETECTED] OKAY_SIGN (paste - thumb+index circle, others extended)")
                    return GestureType.OKAY_SIGN
        
        # ========================================
        # GESTURE 8: PINKY_ONLY (1 finger: pinky only)
        # ========================================
        # DEFINITION: ONLY pinky extended, ALL others (including thumb) CURLED
        # WHY STRICT: Most conflict-prone gesture - overlapped with Open Palm when partial extension
        # CONFLICT PREVENTION: Strict curl detection prevents partial Open Palm from matching
        if count == 1 and fingers['pinky']:  # OPTIMIZATION: Use cached count first
            # OPTIMIZATION: Lazy compute full count only when basic check passes
            if count_with_thumb is None:
                count_with_thumb, fingers_with_thumb = self.count_extended_fingers(landmarks, ignore_thumb=False)
            
            # Verify ONLY pinky extended, all others NOT extended
            if fingers_with_thumb is not None and fingers_with_thumb['pinky'] and not fingers_with_thumb['index'] and not fingers_with_thumb['middle'] and not fingers_with_thumb['ring'] and not fingers_with_thumb['thumb']:
                # STRICT CURL VERIFICATION: All other fingers MUST be clearly curled
                # This is the KEY fix preventing Open Palm → Pinky-Only confusion
                others_curled = (
                    self.is_finger_curled(landmarks, self.INDEX_TIP, self.INDEX_DIP, self.INDEX_MCP) and
                    self.is_finger_curled(landmarks, self.MIDDLE_TIP, self.MIDDLE_DIP, self.MIDDLE_MCP) and
                    self.is_finger_curled(landmarks, self.RING_TIP, self.RING_DIP, self.RING_MCP)
                )
                
                # Additional elevation check: Pinky must be clearly highest
                pinky_tip_y = landmarks[self.PINKY_TIP].y
                index_tip_y = landmarks[self.INDEX_TIP].y
                middle_tip_y = landmarks[self.MIDDLE_TIP].y
                ring_tip_y = landmarks[self.RING_TIP].y
                
                # STRICT: Pinky must be clearly elevated above curled fingers
                pinky_elevated = (
                    pinky_tip_y < (index_tip_y - 0.05) and  # Increased from 0.03 to 0.05 (stricter)
                    pinky_tip_y < (middle_tip_y - 0.05) and
                    pinky_tip_y < (ring_tip_y - 0.05)
                )
                
                if others_curled and pinky_elevated:
                    if Config.DEBUG_GESTURE_DETECTION:
                        print("\n[DETECTED] PINKY_ONLY (mute - pinky only, others curled)")
                    return GestureType.PINKY_ONLY
        
        # ========================================
        # NO MATCH: Ambiguous or unsupported pose
        # ========================================
        # If no gesture matched, return NONE (prefer false negative over false positive)
        # This includes: partial extensions, unclear poses, intermediate finger positions
        return GestureType.NONE


# ============================================================================
# GESTURE STABILIZATION & DEBOUNCING
# ============================================================================

class GestureStabilizer:
    """
    Stabilizes gesture recognition to prevent false positives.
    
    Uses:
        - Frame buffering: Gesture must be consistent across multiple frames
        - Debouncing: Prevents same action from triggering too rapidly
    """
    
    def __init__(self, buffer_size=Config.GESTURE_BUFFER_SIZE):
        """Initialize the stabilizer with a frame buffer"""
        self.buffer = deque(maxlen=buffer_size)
        self.last_action_time = {}
        self.current_stable_gesture = GestureType.NONE
    
    def add_gesture(self, gesture):
        """
        Add a gesture to the buffer.
        
        Args:
            gesture: GestureType detected in current frame
        """
        self.buffer.append(gesture)
    
    def get_stable_gesture(self):
        """
        Returns gesture only if it's been consistent across buffer.
        
        IMPROVED: Better transition handling to reduce flickering.
        
        Logic:
            - If majority of frames in buffer show same gesture, it's stable
            - Requires higher consistency (60%) to prevent jitter
            - Smoothly transitions by requiring new gesture to dominate buffer
            
        Returns:
            GestureType: Stable gesture or NONE
        """
        # Check if buffer is sufficiently filled
        buffer_maxlen = self.buffer.maxlen if self.buffer.maxlen is not None else Config.GESTURE_BUFFER_SIZE
        if len(self.buffer) < buffer_maxlen * 0.5:  # ULTRA FAST (was 0.8 - 50% fill for instant response)
            return GestureType.NONE
        
        # Count occurrences of each gesture in buffer
        gesture_counts = {}
        for gesture in self.buffer:
            gesture_counts[gesture] = gesture_counts.get(gesture, 0) + 1
        
        # Find most common gesture
        if not gesture_counts:
            return GestureType.NONE
            
        most_common = max(gesture_counts, key=lambda k: gesture_counts[k])
        occurrence_ratio = gesture_counts[most_common] / len(self.buffer)
        
        # FIX #2: ULTRA RELAXED hysteresis for instant gesture switching
        # When switching from one gesture to another, require minimal confidence
        if self.current_stable_gesture != GestureType.NONE and most_common != self.current_stable_gesture:
            # ULTRA FAST: Only 50% consistency for switching (was 80% - much easier now)
            required_confidence = 0.50
        else:
            # Use ultra-low confidence for maintaining current gesture
            required_confidence = Config.CONFIDENCE_THRESHOLD
        
        if occurrence_ratio >= required_confidence:
            self.current_stable_gesture = most_common
            return most_common
        
        # If not confident enough, maintain previous stable gesture (reduces jitter)
        return self.current_stable_gesture
    
    def should_execute_action(self, gesture):
        """
        Check if enough time has passed since last execution.
        
        Prevents rapid repeated actions (debouncing).
        
        Args:
            gesture: GestureType to check
            
        Returns:
            bool: True if action should execute
        """
        current_time = time.time()
        
        # Check if this gesture was recently executed
        if gesture in self.last_action_time:
            time_since_last = current_time - self.last_action_time[gesture]
            if time_since_last < Config.DEBOUNCE_TIME:
                return False
        
        # Update last action time
        self.last_action_time[gesture] = current_time
        return True
    
    def reset(self):
        """Clear the buffer and reset state"""
        self.buffer.clear()
        self.current_stable_gesture = GestureType.NONE


# ============================================================================
# GESTURE HISTORY & ANALYTICS
# ============================================================================

class GestureHistory:
    """
    Tracks gesture usage for analytics and learning.
    """
    
    def __init__(self, max_size=Config.HISTORY_SIZE):
        """Initialize history tracking"""
        self.history = deque(maxlen=max_size)
        self.gesture_counts = {}
        self.session_start = time.time()
        self.total_actions = 0
    
    def add(self, gesture, confidence=1.0):
        """
        Add gesture to history.
        
        Args:
            gesture: GestureType detected
            confidence: Detection confidence (0-1)
        """
        timestamp = time.time()
        self.history.append({
            'gesture': gesture,
            'confidence': confidence,
            'timestamp': timestamp
        })
        
        # Update counts
        if gesture != GestureType.NONE:
            gesture_name = gesture.name
            self.gesture_counts[gesture_name] = self.gesture_counts.get(gesture_name, 0) + 1
            self.total_actions += 1
    
    def get_most_used(self, top_n=5):
        """Get most frequently used gestures"""
        sorted_gestures = sorted(self.gesture_counts.items(), 
                                key=lambda x: x[1], reverse=True)
        return sorted_gestures[:top_n]
    
    def get_session_stats(self):
        """Get session statistics"""
        elapsed = time.time() - self.session_start
        return {
            'duration': elapsed,
            'total_actions': self.total_actions,
            'actions_per_minute': (self.total_actions / elapsed * 60) if elapsed > 0 else 0,
            'unique_gestures': len(self.gesture_counts)
        }
    
    def get_recent(self, n=10):
        """Get n most recent gestures"""
        return list(self.history)[-n:]


# ============================================================================
# VISUAL EFFECTS & TRAILS
# ============================================================================

class VisualEffects:
    """
    Handles visual feedback and effects.
    """
    
    def __init__(self):
        """Initialize visual effects"""
        self.trail_points = deque(maxlen=30)
        self.gesture_flash = None
        self.flash_time = 0
        # Color mapping for 8 core gestures only
        self.color_map = {
            GestureType.OPEN_PALM: (0, 255, 0),      # Green
            GestureType.CLOSED_FIST: (255, 0, 0),    # Red
            GestureType.INDEX_ONLY: (255, 255, 0),   # Yellow
            GestureType.PEACE_SIGN: (0, 255, 255),   # Cyan
            GestureType.THUMB_UP: (0, 128, 255),     # Orange
            GestureType.SWIPE_LEFT: (128, 0, 255),   # Purple
            GestureType.SWIPE_RIGHT: (255, 128, 0),  # Light Blue
            GestureType.PINKY_ONLY: (0, 255, 128),   # Cyan-Green
            # Removed: THUMB_DOWN, THREE_FINGERS, FOUR_FINGERS (disabled for hackathon)
        }
    
    def add_trail_point(self, x, y):
        """Add point to gesture trail"""
        self.trail_points.append((int(x), int(y)))
    
    def draw_trail(self, frame):
        """Draw gesture trail on frame"""
        # OPTIMIZATION: Early exit if trail too short
        trail_len = len(self.trail_points)
        if trail_len < 2:
            return
        
        # OPTIMIZATION: Limit trail length to prevent performance degradation
        max_trail = 50  # Keep last 50 points only (~1.5sec at 30fps)
        if trail_len > max_trail:
            self.trail_points = deque(list(self.trail_points)[-max_trail:], maxlen=max_trail)
            trail_len = max_trail
        
        # Draw trail with fading effect
        for i in range(1, trail_len):
            alpha = i / trail_len  # Fade older points
            thickness = max(1, int(alpha * 3))
            cv2.line(frame, self.trail_points[i-1], self.trail_points[i],
                    (0, 255, 255), thickness)
    
    def flash_gesture(self, gesture):
        """Trigger visual flash for gesture confirmation"""
        self.gesture_flash = gesture
        self.flash_time = time.time()
    
    def draw_gesture_flash(self, frame, gesture):
        """Draw visual flash effect"""
        current_time = time.time()
        if self.gesture_flash and (current_time - self.flash_time) < 0.3:
            # Flash effect for 300ms
            h, w = frame.shape[:2]
            color = self.color_map.get(gesture, (255, 255, 255))
            alpha = 1.0 - ((current_time - self.flash_time) / 0.3)
            
            # Draw border flash
            thickness = int(10 * alpha)
            cv2.rectangle(frame, (0, 0), (w, h), color, thickness)
        elif current_time - self.flash_time >= 0.3:
            self.gesture_flash = None


# ============================================================================
# BROWSER CONTROL EXECUTOR
# ============================================================================

class BrowserController:
    """
    Executes browser control actions using PyAutoGUI.
    
    Handles:
        - Mouse movement with smoothing
        - Scrolling
        - Clicking
        - Browser navigation (back/forward)
    """
    
    def __init__(self):
        """Initialize browser controller"""
        pyautogui.FAILSAFE = Config.PYAUTOGUI_FAILSAFE
        pyautogui.PAUSE = 0.01  # Small pause between actions
        
        self.prev_mouse_x = Config.SCREEN_WIDTH // 2
        self.prev_mouse_y = Config.SCREEN_HEIGHT // 2
        
        # Velocity buffer for ultra-smooth movement
        self.velocity_buffer_x = [0.0] * Config.POINTER_VELOCITY_BUFFER
        self.velocity_buffer_y = [0.0] * Config.POINTER_VELOCITY_BUFFER
        self.buffer_index = 0
    
    def move_mouse(self, hand_landmarks):
        """
        Move mouse cursor based on index finger position.
        
        ULTRA SMOOTH: Advanced smoothing with velocity buffer
        - Increased smoothing factor (0.35) for silky movement
        - Velocity averaging over 3 frames for consistent motion
        - Gentler acceleration curve
        - Minimum movement threshold to prevent stuttering
        - Sub-pixel interpolation for fluid tracking
        
        Args:
            hand_landmarks: MediaPipe hand landmarks
        """
        # Get index finger tip position (normalized 0-1)
        index_tip = hand_landmarks.landmark[HandGestureRecognizer.INDEX_TIP]
        
        # Configurable coordinate mapping
        if Config.POINTER_INVERT_X:
            screen_x = int((1 - index_tip.x) * Config.SCREEN_WIDTH)
        else:
            screen_x = int(index_tip.x * Config.SCREEN_WIDTH)
        
        if Config.POINTER_INVERT_Y:
            screen_y = int((1 - index_tip.y) * Config.SCREEN_HEIGHT)
        else:
            screen_y = int(index_tip.y * Config.SCREEN_HEIGHT)
        
        # Calculate movement delta
        delta_x = screen_x - self.prev_mouse_x
        delta_y = screen_y - self.prev_mouse_y
        movement_magnitude = (delta_x**2 + delta_y**2) ** 0.5
        
        # SMOOTHNESS #1: Dead zone - ignore tiny movements (prevents jitter)
        if movement_magnitude < Config.MOUSE_DEAD_ZONE * Config.SCREEN_WIDTH:
            return  # No movement, stay at current position
        
        # SMOOTHNESS #2: Velocity buffer averaging for consistent motion
        # Store current velocity in circular buffer
        self.velocity_buffer_x[self.buffer_index] = delta_x
        self.velocity_buffer_y[self.buffer_index] = delta_y
        self.buffer_index = (self.buffer_index + 1) % Config.POINTER_VELOCITY_BUFFER
        
        # Average velocities over buffer for smooth transitions
        avg_delta_x = sum(self.velocity_buffer_x) / Config.POINTER_VELOCITY_BUFFER
        avg_delta_y = sum(self.velocity_buffer_y) / Config.POINTER_VELOCITY_BUFFER
        
        # Use averaged deltas for smoother movement
        delta_x = avg_delta_x
        delta_y = avg_delta_y
        movement_magnitude = (delta_x**2 + delta_y**2) ** 0.5
        
        # PRECISION ENHANCEMENT: Dual-zone sensitivity
        # Detect if cursor is in precision zone (center area)
        sensitivity_multiplier = 1.0
        if Config.POINTER_PRECISION_MODE:
            # Calculate distance from screen center (normalized 0-1)
            center_x = Config.SCREEN_WIDTH / 2
            center_y = Config.SCREEN_HEIGHT / 2
            dist_from_center_x = abs(self.prev_mouse_x - center_x) / (Config.SCREEN_WIDTH / 2)
            dist_from_center_y = abs(self.prev_mouse_y - center_y) / (Config.SCREEN_HEIGHT / 2)
            max_dist_from_center = max(dist_from_center_x, dist_from_center_y)
            
            # If in precision zone (center area), reduce sensitivity for fine control
            if max_dist_from_center < Config.POINTER_PRECISION_ZONE:
                # Smoothly transition from precision to normal based on distance
                precision_factor = 1 - (max_dist_from_center / Config.POINTER_PRECISION_ZONE)
                sensitivity_multiplier = 1.0 - (precision_factor * (1.0 - Config.POINTER_PRECISION_MULTIPLIER))
            
            # If near edges, boost speed to reach corners easily
            elif max_dist_from_center > 0.85:
                edge_factor = (max_dist_from_center - 0.85) / 0.15  # 0-1 scale near edges
                sensitivity_multiplier = 1.0 + (edge_factor * (Config.POINTER_EDGE_BOOST - 1.0))
        
        # Apply sensitivity multiplier to deltas
        delta_x = delta_x * sensitivity_multiplier
        delta_y = delta_y * sensitivity_multiplier
        screen_x = self.prev_mouse_x + delta_x
        screen_y = self.prev_mouse_y + delta_y
        
        # SMOOTHNESS #3: Velocity-based dynamic smoothing
        # Fast movements = less smoothing (responsive), slow movements = more smoothing (precise)
        normalized_velocity = min(movement_magnitude / 80.0, 1.0)  # 0-1 scale (lowered threshold)
        dynamic_smoothing = Config.MOUSE_SMOOTHING * (1 - normalized_velocity * 0.3)  # Gentler variation
        
        # SMOOTHNESS #4: Gentler acceleration curve
        if movement_magnitude > 50:  # Increased threshold for smoother feel
            # Smoother acceleration curve using square root
            accel_factor = 1.0 + (min(movement_magnitude / 150.0, 1.0) * (Config.MOUSE_ACCELERATION - 1.0))
            delta_x = delta_x * accel_factor
            delta_y = delta_y * accel_factor
            screen_x = self.prev_mouse_x + delta_x
            screen_y = self.prev_mouse_y + delta_y
        
        # Apply dynamic smoothing
        smooth_x = self.prev_mouse_x * dynamic_smoothing + screen_x * (1 - dynamic_smoothing)
        smooth_y = self.prev_mouse_y * dynamic_smoothing + screen_y * (1 - dynamic_smoothing)
        
        # SMOOTHNESS #5: Minimum movement threshold (prevents micro-stuttering)
        final_delta_x = smooth_x - self.prev_mouse_x
        final_delta_y = smooth_y - self.prev_mouse_y
        if abs(final_delta_x) < Config.POINTER_MIN_MOVEMENT and abs(final_delta_y) < Config.POINTER_MIN_MOVEMENT:
            return  # Movement too small, skip to prevent stuttering
        
        smooth_x = int(smooth_x)
        smooth_y = int(smooth_y)
        
        # SMOOTHNESS #6: Edge dampening - gentle slowdown at screen edges
        edge_damping = 1.0
        if smooth_x < Config.MOUSE_EDGE_PADDING:
            edge_damping *= max(0.4, smooth_x / Config.MOUSE_EDGE_PADDING)  # Gentler min speed (40%)
        elif smooth_x > Config.SCREEN_WIDTH - Config.MOUSE_EDGE_PADDING:
            edge_damping *= max(0.4, (Config.SCREEN_WIDTH - smooth_x) / Config.MOUSE_EDGE_PADDING)
        
        if smooth_y < Config.MOUSE_EDGE_PADDING:
            edge_damping *= max(0.4, smooth_y / Config.MOUSE_EDGE_PADDING)
        elif smooth_y > Config.SCREEN_HEIGHT - Config.MOUSE_EDGE_PADDING:
            edge_damping *= max(0.4, (Config.SCREEN_HEIGHT - smooth_y) / Config.MOUSE_EDGE_PADDING)
        
        # Apply edge dampening to movement
        if edge_damping < 1.0:
            smooth_x = int(self.prev_mouse_x + (smooth_x - self.prev_mouse_x) * edge_damping)
            smooth_y = int(self.prev_mouse_y + (smooth_y - self.prev_mouse_y) * edge_damping)
        
        # Clamp to screen bounds
        smooth_x = max(0, min(Config.SCREEN_WIDTH - 1, smooth_x))
        smooth_y = max(0, min(Config.SCREEN_HEIGHT - 1, smooth_y))
        
        # OPTIMIZATION: Single mouse movement (removed duplicate code block)
        # Duration=0 for instant move, smoothing already handled by velocity buffer
        pyautogui.moveTo(smooth_x, smooth_y, duration=0)
        
        # Store for next frame (only once)
        self.prev_mouse_x = smooth_x
        self.prev_mouse_y = smooth_y
    
    def scroll_down(self):
        """
        Scroll webpage down.
        
        ENHANCED: Configurable sensitivity profiles (low/medium/high)
        OPTIMIZED: Reduced loop overhead, single scroll call when possible
        """
        total_scroll = int(Config.SCROLL_BASE_AMOUNT * Config.SCROLL_SPEED_MULTIPLIER)
        
        # OPTIMIZATION: If smooth steps = 1, do single scroll (avoids loop overhead)
        if Config.SCROLL_SMOOTH_STEPS == 1:
            pyautogui.scroll(-total_scroll)
            return
        
        step = total_scroll // Config.SCROLL_SMOOTH_STEPS
        
        # Smooth scrolling in increments with profile-specific delay
        for i in range(Config.SCROLL_SMOOTH_STEPS):
            pyautogui.scroll(-step)
            if i < Config.SCROLL_SMOOTH_STEPS - 1:  # Skip sleep on last iteration
                time.sleep(Config.SCROLL_STEP_DELAY)
    
    def scroll_up(self):
        """
        Scroll webpage up.
        
        ENHANCED: Configurable sensitivity profiles (low/medium/high)
        OPTIMIZED: Reduced loop overhead, single scroll call when possible
        """
        total_scroll = int(Config.SCROLL_BASE_AMOUNT * Config.SCROLL_SPEED_MULTIPLIER)
        
        # OPTIMIZATION: If smooth steps = 1, do single scroll (avoids loop overhead)
        if Config.SCROLL_SMOOTH_STEPS == 1:
            pyautogui.scroll(total_scroll)
            return
        
        step = total_scroll // Config.SCROLL_SMOOTH_STEPS
        
        # Smooth scrolling in increments with profile-specific delay
        for i in range(Config.SCROLL_SMOOTH_STEPS):
            pyautogui.scroll(step)
            if i < Config.SCROLL_SMOOTH_STEPS - 1:  # Skip sleep on last iteration
                time.sleep(Config.SCROLL_STEP_DELAY)
    
    def left_click(self):
        """Perform left mouse click"""
        pyautogui.click()
    
    def right_click(self):
        """Perform right mouse click"""
        pyautogui.rightClick()
    
    def browser_back(self):
        """Navigate browser back"""
        pyautogui.hotkey('alt', 'left')
    
    def browser_forward(self):
        """Navigate browser forward"""
        pyautogui.hotkey('alt', 'right')
    
    def take_screenshot(self):
        """Take screenshot and save"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        return filename
    
    def refresh_page(self):
        """Refresh current page"""
        pyautogui.hotkey('ctrl', 'r')
    
    def zoom_in(self):
        """
        Zoom in webpage.
        
        REFINEMENT #4: Smooth incremental zoom for better visual experience.
        OPTIMIZED: Skip delay on last step.
        """
        for i in range(Config.ZOOM_SMOOTH_STEPS):
            pyautogui.hotkey('ctrl', '+')
            if i < Config.ZOOM_SMOOTH_STEPS - 1:
                time.sleep(Config.ZOOM_STEP_DELAY)  # Creates smooth zoom animation
    
    def zoom_out(self):
        """
        Zoom out webpage.
        
        REFINEMENT #4: Smooth incremental zoom for better visual experience.
        OPTIMIZED: Skip delay on last step.
        """
        for i in range(Config.ZOOM_SMOOTH_STEPS):
            pyautogui.hotkey('ctrl', '-')
            if i < Config.ZOOM_SMOOTH_STEPS - 1:
                time.sleep(Config.ZOOM_STEP_DELAY)  # Creates smooth zoom animation
    
    def fullscreen_toggle(self):
        """Toggle fullscreen mode"""
        pyautogui.press('f11')
    
    def copy(self):
        """Copy selected text/content"""
        pyautogui.hotkey('ctrl', 'c')
    
    def paste(self):
        """Paste clipboard content"""
        pyautogui.hotkey('ctrl', 'v')
    
    def close_browser(self):
        """Close entire browser window"""
        pyautogui.hotkey('alt', 'f4')
    
    def new_tab(self):
        """Open new browser tab"""
        pyautogui.hotkey('ctrl', 't')
    
    def close_tab(self):
        """Close current tab"""
        pyautogui.hotkey('ctrl', 'w')
    
    def next_tab(self):
        """Switch to next tab"""
        pyautogui.hotkey('ctrl', 'tab')
    
    def previous_tab(self):
        """Switch to previous tab"""
        pyautogui.hotkey('ctrl', 'shift', 'tab')
    
    def copy_text(self):
        """Copy selected text"""
        pyautogui.hotkey('ctrl', 'c')
    
    def paste_text(self):
        """Paste from clipboard"""
        pyautogui.hotkey('ctrl', 'v')
    
    def mute_toggle(self):
        """
        Toggle system mute.
        
        REFINEMENT #5: Controlled execution (timing handled in execute_gesture_action).
        """
        pyautogui.press('volumemute')
    
    def launch_browser(self):
        """
        Launch browser using OS-specific commands.
        
        REFINEMENT #6: Keyboard shortcut to open browser (configurable target).
        OPTIMIZED: Uses module-level imports.
        """
        browser = Config.BROWSER_LAUNCH_TARGET.lower()
        system = platform.system()
        
        try:
            if system == 'Windows':
                if browser == 'chrome':
                    subprocess.Popen(['start', 'chrome'], shell=True)
                elif browser == 'edge':
                    subprocess.Popen('start microsoft-edge:', shell=True)
                elif browser == 'firefox':
                    subprocess.Popen('start firefox', shell=True)
                else:  # default browser
                    subprocess.Popen('start http://', shell=True)
            elif system == 'Darwin':  # macOS
                if browser == 'chrome':
                    subprocess.Popen(['open', '-a', 'Google Chrome'])
                elif browser == 'firefox':
                    subprocess.Popen(['open', '-a', 'Firefox'])
                else:
                    subprocess.Popen(['open', 'http://'])
            else:  # Linux
                if browser == 'chrome':
                    subprocess.Popen(['google-chrome'])
                elif browser == 'firefox':
                    subprocess.Popen(['firefox'])
                else:
                    subprocess.Popen(['xdg-open', 'http://'])
        except Exception as e:
            print(f"WARNING: Could not launch browser: {e}")
    
    def volume_up(self):
        """Increase system volume"""
        pyautogui.press('volumeup')
    
    def volume_down(self):
        """Decrease system volume"""
        pyautogui.press('volumedown')


# ============================================================================
# MAIN APPLICATION
# ============================================================================

class HandGestureControlSystem:
    """
    Main application class that orchestrates the entire system.
    
    Combines:
        - Video capture
        - Hand detection
        - Gesture recognition
        - Stabilization
        - Browser control
    """
    
    def __init__(self, socketio=None):
        """Initialize all system components
        
        Args:
            socketio: Optional Flask-SocketIO instance for web dashboard integration
        """
        print("\n" + "="*70)
        print("🚀 GESTURA - Hand Gesture Control System")
        print("="*70)
        print("Initializing components...")
        
        # Web integration (optional)
        self.socketio = socketio
        self.web_frame_counter = 0  # Throttle frame emission
        
        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands  # type: ignore
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=Config.MAX_NUM_HANDS,
            min_detection_confidence=Config.MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=Config.MIN_TRACKING_CONFIDENCE
        )
        self.mp_draw = mp.solutions.drawing_utils  # type: ignore
        
        # Initialize components
        self.recognizer = HandGestureRecognizer()
        self.stabilizer = GestureStabilizer()
        self.state_machine = GestureStateMachine()  # CRITICAL: State machine enforcement
        self.controller = BrowserController()
        self.history = GestureHistory() if Config.ENABLE_GESTURE_HISTORY else None
        self.visual_effects = VisualEffects() if Config.ENABLE_VISUAL_TRAILS else None
        
        # Video capture with validation
        self.cap = cv2.VideoCapture(Config.CAMERA_INDEX)
        
        # SAFETY: Verify camera opened successfully with detailed error handling
        if not self.cap.isOpened():
            error_msg = (
                f"\n{'='*70}\n"
                f"❌ CAMERA INITIALIZATION FAILED\n"
                f"{'='*70}\n\n"
                f"Failed to open camera at index {Config.CAMERA_INDEX}.\n\n"
                f"Common solutions:\n"
                f"  1. ���️ Check camera connection - Ensure webcam is plugged in\n"
                f"  2. 🔒 Grant camera permissions - Check Windows Privacy Settings\n"
                f"  3. ❌ Close conflicting apps - Zoom, Teams, or other webcam apps may be using camera\n"
                f"  4. 🔄 Try different camera index - Change Config.CAMERA_INDEX (0, 1, 2...)\n"
                f"  5. 🔌 Replug your webcam and restart the application\n\n"
                f"💡 Quick Fix: Open Windows Settings → Privacy → Camera → Allow apps to access camera\n"
                f"\n{'='*70}\n"
            )
            print(error_msg)
            raise RuntimeError(error_msg)
        
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, Config.FRAME_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, Config.FRAME_HEIGHT)
        self.cap.set(cv2.CAP_PROP_FPS, Config.FPS_TARGET)
        
        # Performance tracking
        self.fps = 0
        self.frame_count = 0
        self.start_time = time.time()
        
        # OPTIMIZATION: Cache gesture names to avoid repeated string operations
        self._gesture_name_cache = {}
        for gesture_type in GestureType:
            self._gesture_name_cache[gesture_type] = gesture_type.name.replace('_', ' ')
        
        # OPTIMIZATION: Frame rate limiting for CPU efficiency
        self._target_frame_time = 1.0 / Config.FPS_TARGET  # ~33ms for 30 FPS
        self._last_frame_time = time.time()
        
        # Program control
        self.running = True  # Flag to control main loop (for rock sign exit)
        
        # Verify all components initialized
        components_status = [
            ("✅ Camera", self.cap.isOpened()),
            ("✅ Hand Detection (MediaPipe)", self.hands is not None),
            ("✅ Gesture Recognizer", self.recognizer is not None),
            ("✅ Stabilizer", self.stabilizer is not None),
            ("✅ Controller", self.controller is not None),
        ]
        
        print("\n📋 Component Status:")
        for component, status in components_status:
            status_icon = "✅" if status else "❌"
            print(f"   {status_icon} {component.split(' ', 1)[1]}")
        
        print("\n✅ System initialized successfully!")
        print(f"📹 Camera Resolution: {Config.FRAME_WIDTH}x{Config.FRAME_HEIGHT} @ {Config.FPS_TARGET} FPS")
        print(f"🖥️  Screen Resolution: {Config.SCREEN_WIDTH}x{Config.SCREEN_HEIGHT}")
        print("\n" + "="*70)
        print("GESTURE CONTROLS:")
        print("="*70)
        print("  SCROLLING:")
        print("    [PALM] Open Palm       -> Scroll Down (fast!)")
        print("    ✊ Closed Fist     → Scroll Up (fast!)")
        print("\n  MOUSE CONTROL:")
        print("    ☝️ Index Finger     → Move Mouse (Pointer Mode)")
        print("    � Thumb Out        → Click! (show thumb to click)")
        print("    [PEACE] Peace Sign      -> Click (alternative)")
        print("\n  NAVIGATION:")
        print("    👈 Swipe Left      → Browser Back")
        print("    👉 Swipe Right     → Browser Forward")
        print("    [UP] Swipe Up        -> Next Tab")
        print("    [DOWN] Swipe Down      -> Previous Tab")
        print("\n  PAGE ACTIONS:")
        print("    [3-FINGERS] Three Fingers   -> Screenshot")
        print("    [4-FINGERS] Four Fingers    -> Refresh Page")
        print("    👍 Thumb Up        → Zoom In")
        print("    👎 Thumb Down      → Close Tab")
        print("\n  ADVANCED:")
        print("    👌 OK Sign         → New Tab")
        print("    🤘 Rock Sign       → Copy")
        print("    🤙 Call Sign       → Paste")
        print("    🤏 Pinch           → Zoom In (close fingers)")
        print("    [SPREAD] Spread          -> Zoom Out (open fingers)")
        print("    🤙 Pinky Only      → Mute/Unmute")
        print("="*70)
        print("\nKEYBOARD SHORTCUTS:")
        print(f"    'q' - Quit | 's' - Stats | 'h' - Toggle UI | 'b' - Launch {Config.BROWSER_LAUNCH_TARGET.title()}")
        print("="*70 + "\n")
    
    def execute_gesture_action(self, gesture, hand_landmarks, is_first_confirmation=False):
        """
        Execute browser action based on detected gesture.
        HACKATHON VERSION: Only 8 essential gestures supported.
        
        State machine handles timing confirmation.
        This function trusts confirmed gestures and executes actions cleanly.
        
        Args:
            gesture: GestureType to execute (already confirmed by state machine)
            hand_landmarks: MediaPipe hand landmarks
            is_first_confirmation: True if this is first frame of CONFIRMED state
        """
        if gesture == GestureType.NONE:
            # Reset all gesture timers when no gesture detected
            self.recognizer.scroll_gesture_start_time = 0.0
            self.recognizer.scroll_last_gesture = GestureType.NONE
            self.recognizer.browser_nav_gesture_start_time = 0.0
            self.recognizer.browser_nav_last_gesture = GestureType.NONE
            self.recognizer.close_browser_gesture_start_time = 0.0
            self.recognizer.close_browser_last_gesture = GestureType.NONE
            self.recognizer.mute_gesture_start_time = 0.0
            
            # Exit POINTER_MODE when no gesture
            if Config.ENABLE_MODE_SEPARATION and self.recognizer.current_mode == 'POINTER':
                if time.time() - self.recognizer.mode_switch_time > Config.MODE_SWITCH_DEBOUNCE:
                    self.recognizer.current_mode = 'GESTURE'
            return
        
        # Mode management: INDEX_ONLY triggers POINTER_MODE
        current_time = time.time()
        if Config.ENABLE_MODE_SEPARATION:
            if gesture == GestureType.INDEX_ONLY:
                if self.recognizer.current_mode != 'POINTER':
                    self.recognizer.current_mode = 'POINTER'
                    self.recognizer.mode_switch_time = current_time
                    if Config.DEBUG_GESTURE_DETECTION:
                        print("[POINTER MODE] activated")
            else:
                # Any other gesture switches back to GESTURE_MODE
                if self.recognizer.current_mode == 'POINTER':
                    if current_time - self.recognizer.mode_switch_time > Config.MODE_SWITCH_DEBOUNCE:
                        self.recognizer.current_mode = 'GESTURE'
                        if Config.DEBUG_GESTURE_DETECTION:
                            print("[GESTURE MODE] activated")
        
        # Check debounce for non-continuous actions
        if gesture not in [GestureType.INDEX_ONLY]:
            if not self.stabilizer.should_execute_action(gesture):
                return
        
        # === EXECUTE ACTIONS (8 essential gestures only) ===
        try:
            # 1. SCROLL DOWN - Open palm (5 fingers)
            if gesture == GestureType.OPEN_PALM:
                if current_time - self.recognizer.scroll_last_action_time < Config.SCROLL_CONTINUOUS_DELAY:
                    return
                
                self.controller.scroll_down()
                print("[SCROLL DOWN] ✋ Open palm → Scrolling down")
                self.recognizer.scroll_last_action_time = current_time
                self.recognizer.scroll_last_gesture = gesture
                
                # Web: Emit gesture event
                if self.socketio:
                    self.socketio.emit('gesture_detected', {
                        'gesture': 'OPEN_PALM',
                        'action': 'Scroll Down',
                        'timestamp': current_time
                    })
            
            # 2. SCROLL UP - Closed fist (0 fingers)
            elif gesture == GestureType.CLOSED_FIST:
                if current_time - self.recognizer.scroll_last_action_time < Config.SCROLL_CONTINUOUS_DELAY:
                    return
                
                self.controller.scroll_up()
                print("[SCROLL UP] ✊ Closed fist → Scrolling up")
                self.recognizer.scroll_last_action_time = current_time
                self.recognizer.scroll_last_gesture = gesture
                
                # Web: Emit gesture event
                if self.socketio:
                    self.socketio.emit('gesture_detected', {
                        'gesture': 'CLOSED_FIST',
                        'action': 'Scroll Up',
                        'timestamp': current_time
                    })
            
            # 3. POINTER MODE - Index finger only (continuous)
            elif gesture == GestureType.INDEX_ONLY:
                # Continuous mouse movement (no debounce)
                # State machine marks this as CONTINUOUS_GESTURE
                self.controller.move_mouse(hand_landmarks)
            
            # 4. LEFT CLICK - Three fingers (index, middle, ring)
            elif gesture == GestureType.THREE_FINGERS:
                self.controller.left_click()
                print("[CLICK] 🖖 Three fingers → Left click")
                
                # Web: Emit gesture event
                if self.socketio:
                    self.socketio.emit('gesture_detected', {
                        'gesture': 'THREE_FINGERS',
                        'action': 'Left Click',
                        'timestamp': current_time
                    })
            
            # 5. REFRESH PAGE - Four fingers (4 fingers, thumb curled)
            elif gesture == GestureType.FOUR_FINGERS:
                self.controller.refresh_page()
                print("[REFRESH] 🖐️ Four fingers → Refresh page")
            
            # 6. ZOOM IN - Thumb up
            elif gesture == GestureType.THUMB_UP:
                self.controller.zoom_in()
                print("[ZOOM IN] 👍 Thumb up → Zoom in")
            
            # 7. PEACE SIGN - Alternative click (optional)
            elif gesture == GestureType.PEACE_SIGN:
                self.controller.left_click()
                print("[CLICK] ✌️ Peace sign → Left click")
                
                # Web: Emit gesture event
                if self.socketio:
                    self.socketio.emit('gesture_detected', {
                        'gesture': 'PEACE_SIGN',
                        'action': 'Left Click',
                        'timestamp': current_time
                    })
            
            # 8. EXIT PROGRAM - Rock sign (CRITICAL: requires 1.5s hold)
            elif gesture == GestureType.ROCK_SIGN:
                # Check cooldown
                if current_time - self.recognizer.close_browser_last_action_time < Config.CLOSE_BROWSER_COOLDOWN:
                    return
                
                # Initialize dwell timer
                if self.recognizer.close_browser_last_gesture != gesture:
                    self.recognizer.close_browser_gesture_start_time = current_time
                    self.recognizer.close_browser_last_gesture = gesture
                    print("[EXIT PROGRAM] 🤘 Rock sign detected - HOLD for 1.5s to EXIT...")
                    return
                
                # Check dwell time (1.5s hold required)
                elapsed = current_time - self.recognizer.close_browser_gesture_start_time
                if elapsed >= Config.CLOSE_BROWSER_DWELL_TIME:
                    print(f"[EXIT PROGRAM] 🤘 Rock sign held {elapsed:.1f}s → Exiting program...")
                    self.running = False  # Stop main loop
                    return
                else:
                    # Show progress every 0.3s
                    progress = int(elapsed / Config.CLOSE_BROWSER_DWELL_TIME * 100)
                    if progress % 30 == 0 and progress > 0:
                        print(f"[EXIT PROGRAM] 🤘 Hold... {progress}% ({elapsed:.1f}s / {Config.CLOSE_BROWSER_DWELL_TIME}s)")
            
            # 9. CLOSE BROWSER - Call Me gesture (COMFORTABLE & UNIQUE: requires 1.5s hold)
            elif gesture == GestureType.CALL_ME:
                # Check cooldown
                if current_time - self.recognizer.close_browser_last_action_time < Config.CLOSE_BROWSER_COOLDOWN:
                    return
                
                # Initialize dwell timer
                if self.recognizer.close_browser_last_gesture != gesture:
                    self.recognizer.close_browser_gesture_start_time = current_time
                    self.recognizer.close_browser_last_gesture = gesture
                    print("[CLOSE BROWSER] 🤙 Call Me gesture detected - HOLD for 1.5s to CLOSE BROWSER...")
                    return
                
                # Check dwell time (1.5s hold required)
                elapsed = current_time - self.recognizer.close_browser_gesture_start_time
                if elapsed >= Config.CLOSE_BROWSER_DWELL_TIME:
                    self.controller.close_browser()
                    print(f"[CLOSE BROWSER] 🤙 Call Me held {elapsed:.1f}s → Closing browser (Alt+F4)")
                    self.recognizer.close_browser_last_action_time = current_time
                    self.recognizer.close_browser_last_gesture = GestureType.NONE
                else:
                    # Show progress every 0.3s
                    progress = int(elapsed / Config.CLOSE_BROWSER_DWELL_TIME * 100)
                    if progress % 30 == 0 and progress > 0:
                        print(f"[CLOSE BROWSER] 🤙 Hold... {progress}% ({elapsed:.1f}s / {Config.CLOSE_BROWSER_DWELL_TIME}s)")
            
            # 10. PASTE - Okay sign (thumb+index circle)
            elif gesture == GestureType.OKAY_SIGN:
                self.controller.paste()
                print("[PASTE] 👌 Okay sign → Paste (Ctrl+V)")
            
            # 11. BROWSER BACK - Swipe left
            elif gesture == GestureType.SWIPE_LEFT:
                # Check cooldown
                if current_time - self.recognizer.browser_nav_last_action_time < Config.BROWSER_NAV_COOLDOWN:
                    return
                
                # Initialize dwell timer
                if self.recognizer.browser_nav_last_gesture != gesture:
                    self.recognizer.browser_nav_gesture_start_time = current_time
                    self.recognizer.browser_nav_last_gesture = gesture
                    return
                
                # Check dwell time
                if current_time - self.recognizer.browser_nav_gesture_start_time >= Config.BROWSER_NAV_DWELL_TIME:
                    self.controller.browser_back()
                    print("[BROWSER BACK] ← Swipe left → Navigate back")
                    self.recognizer.browser_nav_last_action_time = current_time
                    self.recognizer.browser_nav_last_gesture = GestureType.NONE
            
            # 9. BROWSER FORWARD - Swipe right
            elif gesture == GestureType.SWIPE_RIGHT:
                # Check cooldown
                if current_time - self.recognizer.browser_nav_last_action_time < Config.BROWSER_NAV_COOLDOWN:
                    return
                
                # Initialize dwell timer
                if self.recognizer.browser_nav_last_gesture != gesture:
                    self.recognizer.browser_nav_gesture_start_time = current_time
                    self.recognizer.browser_nav_last_gesture = gesture
                    return
                
                # Check dwell time
                if current_time - self.recognizer.browser_nav_gesture_start_time >= Config.BROWSER_NAV_DWELL_TIME:
                    self.controller.browser_forward()
                    print("[BROWSER FORWARD] → Swipe right → Navigate forward")
                    self.recognizer.browser_nav_last_action_time = current_time
                    self.recognizer.browser_nav_last_gesture = GestureType.NONE
            
            # 10. MUTE TOGGLE - Pinky only (accessibility feature)
            elif gesture == GestureType.PINKY_ONLY:
                # Check cooldown
                if current_time - self.recognizer.mute_last_action_time < Config.MUTE_TOGGLE_COOLDOWN:
                    return
                
                # BUGFIX: Initialize dwell timer (check for 0.0, not None - consistent with init)
                if self.recognizer.mute_gesture_start_time == 0.0:
                    self.recognizer.mute_gesture_start_time = current_time
                    return
                
                # Check dwell time
                if current_time - self.recognizer.mute_gesture_start_time >= Config.MUTE_TOGGLE_DWELL_TIME:
                    self.controller.mute_toggle()
                    print("[MUTE TOGGLE] 🤙 Pinky gesture → Mute toggled")
                    self.recognizer.mute_last_action_time = current_time
                    self.recognizer.mute_gesture_start_time = 0.0
            
            # Add to history
            if self.history:
                self.history.add(gesture)
            
            # Trigger visual feedback
            if self.visual_effects:
                self.visual_effects.flash_gesture(gesture)
        
        except Exception as e:
            print(f"WARNING: Action execution error: {e}")
    
    def draw_info_overlay(self, frame, gesture, hand_landmarks):
        """
        Draw enhanced information overlay on frame.
        
        Args:
            frame: OpenCV frame
            gesture: Current stable gesture
            hand_landmarks: MediaPipe hand landmarks
        """
        height, width, _ = frame.shape
        
        # Draw hand landmarks
        if hand_landmarks:
            self.mp_draw.draw_landmarks(
                frame, 
                hand_landmarks,
                self.mp_hands.HAND_CONNECTIONS,
                self.mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=3),
                self.mp_draw.DrawingSpec(color=(255, 255, 255), thickness=2)
            )
            
            # Add trail effect for index finger
            if Config.ENABLE_VISUAL_TRAILS and self.visual_effects:
                index_tip = hand_landmarks.landmark[HandGestureRecognizer.INDEX_TIP]
                trail_x = int(index_tip.x * width)
                trail_y = int(index_tip.y * height)
                self.visual_effects.add_trail_point(trail_x, trail_y)
                self.visual_effects.draw_trail(frame)
        
        # Draw gesture flash effect
        if self.visual_effects:
            self.visual_effects.draw_gesture_flash(frame, gesture)
        
        # Main info box (top-left)
        info_height = 180 if Config.is_advanced_ui_enabled() else 120
        cv2.rectangle(frame, (10, 10), (450, info_height), (0, 0, 0), -1)
        cv2.rectangle(frame, (10, 10), (450, info_height), (0, 255, 0), 2)
        
        # Display FPS with color coding and performance indicator
        fps_color = (0, 255, 0) if self.fps >= 27 else (0, 255, 255) if self.fps >= 20 else (0, 0, 255)
        fps_status = "⭐ Optimal" if self.fps >= 27 else "⚠️ Low" if self.fps >= 20 else "❌ Poor"
        cv2.putText(frame, f"FPS: {self.fps:.1f} {fps_status}", (20, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, fps_color, 2)
        
        # Display current gesture with color
        # OPTIMIZATION: Use cached gesture name (avoid string operations on every frame)
        gesture_name = self._gesture_name_cache.get(gesture, "NONE")
        gesture_color = self.visual_effects.color_map.get(gesture, (0, 255, 0)) if self.visual_effects else (0, 255, 0)
        cv2.putText(frame, f"Gesture: {gesture_name}", (20, 75),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, gesture_color, 2)
        
        # Display buffer status
        buffer_maxlen = self.stabilizer.buffer.maxlen if self.stabilizer.buffer.maxlen is not None else Config.GESTURE_BUFFER_SIZE
        buffer_fill = len(self.stabilizer.buffer) / buffer_maxlen
        buffer_text = f"Buffer: {len(self.stabilizer.buffer)}/{buffer_maxlen}"
        cv2.putText(frame, buffer_text, (20, 105),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
        
        # PHASE 4: Display CNN recognition status
        cnn_status_y = 135 if not Config.is_advanced_ui_enabled() else 165
        if self.recognizer.cnn_enabled and self.recognizer.cnn_classifier:
            cnn_color = (0, 255, 255)  # Cyan for CNN active
            cv2.putText(frame, "CNN: ON", (320, 40),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, cnn_color, 2)
        else:
            cv2.putText(frame, "Rule-based", (320, 40),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (150, 150, 150), 1)
        
        if Config.is_advanced_ui_enabled():
            # Display session stats
            if self.history:
                stats = self.history.get_session_stats()
                actions_text = f"Actions: {stats['total_actions']} ({stats['actions_per_minute']:.1f}/min)"
                cv2.putText(frame, actions_text, (20, 135),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
                
                # Auto-calibration status
                if self.recognizer.hand_size_baseline:
                    cv2.putText(frame, "✓ Calibrated", (20, 165),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        
        # Gesture hints (bottom)
        if Config.is_advanced_ui_enabled():
            hint_y = height - 100
            cv2.rectangle(frame, (10, hint_y), (width - 10, height - 10), (0, 0, 0), -1)
            
            hints = [
                "Palm: Scroll | Fist: Up | Index: Move | Peace: Click | Swipe: Nav",
                "3 Fingers: Screenshot | 4 Fingers: Refresh | Thumb: Zoom",
                "Press 'q' to quit | 's' for stats | 'h' to hide UI | 'c' to toggle CNN"
            ]
            
            for i, hint in enumerate(hints):
                cv2.putText(frame, hint, (20, hint_y + 25 + i*20),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        else:
            # Simple quit instruction
            cv2.putText(frame, "Press 'q' to quit | 's' for stats | 'c' to toggle CNN", (20, height - 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
        
        return frame
    
    def calculate_fps(self):
        """Calculate and update FPS counter"""
        self.frame_count += 1
        elapsed_time = time.time() - self.start_time
        
        if elapsed_time >= 1.0:
            self.fps = self.frame_count / elapsed_time
            self.frame_count = 0
            self.start_time = time.time()
    
    def run(self):
        """
        Main loop - processes video frames and controls browser.
        
        Process:
            1. Capture frame from webcam
            2. Detect hand using MediaPipe
            3. Recognize gesture from landmarks
            4. Stabilize gesture using buffer
            5. Execute browser control action
            6. Display visual feedback
        """
        print("[STARTING] Starting video capture...\n")
        
        # STABILITY: Camera retry logic for robustness
        max_retries = 3
        retry_count = 0
        
        try:
            while self.running and self.cap.isOpened():
                success, frame = self.cap.read()
                if not success:
                    retry_count += 1
                    if retry_count >= max_retries:
                        print("ERROR: Failed to capture frame after retries. Check camera.")
                        break
                    print(f"WARNING: Frame capture failed (retry {retry_count}/{max_retries})")
                    time.sleep(0.1)  # Brief pause before retry
                    continue
                
                # Reset retry counter on successful frame
                retry_count = 0
                
                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)
                
                # Convert BGR to RGB for MediaPipe
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Process frame with MediaPipe
                results = self.hands.process(rgb_frame)
                
                # Initialize variables
                current_gesture = GestureType.NONE
                hand_landmarks = None
                
                # If hand detected, recognize gesture
                if results.multi_hand_landmarks:
                    hand_landmarks = results.multi_hand_landmarks[0]
                    
                    # PERFORMANCE IMPROVEMENT: Smooth landmark coordinates
                    # Reduces hand tremor, improves pointer stability and swipe consistency
                    # Pipeline: Raw landmarks → EMA smoothing → Smoothed landmarks
                    if self.recognizer.smoothing_pipeline is not None:
                        # Smooth coordinates (reduces jitter in pointer mode)
                        # Note: smooth_landmarks modifies landmarks in-place
                        self.recognizer.smoothing_pipeline.smooth_landmarks(
                            hand_landmarks.landmark
                        )
                    
                    # PHASE 4: Hybrid CNN + Rule-based Recognition with temporal voting
                    current_gesture = self.recognizer.recognize_gesture_hybrid(hand_landmarks, frame)
                
                # STATE MACHINE: Update with current detection (enforces NONE→CANDIDATE→CONFIRMED→COOLDOWN)
                current_time = time.time()
                should_execute, confirmed_gesture, is_first_confirmation = self.state_machine.update(current_gesture, current_time)
                
                # FIX #1: Provide user feedback on first confirmation frame (dwell-based gestures)
                if is_first_confirmation and confirmed_gesture in self.state_machine.DWELL_GESTURES:
                    dwell_time = self.state_machine.DWELL_GESTURES[confirmed_gesture]
                    gesture_name = confirmed_gesture.name.replace('_', ' ')
                    print(f"[{gesture_name}] Detected! Hold for {dwell_time:.2f}s...")
                
                # STRICT GATING: Only execute if state machine confirms
                if should_execute and confirmed_gesture != GestureType.NONE:
                    # Execute action (state machine has confirmed gesture is stable)
                    # Pass is_first_confirmation to help action handler
                    self.execute_gesture_action(confirmed_gesture, hand_landmarks, is_first_confirmation)
                    
                    # FIX #1: Only trigger cooldown for non-continuous gestures
                    if confirmed_gesture not in self.state_machine.CONTINUOUS_GESTURES:
                        self.state_machine.trigger_cooldown(current_time)
                
                # For display: Use state machine's current gesture (not raw detection)
                display_gesture = confirmed_gesture if confirmed_gesture != GestureType.NONE else current_gesture
                
                # Draw overlay information
                frame = self.draw_info_overlay(frame, display_gesture, hand_landmarks)
                
                # Calculate FPS
                self.calculate_fps()
                
                # Web: Emit frame and metrics (throttled)
                self.web_frame_counter += 1
                if self.socketio and self.web_frame_counter % 10 == 0:  # Every 10th frame
                    # Emit metrics
                    self.socketio.emit('metrics_update', {
                        'fps': self.fps,
                        'gesture_count': 0,  # Can track this if needed
                        'timestamp': time.time()
                    })
                    
                    # Emit frame (optimized: every 90th frame for smooth web performance)
                    if self.web_frame_counter % 90 == 0:  # ~0.33 FPS for minimal latency
                        import base64
                        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 55])
                        frame_b64 = base64.b64encode(buffer.tobytes()).decode('utf-8')
                        self.socketio.emit('frame_update', {'image': frame_b64})
                
                # OPTIMIZATION: Frame rate limiting to prevent CPU waste
                # Target: 30 FPS = 33ms per frame. If frame processed faster, sleep briefly.
                current_frame_time = time.time()
                frame_elapsed = current_frame_time - self._last_frame_time
                if frame_elapsed < self._target_frame_time:
                    time.sleep(self._target_frame_time - frame_elapsed)
                self._last_frame_time = time.time()
                
                # Display frame
                cv2.imshow('Hand Gesture Control System', frame)
                
                # Check for quit command
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    print("\n[SHUTDOWN] Shutting down safely...")
                    break
                elif key == ord('s'):
                    # Show statistics
                    self.print_statistics()
                elif key == ord('h'):
                    # Toggle advanced UI
                    Config.toggle_advanced_ui()
                    print(f"Advanced UI: {'ON' if Config.is_advanced_ui_enabled() else 'OFF'}")
                elif key == ord('b') and Config.BROWSER_LAUNCH_ENABLED:
                    # REFINEMENT #6: Launch browser with 'b' key
                    print(f"[BROWSER] Launching {Config.BROWSER_LAUNCH_TARGET} browser...")
                    self.controller.launch_browser()
                elif key == ord('c'):
                    # PHASE 4: Toggle CNN classification on/off
                    if CNN_AVAILABLE:
                        self.recognizer.cnn_enabled = not self.recognizer.cnn_enabled
                        mode_str = "CNN + Rule-based" if self.recognizer.cnn_enabled else "Rule-based only"
                        print(f"[CNN MODE] Recognition mode: {mode_str}")
                        if self.recognizer.cnn_enabled and self.recognizer.cnn_classifier:
                            # Reset CNN buffers when re-enabling
                            self.recognizer.cnn_classifier.reset_buffers()
                            print("   CNN temporal voting buffers reset")
                    else:
                        print("WARNING: CNN module not available - using rule-based recognition only")
        
        except KeyboardInterrupt:
            print("\nWARNING: Interrupted by user")
        
        except Exception as e:
            print(f"\n[ERROR] Error: {e}")
        
        finally:
            self.cleanup()
    
    def print_statistics(self):
        """Print session statistics to console"""
        if not self.history:
            print("Statistics not available (history disabled)")
            return
        
        print("\n" + "="*60)
        print("SESSION STATISTICS")
        print("="*60)
        
        stats = self.history.get_session_stats()
        print(f"Duration: {stats['duration']:.1f} seconds")
        print(f"Total Actions: {stats['total_actions']}")
        print(f"Actions per Minute: {stats['actions_per_minute']:.1f}")
        print(f"Unique Gestures Used: {stats['unique_gestures']}")
        
        print("\nMost Used Gestures:")
        for gesture, count in self.history.get_most_used():
            print(f"  {gesture.replace('_', ' ')}: {count} times")
        
        print("\nRecent Gestures:")
        recent = self.history.get_recent(5)
        for entry in recent:
            gesture_name = entry['gesture'].name.replace('_', ' ')
            print(f"  - {gesture_name} (confidence: {entry['confidence']:.2f})")
        
        print("="*60 + "\n")
    
    def cleanup(self):
        """Clean up resources safely with detailed feedback"""
        print("\n" + "="*70)
        print("🧹 CLEANUP & SHUTDOWN")
        print("="*70)
        
        try:
            # Release camera
            if hasattr(self, 'cap') and self.cap is not None:
                self.cap.release()
                print("✅ Camera released successfully")
            
            # Close windows
            cv2.destroyAllWindows()
            print("✅ Display windows closed")
            
            # Close MediaPipe
            if hasattr(self, 'hands') and self.hands is not None:
                self.hands.close()
                print("✅ MediaPipe hands module closed")
            
            # Print session summary
            if self.frame_count > 0:
                duration = time.time() - self.start_time
                avg_fps = self.frame_count / duration if duration > 0 else 0
                print(f"\n📊 Session Statistics:")
                print(f"   Total Frames: {self.frame_count}")
                print(f"   Duration: {duration:.1f}s")
                print(f"   Average FPS: {avg_fps:.1f}")
            
        except Exception as e:
            print(f"⚠️ Cleanup warning (non-critical): {e}")
        finally:
            print("\n✅ Cleanup complete. Thank you for using Gestura!")
            print("="*70 + "\n")


# ============================================================================
# ENTRY POINT
# ============================================================================

def main():
    """Main entry point"""
    print("\n" + "="*60)
    print("  HAND GESTURE CONTROL SYSTEM FOR WEB BROWSERS")
    print("="*60 + "\n")
    
    # Create and run system
    system = HandGestureControlSystem()
    system.run()


if __name__ == "__main__":
    main()

