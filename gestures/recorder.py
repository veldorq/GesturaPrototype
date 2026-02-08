"""
Gesture recording utility for custom gesture creation.
Allows users to record their own gestures for personalization.
"""

import time
from typing import Optional
from collections import deque

from hand_tracking.detector import HandLandmarks
from gestures.gesture import Gesture, GestureLibrary
from gestures.recognizer import GestureRecognizer


class GestureRecorder:
    """
    Records custom gestures from user demonstrations.
    Captures multiple samples and averages features for robustness.
    """
    
    def __init__(self, gesture_library: GestureLibrary):
        """
        Initialize gesture recorder.
        
        Args:
            gesture_library: Library to save recorded gestures to
        """
        self.library = gesture_library
        self.recognizer = GestureRecognizer(gesture_library)
        
        self.is_recording = False
        self.recording_samples: deque = deque()
        self.gesture_name: Optional[str] = None
        self.gesture_description: Optional[str] = None
        
        # Recording parameters
        self.target_samples = 30  # Number of frames to capture
        self.recording_duration = 2.0  # Seconds to hold gesture
    
    def start_recording(
        self,
        gesture_name: str,
        description: str = ""
    ) -> None:
        """
        Start recording a new gesture.
        
        Args:
            gesture_name: Name for the new gesture
            description: Optional description
        """
        self.is_recording = True
        self.recording_samples.clear()
        self.gesture_name = gesture_name
        self.gesture_description = description or f"Custom gesture: {gesture_name}"
        
        print(f"Recording gesture '{gesture_name}' - hold pose steady...")
    
    def add_sample(self, landmarks: HandLandmarks) -> bool:
        """
        Add a sample frame during recording.
        
        Args:
            landmarks: Hand landmarks from current frame
            
        Returns:
            True if recording complete, False if more samples needed
        """
        if not self.is_recording:
            return False
        
        # Extract features for this sample
        features = self.recognizer.extract_features(landmarks)
        self.recording_samples.append(features)
        
        # Check if we have enough samples
        if len(self.recording_samples) >= self.target_samples:
            return True
        
        return False
    
    def stop_recording(self) -> Optional[Gesture]:
        """
        Stop recording and create gesture from samples.
        
        Returns:
            The newly created Gesture, or None if recording failed
        """
        if not self.is_recording or not self.recording_samples:
            return None
        
        self.is_recording = False
        
        # Average features across all samples for robustness
        # This reduces the impact of hand tremors and slight variations
        all_feature_keys = set()
        for sample in self.recording_samples:
            all_feature_keys.update(sample.keys())
        
        averaged_features = {}
        for feature_key in all_feature_keys:
            # Collect all values for this feature
            values = [
                sample[feature_key]
                for sample in self.recording_samples
                if feature_key in sample
            ]
            
            if values:
                # Use median instead of mean for better outlier resistance
                import statistics
                averaged_features[feature_key] = statistics.median(values)
        
        # Create new gesture
        new_gesture = Gesture(
            name=self.gesture_name,
            description=self.gesture_description,
            features=averaged_features
        )
        
        # Add to library
        self.library.add_gesture(new_gesture)
        
        print(f"Gesture '{self.gesture_name}' recorded successfully!")
        print(f"Captured {len(self.recording_samples)} samples")
        
        # Clear recording state
        self.recording_samples.clear()
        self.gesture_name = None
        
        return new_gesture
    
    def cancel_recording(self) -> None:
        """Cancel current recording without saving."""
        self.is_recording = False
        self.recording_samples.clear()
        self.gesture_name = None
        print("Recording cancelled")
    
    def get_recording_progress(self) -> float:
        """
        Get recording progress for UI feedback.
        
        Returns:
            Progress value in [0, 1]
        """
        if not self.is_recording:
            return 0.0
        
        return len(self.recording_samples) / self.target_samples
