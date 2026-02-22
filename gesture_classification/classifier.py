"""
Mutually Exclusive Gesture Classifier with Confidence Scoring.

CRITICAL DESIGN PRINCIPLE:
Each gesture is evaluated independently and returns a confidence score.
Only the HIGHEST confidence gesture above threshold is selected.
Uses strict elif chains to guarantee mutual exclusivity.
"""

import numpy as np
from typing import Optional, Dict, Tuple
from collections import deque
from dataclasses import dataclass

from hand_tracking.detector import HandLandmarks
from config.constants import Constants


@dataclass
class GestureResult:
    """
    Result of gesture classification with confidence score.
    
    Attributes:
        gesture_name: Name of detected gesture or None
        confidence: Confidence score [0, 1]
        reason: Human-readable explanation of classification
    """
    gesture_name: Optional[str]
    confidence: float
    reason: str


class MutuallyExclusiveGestureClassifier:
    """
    Classifies hand poses into mutually exclusive gestures with confidence scores.
    
    CONFLICT PREVENTION STRATEGY:
    1. Each gesture has a dedicated classification function
    2. Functions return (gesture_name, confidence, reason)
    3. All classifiers are called, highest confidence wins
    4. Threshold filtering prevents weak matches
    5. Explicit priority order for edge cases
    """
    
    def __init__(self):
        """Initialize classifier with gesture priority order."""
        # Priority order: specific gestures before generic ones
        # If two gestures have similar confidence, higher priority wins
        self.gesture_priority = [
            'open_palm',      # Most specific - all fingers extended and spread
            'fist',           # Most specific - all fingers curled
            'thumbs_up',      # Distinctive - only thumb extended upward
            'thumbs_down',    # Distinctive - only thumb extended downward
            'peace_sign',     # Specific - exactly 2 fingers (index + middle)
            'pointing',       # Less specific - 1 finger extended
        ]
    
    def extract_features(self, landmarks: HandLandmarks) -> Dict[str, float]:
        """
        Extract geometric features from hand landmarks.
        Returns normalized, scale-invariant features.
        """
        features = {}
        
        # Get key points
        wrist = np.array(landmarks.get_landmark(0)[:2])
        
        # Calculate palm size for normalization
        middle_base = np.array(landmarks.get_landmark(9)[:2])
        palm_size = np.linalg.norm(middle_base - wrist)
        
        if palm_size < 0.001:
            palm_size = 0.001
        
        # Feature: Individual finger extensions
        fingers = {
            'thumb': (4, 2),
            'index': (8, 5),
            'middle': (12, 9),
            'ring': (16, 13),
            'pinky': (20, 17),
        }
        
        extended_count = 0
        for finger_name, (tip_idx, base_idx) in fingers.items():
            tip = np.array(landmarks.get_landmark(tip_idx)[:2])
            base = np.array(landmarks.get_landmark(base_idx)[:2])
            
            tip_dist = np.linalg.norm(tip - wrist)
            base_dist = np.linalg.norm(base - wrist)
            
            extension = (tip_dist - base_dist) / palm_size
            
            # Use stricter threshold for better accuracy
            # Thumb has lower threshold due to different anatomy
            if finger_name == 'thumb':
                is_extended = extension > 0.25
            else:
                is_extended = extension > 0.4
            
            features[f'{finger_name}_extended'] = 1.0 if is_extended else 0.0
            if is_extended:
                extended_count += 1
        
        features['total_extended'] = float(extended_count)
        
        # Feature: Finger curl (for fist detection)
        curl_values = []
        for finger in ['index', 'middle', 'ring', 'pinky']:
            curl_values.append(1.0 - features[f'{finger}_extended'])
        features['avg_curl'] = np.mean(curl_values)
        
        # Feature: Finger spread
        index_tip = np.array(landmarks.get_landmark(8)[:2])
        middle_tip = np.array(landmarks.get_landmark(12)[:2])
        ring_tip = np.array(landmarks.get_landmark(16)[:2])
        pinky_tip = np.array(landmarks.get_landmark(20)[:2])
        
        spreads = [
            np.linalg.norm(index_tip - middle_tip),
            np.linalg.norm(middle_tip - ring_tip),
            np.linalg.norm(ring_tip - pinky_tip),
        ]
        features['avg_spread'] = np.mean(spreads) / palm_size
        
        # Feature: Thumb angle
        thumb_tip = np.array(landmarks.get_landmark(4)[:2])
        thumb_base = np.array(landmarks.get_landmark(2)[:2])
        
        palm_vector = middle_base - wrist
        thumb_vector = thumb_tip - thumb_base
        
        palm_vector = palm_vector / (np.linalg.norm(palm_vector) + 1e-6)
        thumb_vector = thumb_vector / (np.linalg.norm(thumb_vector) + 1e-6)
        
        features['thumb_angle'] = np.dot(palm_vector, thumb_vector)
        
        return features
    
    def classify_open_palm(self, features: Dict[str, float]) -> Tuple[float, str]:
        """
        Classify open palm gesture.
        
        Criteria:
        - All 5 fingers extended
        - Fingers spread apart
        
        Returns:
            (confidence, reason)
        """
        # Check all fingers extended
        if features['total_extended'] != 5.0:
            return 0.0, "Not all fingers extended"
        
        # Check spread
        if features['avg_spread'] < 0.5:
            return 0.0, "Fingers not spread enough"
        
        # High confidence if criteria met
        confidence = 0.9
        
        # Bonus for wide spread
        if features['avg_spread'] > 0.7:
            confidence = 0.95
        
        return confidence, "All fingers extended and spread"
    
    def classify_fist(self, features: Dict[str, float]) -> Tuple[float, str]:
        """
        Classify closed fist gesture.
        
        Criteria:
        - No fingers extended (all curled)
        - High average curl
        
        Returns:
            (confidence, reason)
        """
        # Check no fingers extended
        if features['total_extended'] != 0.0:
            return 0.0, "Fingers detected as extended"
        
        # Check high curl
        if features['avg_curl'] < 0.8:
            return 0.0, "Insufficient finger curl"
        
        # High confidence if criteria met
        confidence = 0.9
        
        # Bonus for very tight curl
        if features['avg_curl'] > 0.9:
            confidence = 0.95
        
        return confidence, "All fingers tightly curled"
    
    def classify_thumbs_up(self, features: Dict[str, float]) -> Tuple[float, str]:
        """
        Classify thumbs up gesture.
        
        Criteria:
        - Only thumb extended
        - Thumb pointing upward (positive angle)
        - All other fingers curled
        
        Returns:
            (confidence, reason)
        """
        # Must have exactly 1 finger extended
        if features['total_extended'] != 1.0:
            return 0.0, f"Expected 1 finger, got {features['total_extended']}"
        
        # That finger must be thumb
        if features['thumb_extended'] != 1.0:
            return 0.0, "Extended finger is not thumb"
        
        # Explicitly check other fingers are NOT extended
        if (features['index_extended'] == 1.0 or
            features['middle_extended'] == 1.0 or
            features['ring_extended'] == 1.0 or
            features['pinky_extended'] == 1.0):
            return 0.0, "Other fingers are extended"
        
        # Thumb must point upward (positive angle)
        if features['thumb_angle'] < 0.5:
            return 0.0, f"Thumb angle {features['thumb_angle']:.2f} not upward"
        
        # Calculate confidence based on angle
        confidence = 0.7 + (features['thumb_angle'] * 0.2)
        confidence = min(confidence, 0.95)
        
        return confidence, f"Thumb up (angle={features['thumb_angle']:.2f})"
    
    def classify_thumbs_down(self, features: Dict[str, float]) -> Tuple[float, str]:
        """
        Classify thumbs down gesture.
        
        Criteria:
        - Only thumb extended
        - Thumb pointing downward (negative angle)
        - All other fingers curled
        
        Returns:
            (confidence, reason)
        """
        # Must have exactly 1 finger extended
        if features['total_extended'] != 1.0:
            return 0.0, f"Expected 1 finger, got {features['total_extended']}"
        
        # That finger must be thumb
        if features['thumb_extended'] != 1.0:
            return 0.0, "Extended finger is not thumb"
        
        # Explicitly check other fingers are NOT extended
        if (features['index_extended'] == 1.0 or
            features['middle_extended'] == 1.0 or
            features['ring_extended'] == 1.0 or
            features['pinky_extended'] == 1.0):
            return 0.0, "Other fingers are extended"
        
        # Thumb must point downward (negative angle)
        if features['thumb_angle'] > -0.5:
            return 0.0, f"Thumb angle {features['thumb_angle']:.2f} not downward"
        
        # Calculate confidence based on angle
        confidence = 0.7 + (abs(features['thumb_angle']) * 0.2)
        confidence = min(confidence, 0.95)
        
        return confidence, f"Thumb down (angle={features['thumb_angle']:.2f})"
    
    def classify_peace_sign(self, features: Dict[str, float]) -> Tuple[float, str]:
        """
        Classify peace sign (V sign) gesture.
        
        Criteria:
        - Exactly 2 fingers extended
        - Must be index and middle
        - Other fingers curled
        
        Returns:
            (confidence, reason)
        """
        # Must have exactly 2 fingers extended
        if features['total_extended'] != 2.0:
            return 0.0, f"Expected 2 fingers, got {features['total_extended']}"
        
        # Check it's index and middle
        if features['index_extended'] != 1.0:
            return 0.0, "Index finger not extended"
        
        if features['middle_extended'] != 1.0:
            return 0.0, "Middle finger not extended"
        
        # Verify others are curled
        if features['ring_extended'] == 1.0 or features['pinky_extended'] == 1.0:
            return 0.0, "Ring or pinky also extended"
        
        confidence = 0.9
        return confidence, "Index and middle fingers extended"
    
    def classify_pointing(self, features: Dict[str, float]) -> Tuple[float, str]:
        """
        Classify pointing gesture.
        
        Criteria:
        - Exactly 1 finger extended
        - Must be index finger
        - Other fingers curled
        
        Returns:
            (confidence, reason)
        """
        # Must have exactly 1 finger extended
        if features['total_extended'] != 1.0:
            return 0.0, f"Expected 1 finger, got {features['total_extended']}"
        
        # That finger must be index
        if features['index_extended'] != 1.0:
            return 0.0, "Extended finger is not index"
        
        confidence = 0.85
        return confidence, "Index finger pointing"
    
    def classify(self, landmarks: HandLandmarks) -> GestureResult:
        """
        Classify hand pose into a single gesture with confidence.
        
        MUTUAL EXCLUSIVITY GUARANTEE:
        1. Extract features once
        2. Evaluate each gesture classifier independently
        3. Select ONLY the highest confidence gesture
        4. Apply threshold filter
        5. Return at most ONE gesture
        
        Args:
            landmarks: Hand landmarks from detector
            
        Returns:
            GestureResult with gesture name, confidence, and reason
        """
        # Extract features once
        features = self.extract_features(landmarks)
        
        # Evaluate all gesture classifiers
        candidates = []
        
        # Open palm
        conf, reason = self.classify_open_palm(features)
        if conf > 0:
            candidates.append(('open_palm', conf, reason))
        
        # Fist
        conf, reason = self.classify_fist(features)
        if conf > 0:
            candidates.append(('fist', conf, reason))
        
        # Thumbs up
        conf, reason = self.classify_thumbs_up(features)
        if conf > 0:
            candidates.append(('thumbs_up', conf, reason))
        
        # Thumbs down
        conf, reason = self.classify_thumbs_down(features)
        if conf > 0:
            candidates.append(('thumbs_down', conf, reason))
        
        # Peace sign
        conf, reason = self.classify_peace_sign(features)
        if conf > 0:
            candidates.append(('peace_sign', conf, reason))
        
        # Pointing
        conf, reason = self.classify_pointing(features)
        if conf > 0:
            candidates.append(('pointing', conf, reason))
        
        # No candidates above threshold
        if not candidates:
            return GestureResult(
                gesture_name=None,
                confidence=0.0,
                reason="No gesture meets criteria"
            )
        
        # Select highest confidence
        best_gesture, best_conf, best_reason = max(candidates, key=lambda x: x[1])
        
        # If tie, use priority order
        if len(candidates) > 1:
            top_candidates = [c for c in candidates if abs(c[1] - best_conf) < 0.05]
            if len(top_candidates) > 1:
                # Use priority order
                for priority_gesture in self.gesture_priority:
                    for candidate in top_candidates:
                        if candidate[0] == priority_gesture:
                            best_gesture, best_conf, best_reason = candidate
                            break
        
        # Apply confidence threshold
        if best_conf < Constants.GESTURE_CONFIDENCE_THRESHOLD:
            return GestureResult(
                gesture_name=None,
                confidence=best_conf,
                reason=f"{best_gesture}: confidence {best_conf:.2f} below threshold"
            )
        
        return GestureResult(
            gesture_name=best_gesture,
            confidence=best_conf,
            reason=best_reason
        )
