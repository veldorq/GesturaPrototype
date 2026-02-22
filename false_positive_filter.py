# false_positive_filter.py
import numpy as np
from collections import deque
from typing import Optional

class MotionGate:
    """
    Suppresses gesture recognition during fast hand motion.
    Fast motion = high velocity of wrist landmark = likely transitioning.
    """

    def __init__(
        self,
        velocity_threshold: float = 0.04,
        history_len: int = 4,
    ):
        self.velocity_threshold = velocity_threshold
        self._wrist_history: deque = deque(maxlen=history_len)

    def update(self, smoothed_landmarks: np.ndarray) -> bool:
        """
        Returns True if motion is LOW enough to allow gesture detection.
        Blocks detection during rapid movement.
        """
        wrist = smoothed_landmarks[0]  # landmark 0 = wrist
        self._wrist_history.append(wrist)

        if len(self._wrist_history) < 2:
            return False

        positions = np.stack(self._wrist_history)
        deltas = np.diff(positions, axis=0)
        velocity = float(np.mean(np.linalg.norm(deltas, axis=1)))

        return velocity < self.velocity_threshold


class GestureHysteresis:
    """
    Prevents rapid toggling between two similar gestures.
    Once a gesture is active, a different gesture must persist
    for hysteresis_frames before it replaces it.
    """

    def __init__(self, hysteresis_frames: int = 6):
        self.hysteresis_frames = hysteresis_frames
        self._current: Optional[str] = None
        self._challenger: Optional[str] = None
        self._challenger_count: int = 0

    def update(self, gesture: Optional[str]) -> Optional[str]:
        if gesture == self._current:
            self._challenger = None
            self._challenger_count = 0
            return self._current

        if gesture == self._challenger:
            self._challenger_count += 1
        else:
            self._challenger = gesture
            self._challenger_count = 1

        if self._challenger_count >= self.hysteresis_frames:
            self._current = self._challenger
            self._challenger = None
            self._challenger_count = 0

        return self._current
