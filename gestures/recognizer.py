"""
Gesture recognition engine with stabilization and confidence scoring.
Converts hand landmarks into gesture classifications.
"""

import numpy as np
from typing import Optional, Dict, Tuple
from collections import deque
import time

from hand_tracking.detector import HandLandmarks
from gestures.gesture import Gesture, GestureLibrary
from config.constants import Constants


class GestureRecognizer:
    """
    Recognizes gestures from hand landmarks with stabilization.
    
    Uses geometric features derived from landmarks to classify gestures,
    making the system robust to hand size, position, and camera distance.
    """
    
    def __init__(self, gesture_library: GestureLibrary):
        """
        Initialize gesture recognizer.
        
        Args:
            gesture_library: Library of known gestures
        """
        self.library = gesture_library
        
        # Stabilization: store recent gesture detections
        self.gesture_history: deque = deque(
            maxlen=Constants.STABILIZATION_WINDOW
        )
        
        # Dwell time tracking
        self.current_gesture: Optional[str] = None
        self.gesture_start_time: Optional[float] = None
        self.last_activation_time: float = 0.0
        
    def extract_features(self, landmarks: HandLandmarks) -> Dict[str, float]:
        """
        Extract geometric features from hand landmarks.
        
        Features are position/scale invariant to work regardless of:
        - Hand size
        - Distance from camera
        - Position in frame
        
        Args:
            landmarks: Detected hand landmarks
            
        Returns:
            Dictionary of normalized geometric features
        """
        features = {}
        
        # Get key landmark positions
        wrist = np.array(landmarks.get_landmark(0)[:2])  # Use only x,y
        
        # Define finger tip and base indices
        fingers = {
            'thumb': (4, 2),      # tip, base
            'index': (8, 5),
            'middle': (12, 9),
            'ring': (16, 13),
            'pinky': (20, 17),
        }
        
        # Calculate palm size for normalization
        # Distance from wrist to middle finger base
        middle_base = np.array(landmarks.get_landmark(9)[:2])
        palm_size = np.linalg.norm(middle_base - wrist)
        
        # Avoid division by zero
        if palm_size < 0.001:
            palm_size = 0.001
        
        # Feature 1: Count extended fingers
        # A finger is "extended" if its tip is farther from wrist than its base
        extended_fingers = 0
        
        for finger_name, (tip_idx, base_idx) in fingers.items():
            tip = np.array(landmarks.get_landmark(tip_idx)[:2])
            base = np.array(landmarks.get_landmark(base_idx)[:2])
            
            tip_dist = np.linalg.norm(tip - wrist)
            base_dist = np.linalg.norm(base - wrist)
            
            # Normalized extension
            extension = (tip_dist - base_dist) / palm_size
            
            # Store individual finger extension
            is_extended = extension > 0.3  # Threshold for "extended"
            features[f'{finger_name}_extended'] = 1.0 if is_extended else 0.0
            
            if is_extended:
                extended_fingers += 1
        
        features['fingers_extended'] = float(extended_fingers)
        
        # Feature 2: Finger curl (inverse of extension)
        # Average how curled the fingers are
        curl_sum = sum(
            1.0 - features[f'{finger}_extended']
            for finger in ['index', 'middle', 'ring', 'pinky']
        )
        features['finger_curl'] = curl_sum / 4.0
        
        # Feature 3: Finger spread (distance between adjacent tips)
        index_tip = np.array(landmarks.get_landmark(8)[:2])
        middle_tip = np.array(landmarks.get_landmark(12)[:2])
        ring_tip = np.array(landmarks.get_landmark(16)[:2])
        pinky_tip = np.array(landmarks.get_landmark(20)[:2])
        
        spread_distances = [
            np.linalg.norm(index_tip - middle_tip),
            np.linalg.norm(middle_tip - ring_tip),
            np.linalg.norm(ring_tip - pinky_tip),
        ]
        
        # Normalize by palm size
        avg_spread = np.mean(spread_distances) / palm_size
        features['finger_spread'] = min(avg_spread, 1.0)  # Clamp to [0,1]
        
        # Feature 4: Thumb angle (relative to palm)
        thumb_tip = np.array(landmarks.get_landmark(4)[:2])
        thumb_base = np.array(landmarks.get_landmark(2)[:2])
        
        # Vector from wrist to middle base (palm direction)
        palm_vector = middle_base - wrist
        # Vector from thumb base to tip
        thumb_vector = thumb_tip - thumb_base
        
        # Normalize vectors
        palm_vector = palm_vector / (np.linalg.norm(palm_vector) + 1e-6)
        thumb_vector = thumb_vector / (np.linalg.norm(thumb_vector) + 1e-6)
        
        # Dot product gives cosine of angle
        thumb_angle = np.dot(palm_vector, thumb_vector)
        features['thumb_angle'] = thumb_angle
        
        # Thumb extension
        thumb_tip_dist = np.linalg.norm(thumb_tip - wrist)
        thumb_base_dist = np.linalg.norm(thumb_base - wrist)
        thumb_ext = (thumb_tip_dist - thumb_base_dist) / palm_size
        features['thumb_extended'] = 1.0 if thumb_ext > 0.3 else 0.0
        
        return features
    
    def compute_similarity(
        self,
        features: Dict[str, float],
        gesture: Gesture
    ) -> float:
        """
        Compute similarity between extracted features and a known gesture.
        
        Uses normalized feature distance, where lower distance = higher similarity.
        
        Args:
            features: Extracted features from current hand
            gesture: Known gesture to compare against
            
        Returns:
            Similarity score in [0, 1], where 1 is perfect match
        """
        # Only compare features that exist in both
        common_features = set(features.keys()) & set(gesture.features.keys())
        
        if not common_features:
            return 0.0
        
        # Calculate normalized Euclidean distance
        distances = [
            (features[feat] - gesture.features[feat]) ** 2
            for feat in common_features
        ]
        
        distance = np.sqrt(np.mean(distances))
        
        # Convert distance to similarity (0 distance = 1.0 similarity)
        # Use exponential decay for smoother scoring
        similarity = np.exp(-distance * 3.0)  # Scale factor for sensitivity
        
        return similarity
    
    def recognize(
        self,
        landmarks: HandLandmarks,
        current_time: float
    ) -> Tuple[Optional[str], float, bool]:
        """
        Recognize gesture from hand landmarks with stabilization.
        
        Args:
            landmarks: Detected hand landmarks
            current_time: Current timestamp for dwell tracking
            
        Returns:
            Tuple of (gesture_name, confidence, should_activate) where:
                gesture_name: Name of recognized gesture or None
                confidence: Confidence score [0, 1]
                should_activate: True if dwell time met and action should trigger
        """
        # Extract features from current hand pose
        features = self.extract_features(landmarks)
        
        # Score all gestures in library
        gesture_scores = {}
        for gesture in self.library.get_all_gestures():
            score = self.compute_similarity(features, gesture)
            gesture_scores[gesture.name] = score
        
        # Get best matching gesture
        if not gesture_scores:
            return None, 0.0, False
        
        best_gesture = max(gesture_scores.keys(), key=lambda k: gesture_scores[k])
        best_score = gesture_scores[best_gesture]
        
        # Apply confidence threshold
        if best_score < Constants.GESTURE_CONFIDENCE_THRESHOLD:
            # Reset tracking if confidence too low
            self.current_gesture = None
            self.gesture_start_time = None
            return None, best_score, False
        
        # Add to history for stabilization
        self.gesture_history.append(best_gesture)
        
        # Stabilization: require consistent detection over multiple frames
        if len(self.gesture_history) < Constants.STABILIZATION_WINDOW:
            return best_gesture, best_score, False
        
        # Check if gesture is stable (most common in recent history)
        from collections import Counter
        gesture_counts = Counter(self.gesture_history)
        most_common_gesture, count = gesture_counts.most_common(1)[0]
        
        # Require at least 60% consistency
        stability_threshold = Constants.STABILIZATION_WINDOW * 0.6
        if count < stability_threshold:
            return best_gesture, best_score, False
        
        # Stable gesture detected
        stabilized_gesture = most_common_gesture
        
        # Dwell time logic
        should_activate = False
        
        if stabilized_gesture != self.current_gesture:
            # New gesture - start tracking dwell time
            self.current_gesture = stabilized_gesture
            self.gesture_start_time = current_time
        else:
            # Same gesture - check if dwell time met
            if self.gesture_start_time is not None:
                dwell_elapsed = current_time - self.gesture_start_time
                
                # Check debounce cooldown
                time_since_last_activation = current_time - self.last_activation_time
                
                if (dwell_elapsed >= Constants.DWELL_TIME_SECONDS and
                    time_since_last_activation >= Constants.DEBOUNCE_COOLDOWN_SECONDS):
                    
                    should_activate = True
                    self.last_activation_time = current_time
                    # Reset dwell tracking after activation
                    self.gesture_start_time = current_time
        
        # Calculate dwell progress (for UI feedback)
        dwell_progress = 0.0
        if self.gesture_start_time is not None:
            elapsed = current_time - self.gesture_start_time
            dwell_progress = min(elapsed / Constants.DWELL_TIME_SECONDS, 1.0)
        
        return stabilized_gesture, best_score, should_activate
    
    def get_dwell_progress(self) -> float:
        """
        Get current dwell time progress for UI feedback.
        
        Returns:
            Progress value in [0, 1]
        """
        if self.gesture_start_time is None:
            return 0.0
        
        elapsed = time.time() - self.gesture_start_time
        progress = min(elapsed / Constants.DWELL_TIME_SECONDS, 1.0)
        return progress
    
    def reset(self) -> None:
        """Reset recognizer state."""
        self.gesture_history.clear()
        self.current_gesture = None
        self.gesture_start_time = None
