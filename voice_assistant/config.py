"""
Voice Assistant Configuration

Shared settings for voice recognition, command mapping, and system behavior.
Thread-safe flags for gesture system integration.

Author: Gestura Development Team
"""

import threading
from dataclasses import dataclass
from typing import Dict


@dataclass
class VoiceConfig:
    """Voice assistant configuration and shared state."""
    
    # ═══════════════════════════════════════════════════════════════
    # RECOGNITION SETTINGS
    # ═══════════════════════════════════════════════════════════════
    
    # Language for speech recognition
    LANGUAGE = "en-US"
    
    # Recognition backend priority: vosk (offline) > sphinx (offline) > google (online)
    USE_OFFLINE_RECOGNITION = True
    
    # Energy threshold for voice detection (300-4000, lower = more sensitive)
    ENERGY_THRESHOLD = 300  # Lowered for better voice pickup
    
    # Pause duration before phrase is considered complete (seconds)
    PAUSE_THRESHOLD = 1.2  # Increased for better phrase detection
    
    # Timeout for listening to a single phrase (seconds)
    PHRASE_TIMEOUT = 3.0  # Reduced for faster response
    
    # Path to vosk model (download from https://alphacephei.com/vosk/models)
    VOSK_MODEL_PATH = "models/vosk-model-small-en-us-0.15"
    
    # ═══════════════════════════════════════════════════════════════
    # COMMAND MAPPING
    # ═══════════════════════════════════════════════════════════════
    
    # Maps spoken phrases to action identifiers
    COMMAND_MAP: Dict[str, str] = {
        # Mouse actions
        "click": "click",
        "double click": "double_click",
        "right click": "right_click",
        
        # Scrolling
        "scroll up": "scroll_up",
        "scroll down": "scroll_down",
        "page up": "page_up",
        "page down": "page_down",
        
        # Browser navigation
        "go back": "browser_back",
        "go forward": "browser_forward",
        "new tab": "new_tab",
        "close tab": "close_tab",
        "refresh": "refresh",
        "refresh page": "refresh",
        
        # Zoom
        "zoom in": "zoom_in",
        "zoom out": "zoom_out",
        "reset zoom": "reset_zoom",
        
        # Media controls
        "mute": "mute",
        "unmute": "unmute",
        "volume up": "volume_up",
        "volume down": "volume_down",
        
        # Screenshot
        "screenshot": "screenshot",
        "take screenshot": "screenshot",
        
        # System control
        "pause gestura": "pause_gestures",
        "resume gestura": "resume_gestures",
        "stop gestura": "stop_gestures",
        "show help": "show_help",
    }
    
    # ═══════════════════════════════════════════════════════════════
    # TEXT-TO-SPEECH FEEDBACK
    # ═══════════════════════════════════════════════════════════════
    
    # Enable voice feedback (requires pyttsx3)
    VOICE_FEEDBACK_ENABLED = True
    
    # TTS speech rate (words per minute)
    TTS_RATE = 180
    
    # TTS volume (0.0 to 1.0)
    TTS_VOLUME = 0.8
    
    # Debug mode for voice recognition
    DEBUG_MODE = False  # Set to True for detailed voice debugging
    
    # Feedback messages for specific commands
    FEEDBACK_MESSAGES: Dict[str, str] = {
        "pause_gestures": "Gestura paused",
        "resume_gestures": "Gestura resumed",
        "stop_gestures": "Stopping Gestura",
        "show_help": "Voice commands available",
    }
    
    # ═══════════════════════════════════════════════════════════════
    # SHARED STATE (Thread-Safe)
    # ═══════════════════════════════════════════════════════════════
    
    # Threading lock for shared state
    _state_lock = threading.Lock()
    
    # Gesture system active flag (can be paused by voice)
    _gesture_active = True
    
    # Voice listening active flag
    _voice_active = True
    
    # System running flag
    _system_running = True
    
    @classmethod
    def is_gesture_active(cls) -> bool:
        """Thread-safe check if gesture system is active."""
        with cls._state_lock:
            return cls._gesture_active
    
    @classmethod
    def set_gesture_active(cls, active: bool) -> None:
        """Thread-safe set gesture system state."""
        with cls._state_lock:
            cls._gesture_active = active
    
    @classmethod
    def is_voice_active(cls) -> bool:
        """Thread-safe check if voice system is active."""
        with cls._state_lock:
            return cls._voice_active
    
    @classmethod
    def set_voice_active(cls, active: bool) -> None:
        """Thread-safe set voice system state."""
        with cls._state_lock:
            cls._voice_active = active
    
    @classmethod
    def is_system_running(cls) -> bool:
        """Thread-safe check if system is running."""
        with cls._state_lock:
            return cls._system_running
    
    @classmethod
    def stop_system(cls) -> None:
        """Thread-safe stop entire system."""
        with cls._state_lock:
            cls._system_running = False
