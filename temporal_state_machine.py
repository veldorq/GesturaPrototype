# gesture_state_machine.py
from enum import Enum, auto
import time
from typing import Optional, Callable

class GestureState(Enum):
    IDLE      = auto()
    DETECTING = auto()
    CONFIRMED = auto()
    ACTIVE    = auto()
    RELEASED  = auto()

class GestureStateMachine:
    """
    State diagram:
        IDLE → DETECTING (gesture candidate appears)
        DETECTING → CONFIRMED (temporal validator confirms)
        DETECTING → IDLE (gesture lost)
        CONFIRMED → ACTIVE (command dispatched)
        ACTIVE → RELEASED (gesture ends)
        RELEASED → IDLE (after cooldown)
    """

    def __init__(
        self,
        cooldown_seconds: float = 0.8,
        on_activate: Optional[Callable[[str], None]] = None,
    ):
        self.cooldown_seconds = cooldown_seconds
        self.on_activate = on_activate  # callback(gesture_name)

        self.state = GestureState.IDLE
        self.active_gesture: Optional[str] = None
        self._last_release_time: float = 0.0

    def update(self, confirmed_gesture: Optional[str]) -> GestureState:
        now = time.monotonic()

        if self.state == GestureState.IDLE:
            if confirmed_gesture:
                self.active_gesture = confirmed_gesture
                self.state = GestureState.DETECTING

        elif self.state == GestureState.DETECTING:
            if confirmed_gesture == self.active_gesture:
                self.state = GestureState.CONFIRMED
            else:
                self._reset()

        elif self.state == GestureState.CONFIRMED:
            if confirmed_gesture == self.active_gesture:
                self._dispatch()
                self.state = GestureState.ACTIVE
            else:
                self._reset()

        elif self.state == GestureState.ACTIVE:
            if confirmed_gesture != self.active_gesture:
                self.state = GestureState.RELEASED
                self._last_release_time = now

        elif self.state == GestureState.RELEASED:
            if (now - self._last_release_time) >= self.cooldown_seconds:
                self._reset()

        return self.state

    def _dispatch(self):
        if self.on_activate and self.active_gesture:
            self.on_activate(self.active_gesture)

    def _reset(self):
        self.state = GestureState.IDLE
        self.active_gesture = None

    def is_locked(self) -> bool:
        """True when system should ignore new gestures."""
        return self.state in (GestureState.ACTIVE, GestureState.RELEASED)
