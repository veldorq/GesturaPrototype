"""
Settings manager for persisting user preferences and gesture mappings.
"""

import json
import os
from typing import Dict, Any, Optional
from pathlib import Path


class Settings:
    """
    Manages loading, saving, and accessing user configuration.
    Handles gesture-to-action mappings and user preferences.
    """
    
    def __init__(self, config_dir: str = 'config'):
        """
        Initialize settings manager.
        
        Args:
            config_dir: Directory to store configuration files
        """
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        
        self.gestures_file = self.config_dir / 'gestures_config.json'
        self.settings_file = self.config_dir / 'user_settings.json'
        
        self.gesture_mappings: Dict[str, str] = {}
        self.user_preferences: Dict[str, Any] = {}
        
        self._load_defaults()
        self.load()
    
    def _load_defaults(self) -> None:
        """Load default gesture mappings and preferences."""
        # Default gesture-to-action mappings
        self.gesture_mappings = {
            'open_palm': 'none',  # Neutral/pause gesture
            'fist': 'left_click',
            'peace_sign': 'right_click',
            'thumbs_up': 'scroll_up',
            'thumbs_down': 'scroll_down',
            'swipe_left': 'browser_back',
            'swipe_right': 'browser_forward',
        }
        
        # Default user preferences
        self.user_preferences = {
            'dwell_time': 1.5,
            'sensitivity': 0.75,
            'show_overlay': True,
            'sound_feedback': False,
            'left_handed': False,
        }
    
    def load(self) -> None:
        """Load configuration from files if they exist."""
        # Load gesture mappings
        if self.gestures_file.exists():
            try:
                with open(self.gestures_file, 'r') as f:
                    loaded_mappings = json.load(f)
                    self.gesture_mappings.update(loaded_mappings)
            except Exception as e:
                print(f"Warning: Could not load gesture mappings: {e}")
        
        # Load user preferences
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r') as f:
                    loaded_prefs = json.load(f)
                    self.user_preferences.update(loaded_prefs)
            except Exception as e:
                print(f"Warning: Could not load user settings: {e}")
    
    def save(self) -> None:
        """Persist current configuration to disk."""
        try:
            # Save gesture mappings
            with open(self.gestures_file, 'w') as f:
                json.dump(self.gesture_mappings, f, indent=2)
            
            # Save user preferences
            with open(self.settings_file, 'w') as f:
                json.dump(self.user_preferences, f, indent=2)
                
        except Exception as e:
            print(f"Error saving configuration: {e}")
    
    def get_action_for_gesture(self, gesture_name: str) -> Optional[str]:
        """
        Get the action mapped to a gesture.
        
        Args:
            gesture_name: Name of the detected gesture
            
        Returns:
            Action name or None if not mapped
        """
        return self.gesture_mappings.get(gesture_name)
    
    def map_gesture_to_action(self, gesture_name: str, action_name: str) -> None:
        """
        Create or update a gesture-to-action mapping.
        
        Args:
            gesture_name: Name of the gesture
            action_name: Name of the action to trigger
        """
        self.gesture_mappings[gesture_name] = action_name
        self.save()
    
    def get_preference(self, key: str, default: Any = None) -> Any:
        """
        Get a user preference value.
        
        Args:
            key: Preference key
            default: Default value if key not found
            
        Returns:
            Preference value
        """
        return self.user_preferences.get(key, default)
    
    def set_preference(self, key: str, value: Any) -> None:
        """
        Set a user preference.
        
        Args:
            key: Preference key
            value: Value to set
        """
        self.user_preferences[key] = value
        self.save()
