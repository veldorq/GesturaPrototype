"""
Constants module for AccessAble.
Contains all configuration values to avoid magic numbers and enable easy tuning.
"""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Constants:
    """
    Centralized constants for the AccessAble application.
    Frozen dataclass ensures immutability at runtime.
    """
    
    # === Camera Configuration ===
    CAMERA_INDEX: int = 0
    FRAME_WIDTH: int = 1280
    FRAME_HEIGHT: int = 720
    TARGET_FPS: int = 30
    
    # === Hand Detection Configuration ===
    MAX_NUM_HANDS: int = 1  # Single hand only for accessibility
    MIN_DETECTION_CONFIDENCE: float = 0.7  # Higher = fewer false positives
    MIN_TRACKING_CONFIDENCE: float = 0.5  # Lower = more stable tracking
    
    # === Smoothing Configuration ===
    USE_SMOOTHING: bool = True  # Enable landmark smoothing
    SMOOTHING_TYPE: str = "exponential"  # Options: "moving_avg", "exponential", "kalman"
    SMOOTHING_WINDOW_SIZE: int = 5  # For moving average
    SMOOTHING_ALPHA: float = 0.3  # For exponential smoothing (0-1, lower = more smoothing)
    KALMAN_PROCESS_NOISE: float = 0.01  # For Kalman filter
    KALMAN_MEASUREMENT_NOISE: float = 0.1  # For Kalman filter
    
    # === Voice Control Configuration ===
    ENABLE_VOICE_CONTROL: bool = False  # Voice control off by default
    VOICE_LANGUAGE: str = "en-US"  # Language code for speech recognition
    VOICE_CALIBRATION_DURATION: float = 1.0  # Seconds to calibrate mic
    
    # === Gesture Recognition Configuration ===
    GESTURE_CONFIDENCE_THRESHOLD: float = 0.75  # Minimum confidence to trigger
    DWELL_TIME_SECONDS: float = 1.5  # How long to hold gesture before activation
    STABILIZATION_WINDOW: int = 5  # Number of frames for smoothing
    DEBOUNCE_COOLDOWN_SECONDS: float = 0.5  # Prevent rapid re-triggering
    
    # === UI Configuration ===
    OVERLAY_PADDING: int = 20
    TEXT_FONT_SCALE: float = 0.7
    TEXT_THICKNESS: int = 2
    PROGRESS_BAR_HEIGHT: int = 20
    PROGRESS_BAR_WIDTH: int = 200
    
    # Color scheme (BGR format for OpenCV)
    COLOR_PRIMARY: Tuple[int, int, int] = (0, 255, 0)  # Green
    COLOR_SECONDARY: Tuple[int, int, int] = (0, 165, 255)  # Orange
    COLOR_DANGER: Tuple[int, int, int] = (0, 0, 255)  # Red
    COLOR_INFO: Tuple[int, int, int] = (255, 255, 0)  # Cyan
    COLOR_BACKGROUND: Tuple[int, int, int] = (40, 40, 40)  # Dark gray
    COLOR_TEXT: Tuple[int, int, int] = (255, 255, 255)  # White
    
    # === Action Configuration ===
    SCROLL_AMOUNT: int = 100  # Pixels to scroll per action
    CLICK_DURATION: float = 0.1  # Seconds for click animation
    
    # === Emergency Controls ===
    EMERGENCY_STOP_KEY: str = 'esc'  # Key to immediately stop application
    
    # === File Paths ===
    GESTURE_CONFIG_FILE: str = 'gestures_config.json'
    USER_SETTINGS_FILE: str = 'user_settings.json'
