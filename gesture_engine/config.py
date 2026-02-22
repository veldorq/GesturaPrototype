"""
Gesture Engine Configuration Module

Centralized configuration management for the Gestura gesture recognition system.
All tunable parameters, thresholds, and system constants are defined here.

Author: Gestura Development Team
Version: 2.0.0
"""

from typing import Dict, Any
from dataclasses import dataclass, field


@dataclass
class HandTrackingConfig:
    """Configuration for MediaPipe hand tracking."""
    
    # MediaPipe Hands parameters
    max_num_hands: int = 2
    min_detection_confidence: float = 0.7
    min_tracking_confidence: float = 0.5
    model_complexity: int = 1  # 0=Lite, 1=Full
    
    # Camera settings
    camera_index: int = 0
    frame_width: int = 1280
    frame_height: int = 720
    target_fps: int = 30


@dataclass
class SmoothingConfig:
    """Configuration for motion smoothing filters."""
    
    # Moving average filter
    moving_avg_window: int = 5
    
    # Exponential smoothing
    exp_smoothing_alpha: float = 0.3  # 0.0-1.0, lower = more smoothing
    
    # Kalman filter
    kalman_process_noise: float = 0.01
    kalman_measurement_noise: float = 0.1


@dataclass
class GestureClassificationConfig:
    """Configuration for gesture recognition."""
    
    # Recognition thresholds
    min_gesture_confidence: float = 0.75
    gesture_hold_time: float = 0.3  # seconds to confirm gesture
    cooldown_time: float = 0.5  # seconds between same gesture triggers
    
    # Feature extraction
    landmark_features: bool = True
    angle_features: bool = True
    distance_features: bool = True
    
    # Gesture types
    supported_gestures: list = field(default_factory=lambda: [
        "pinch", "swipe_left", "swipe_right", "swipe_up", "swipe_down",
        "fist", "palm", "thumbs_up", "peace", "pointing",
        "two_hand_spread", "two_hand_pinch"
    ])


@dataclass
class GestureTrainingConfig:
    """Configuration for custom gesture training."""
    
    # Training parameters
    training_samples_per_gesture: int = 30
    training_sample_rate: int = 5  # frames between samples
    
    # Storage
    gestures_file: str = "config/trained_gestures.json"
    backup_enabled: bool = True
    backup_file: str = "config/trained_gestures_backup.json"
    
    # Matching
    match_threshold: float = 0.80
    feature_vector_size: int = 63  # 21 landmarks * 3 coordinates


@dataclass
class VoiceControlConfig:
    """Configuration for voice command integration."""
    
    # Voice recognition
    engine: str = "speech_recognition"  # or "vosk"
    language: str = "en-US"
    energy_threshold: int = 4000
    pause_threshold: float = 0.8
    
    # Command mapping
    voice_commands: Dict[str, str] = field(default_factory=lambda: {
        "scroll mode": "enable_scroll",
        "navigation mode": "enable_navigation",
        "stop listening": "disable_voice",
        "click": "mouse_click",
        "double click": "mouse_double_click",
        "go back": "browser_back",
        "go forward": "browser_forward",
        "new tab": "browser_new_tab",
        "close tab": "browser_close_tab"
    })
    
    # Voice priority
    voice_overrides_gesture: bool = True
    timeout_seconds: float = 5.0


@dataclass
class CommandExecutionConfig:
    """Configuration for action execution."""
    
    # Execution settings
    action_delay: float = 0.1  # seconds between actions
    enable_feedback: bool = True
    feedback_duration: float = 0.5
    
    # Action mapping
    gesture_actions: Dict[str, str] = field(default_factory=lambda: {
        "pinch": "mouse_click",
        "swipe_left": "key_left",
        "swipe_right": "key_right",
        "swipe_up": "scroll_up",
        "swipe_down": "scroll_down",
        "fist": "pause_gesture",
        "palm": "resume_gesture",
        "thumbs_up": "volume_up",
        "peace": "screenshot",
        "two_hand_spread": "zoom_in",
        "two_hand_pinch": "zoom_out"
    })


@dataclass
class PerformanceConfig:
    """Configuration for performance optimization."""
    
    # Processing optimization
    skip_frames: int = 0  # 0=process every frame, 1=skip every other
    downsample_factor: float = 1.0  # 0.5=half resolution
    
    # Threading
    use_threading: bool = True
    max_threads: int = 2
    
    # Monitoring
    show_fps: bool = True
    log_performance: bool = False
    performance_log_file: str = "logs/performance.log"


class GestureEngineConfig:
    """Main configuration manager for the gesture engine."""
    
    def __init__(self):
        self.hand_tracking = HandTrackingConfig()
        self.smoothing = SmoothingConfig()
        self.classification = GestureClassificationConfig()
        self.training = GestureTrainingConfig()
        self.voice = VoiceControlConfig()
        self.execution = CommandExecutionConfig()
        self.performance = PerformanceConfig()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "hand_tracking": self.hand_tracking.__dict__,
            "smoothing": self.smoothing.__dict__,
            "classification": self.classification.__dict__,
            "training": self.training.__dict__,
            "voice": self.voice.__dict__,
            "execution": self.execution.__dict__,
            "performance": self.performance.__dict__
        }
    
    def update_from_dict(self, config_dict: Dict[str, Any]) -> None:
        """Update configuration from dictionary."""
        for section, values in config_dict.items():
            if hasattr(self, section):
                section_config = getattr(self, section)
                for key, value in values.items():
                    if hasattr(section_config, key):
                        setattr(section_config, key, value)


# Global configuration instance
CONFIG = GestureEngineConfig()


if __name__ == "__main__":
    # Configuration validation and testing
    import json
    
    print("Gesture Engine Configuration")
    print("=" * 50)
    print(json.dumps(CONFIG.to_dict(), indent=2))
