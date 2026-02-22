# gesture_temporal.py
from collections import deque
from typing import Optional
import time

class TemporalGestureValidator:
    """
    Multi-frame sliding window with majority-vote classification.
    A gesture is only confirmed when it holds majority across N frames
    for at least a minimum duration.
    """

    def __init__(
        self,
        window_size: int = 10,
        confirmation_threshold: float = 0.7,
        min_hold_seconds: float = 0.3,
    ):
        self.window_size = window_size
        self.confirmation_threshold = confirmation_threshold  # 70% majority required
        self.min_hold_seconds = min_hold_seconds

        self._window: deque = deque(maxlen=window_size)
        self._candidate: Optional[str] = None
        self._candidate_start: float = 0.0

    def update(self, raw_gesture: Optional[str]) -> Optional[str]:
        """
        Feed a raw per-frame gesture label. Returns confirmed gesture or None.
        """
        label = raw_gesture if raw_gesture else "NONE"
        self._window.append(label)

        if len(self._window) < self.window_size:
            return None  # Not enough history yet

        confirmed = self._majority_vote()

        if confirmed == "NONE":
            self._candidate = None
            return None

        now = time.monotonic()
        if confirmed != self._candidate:
            self._candidate = confirmed
            self._candidate_start = now
            return None  # Reset hold timer on gesture change

        if (now - self._candidate_start) >= self.min_hold_seconds:
            return confirmed

        return None  # Still within hold threshold

    def _majority_vote(self) -> str:
        from collections import Counter
        counts = Counter(self._window)
        top_label, top_count = counts.most_common(1)[0]
        if top_count / self.window_size >= self.confirmation_threshold:
            return top_label
        return "NONE"
