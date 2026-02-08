"""
Gesture State Machine for temporal stability and action control.

STATE LIFECYCLE:
NONE → CANDIDATE → CONFIRMED → COOLDOWN → NONE

NONE: No gesture detected
CANDIDATE: Gesture detected but not yet stable
CONFIRMED: Gesture is stable and validated, action can fire
COOLDOWN: Action fired, block all gestures temporarily
"""

import time
from enum import Enum
from typing import Optional
from collections import deque
from dataclasses import dataclass

from gesture_classification import GestureResult
from config.constants import Constants


class GestureState(Enum):
    """
    States in the gesture lifecycle.
    
    NONE: No gesture detected or recognized
    CANDIDATE: Gesture detected, collecting frames for stability
    CONFIRMED: Gesture stable across frames, ready to trigger action
    COOLDOWN: Action triggered, blocking further gestures
    """
    NONE = "none"
    CANDIDATE = "candidate"
    CONFIRMED = "confirmed"
    COOLDOWN = "cooldown"


@dataclass
class GestureFrameData:
    """Data stored for each frame in the stability window."""
    gesture_name: Optional[str]
    confidence: float
    timestamp: float


class GestureStateMachine:
    """
    Manages gesture state transitions and temporal stability.
    
    CONFLICT PREVENTION:
    - Only ONE gesture can be in CONFIRMED state at a time
    - COOLDOWN state blocks ALL gestures after action fires
    - Stability window ensures transient detections are ignored
    - Dwell time prevents accidental triggers
    
    TRANSITION RULES:
    1. NONE → CANDIDATE: Gesture detected above confidence threshold
    2. CANDIDATE → CONFIRMED: Same gesture stable for N frames + dwell time met
    3. CANDIDATE → NONE: Gesture lost or changes
    4. CONFIRMED → COOLDOWN: Action executed
    5. COOLDOWN → NONE: Cooldown timer expires
    """
    
    def __init__(
        self,
        stability_window: int = Constants.STABILIZATION_WINDOW,
        dwell_time: float = Constants.DWELL_TIME_SECONDS,
        cooldown_time: float = Constants.DEBOUNCE_COOLDOWN_SECONDS
    ):
        """
        Initialize state machine.
        
        Args:
            stability_window: Number of frames gesture must be consistent
            dwell_time: Seconds gesture must be held before confirming
            cooldown_time: Seconds to block gestures after action
        """
        self.stability_window = stability_window
        self.dwell_time = dwell_time
        self.cooldown_time = cooldown_time
        
        # Current state
        self.state = GestureState.NONE
        
        # Frame buffer for stability checking
        self.frame_buffer: deque[GestureFrameData] = deque(
            maxlen=stability_window
        )
        
        # Candidate tracking
        self.candidate_gesture: Optional[str] = None
        self.candidate_start_time: Optional[float] = None
        
        # Confirmed tracking
        self.confirmed_gesture: Optional[str] = None
        self.confirmed_time: Optional[float] = None
        
        # Cooldown tracking
        self.cooldown_start_time: Optional[float] = None
        
        # Metrics
        self.last_action_time: float = 0.0
        self.action_count: int = 0
    
    def update(self, gesture_result: GestureResult, current_time: float) -> bool:
        """
        Update state machine with new gesture detection.
        
        Args:
            gesture_result: Result from gesture classifier
            current_time: Current timestamp
            
        Returns:
            True if action should be triggered, False otherwise
        """
        # Add to frame buffer
        self.frame_buffer.append(GestureFrameData(
            gesture_name=gesture_result.gesture_name,
            confidence=gesture_result.confidence,
            timestamp=current_time
        ))
        
        # State machine logic
        if self.state == GestureState.COOLDOWN:
            return self._handle_cooldown_state(current_time)
        
        elif self.state == GestureState.NONE:
            return self._handle_none_state(gesture_result, current_time)
        
        elif self.state == GestureState.CANDIDATE:
            return self._handle_candidate_state(gesture_result, current_time)
        
        elif self.state == GestureState.CONFIRMED:
            return self._handle_confirmed_state(gesture_result, current_time)
        
        return False
    
    def _handle_none_state(
        self,
        gesture_result: GestureResult,
        current_time: float
    ) -> bool:
        """
        Handle NONE state - waiting for gesture detection.
        
        Transition: NONE → CANDIDATE if gesture detected
        """
        if gesture_result.gesture_name is not None:
            # Gesture detected - transition to CANDIDATE
            self.state = GestureState.CANDIDATE
            self.candidate_gesture = gesture_result.gesture_name
            self.candidate_start_time = current_time
            return False
        
        # Stay in NONE
        return False
    
    def _handle_candidate_state(
        self,
        gesture_result: GestureResult,
        current_time: float
    ) -> bool:
        """
        Handle CANDIDATE state - checking stability.
        
        Transition: 
        - CANDIDATE → CONFIRMED if stable + dwell time met
        - CANDIDATE → NONE if gesture lost or changed
        """
        # Check if gesture lost
        if gesture_result.gesture_name is None:
            self._reset_to_none()
            return False
        
        # Check if gesture changed
        if gesture_result.gesture_name != self.candidate_gesture:
            # Different gesture detected - restart as new candidate
            self.candidate_gesture = gesture_result.gesture_name
            self.candidate_start_time = current_time
            return False
        
        # Check stability across frame buffer
        if not self._is_gesture_stable(self.candidate_gesture):
            # Not yet stable - stay in CANDIDATE
            return False
        
        # Check dwell time
        elapsed = current_time - self.candidate_start_time
        if elapsed < self.dwell_time:
            # Not held long enough - stay in CANDIDATE
            return False
        
        # Stable and dwell time met - transition to CONFIRMED
        self.state = GestureState.CONFIRMED
        self.confirmed_gesture = self.candidate_gesture
        self.confirmed_time = current_time
        
        # Trigger action
        self.action_count += 1
        self.last_action_time = current_time
        
        # Immediately transition to COOLDOWN
        self.state = GestureState.COOLDOWN
        self.cooldown_start_time = current_time
        
        return True  # Signal action should execute
    
    def _handle_confirmed_state(
        self,
        gesture_result: GestureResult,
        current_time: float
    ) -> bool:
        """
        Handle CONFIRMED state - gesture confirmed, action triggered.
        
        This state should immediately transition to COOLDOWN after
        action is triggered, so this handler should rarely be reached.
        
        Transition: CONFIRMED → COOLDOWN
        """
        # Immediately go to cooldown
        self.state = GestureState.COOLDOWN
        self.cooldown_start_time = current_time
        return False
    
    def _handle_cooldown_state(self, current_time: float) -> bool:
        """
        Handle COOLDOWN state - blocking all gestures temporarily.
        
        Transition: COOLDOWN → NONE when cooldown expires
        """
        elapsed = current_time - self.cooldown_start_time
        
        if elapsed >= self.cooldown_time:
            # Cooldown expired - return to NONE
            self._reset_to_none()
            return False
        
        # Still in cooldown - block all gestures
        return False
    
    def _is_gesture_stable(self, gesture_name: str) -> bool:
        """
        Check if gesture is stable across frame buffer.
        
        Stability criteria:
        - Buffer must be full
        - Majority of frames must contain the same gesture
        - Confidence must be consistently high
        
        Args:
            gesture_name: Gesture to check for stability
            
        Returns:
            True if gesture is stable
        """
        # Buffer must be full
        if len(self.frame_buffer) < self.stability_window:
            return False
        
        # Count matching gestures
        matching_count = sum(
            1 for frame in self.frame_buffer
            if frame.gesture_name == gesture_name
        )
        
        # Require at least 80% consistency (stricter than original)
        required_consistency = self.stability_window * 0.8
        
        if matching_count < required_consistency:
            return False
        
        # Check average confidence
        matching_confidences = [
            frame.confidence for frame in self.frame_buffer
            if frame.gesture_name == gesture_name
        ]
        
        if not matching_confidences:
            return False
        
        avg_confidence = sum(matching_confidences) / len(matching_confidences)
        
        if avg_confidence < Constants.GESTURE_CONFIDENCE_THRESHOLD:
            return False
        
        return True
    
    def _reset_to_none(self) -> None:
        """Reset state machine to NONE state."""
        self.state = GestureState.NONE
        self.candidate_gesture = None
        self.candidate_start_time = None
        self.confirmed_gesture = None
        self.confirmed_time = None
    
    def get_dwell_progress(self, current_time: float) -> float:
        """
        Get current dwell time progress for UI feedback.
        
        Returns:
            Progress value in [0, 1]
        """
        if self.state != GestureState.CANDIDATE:
            return 0.0
        
        if self.candidate_start_time is None:
            return 0.0
        
        # Check if stable first
        if not self._is_gesture_stable(self.candidate_gesture):
            return 0.0
        
        elapsed = current_time - self.candidate_start_time
        progress = min(elapsed / self.dwell_time, 1.0)
        
        return progress
    
    def get_cooldown_progress(self, current_time: float) -> float:
        """
        Get cooldown progress for UI feedback.
        
        Returns:
            Progress value in [0, 1], where 1 = cooldown complete
        """
        if self.state != GestureState.COOLDOWN:
            return 1.0
        
        if self.cooldown_start_time is None:
            return 1.0
        
        elapsed = current_time - self.cooldown_start_time
        progress = min(elapsed / self.cooldown_time, 1.0)
        
        return progress
    
    def force_cooldown(self, current_time: float) -> None:
        """
        Force immediate transition to cooldown state.
        Used for emergency stops or manual action triggers.
        """
        self.state = GestureState.COOLDOWN
        self.cooldown_start_time = current_time
    
    def reset(self) -> None:
        """Complete reset of state machine."""
        self._reset_to_none()
        self.frame_buffer.clear()
        self.cooldown_start_time = None
    
    def get_state_info(self, current_time: float) -> dict:
        """
        Get detailed state information for debugging/UI.
        
        Returns:
            Dictionary with state machine status
        """
        info = {
            'state': self.state.value,
            'current_gesture': None,
            'dwell_progress': 0.0,
            'cooldown_progress': 1.0,
            'buffer_fill': len(self.frame_buffer) / self.stability_window,
            'action_count': self.action_count,
        }
        
        if self.state == GestureState.CANDIDATE:
            info['current_gesture'] = self.candidate_gesture
            info['dwell_progress'] = self.get_dwell_progress(current_time)
        
        elif self.state == GestureState.CONFIRMED:
            info['current_gesture'] = self.confirmed_gesture
            info['dwell_progress'] = 1.0
        
        elif self.state == GestureState.COOLDOWN:
            info['cooldown_progress'] = self.get_cooldown_progress(current_time)
        
        return info
