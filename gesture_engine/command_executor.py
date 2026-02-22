"""
Command Execution Module

Unified command executor for both gesture and voice commands.
Handles system actions like mouse control, keyboard input, and application control.

Author: Gestura Development Team
Version: 2.0.0
"""

import time
import pyautogui
from typing import Optional, Dict, Callable
from enum import Enum
from dataclasses import dataclass

from gesture_engine.gesture_classifier import GestureType
# VoiceCommand no longer exists - voice commands handled by voice_commands module
from gesture_engine.config import CONFIG

# Disable PyAutoGUI fail-safe (Ctrl+C still works)
pyautogui.FAILSAFE = False


class ActionType(Enum):
    """Types of actions that can be executed."""
    MOUSE_CLICK = "mouse_click"
    MOUSE_DOUBLE_CLICK = "mouse_double_click"
    MOUSE_RIGHT_CLICK = "mouse_right_click"
    KEY_PRESS = "key_press"
    KEY_COMBINATION = "key_combination"
    SCROLL = "scroll"
    VOLUME = "volume"
    BROWSER_ACTION = "browser_action"
    SYSTEM_ACTION = "system_action"
    MODE_SWITCH = "mode_switch"
    CUSTOM = "custom"


@dataclass
class ActionResult:
    """Result of action execution."""
    success: bool
    action_type: ActionType
    details: str
    timestamp: float


class CommandExecutor:
    """
    Executes commands from gestures and voice input.
    
    Features:
    - Unified gesture and voice command handling
    - Configurable action mapping
    - Action cooldown/debouncing
    - Visual/audio feedback (optional)
    - Command priority (voice overrides gesture)
    - Custom action hooks
    """
    
    def __init__(self):
        """Initialize command executor."""
        self.config = CONFIG.execution
        
        # Load action mappings from config
        self.gesture_actions = self.config.gesture_actions.copy()
        self.voice_actions = CONFIG.voice.voice_commands.copy()
        
        # Execution state
        self.last_action_time = 0.0
        self.current_mode = "default"
        self.actions_executed = 0
        
        # Custom action handlers
        self.custom_handlers: Dict[str, Callable] = {}
        
        # Action history (for debugging/logging)
        self.action_history: list = []
        self.max_history_size = 100
    
    def execute_gesture(self, gesture: GestureType) -> Optional[ActionResult]:
        """
        Execute action for recognized gesture.
        
        Args:
            gesture: Detected gesture type
            
        Returns:
            ActionResult if action executed, None if skipped
        """
        # Get mapped action
        action_name = self.gesture_actions.get(gesture.value)
        
        if not action_name:
            return None
        
        return self._execute_action(action_name, source="gesture", details=gesture.value)
    
    def execute_voice_command(self, command: str) -> Optional[ActionResult]:  # type: ignore
        """
        Execute action for voice command.
        
        Args:
            command: Recognized voice command (String, not enum anymore)
            
        Returns:
            ActionResult if action executed, None if skipped
        """
        action_name = command  # command is now a string, not an enum
        return self._execute_action(action_name, source="voice", details=command)
    
    def _execute_action(
        self,
        action_name: str,
        source: str,
        details: str
    ) -> Optional[ActionResult]:
        """
        Internal action execution with cooldown and routing.
        
        Args:
            action_name: Name of action to execute
            source: Source of command ("gesture" or "voice")
            details: Additional context
            
        Returns:
            ActionResult or None if cooldown active
        """
        current_time = time.time()
        
        # Check cooldown
        if current_time - self.last_action_time < self.config.action_delay:
            return None
        
        # Route to appropriate handler
        result = None
        
        if action_name == "mouse_click":
            result = self._action_mouse_click()
        elif action_name == "mouse_double_click":
            result = self._action_mouse_double_click()
        elif action_name == "mouse_right_click":
            result = self._action_mouse_right_click()
        elif action_name.startswith("key_"):
            key = action_name.replace("key_", "")
            result = self._action_key_press(key)
        elif action_name.startswith("scroll_"):
            direction = action_name.replace("scroll_", "")
            result = self._action_scroll(direction)
        elif action_name.startswith("volume_"):
            direction = action_name.replace("volume_", "")
            result = self._action_volume(direction)
        elif action_name.startswith("browser_"):
            browser_action = action_name.replace("browser_", "")
            result = self._action_browser(browser_action)
        elif action_name.startswith("enable_"):
            mode = action_name.replace("enable_", "")
            result = self._action_mode_switch(mode, True)
        elif action_name.startswith("disable_"):
            mode = action_name.replace("disable_", "")
            result = self._action_mode_switch(mode, False)
        elif action_name in ["pause_gesture", "resume_gesture"]:
            result = self._action_pause_resume(action_name)
        elif action_name == "screenshot":
            result = self._action_screenshot()
        elif action_name in ["zoom_in", "zoom_out"]:
            result = self._action_zoom(action_name)
        elif action_name in self.custom_handlers:
            result = self._action_custom(action_name)
        else:
            result = ActionResult(
                success=False,
                action_type=ActionType.CUSTOM,
                details=f"Unknown action: {action_name}",
                timestamp=current_time
            )
        
        if result and result.success:
            self.last_action_time = current_time
            self.actions_executed += 1
            self._add_to_history(result, source, details)
            
            # Optional feedback
            if self.config.enable_feedback:
                self._provide_feedback(result)
        
        return result
    
    # ============ ACTION IMPLEMENTATIONS ============
    
    def _action_mouse_click(self) -> ActionResult:
        """Execute mouse left click."""
        try:
            pyautogui.click()
            return ActionResult(
                success=True,
                action_type=ActionType.MOUSE_CLICK,
                details="Left click",
                timestamp=time.time()
            )
        except Exception as e:
            return self._error_result(ActionType.MOUSE_CLICK, str(e))
    
    def _action_mouse_double_click(self) -> ActionResult:
        """Execute mouse double click."""
        try:
            pyautogui.doubleClick()
            return ActionResult(
                success=True,
                action_type=ActionType.MOUSE_DOUBLE_CLICK,
                details="Double click",
                timestamp=time.time()
            )
        except Exception as e:
            return self._error_result(ActionType.MOUSE_DOUBLE_CLICK, str(e))
    
    def _action_mouse_right_click(self) -> ActionResult:
        """Execute mouse right click."""
        try:
            pyautogui.rightClick()
            return ActionResult(
                success=True,
                action_type=ActionType.MOUSE_CLICK,
                details="Right click",
                timestamp=time.time()
            )
        except Exception as e:
            return self._error_result(ActionType.MOUSE_CLICK, str(e))
    
    def _action_key_press(self, key: str) -> ActionResult:
        """Execute keyboard key press."""
        try:
            pyautogui.press(key)
            return ActionResult(
                success=True,
                action_type=ActionType.KEY_PRESS,
                details=f"Key: {key}",
                timestamp=time.time()
            )
        except Exception as e:
            return self._error_result(ActionType.KEY_PRESS, str(e))
    
    def _action_scroll(self, direction: str) -> ActionResult:
        """Execute scroll action."""
        try:
            amount = 3  # Scroll lines
            if direction == "up":
                pyautogui.scroll(amount)
            elif direction == "down":
                pyautogui.scroll(-amount)
            else:
                return self._error_result(ActionType.SCROLL, f"Invalid direction: {direction}")
            
            return ActionResult(
                success=True,
                action_type=ActionType.SCROLL,
                details=f"Scroll {direction}",
                timestamp=time.time()
            )
        except Exception as e:
            return self._error_result(ActionType.SCROLL, str(e))
    
    def _action_volume(self, direction: str) -> ActionResult:
        """Execute volume control."""
        try:
            if direction == "up":
                pyautogui.press("volumeup")
            elif direction == "down":
                pyautogui.press("volumedown")
            elif direction == "mute":
                pyautogui.press("volumemute")
            else:
                return self._error_result(ActionType.VOLUME, f"Invalid direction: {direction}")
            
            return ActionResult(
                success=True,
                action_type=ActionType.VOLUME,
                details=f"Volume {direction}",
                timestamp=time.time()
            )
        except Exception as e:
            return self._error_result(ActionType.VOLUME, str(e))
    
    def _action_browser(self, action: str) -> ActionResult:
        """Execute browser-specific actions."""
        try:
            if action == "back":
                pyautogui.hotkey("alt", "left")
            elif action == "forward":
                pyautogui.hotkey("alt", "right")
            elif action == "new_tab":
                pyautogui.hotkey("ctrl", "t")
            elif action == "close_tab":
                pyautogui.hotkey("ctrl", "w")
            elif action == "refresh":
                pyautogui.hotkey("ctrl", "r")
            else:
                return self._error_result(ActionType.BROWSER_ACTION, f"Unknown action: {action}")
            
            return ActionResult(
                success=True,
                action_type=ActionType.BROWSER_ACTION,
                details=f"Browser {action}",
                timestamp=time.time()
            )
        except Exception as e:
            return self._error_result(ActionType.BROWSER_ACTION, str(e))
    
    def _action_mode_switch(self, mode: str, enable: bool) -> ActionResult:
        """Switch between control modes."""
        if enable:
            self.current_mode = mode
            details = f"Enabled {mode} mode"
        else:
            self.current_mode = "default"
            details = f"Disabled {mode} mode"
        
        return ActionResult(
            success=True,
            action_type=ActionType.MODE_SWITCH,
            details=details,
            timestamp=time.time()
        )
    
    def _action_pause_resume(self, action: str) -> ActionResult:
        """Pause or resume gesture recognition."""
        details = "Paused" if action == "pause_gesture" else "Resumed"
        return ActionResult(
            success=True,
            action_type=ActionType.SYSTEM_ACTION,
            details=details,
            timestamp=time.time()
        )
    
    def _action_screenshot(self) -> ActionResult:
        """Take screenshot."""
        try:
            pyautogui.hotkey("win", "printscreen")
            return ActionResult(
                success=True,
                action_type=ActionType.SYSTEM_ACTION,
                details="Screenshot taken",
                timestamp=time.time()
            )
        except Exception as e:
            return self._error_result(ActionType.SYSTEM_ACTION, str(e))
    
    def _action_zoom(self, action: str) -> ActionResult:
        """Execute zoom in/out."""
        try:
            if action == "zoom_in":
                pyautogui.hotkey("ctrl", "+")
            else:
                pyautogui.hotkey("ctrl", "-")
            
            return ActionResult(
                success=True,
                action_type=ActionType.SYSTEM_ACTION,
                details=action,
                timestamp=time.time()
            )
        except Exception as e:
            return self._error_result(ActionType.SYSTEM_ACTION, str(e))
    
    def _action_custom(self, action_name: str) -> ActionResult:
        """Execute custom registered action."""
        try:
            handler = self.custom_handlers[action_name]
            handler()
            return ActionResult(
                success=True,
                action_type=ActionType.CUSTOM,
                details=f"Custom: {action_name}",
                timestamp=time.time()
            )
        except Exception as e:
            return self._error_result(ActionType.CUSTOM, str(e))
    
    def _error_result(self, action_type: ActionType, error: str) -> ActionResult:
        """Create error result."""
        return ActionResult(
            success=False,
            action_type=action_type,
            details=f"Error: {error}",
            timestamp=time.time()
        )
    
    # ============ UTILITY METHODS ============
    
    def register_custom_action(self, action_name: str, handler: Callable) -> None:
        """Register custom action handler."""
        self.custom_handlers[action_name] = handler
        print(f"Registered custom action: {action_name}")
    
    def _add_to_history(self, result: ActionResult, source: str, details: str) -> None:
        """Add action to history log."""
        self.action_history.append({
            "result": result,
            "source": source,
            "details": details
        })
        
        # Trim history if too large
        if len(self.action_history) > self.max_history_size:
            self.action_history = self.action_history[-self.max_history_size:]
    
    def _provide_feedback(self, result: ActionResult) -> None:
        """Provide visual/audio feedback for action."""
        # Simple console feedback (can be extended to GUI)
        print(f"[{result.action_type.value}] {result.details}")
    
    def get_statistics(self) -> Dict:
        """Get execution statistics."""
        return {
            "actions_executed": self.actions_executed,
            "current_mode": self.current_mode,
            "last_action_time": self.last_action_time,
            "history_size": len(self.action_history)
        }


if __name__ == "__main__":
    # Test command executor
    print("Command Executor Test")
    print("=" * 50)
    
    executor = CommandExecutor()
    
    # Test mouse actions
    print("\nTesting mouse click...")
    result = executor._action_mouse_click()
    print(f"Result: {result.success} - {result.details}")
    
    print("\nTesting scroll...")
    result = executor._action_scroll("up")
    print(f"Result: {result.success} - {result.details}")
    
    print("\nStatistics:")
    stats = executor.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
