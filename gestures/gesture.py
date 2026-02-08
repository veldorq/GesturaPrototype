"""
Gesture definition and library management.
Defines the abstraction layer between raw landmarks and semantic gestures.
"""

import json
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
from pathlib import Path


@dataclass
class Gesture:
    """
    Represents a gesture with its defining characteristics.
    
    A gesture is defined by hand shape features derived from landmarks,
    not by raw landmark positions (which vary by hand size and position).
    """
    name: str
    description: str
    features: Dict[str, float]  # Normalized geometric features
    
    def to_dict(self) -> Dict:
        """Convert gesture to dictionary for serialization."""
        return asdict(self)
    
    @staticmethod
    def from_dict(data: Dict) -> 'Gesture':
        """Create gesture from dictionary."""
        return Gesture(**data)


class GestureLibrary:
    """
    Manages a collection of known gestures.
    Handles loading, saving, and querying gesture definitions.
    """
    
    def __init__(self, library_file: Optional[str] = None):
        """
        Initialize gesture library.
        
        Args:
            library_file: Path to JSON file containing gesture definitions
        """
        self.gestures: Dict[str, Gesture] = {}
        self.library_file = library_file
        
        # Load default gestures
        self._load_default_gestures()
        
        # Load custom gestures from file if provided
        if library_file and Path(library_file).exists():
            self.load_from_file(library_file)
    
    def _load_default_gestures(self) -> None:
        """
        Load built-in default gestures.
        These are baseline gestures that provide good accessibility.
        """
        # Open palm - neutral/pause gesture
        # Features: All fingers extended, spread apart
        self.add_gesture(Gesture(
            name='open_palm',
            description='Open palm with fingers extended',
            features={
                'fingers_extended': 5.0,
                'finger_spread': 0.8,
                'thumb_angle': 0.7,
            }
        ))
        
        # Fist - click gesture
        # Features: All fingers curled
        self.add_gesture(Gesture(
            name='fist',
            description='Closed fist',
            features={
                'fingers_extended': 0.0,
                'finger_curl': 0.9,
                'thumb_angle': 0.2,
            }
        ))
        
        # Peace sign - two fingers extended
        self.add_gesture(Gesture(
            name='peace_sign',
            description='Index and middle fingers extended',
            features={
                'fingers_extended': 2.0,
                'index_extended': 1.0,
                'middle_extended': 1.0,
                'ring_extended': 0.0,
                'pinky_extended': 0.0,
            }
        ))
        
        # Thumbs up - scroll up
        self.add_gesture(Gesture(
            name='thumbs_up',
            description='Thumb pointing upward',
            features={
                'thumb_extended': 1.0,
                'thumb_angle': 0.9,
                'fingers_extended': 0.0,
                'finger_curl': 0.8,
            }
        ))
        
        # Thumbs down - scroll down
        self.add_gesture(Gesture(
            name='thumbs_down',
            description='Thumb pointing downward',
            features={
                'thumb_extended': 1.0,
                'thumb_angle': -0.9,
                'fingers_extended': 0.0,
                'finger_curl': 0.8,
            }
        ))
    
    def add_gesture(self, gesture: Gesture) -> None:
        """
        Add or update a gesture in the library.
        
        Args:
            gesture: Gesture to add
        """
        self.gestures[gesture.name] = gesture
    
    def get_gesture(self, name: str) -> Optional[Gesture]:
        """
        Retrieve a gesture by name.
        
        Args:
            name: Gesture name
            
        Returns:
            Gesture if found, None otherwise
        """
        return self.gestures.get(name)
    
    def get_all_gestures(self) -> List[Gesture]:
        """Get list of all gestures in library."""
        return list(self.gestures.values())
    
    def remove_gesture(self, name: str) -> bool:
        """
        Remove a gesture from library.
        
        Args:
            name: Gesture name
            
        Returns:
            True if removed, False if not found
        """
        if name in self.gestures:
            del self.gestures[name]
            return True
        return False
    
    def save_to_file(self, file_path: str) -> None:
        """
        Save gesture library to JSON file.
        
        Args:
            file_path: Path to save file
        """
        data = {
            name: gesture.to_dict()
            for name, gesture in self.gestures.items()
        }
        
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_from_file(self, file_path: str) -> None:
        """
        Load gestures from JSON file.
        
        Args:
            file_path: Path to load from
        """
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            for name, gesture_dict in data.items():
                gesture = Gesture.from_dict(gesture_dict)
                self.add_gesture(gesture)
                
        except Exception as e:
            print(f"Warning: Could not load gesture library: {e}")
