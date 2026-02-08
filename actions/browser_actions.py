"""
Browser action automation using PyAutoGUI.
Executes user actions based on recognized gestures.
"""

import pyautogui
import time
from typing import Callable, Dict
from config.constants import Constants


# Configure PyAutoGUI safety features
pyautogui.FAILSAFE = True  # Move mouse to corner to abort
pyautogui.PAUSE = 0.1  # Small pause between actions for stability


class BrowserActions:
    """
    Executes browser and system actions via PyAutoGUI.
    
    This class serves as the action execution layer, mapping
    abstract action names to concrete system interactions.
    """
    
    def __init__(self):
        """Initialize browser actions handler."""
        # Map action names to methods
        self.action_map: Dict[str, Callable] = {
            'none': self.do_nothing,
            'left_click': self.left_click,
            'right_click': self.right_click,
            'scroll_up': self.scroll_up,
            'scroll_down': self.scroll_down,
            'browser_back': self.browser_back,
            'browser_forward': self.browser_forward,
        }
        
        self.last_action_time = 0.0
    
    def execute(self, action_name: str) -> bool:
        """
        Execute an action by name.
        
        Args:
            action_name: Name of action to execute
            
        Returns:
            True if action executed successfully, False otherwise
        """
        if action_name not in self.action_map:
            print(f"Warning: Unknown action '{action_name}'")
            return False
        
        try:
            # Execute the action
            action_func = self.action_map[action_name]
            action_func()
            
            self.last_action_time = time.time()
            return True
            
        except Exception as e:
            print(f"Error executing action '{action_name}': {e}")
            return False
    
    def do_nothing(self) -> None:
        """
        Neutral action - used for pause gesture.
        This is intentional - allows users to rest without triggering actions.
        """
        pass
    
    def left_click(self) -> None:
        """
        Perform left mouse click at current cursor position.
        Most common action for web interaction (links, buttons, etc).
        """
        pyautogui.click()
        print("Action: Left Click")
    
    def right_click(self) -> None:
        """
        Perform right mouse click at current cursor position.
        Opens context menus in most applications.
        """
        pyautogui.rightClick()
        print("Action: Right Click")
    
    def scroll_up(self) -> None:
        """
        Scroll page upward.
        Uses configured scroll amount for consistent behavior.
        """
        pyautogui.scroll(Constants.SCROLL_AMOUNT)
        print("Action: Scroll Up")
    
    def scroll_down(self) -> None:
        """
        Scroll page downward.
        Negative value scrolls down in PyAutoGUI.
        """
        pyautogui.scroll(-Constants.SCROLL_AMOUNT)
        print("Action: Scroll Down")
    
    def browser_back(self) -> None:
        """
        Navigate back in browser history.
        Uses Alt+Left Arrow keyboard shortcut (works in most browsers).
        """
        pyautogui.hotkey('alt', 'left')
        print("Action: Browser Back")
    
    def browser_forward(self) -> None:
        """
        Navigate forward in browser history.
        Uses Alt+Right Arrow keyboard shortcut (works in most browsers).
        """
        pyautogui.hotkey('alt', 'right')
        print("Action: Browser Forward")
    
    def get_available_actions(self) -> list:
        """
        Get list of all available action names.
        
        Returns:
            List of action names
        """
        return list(self.action_map.keys())
