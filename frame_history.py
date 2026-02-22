# frame_history.py
from collections import deque
from dataclasses import dataclass, field
from typing import Optional, List
import time
import numpy as np

@dataclass
class FrameRecord:
    timestamp: float
    raw_gesture: Optional[str]
    confidence: float
    smoothed_landmarks: Optional[np.ndarray]

class FrameHistoryBuffer:
    """
    Stores per-frame records for temporal analysis and debugging.
    Also provides gesture sequence validation.
    """

    def __init__(self, max_frames: int = 60):
        self._buffer: deque = deque(maxlen=max_frames)

    def record(
        self,
        raw_gesture: Optional[str],
        confidence: float,
        smoothed_landmarks: Optional[np.ndarray] = None,
    ):
        self._buffer.append(FrameRecord(
            timestamp=time.monotonic(),
            raw_gesture=raw_gesture,
            confidence=confidence,
            smoothed_landmarks=smoothed_landmarks,
        ))

    def gesture_stability_score(self, last_n: int = 15) -> float:
        """
        What fraction of the last N frames agree on the same gesture?
        Returns [0.0, 1.0].
        """
        recent = list(self._buffer)[-last_n:]
        if not recent:
            return 0.0
        labels = [r.raw_gesture for r in recent]
        from collections import Counter
        most_common_count = Counter(labels).most_common(1)[0][1]
        return most_common_count / len(labels)

    def recent_gestures(self, last_n: int = 10) -> List[Optional[str]]:
        return [r.raw_gesture for r in list(self._buffer)[-last_n:]]

    def average_confidence(self, last_n: int = 10) -> float:
        recent = list(self._buffer)[-last_n:]
        if not recent:
            return 0.0
        return float(np.mean([r.confidence for r in recent]))
