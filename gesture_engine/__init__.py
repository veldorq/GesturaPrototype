"""
Gestura 2.0 - Modular Gesture Recognition Engine

A production-ready gesture control system featuring:
- Two-hand tracking with MediaPipe
- 12 built-in gesture types (single-hand and two-hand)
- Custom gesture training and recognition
- Three smoothing algorithms (moving average, exponential, Kalman)
- Voice command integration
- Unified command execution
- Configurable via centralized config

Author: Gestura Development Team
Version: 2.0.0

Usage:
    from gesture_engine import GestureEngine
    
    engine = GestureEngine(use_smoothing=True, enable_voice=True)
    engine.start()
"""

__version__ = "2.0.0"
__author__ = "Gestura Development Team"

# Core exports
from gesture_engine.main import GestureEngine, EngineMode, EngineState
from gesture_engine.hand_tracker import TwoHandTracker, HandData, HandLabel
from gesture_engine.gesture_classifier import GestureClassifier, GestureType, GestureResult
from gesture_engine.gesture_trainer import GestureTrainer, TrainedGesture
# VoiceController is new Vosk-based system - VoiceControllerClass/VoiceCommand no longer exist
from gesture_engine.command_executor import CommandExecutor, ActionType, ActionResult
from gesture_engine.smoothing import (
    MovingAverageFilter,
    ExponentialSmoothingFilter,
    KalmanFilter,
    MultiLandmarkSmoother,
    LandmarkPoint
)
from gesture_engine.config import (
    CONFIG,
    GestureEngineConfig,
    HandTrackingConfig,
    SmoothingConfig,
    GestureClassificationConfig,
    GestureTrainingConfig,
    VoiceControlConfig,
    CommandExecutionConfig,
    PerformanceConfig
)

__all__ = [
    # Main Engine
    "GestureEngine",
    "EngineMode",
    "EngineState",
    
    # Hand Tracking
    "TwoHandTracker",
    "HandData",
    "HandLabel",
    
    # Gesture Classification
    "GestureClassifier",
    "GestureType",
    "GestureResult",
    
    # Gesture Training
    "GestureTrainer",
    "TrainedGesture",
    
    # Voice Control
    # VoiceController and VoiceCommand removed (replaced with Vosk-based system)
    
    # Command Execution
    "CommandExecutor",
    "ActionType",
    "ActionResult",
    
    # Smoothing
    "MovingAverageFilter",
    "ExponentialSmoothingFilter",
    "KalmanFilter",
    "MultiLandmarkSmoother",
    "LandmarkPoint",
    
    # Configuration
    "CONFIG",
    "GestureEngineConfig",
    "HandTrackingConfig",
    "SmoothingConfig",
    "GestureClassificationConfig",
    "GestureTrainingConfig",
    "VoiceControlConfig",
    "CommandExecutionConfig",
    "PerformanceConfig",
]
