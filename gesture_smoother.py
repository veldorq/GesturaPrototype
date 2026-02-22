# gesture_smoother.py
import numpy as np
from collections import deque
from typing import List, Optional

class LandmarkSmoother:
    """
    Exponential moving average over MediaPipe hand landmarks.
    Reduces jitter without adding significant latency.
    """

    def __init__(self, alpha: float = 0.4, num_landmarks: int = 21):
        """
        alpha: smoothing factor. Lower = smoother but more lag.
               0.4 is a good balance for real-time use.
        """
        self.alpha = alpha
        self.num_landmarks = num_landmarks
        self._smoothed: Optional[np.ndarray] = None  # shape (21, 3)

    def update(self, landmarks) -> np.ndarray:
        """
        landmarks: mediapipe hand_landmarks.landmark list
        Returns smoothed numpy array of shape (21, 3).
        """
        raw = np.array([[lm.x, lm.y, lm.z] for lm in landmarks])

        if self._smoothed is None:
            self._smoothed = raw.copy()
        else:
            self._smoothed = self.alpha * raw + (1 - self.alpha) * self._smoothed

        return self._smoothed

    def reset(self):
        self._smoothed = None


class GestureConfidenceScorer:
    """
    Scores landmark consistency across recent frames.
    Low variance = high confidence the hand is stable.
    """

    def __init__(self, buffer_size: int = 8):
        self._history: deque = deque(maxlen=buffer_size)

    def update(self, smoothed_landmarks: np.ndarray) -> float:
        """Returns confidence score in [0.0, 1.0]."""
        self._history.append(smoothed_landmarks)
        if len(self._history) < 3:
            return 0.0

        stack = np.stack(self._history)          # (N, 21, 3)
        variance = np.mean(np.var(stack, axis=0))

        # Map variance to confidence: lower variance → higher confidence
        # Tuned empirically; adjust MAX_VAR to your camera/resolution
        MAX_VAR = 0.002
        confidence = float(np.clip(1.0 - (variance / MAX_VAR), 0.0, 1.0))
        return confidence
