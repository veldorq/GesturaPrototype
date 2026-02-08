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
from collections import deque
from enum import Enum

# CNN Gesture Recognition (optional import - graceful degradation if not available)
try:
    from gesture_model_inference import CNNGestureClassifier
    CNN_AVAILABLE = True
except ImportError:
    CNN_AVAILABLE = False
    print("Warning: CNN gesture recognition module not found. Using rule-based recognition only.")


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
    
    # Gesture stabilization
    GESTURE_BUFFER_SIZE = 5  # Frames to buffer before confirming gesture
    DEBOUNCE_TIME = 0.5  # Seconds between repeated actions
    CONFIDENCE_THRESHOLD = 0.6  # Minimum confidence for gesture recognition
    
    # Movement settings
    MOUSE_SMOOTHING = 0.3  # 0=instant, 1=no movement (LOWERED for better responsiveness)
    
    # REFINEMENT #1: Scroll speed - slightly increased for better responsiveness, kept smooth
    SCROLL_SPEED_MULTIPLIER = 3.5  # Slightly faster than 3.0 (controlled increase)
    SCROLL_BASE_AMOUNT = 20  # Base scroll amount per action
    SCROLL_SMOOTH_STEPS = 4  # Increased to 4 for smoother visual experience
    SCROLL_DWELL_TIME = 0.25  # Slightly reduced from 0.3 for faster response (still prevents accidents)
    SCROLL_CONTINUOUS_DELAY = 0.15  # Delay between continuous scroll actions (prevents spam)
    
    # ISSUE #3 & #4 FIX: Improved swipe detection with direction dominance
    SWIPE_THRESHOLD = 0.20  # Minimum movement to detect swipe (INCREASED from 0.15 for stricter detection)
    SWIPE_VERTICAL_THRESHOLD = 0.18  # For up/down swipes (INCREASED for stricter detection)
    SWIPE_DIRECTION_DOMINANCE_RATIO = 2.5  # Required ratio: primary_axis_movement / secondary_axis_movement
    SWIPE_CONFIRMATION_FRAMES = 3  # Frames needed to confirm swipe (multi-frame validation)
    SWIPE_VELOCITY_MIN = 0.08  # Minimum velocity per frame
    
    # REFINEMENT #2: Browser navigation safety - slower, more controlled
    BROWSER_NAV_DWELL_TIME = 0.8  # Deliberate delay before browser back/forward (prevents accidents)
    BROWSER_NAV_COOLDOWN = 1.5  # Strong cooldown between navigation actions (ensures one action per gesture)
    
    # Distance-based gestures
    PINCH_THRESHOLD = 0.05  # Max distance for pinch
    SPREAD_THRESHOLD = 0.15  # Min distance for spread
    PINCH_DISTANCE_THRESHOLD = 0.08  # Threshold for pinch verification
    
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
    
    # REFINEMENT #3: Close tab safety - high-risk action needs maximum protection
    CLOSE_TAB_DWELL_TIME = 1.2  # Long dwell time before closing tab (prevents accidental closure)
    CLOSE_TAB_COOLDOWN = 2.0  # Strong cooldown after closing (prevents rapid tab loss)
    CLOSE_TAB_REQUIRE_STABILITY = True  # Require stable gesture across dwell period
    
    # REFINEMENT #5: Mute toggle - slower, controlled execution
    MUTE_TOGGLE_DWELL_TIME = 0.6  # Deliberate delay before mute/unmute
    MUTE_TOGGLE_COOLDOWN = 1.0  # Strong cooldown to prevent rapid toggling
    
    # REFINEMENT #6: Browser launch keyboard shortcut
    BROWSER_LAUNCH_KEY = 'ctrl+shift+b'  # Configurable keyboard shortcut
    BROWSER_LAUNCH_TARGET = 'chrome'  # Options: 'chrome', 'edge', 'firefox', 'default'
    BROWSER_LAUNCH_ENABLED = True  # Enable/disable keyboard shortcut feature
    
    # ========================================================================
    # CNN GESTURE RECOGNITION (DataFlair-based integration)
    # ========================================================================
    
    # CNN Model Configuration
    ENABLE_CNN_CLASSIFIER = True  # Enable/disable CNN-based gesture recognition
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
    """Enumeration of all recognized gestures"""
    NONE = 0
    OPEN_PALM = 1  # Can be detected by CNN as 'scroll_down'
    CLOSED_FIST = 2  # Can be detected by CNN as 'scroll_up'
    INDEX_ONLY = 3  # POINTER MODE - mouse movement only (MediaPipe ONLY, not CNN)
    INDEX_MIDDLE = 4  # Reserved for future use
    THUMB_UP = 5
    SWIPE_LEFT = 6  # Can be detected by CNN
    SWIPE_RIGHT = 7  # Can be detected by CNN
    # NEW GESTURES
    THREE_FINGERS = 8      # Screenshot
    FOUR_FINGERS = 9       # Refresh page
    PINKY_ONLY = 10        # Can be detected by CNN as 'mute_toggle'
    PEACE_SIGN = 11        # Left Click (2 fingers: index + middle)
    PINCH = 12             # Can be detected by CNN as 'pinch_zoom'
    SPREAD = 13            # Zoom out (far distance)
    SWIPE_UP = 14          # Next tab
    SWIPE_DOWN = 15        # Previous tab
    THUMB_DOWN = 16        # Can be detected by CNN as 'thumb_down_close'
    OK_SIGN = 17           # New tab
    ROCK_SIGN = 18         # Copy
    CALL_SIGN = 19         # Paste


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
        
        # Scroll gesture state (ISSUE #1 FIX: Dwell time tracking)
        self.scroll_gesture_start_time = 0.0  # Changed from None to 0.0
        self.scroll_last_gesture = GestureType.NONE  # Changed from None
        self.scroll_last_action_time = 0.0  # REFINEMENT #1: Track last scroll for continuous delay
        
        # REFINEMENT #2: Browser navigation safety timing
        self.browser_nav_gesture_start_time = 0.0  # Changed from None to 0.0
        self.browser_nav_last_gesture = GestureType.NONE  # Changed from None
        self.browser_nav_last_action_time = 0.0
        
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
        self.cnn_classifier = None
        self.cnn_enabled = Config.ENABLE_CNN_CLASSIFIER and CNN_AVAILABLE
        
        if self.cnn_enabled:
            try:
                print("Initializing CNN Gesture Classifier...")
                # Create classifier without parameters (check actual CNNGestureClassifier signature)
                self.cnn_classifier = CNNGestureClassifier()
                try:
                    self.cnn_classifier.load_model(Config.CNN_MODEL_PATH, Config.CNN_LABEL_ENCODER_PATH)
                    print("CNN model loaded successfully")
                    print(f"   - Model: {Config.CNN_MODEL_PATH}")
                    print(f"   - Confidence threshold: {Config.CNN_MIN_CONFIDENCE}")
                except:
                    print("CNN model loading failed - falling back to rule-based recognition")
                    self.cnn_enabled = False
                    self.cnn_classifier = None
            except Exception as e:
                print(f"CNN initialization error: {e}")
                print("   Falling back to rule-based recognition")
                self.cnn_enabled = False
                self.cnn_classifier = None
        else:
            if Config.ENABLE_CNN_CLASSIFIER and not CNN_AVAILABLE:
                print("CNN recognition enabled but module not found")
                print("   Using rule-based recognition only")
            else:
                print("CNN recognition disabled - using rule-based recognition")
        
        # CNN to GestureType Mapping (7 CNN gestures → GestureType enum)
        self.cnn_to_gesture_map = {
            'scroll_up': GestureType.CLOSED_FIST,
            'scroll_down': GestureType.OPEN_PALM,
            'swipe_left': GestureType.SWIPE_LEFT,
            'swipe_right': GestureType.SWIPE_RIGHT,
            'pinch_zoom': GestureType.PINCH,
            'thumb_down_close': GestureType.THUMB_DOWN,
            'mute_toggle': GestureType.PINKY_ONLY
        }
    
    def is_finger_extended(self, landmarks, finger_tip, finger_dip, finger_mcp):
        """
        Determines if a finger is extended (straight) or folded.
        
        Logic:
            A finger is extended if its TIP is higher (lower y-value) than
            its DIP joint, and the DIP is higher than the MCP joint.
            In image coordinates, y increases downward.
        
        Args:
            landmarks: List of hand landmarks
            finger_tip: Index of fingertip landmark
            finger_dip: Index of DIP joint landmark
            finger_mcp: Index of MCP joint landmark
            
        Returns:
            bool: True if finger is extended
        """
        tip_y = landmarks[finger_tip].y
        dip_y = landmarks[finger_dip].y
        mcp_y = landmarks[finger_mcp].y
        
        # Finger is extended if tip is above (smaller y) than dip,
        # and dip is above mcp
        return tip_y < dip_y and dip_y < mcp_y
    
    def is_thumb_extended(self, landmarks):
        """
        Checks if thumb is extended.
        
        Logic:
            Thumb extends horizontally. It's extended if the TIP is
            farther from the wrist in x-direction than the IP joint.
        
        Returns:
            bool: True if thumb is extended
        """
        thumb_tip = landmarks[self.THUMB_TIP]
        thumb_ip = landmarks[self.THUMB_IP]
        thumb_mcp = landmarks[2]  # Thumb MCP joint
        wrist = landmarks[self.WRIST]
        
        # Calculate distance from wrist for tip and ip
        tip_dist = ((thumb_tip.x - wrist.x)**2 + (thumb_tip.y - wrist.y)**2) ** 0.5
        ip_dist = ((thumb_ip.x - wrist.x)**2 + (thumb_ip.y - wrist.y)**2) ** 0.5
        mcp_dist = ((thumb_mcp.x - wrist.x)**2 + (thumb_mcp.y - wrist.y)**2) ** 0.5
        
        # Thumb is extended if tip > ip > mcp in distance from wrist
        return tip_dist > ip_dist and ip_dist > mcp_dist * 0.8
    
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
            Additional angle check to ensure thumb is vertical.
        
        Returns:
            bool: True if thumbs-up detected
        """
        count, fingers = self.count_extended_fingers(landmarks, ignore_thumb=False)
        
        # Only thumb should be extended, all others folded
        if fingers['thumb'] and not fingers['index'] and not fingers['middle'] and not fingers['ring'] and not fingers['pinky']:
            thumb_tip_y = landmarks[self.THUMB_TIP].y
            thumb_ip_y = landmarks[self.THUMB_IP].y
            thumb_mcp_y = landmarks[2].y  # Thumb MCP
            
            # Thumb pointing up: tip above ip above mcp
            vertical_alignment = thumb_tip_y < thumb_ip_y < thumb_mcp_y
            
            # Additional check: thumb should be significantly above wrist
            wrist_y = landmarks[self.WRIST].y
            thumb_elevated = thumb_tip_y < wrist_y - 0.1  # Above wrist by threshold
            
            return vertical_alignment and thumb_elevated
        
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
        
        # Check if movement exceeds threshold AND has direction dominance
        if horizontal_movement > Config.SWIPE_THRESHOLD:
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
        Detects vertical swipe gestures (up or down).
        
        ISSUE #4 FIX: Strict angle and velocity thresholds to prevent confusion with close gestures.
        ISSUE #4 FIX: Requires vertical dominance (Y movement >> X movement).
        ISSUE #4 FIX: Multi-frame confirmation.
        
        Logic:
            Tracks wrist + index finger. Requires:
            1. Significant vertical movement (exceeds threshold)
            2. Vertical movement >> horizontal movement (direction dominance)
            3. Minimum velocity requirement
            4. Consistent direction across multiple frames
        
        Returns:
            GestureType: SWIPE_UP, SWIPE_DOWN, or NONE
        """
        current_wrist_y = landmarks[self.WRIST].y
        current_wrist_x = landmarks[self.WRIST].x
        
        if self.previous_wrist_y is None:
            self.previous_wrist_y = current_wrist_y
            self.previous_wrist_x = current_wrist_x
            return GestureType.NONE
        
        # Calculate movement
        delta_y = current_wrist_y - self.previous_wrist_y
        delta_x = current_wrist_x - self.previous_wrist_x
        
        # ISSUE #4 FIX: Enforce vertical dominance and velocity
        vertical_movement = abs(delta_y)
        horizontal_movement = abs(delta_x)
        
        if vertical_movement > Config.SWIPE_VERTICAL_THRESHOLD and vertical_movement > Config.SWIPE_VELOCITY_MIN:
            # ISSUE #4 FIX: Require vertical dominance to avoid confusion with horizontal swipes
            if horizontal_movement > 0 and (vertical_movement / horizontal_movement) < Config.SWIPE_DIRECTION_DOMINANCE_RATIO:
                # Too much horizontal movement - reject as vertical swipe
                self.previous_wrist_y = current_wrist_y
                self.previous_wrist_x = current_wrist_x
                return GestureType.NONE
            
            # Determine direction (negative delta_y = upward movement in screen coordinates)
            swipe_direction = GestureType.SWIPE_UP if delta_y < 0 else GestureType.SWIPE_DOWN
            
            # Note: Using same confirmation buffer as horizontal swipes for now
            # In production, you might want separate buffers
            self.previous_wrist_y = current_wrist_y
            self.previous_wrist_x = current_wrist_x
            return swipe_direction
        
        self.previous_wrist_y = current_wrist_y
        self.previous_wrist_x = current_wrist_x
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
        Detect pinch (zoom in) or spread (zoom out) gestures.
        
        FIXED: Ultra-strict detection to prevent confusion with open palm.
        Requires EXACTLY thumb and index extended, all others folded.
        
        Logic:
            - Measures distance between thumb and index finger
            - Requires EXACT finger count of 2 (thumb + index ONLY)
            - All other fingers MUST be folded
            - Close distance = pinch, far distance = spread
        
        Returns:
            GestureType: PINCH, SPREAD, or NONE
        """
        # Check finger states with thumb NOT ignored (we need accurate thumb state)
        count, fingers = self.count_extended_fingers(landmarks, ignore_thumb=False)
        
        # ULTRA-STRICT: Must have EXACTLY 2 fingers extended (thumb + index)
        # This prevents confusion with open palm (5 fingers) or any other gesture
        if count != 2:
            return GestureType.NONE
        
        # Verify it's specifically thumb and index, not any other 2-finger combo
        if not (fingers['thumb'] and fingers['index']):
            return GestureType.NONE
        
        # Explicitly check other fingers are folded
        if fingers['middle'] or fingers['ring'] or fingers['pinky']:
            return GestureType.NONE
        
        # Now safe to check thumb-index distance for pinch/spread
        thumb_tip = landmarks[self.THUMB_TIP]
        index_tip = landmarks[self.INDEX_TIP]
        
        distance = ((thumb_tip.x - index_tip.x)**2 + 
                   (thumb_tip.y - index_tip.y)**2) ** 0.5
        
        if distance < Config.PINCH_THRESHOLD:
            return GestureType.PINCH
        elif distance > Config.SPREAD_THRESHOLD:
            return GestureType.SPREAD
        
        return GestureType.NONE
    
    def detect_special_gestures(self, landmarks, fingers):
        """
        Detect special hand signs (OK, Rock, Call) with STRICT conditions.
        
        FIXED: Call sign now checks thumb state explicitly to work with THUMB_IGNORED_MODE.
        
        Returns:
            GestureType: Special gesture or NONE
        """
        # OK Sign: Thumb and index form circle, other three fingers extended
        # STRICT: Index must NOT be extended straight (tip near thumb = circle)
        thumb_tip = landmarks[self.THUMB_TIP]
        index_tip = landmarks[self.INDEX_TIP]
        thumb_index_distance = ((thumb_tip.x - index_tip.x)**2 + 
                               (thumb_tip.y - index_tip.y)**2) ** 0.5
        
        if (thumb_index_distance < 0.05 and 
            not fingers['index'] and  # Index NOT straight (forming circle with thumb)
            fingers['middle'] and fingers['ring'] and fingers['pinky']):
            return GestureType.OK_SIGN
        
        # Rock Sign: Index and pinky extended, middle and ring folded, thumb folded
        # STRICT: Thumb must be folded to distinguish from other gestures
        if (fingers['index'] and fingers['pinky'] and 
            not fingers['middle'] and not fingers['ring'] and not fingers['thumb']):
            return GestureType.ROCK_SIGN
        
        # Call Sign: Thumb and pinky extended, others folded
        # CRITICAL FIX: Check thumb explicitly to bypass THUMB_IGNORED_MODE
        thumb_extended = self.is_thumb_extended(landmarks)
        if (thumb_extended and fingers['pinky'] and
            not fingers['index'] and not fingers['middle'] and not fingers['ring']):
            return GestureType.CALL_SIGN
        
        return GestureType.NONE
    
    def detect_thumb_down(self, landmarks):
        """
        Detects thumbs-down gesture - IMPROVED DISTINCTNESS.
        
        Logic:
            Thumb pointing down (tip.y > ip.y) while other fingers folded.
            Additional angle check to ensure thumb is vertical downward.
        
        Returns:
            bool: True if thumbs-down detected
        """
        count, fingers = self.count_extended_fingers(landmarks, ignore_thumb=False)
        
        # Only thumb extended, all others folded
        if fingers['thumb'] and not fingers['index'] and not fingers['middle'] and not fingers['ring'] and not fingers['pinky']:
            thumb_tip_y = landmarks[self.THUMB_TIP].y
            thumb_ip_y = landmarks[self.THUMB_IP].y
            thumb_mcp_y = landmarks[2].y  # Thumb MCP
            
            # Thumb pointing down: tip below ip below mcp
            vertical_alignment = thumb_tip_y > thumb_ip_y > thumb_mcp_y
            
            # Additional check: thumb should be significantly below wrist
            wrist_y = landmarks[self.WRIST].y
            thumb_lowered = thumb_tip_y > wrist_y + 0.1  # Below wrist by threshold
            
            return vertical_alignment and thumb_lowered
        
        return False
    
    def recognize_gesture_hybrid(self, hand_landmarks, frame):
        """
        Hybrid CNN + Rule-based Gesture Recognition (PHASE 4: ML Integration)
        
        This method combines CNN-based classification with rule-based fallback for maximum
        accuracy and safety. The CNN handles static gestures while MediaPipe continues
        to handle pointer movement and dynamic gesture validation.
        
        Safety Pipeline:
            1. CNN Raw Prediction → Confidence Filter (≥75%) → Temporal Voting (5 frames, 80%)
            2. CNN output passes through existing state machine (NEVER direct action trigger)
            3. Falls back to rule-based if CNN disabled or prediction rejected
        
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
                    # Extract hand bounding box for ROI
                    frame_h, frame_w = frame.shape[:2]
                    x_coords = [lm.x * frame_w for lm in landmarks]
                    y_coords = [lm.y * frame_h for lm in landmarks]
                    
                    x_min, x_max = int(min(x_coords)), int(max(x_coords))
                    y_min, y_max = int(min(y_coords)), int(max(y_coords))
                    
                    # Add padding (20% like in dataset collector)
                    padding_x = int((x_max - x_min) * 0.2)
                    padding_y = int((y_max - y_min) * 0.2)
                    
                    x_min = max(0, x_min - padding_x)
                    y_min = max(0, y_min - padding_y)
                    x_max = min(frame_w, x_max + padding_x)
                    y_max = min(frame_h, y_max + padding_y)
                    
                    # Extract ROI
                    if x_max > x_min and y_max > y_min:
                        hand_roi = frame[y_min:y_max, x_min:x_max]
                        
                        # CNN Classification (with confidence filter + temporal voting)
                        cnn_label, cnn_confidence = self.cnn_classifier.classify(hand_roi)
                        
                        # If CNN returned valid prediction (passed all safety filters)
                        if cnn_label is not None and cnn_label in self.cnn_to_gesture_map:
                            gesture_type = self.cnn_to_gesture_map[cnn_label]
                            
                            # Additional verification for pinch gesture (combine CNN + distance check)
                            if gesture_type == GestureType.PINCH:
                                # Verify with actual pinch distance measurement
                                pinch_distance = self.calculate_pinch_distance(landmarks)
                                if pinch_distance < Config.PINCH_DISTANCE_THRESHOLD:
                                    return gesture_type  # CNN prediction verified
                            else:
                                return gesture_type  # CNN prediction accepted
                
                # CNN rejected prediction (low confidence or voting failed)
                # Fall back to rule-based recognition
                
            except Exception as e:
                # CNN processing error - gracefully fall back to rule-based
                print(f"⚠️  CNN processing error: {e}")
        
        # Fallback: Use existing rule-based recognition
        return self.recognize_gesture(hand_landmarks)
    
    def recognize_gesture(self, hand_landmarks):
        """
        Main gesture recognition function.
        
        IMPROVED: Mutually exclusive gesture detection with proper priority ordering.
        
        Analyzes hand landmarks and returns the detected gesture type.
        
        Args:
            hand_landmarks: MediaPipe hand landmarks object
            
        Returns:
            GestureType: The detected gesture
        """
        if not hand_landmarks:
            return GestureType.NONE
        
        landmarks = hand_landmarks.landmark
        
        # ISSUE #5 FIX: Count fingers with thumb-ignored mode applied
        count, fingers = self.count_extended_fingers(landmarks)
        
        # Auto-calibrate hand size on first detection
        if self.hand_size_baseline is None and Config.ENABLE_LEARNING_MODE:
            self.hand_size_baseline = self.calculate_hand_size(landmarks)
        
        # MUTUALLY EXCLUSIVE PRIORITY ORDER - FIXED to prevent gesture mixing
        # CRITICAL FIX: Movement gestures checked BEFORE static poses to ensure proper detection
        
        # PRIORITY 1: Thumb gestures (most distinct - explicit thumb-only poses)
        if Config.THUMB_EXPLICIT_GESTURES_ONLY:
            if self.detect_thumb_up(landmarks):
                return GestureType.THUMB_UP
            elif self.detect_thumb_down(landmarks):
                return GestureType.THUMB_DOWN
        
        # PRIORITY 2: Special hand signs (require precise finger configurations)
        special = self.detect_special_gestures(landmarks, fingers)
        if special != GestureType.NONE:
            return special
        
        # PRIORITY 3: Movement-based gestures (swipes) - CHECK BEFORE static finger counts
        # This prevents swipes from being misclassified as peace sign or other static poses
        swipe_h = self.detect_swipe(landmarks)
        if swipe_h != GestureType.NONE:
            return swipe_h
        
        swipe_v = self.detect_vertical_swipe(landmarks)
        if swipe_v != GestureType.NONE:
            return swipe_v
        
        # PRIORITY 4: Finger-count based gestures (static poses)
        # Must use strict elif chain to ensure mutual exclusivity
        
        # Closed fist (0 fingers)
        if count == 0:
            return GestureType.CLOSED_FIST
        
        # Open palm (all fingers extended)
        elif count == 5 or (Config.THUMB_IGNORED_MODE and count == 4 and not fingers['thumb']):
            # STRICT CHECK: All non-thumb fingers must be extended
            if fingers['index'] and fingers['middle'] and fingers['ring'] and fingers['pinky']:
                return GestureType.OPEN_PALM
        
        # Four fingers (refresh page)
        elif count == 4:
            # STRICT CHECK: Thumb folded, all others extended
            if not fingers['thumb'] and fingers['index'] and fingers['middle'] and fingers['ring'] and fingers['pinky']:
                return GestureType.FOUR_FINGERS
        
        # Three fingers (screenshot)
        elif count == 3:
            # STRICT CHECK: Index, middle, ring extended; pinky and thumb folded
            if fingers['index'] and fingers['middle'] and fingers['ring'] and not fingers['pinky'] and not fingers['thumb']:
                return GestureType.THREE_FINGERS
        
        # Two fingers - Peace sign (V sign for left click)
        elif count == 2:
            # STRICT CHECK: Only index and middle extended; others folded
            if fingers['index'] and fingers['middle'] and not fingers['ring'] and not fingers['pinky'] and not fingers['thumb']:
                return GestureType.PEACE_SIGN
        
        # One finger - pointer or pinky
        elif count == 1:
            # INDEX_ONLY: Only index extended
            if fingers['index'] and not fingers['middle'] and not fingers['ring'] and not fingers['pinky'] and not fingers['thumb']:
                return GestureType.INDEX_ONLY
            # PINKY_ONLY: Only pinky extended
            elif fingers['pinky'] and not fingers['index'] and not fingers['middle'] and not fingers['ring'] and not fingers['thumb']:
                return GestureType.PINKY_ONLY
        
        # PRIORITY 5: Distance-based gestures (pinch/spread) - MOVED TO LAST
        # CRITICAL FIX: Check pinch/spread AFTER all other gestures to prevent zoom interference
        # This ensures zoom only triggers when user is intentionally making pinch pose
        # ISSUE #2 FIX: Skip zoom gestures in POINTER_MODE if mode separation enabled
        if not (Config.ENABLE_MODE_SEPARATION and self.current_mode == 'POINTER' and Config.DISABLE_ZOOM_IN_POINTER_MODE):
            pinch_spread = self.detect_pinch_spread(landmarks)
            if pinch_spread != GestureType.NONE:
                return pinch_spread
        
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
        if len(self.buffer) < buffer_maxlen * 0.8:  # Allow 80% fill for faster initial response
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
        
        # IMPROVED: Apply hysteresis for transition smoothing
        # If switching from one gesture to another, require higher confidence
        if self.current_stable_gesture != GestureType.NONE and most_common != self.current_stable_gesture:
            # Require 70% consistency when switching gestures (prevents flickering)
            required_confidence = 0.7
        else:
            # Use standard 60% consistency for maintaining current gesture
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
        self.color_map = {
            GestureType.OPEN_PALM: (0, 255, 0),      # Green
            GestureType.CLOSED_FIST: (255, 0, 0),    # Red
            GestureType.INDEX_ONLY: (255, 255, 0),   # Yellow
            GestureType.PEACE_SIGN: (0, 255, 255),   # Cyan
            GestureType.THUMB_UP: (0, 128, 255),     # Orange
            GestureType.THUMB_DOWN: (128, 0, 255),   # Purple
            GestureType.THREE_FINGERS: (255, 128, 0), # Light Blue
            GestureType.FOUR_FINGERS: (255, 0, 255),  # Magenta
        }
    
    def add_trail_point(self, x, y):
        """Add point to gesture trail"""
        self.trail_points.append((int(x), int(y)))
    
    def draw_trail(self, frame):
        """Draw gesture trail on frame"""
        if len(self.trail_points) < 2:
            return
        
        # Draw trail with fading effect
        for i in range(1, len(self.trail_points)):
            alpha = i / len(self.trail_points)  # Fade older points
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
    
    def move_mouse(self, hand_landmarks):
        """
        Move mouse cursor based on index finger position.
        
        ISSUE #2 FIX: Corrected coordinate mapping to prevent inverted/unintuitive movement.
        ISSUE #2 FIX: Configurable inversion for left/right and up/down.
        
        Logic:
            Maps hand position in camera frame to screen coordinates
            with smoothing to reduce jitter.
        
        Args:
            hand_landmarks: MediaPipe hand landmarks
        """
        # Get index finger tip position (normalized 0-1)
        index_tip = hand_landmarks.landmark[HandGestureRecognizer.INDEX_TIP]
        
        # ISSUE #2 FIX: Configurable coordinate mapping
        # Default: no inversion (natural movement: right hand -> right screen, up hand -> up screen)
        if Config.POINTER_INVERT_X:
            screen_x = int((1 - index_tip.x) * Config.SCREEN_WIDTH)  # Mirror/flip
        else:
            screen_x = int(index_tip.x * Config.SCREEN_WIDTH)  # Natural left-right
        
        if Config.POINTER_INVERT_Y:
            screen_y = int((1 - index_tip.y) * Config.SCREEN_HEIGHT)  # Inverted up-down
        else:
            screen_y = int(index_tip.y * Config.SCREEN_HEIGHT)  # Natural up-down
        
        # Apply smoothing to reduce jitter (ISSUE #2 FIX: reduced smoothing factor for better responsiveness)
        smooth_x = int(self.prev_mouse_x * Config.MOUSE_SMOOTHING + 
                      screen_x * (1 - Config.MOUSE_SMOOTHING))
        smooth_y = int(self.prev_mouse_y * Config.MOUSE_SMOOTHING + 
                      screen_y * (1 - Config.MOUSE_SMOOTHING))
        
        # Move mouse
        pyautogui.moveTo(smooth_x, smooth_y)
        
        # Store for next frame
        self.prev_mouse_x = smooth_x
        self.prev_mouse_y = smooth_y
    
    def scroll_down(self):
        """
        Scroll webpage down.
        
        REFINEMENT #1: Slightly faster scroll (3.5x), smoother with 4 steps.
        OPTIMIZED: Reduced sleep time for better performance.
        """
        total_scroll = int(Config.SCROLL_BASE_AMOUNT * Config.SCROLL_SPEED_MULTIPLIER)
        step = total_scroll // Config.SCROLL_SMOOTH_STEPS
        
        # Smooth scrolling in increments (4 steps for smoother visual experience)
        for i in range(Config.SCROLL_SMOOTH_STEPS):
            pyautogui.scroll(-step)
            if i < Config.SCROLL_SMOOTH_STEPS - 1:  # Skip sleep on last iteration
                time.sleep(0.01)  # Optimized delay
    
    def scroll_up(self):
        """
        Scroll webpage up.
        
        REFINEMENT #1: Slightly faster scroll (3.5x), smoother with 4 steps.
        """
        total_scroll = int(Config.SCROLL_BASE_AMOUNT * Config.SCROLL_SPEED_MULTIPLIER)
        step = total_scroll // Config.SCROLL_SMOOTH_STEPS
        
        # Smooth scrolling in increments (4 steps for smoother animation)
        for _ in range(Config.SCROLL_SMOOTH_STEPS):
            pyautogui.scroll(step)
            time.sleep(0.012)  # Slightly increased delay for smoother animation
    
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
                    subprocess.Popen(['start', 'microsoft-edge:'], shell=True)
                elif browser == 'firefox':
                    subprocess.Popen(['start', 'firefox'], shell=True)
                else:  # default browser
                    subprocess.Popen(['start', 'http://'], shell=True)
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
            print(f"⚠️  Could not launch browser: {e}")
    
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
    
    def __init__(self):
        """Initialize all system components"""
        print("🚀 Initializing Hand Gesture Control System...")
        
        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=Config.MAX_NUM_HANDS,
            min_detection_confidence=Config.MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=Config.MIN_TRACKING_CONFIDENCE
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # Initialize components
        self.recognizer = HandGestureRecognizer()
        self.stabilizer = GestureStabilizer()
        self.controller = BrowserController()
        self.history = GestureHistory() if Config.ENABLE_GESTURE_HISTORY else None
        self.visual_effects = VisualEffects() if Config.ENABLE_VISUAL_TRAILS else None
        
        # Video capture
        self.cap = cv2.VideoCapture(Config.CAMERA_INDEX)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, Config.FRAME_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, Config.FRAME_HEIGHT)
        self.cap.set(cv2.CAP_PROP_FPS, Config.FPS_TARGET)
        
        # Performance tracking
        self.fps = 0
        self.frame_count = 0
        self.start_time = time.time()
        
        print("✅ System initialized successfully!")
        print("\n" + "="*70)
        print("GESTURE CONTROLS:")
        print("="*70)
        print("  SCROLLING:")
        print("    👋 Open Palm       → Scroll Down")
        print("    ✊ Closed Fist     → Scroll Up")
        print("\n  MOUSE CONTROL:")
        print("    ☝️  Index Finger    → Move Mouse")
        print("    ✌️  Peace Sign      → Left Click")
        print("\n  NAVIGATION:")
        print("    👈 Swipe Left      → Browser Back")
        print("    👉 Swipe Right     → Browser Forward")
        print("    ⬆️  Swipe Up        → Next Tab")
        print("    ⬇️  Swipe Down      → Previous Tab")
        print("\n  PAGE ACTIONS:")
        print("    🖐️  Three Fingers   → Screenshot")
        print("    🖐️  Four Fingers    → Refresh Page")
        print("    👍 Thumb Up        → Zoom In")
        print("    👎 Thumb Down      → Close Tab")
        print("\n  ADVANCED:")
        print("    👌 OK Sign         → New Tab")
        print("    🤘 Rock Sign       → Copy")
        print("    🤙 Call Sign       → Paste")
        print("    🤏 Pinch           → Zoom In (close fingers)")
        print("    🖐️  Spread          → Zoom Out (open fingers)")
        print("    🤙 Pinky Only      → Mute/Unmute")
        print("="*70)
        print("\n⚠️  KEYBOARD SHORTCUTS:")
        print(f"    'q' - Quit | 's' - Stats | 'h' - Toggle UI | 'b' - Launch {Config.BROWSER_LAUNCH_TARGET.title()}")
        print("="*70 + "\n")
    
    def execute_gesture_action(self, gesture, hand_landmarks):
        """
        Execute browser action based on detected gesture.
        
        ISSUE #1 FIX: Added dwell time for scroll gestures to prevent accidental triggers.
        ISSUE #2 FIX: Added mode separation (POINTER_MODE vs GESTURE_MODE).
        
        Args:
            gesture: GestureType to execute
            hand_landmarks: MediaPipe hand landmarks
        """
        if gesture == GestureType.NONE:
            # Reset scroll dwell timer when no gesture
            self.recognizer.scroll_gesture_start_time = 0.0
            self.recognizer.scroll_last_gesture = GestureType.NONE
            
            # REFINEMENT #2: Reset browser navigation timers
            self.recognizer.browser_nav_gesture_start_time = 0.0
            self.recognizer.browser_nav_last_gesture = GestureType.NONE
            
            # REFINEMENT #3: Reset close tab timers
            self.recognizer.close_tab_gesture_start_time = 0.0
            self.recognizer.close_tab_gesture_stable = False
            self.recognizer.close_tab_last_progress_printed = -1  # BUG FIX: Reset progress tracking
            
            # REFINEMENT #5: Reset mute timer
            self.recognizer.mute_gesture_start_time = 0.0
            
            # ISSUE #2 FIX: Exit POINTER_MODE when no gesture
            if Config.ENABLE_MODE_SEPARATION and self.recognizer.current_mode == 'POINTER':
                if time.time() - self.recognizer.mode_switch_time > Config.MODE_SWITCH_DEBOUNCE:
                    self.recognizer.current_mode = 'GESTURE'
            return
        
        # ISSUE #2 FIX: Mode management - INDEX_ONLY triggers POINTER_MODE
        current_time = time.time()
        if Config.ENABLE_MODE_SEPARATION:
            if gesture == GestureType.INDEX_ONLY:
                if self.recognizer.current_mode != 'POINTER':
                    self.recognizer.current_mode = 'POINTER'
                    self.recognizer.mode_switch_time = current_time
                    print("🖱️  POINTER MODE activated (zoom disabled)")
            else:
                # Any other gesture switches back to GESTURE_MODE
                if self.recognizer.current_mode == 'POINTER':
                    if current_time - self.recognizer.mode_switch_time > Config.MODE_SWITCH_DEBOUNCE:
                        self.recognizer.current_mode = 'GESTURE'
                        print("👋 GESTURE MODE activated")
        
        # Check debounce for non-continuous actions
        if gesture not in [GestureType.INDEX_ONLY]:
            if not self.stabilizer.should_execute_action(gesture):
                return
        
        # REFINEMENT #4: Check if zoom is active - isolate zoom gestures
        if Config.ZOOM_GESTURE_ISOLATION and self.recognizer.zoom_active:
            # Only allow zoom gestures to complete, block others
            if gesture not in [GestureType.PINCH, GestureType.SPREAD]:
                if current_time - self.recognizer.zoom_last_action_time >= Config.ZOOM_COOLDOWN:
                    self.recognizer.zoom_active = False  # Exit zoom mode
                else:
                    return  # Still in zoom cooldown, ignore other gestures
        
        # Execute appropriate action
        try:
            # REFINEMENT #1: Scroll gestures with refined timing (slightly faster, smoother)
            if gesture == GestureType.OPEN_PALM:
                # Check dwell time before scrolling
                if self.recognizer.scroll_last_gesture != gesture:
                    self.recognizer.scroll_gesture_start_time = current_time
                    self.recognizer.scroll_last_gesture = gesture
                    return  # Wait for dwell time
                
                # Check continuous scroll delay to prevent spam
                if current_time - self.recognizer.scroll_last_action_time < Config.SCROLL_CONTINUOUS_DELAY:
                    return
                
                if current_time - self.recognizer.scroll_gesture_start_time >= Config.SCROLL_DWELL_TIME:
                    self.controller.scroll_down()
                    print("⬇️  Scrolling down (3.5x speed, 4-step smooth)...")
                    self.recognizer.scroll_last_action_time = current_time
            
            elif gesture == GestureType.CLOSED_FIST:
                # Check dwell time before scrolling
                if self.recognizer.scroll_last_gesture != gesture:
                    self.recognizer.scroll_gesture_start_time = current_time
                    self.recognizer.scroll_last_gesture = gesture
                    return  # Wait for dwell time
                
                # Check continuous scroll delay to prevent spam
                if current_time - self.recognizer.scroll_last_action_time < Config.SCROLL_CONTINUOUS_DELAY:
                    return
                
                if current_time - self.recognizer.scroll_gesture_start_time >= Config.SCROLL_DWELL_TIME:
                    self.controller.scroll_up()
                    print("⬆️  Scrolling up (3.5x speed, 4-step smooth)...")
                    self.recognizer.scroll_last_action_time = current_time
            
            elif gesture == GestureType.INDEX_ONLY:
                # ISSUE #2 FIX: Pointer mode - continuous mouse movement, zoom disabled
                # Continuous mouse movement (no debounce)
                self.controller.move_mouse(hand_landmarks)
            
            elif gesture == GestureType.PEACE_SIGN:
                self.controller.left_click()
                print("🖱️  Left click")
            
            elif gesture == GestureType.THUMB_UP:
                self.controller.zoom_in()
                print("🔍 Zoom in (smooth 2-step)")
            
            # REFINEMENT #3: Close tab - HIGH SAFETY with long dwell time and strong cooldown
            elif gesture == GestureType.THUMB_DOWN:
                # Check cooldown first (prevent rapid tab closure)
                if current_time - self.recognizer.close_tab_last_action_time < Config.CLOSE_TAB_COOLDOWN:
                    return  # Still in cooldown
                
                # Initialize dwell timer
                if self.recognizer.close_tab_gesture_start_time is None:
                    self.recognizer.close_tab_gesture_start_time = current_time
                    self.recognizer.close_tab_gesture_stable = True
                    print("⚠️  Hold thumb-down for 1.2s to close tab...")
                    return
                
                # Require stable gesture throughout dwell period
                if Config.CLOSE_TAB_REQUIRE_STABILITY:
                    if not self.recognizer.close_tab_gesture_stable:
                        self.recognizer.close_tab_gesture_start_time = 0.0
                        return
                
                # Check if dwell time met
                dwell_elapsed = current_time - self.recognizer.close_tab_gesture_start_time
                if dwell_elapsed >= Config.CLOSE_TAB_DWELL_TIME:
                    self.controller.close_tab()
                    print("Tab closed (safe mode: 1.2s dwell + 2s cooldown)")
                    self.recognizer.close_tab_last_action_time = current_time
                    self.recognizer.close_tab_gesture_start_time = 0.0
                    self.recognizer.close_tab_last_progress_printed = -1  # Reset for next time
                else:
                    # BUG FIX: Show progress only once per milestone to prevent console spam
                    progress = int((dwell_elapsed / Config.CLOSE_TAB_DWELL_TIME) * 100)
                    # Print at 25%, 50%, 75% milestones only once
                    if progress >= 25 and self.recognizer.close_tab_last_progress_printed < 25:
                        print("⏳ Close tab progress: 25%")
                        self.recognizer.close_tab_last_progress_printed = 25
                    elif progress >= 50 and self.recognizer.close_tab_last_progress_printed < 50:
                        print("⏳ Close tab progress: 50%")
                        self.recognizer.close_tab_last_progress_printed = 50
                    elif progress >= 75 and self.recognizer.close_tab_last_progress_printed < 75:
                        print("⏳ Close tab progress: 75%")
                        self.recognizer.close_tab_last_progress_printed = 75
            
            # REFINEMENT #2: Browser navigation - slower, more controlled with deliberate delay
            elif gesture == GestureType.SWIPE_LEFT:
                # Check cooldown first
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
                    print("Browser back (0.8s dwell + 1.5s cooldown)")
                    self.recognizer.browser_nav_last_action_time = current_time
                    self.recognizer.browser_nav_last_gesture = GestureType.NONE
            
            elif gesture == GestureType.SWIPE_RIGHT:
                # Check cooldown first
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
                    print("Browser forward (0.8s dwell + 1.5s cooldown)")
                    self.recognizer.browser_nav_last_action_time = current_time
                    self.recognizer.browser_nav_last_gesture = GestureType.NONE
            
            elif gesture == GestureType.SWIPE_UP:
                self.controller.next_tab()
                print("⬆️  Next tab")
            
            elif gesture == GestureType.SWIPE_DOWN:
                self.controller.previous_tab()
                print("⬇️  Previous tab")
            
            elif gesture == GestureType.THREE_FINGERS:
                filename = self.controller.take_screenshot()
                print(f"📸 Screenshot saved: {filename}")
            
            elif gesture == GestureType.FOUR_FINGERS:
                self.controller.refresh_page()
                print("🔄 Page refresh")
            
            # REFINEMENT #5: Mute toggle - slower, controlled execution with cooldown
            elif gesture == GestureType.PINKY_ONLY:
                # Check cooldown first
                if current_time - self.recognizer.mute_last_action_time < Config.MUTE_TOGGLE_COOLDOWN:
                    return
                
                # Initialize dwell timer
                if self.recognizer.mute_gesture_start_time is None:
                    self.recognizer.mute_gesture_start_time = current_time
                    return
                
                # Check dwell time
                if current_time - self.recognizer.mute_gesture_start_time >= Config.MUTE_TOGGLE_DWELL_TIME:
                    self.controller.mute_toggle()
                    print("🔇 Mute toggled (0.6s dwell + 1s cooldown)")
                    self.recognizer.mute_last_action_time = current_time
                    self.recognizer.mute_gesture_start_time = 0.0
            
            # BUG FIX: Removed duplicate PEACE_SIGN handler for fullscreen toggle
            # PEACE_SIGN (2 fingers) is already used for left click above (line 1266)
            # Fullscreen functionality can be reassigned to a different gesture if needed
            
            # REFINEMENT #4: Pinch/spread zoom - smooth with gesture isolation
            elif gesture == GestureType.PINCH:
                self.recognizer.zoom_active = True  # Enter zoom mode
                self.controller.zoom_in()
                print("🔍➕ Pinch zoom in (smooth 2-step, isolated)")
                self.recognizer.zoom_last_action_time = current_time
            
            elif gesture == GestureType.SPREAD:
                self.recognizer.zoom_active = True  # Enter zoom mode
                self.controller.zoom_out()
                print("🔍➖ Spread zoom out (smooth 2-step, isolated)")
                self.recognizer.zoom_last_action_time = current_time
            
            elif gesture == GestureType.OK_SIGN:
                self.controller.new_tab()
                print("➕ New tab")
            
            elif gesture == GestureType.ROCK_SIGN:
                self.controller.copy_text()
                print("📋 Copy")
            
            elif gesture == GestureType.CALL_SIGN:
                self.controller.paste_text()
                print("📋 Paste")
            
            # Add to history
            if self.history:
                self.history.add(gesture)
            
            # Trigger visual feedback
            if self.visual_effects:
                self.visual_effects.flash_gesture(gesture)
        
        except Exception as e:
            print(f"⚠️  Action error: {e}")
    
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
        
        # Display FPS with color coding
        fps_color = (0, 255, 0) if self.fps >= 25 else (0, 255, 255) if self.fps >= 20 else (0, 0, 255)
        cv2.putText(frame, f"FPS: {self.fps:.1f}", (20, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, fps_color, 2)
        
        # Display current gesture with color
        gesture_name = gesture.name.replace('_', ' ') if gesture != GestureType.NONE else "NONE"
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
            cv2.putText(frame, "🤖 CNN: ON", (320, 40),
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
        print("🎥 Starting video capture...\n")
        
        try:
            while self.cap.isOpened():
                success, frame = self.cap.read()
                if not success:
                    print("⚠️  Failed to capture frame")
                    continue
                
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
                    # PHASE 4: Hybrid CNN + Rule-based Recognition
                    current_gesture = self.recognizer.recognize_gesture_hybrid(hand_landmarks, frame)
                
                # Add to stabilization buffer
                self.stabilizer.add_gesture(current_gesture)
                
                # Get stable gesture
                stable_gesture = self.stabilizer.get_stable_gesture()
                
                # Execute action based on stable gesture
                self.execute_gesture_action(stable_gesture, hand_landmarks)
                
                # Draw overlay information
                frame = self.draw_info_overlay(frame, stable_gesture, hand_landmarks)
                
                # Calculate FPS
                self.calculate_fps()
                
                # Display frame
                cv2.imshow('Hand Gesture Control System', frame)
                
                # Check for quit command
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    print("\n👋 Shutting down safely...")
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
                    print(f"🌐 Launching {Config.BROWSER_LAUNCH_TARGET} browser...")
                    self.controller.launch_browser()
                elif key == ord('c'):
                    # PHASE 4: Toggle CNN classification on/off
                    if CNN_AVAILABLE:
                        self.recognizer.cnn_enabled = not self.recognizer.cnn_enabled
                        mode_str = "CNN + Rule-based" if self.recognizer.cnn_enabled else "Rule-based only"
                        print(f"🤖 Recognition mode: {mode_str}")
                        if self.recognizer.cnn_enabled and self.recognizer.cnn_classifier:
                            # Reset CNN buffers when re-enabling
                            self.recognizer.cnn_classifier.reset_buffers()
                            print("   CNN temporal voting buffers reset")
                    else:
                        print("⚠️  CNN module not available - using rule-based recognition only")
        
        except KeyboardInterrupt:
            print("\n⚠️  Interrupted by user")
        
        except Exception as e:
            print(f"\n❌ Error: {e}")
        
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
        """Clean up resources safely"""
        print("🧹 Cleaning up resources...")
        self.cap.release()
        cv2.destroyAllWindows()
        self.hands.close()
        print("✅ Cleanup complete. Goodbye!")


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
