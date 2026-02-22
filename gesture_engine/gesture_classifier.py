"""
Gesture Classification Module

Real-time gesture recognition system supporting single-hand and two-hand gestures.
Uses geometric feature extraction and trained models for accurate classification.

Author: Gestura Development Team
Version: 2.0.0
"""

import numpy as np
import time
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum

from gesture_engine.hand_tracker import HandData, HandLabel
from gesture_engine.config import CONFIG


class GestureType(Enum):
    """Supported gesture types."""
    # Single-hand gestures
    PINCH = "pinch"
    SWIPE_LEFT = "swipe_left"
    SWIPE_RIGHT = "swipe_right"
    SWIPE_UP = "swipe_up"
    SWIPE_DOWN = "swipe_down"
    FIST = "fist"
    PALM = "palm"
    THUMBS_UP = "thumbs_up"
    PEACE = "peace"
    POINTING = "pointing"
    
    # Two-hand gestures
    TWO_HAND_SPREAD = "two_hand_spread"
    TWO_HAND_PINCH = "two_hand_pinch"
    
    # Meta gestures
    NONE = "none"
    UNKNOWN = "unknown"


@dataclass
class GestureResult:
    """
    Result of gesture classification.
    
    Attributes:
        gesture: Detected gesture type
        confidence: Classification confidence (0-1)
        hand_label: Which hand performed gesture (for single-hand)
        timestamp: When gesture was detected
        features: Feature vector used for classification
    """
    gesture: GestureType
    confidence: float
    hand_label: Optional[HandLabel]
    timestamp: float
    features: Dict[str, float]


class GeometricFeatureExtractor:
    """
    Extracts geometric features from hand landmarks for classification.
    
    Features include:
    - Finger angles (joint angles for each finger)
    - Finger distances (tip to palm center)
    - Hand orientation (wrist to middle finger angle)
    - Finger states (extended/curled)
    """
    
    # MediaPipe hand landmark indices
    WRIST = 0
    THUMB_TIP = 4
    INDEX_TIP = 8
    MIDDLE_TIP = 12
    RING_TIP = 16
    PINKY_TIP = 20
    
    THUMB_IP = 3
    INDEX_PIP = 6
    MIDDLE_PIP = 10
    RING_PIP = 14
    PINKY_PIP = 18
    
    @staticmethod
    def calculate_angle(p1: np.ndarray, p2: np.ndarray, p3: np.ndarray) -> float:
        """
        Calculate angle at p2 formed by points p1-p2-p3.
        
        Returns: Angle in degrees (0-180)
        """
        v1 = p1 - p2
        v2 = p3 - p2
        
        cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-8)
        cos_angle = np.clip(cos_angle, -1.0, 1.0)
        
        angle = np.arccos(cos_angle)
        return np.degrees(angle)
    
    @staticmethod
    def calculate_distance(p1: np.ndarray, p2: np.ndarray) -> float:
        """Calculate Euclidean distance between two points."""
        return np.linalg.norm(p1 - p2)
    
    @classmethod
    def is_finger_extended(cls, hand_data: HandData, finger_tip_idx: int) -> bool:
        """
        Determine if a finger is extended based on landmark positions.
        
        Args:
            hand_data: Hand landmark data
            finger_tip_idx: Index of finger tip landmark (4, 8, 12, 16, 20)
            
        Returns:
            True if finger is extended, False if curled
        """
        landmarks = np.array(hand_data.landmarks)
        
        # Get wrist and palm center
        wrist = landmarks[cls.WRIST]
        palm_center = np.mean(landmarks[[0, 5, 9, 13, 17]], axis=0)
        
        # Get finger tip and intermediate joint
        tip = landmarks[finger_tip_idx]
        
        # Map tip index to intermediate joint
        joint_map = {4: 3, 8: 6, 12: 10, 16: 14, 20: 18}
        joint_idx = joint_map.get(finger_tip_idx, finger_tip_idx - 2)
        joint = landmarks[joint_idx]
        
        # Distance from palm center to tip
        tip_distance = cls.calculate_distance(palm_center, tip)
        
        # Distance from palm center to joint
        joint_distance = cls.calculate_distance(palm_center, joint)
        
        # Extended if tip is farther than joint
        return tip_distance > joint_distance * 1.1
    
    @classmethod
    def extract_features(cls, hand_data: HandData) -> Dict[str, float]:
        """
        Extract all geometric features from hand data.
        
        Returns:
            Dictionary of feature names to values
        """
        landmarks = np.array(hand_data.landmarks)
        
        features = {}
        
        # Finger extension states
        features["thumb_extended"] = float(cls.is_finger_extended(hand_data, cls.THUMB_TIP))
        features["index_extended"] = float(cls.is_finger_extended(hand_data, cls.INDEX_TIP))
        features["middle_extended"] = float(cls.is_finger_extended(hand_data, cls.MIDDLE_TIP))
        features["ring_extended"] = float(cls.is_finger_extended(hand_data, cls.RING_TIP))
        features["pinky_extended"] = float(cls.is_finger_extended(hand_data, cls.PINKY_TIP))
        
        # Finger tip to palm distances
        palm_center = np.mean(landmarks[[0, 5, 9, 13, 17]], axis=0)
        features["thumb_distance"] = cls.calculate_distance(landmarks[cls.THUMB_TIP], palm_center)
        features["index_distance"] = cls.calculate_distance(landmarks[cls.INDEX_TIP], palm_center)
        features["middle_distance"] = cls.calculate_distance(landmarks[cls.MIDDLE_TIP], palm_center)
        
        # Pinch detection (thumb-index distance)
        features["pinch_distance"] = cls.calculate_distance(
            landmarks[cls.THUMB_TIP], landmarks[cls.INDEX_TIP]
        )
        
        # Hand orientation (wrist to middle finger angle)
        wrist = landmarks[cls.WRIST]
        middle_tip = landmarks[cls.MIDDLE_TIP]
        features["hand_angle"] = np.arctan2(
            middle_tip[1] - wrist[1],
            middle_tip[0] - wrist[0]
        )
        
        # Total fingers extended
        features["fingers_extended_count"] = sum([
            features["thumb_extended"],
            features["index_extended"],
            features["middle_extended"],
            features["ring_extended"],
            features["pinky_extended"]
        ])
        
        return features


class GestureClassifier:
    """
    Classifies gestures from hand landmark data using geometric rules and confidence scoring.
    
    Supports both single-hand and two-hand gesture recognition with
    configurable thresholds and cooldown periods.
    """
    
    def __init__(self):
        """Initialize gesture classifier with configuration."""
        self.config = CONFIG.classification
        
        # Gesture state tracking
        self.last_gesture: GestureType = GestureType.NONE
        self.last_gesture_time: float = 0.0
        self.gesture_start_time: Optional[float] = None
        self.current_candidate: Optional[GestureType] = None
        
        # Feature extractor
        self.feature_extractor = GeometricFeatureExtractor()
    
    def classify(
        self, 
        left_hand: Optional[HandData],
        right_hand: Optional[HandData]
    ) -> Optional[GestureResult]:
        """
        Classify gesture from hand data.
        
        Args:
            left_hand: Left hand data (None if not visible)
            right_hand: Right hand data (None if not visible)
            
        Returns:
            GestureResult if confident gesture detected, None otherwise
        """
        current_time = time.time()
        
        # Check cooldown period
        if current_time - self.last_gesture_time < self.config.cooldown_time:
            return None
        
        # Two-hand gestures (priority over single-hand)
        if left_hand and right_hand:
            result = self._classify_two_hand(left_hand, right_hand, current_time)
            if result:
                return self._finalize_gesture(result, current_time)
        
        # Single-hand gestures
        if right_hand:
            result = self._classify_single_hand(right_hand, HandLabel.RIGHT, current_time)
            if result:
                return self._finalize_gesture(result, current_time)
        
        if left_hand:
            result = self._classify_single_hand(left_hand, HandLabel.LEFT, current_time)
            if result:
                return self._finalize_gesture(result, current_time)
        
        # No gesture detected, reset candidate
        self.current_candidate = None
        self.gesture_start_time = None
        
        return None
    
    def _classify_single_hand(
        self,
        hand_data: HandData,
        hand_label: HandLabel,
        current_time: float
    ) -> Optional[GestureResult]:
        """Classify single-hand gestures."""
        features = self.feature_extractor.extract_features(hand_data)
        
        # Rule-based classification
        gesture, confidence = self._match_gesture_rules(features)
        
        if gesture == GestureType.NONE or confidence < self.config.min_gesture_confidence:
            return None
        
        return GestureResult(
            gesture=gesture,
            confidence=confidence,
            hand_label=hand_label,
            timestamp=current_time,
            features=features
        )
    
    def _classify_two_hand(
        self,
        left_hand: HandData,
        right_hand: HandData,
        current_time: float
    ) -> Optional[GestureResult]:
        """Classify two-hand gestures."""
        left_features = self.feature_extractor.extract_features(left_hand)
        right_features = self.feature_extractor.extract_features(right_hand)
        
        # Calculate distance between hands
        left_wrist = np.array(left_hand.landmarks[0])
        right_wrist = np.array(right_hand.landmarks[0])
        hand_distance = np.linalg.norm(left_wrist - right_wrist)
        
        combined_features = {
            "hand_distance": hand_distance,
            "left_fingers_extended": left_features["fingers_extended_count"],
            "right_fingers_extended": right_features["fingers_extended_count"]
        }
        
        # Two-hand gesture rules
        gesture = GestureType.NONE
        confidence = 0.0
        
        # Two-hand spread (hands apart, palms open)
        if (hand_distance > 0.3 and
            left_features["fingers_extended_count"] >= 4 and
            right_features["fingers_extended_count"] >= 4):
            gesture = GestureType.TWO_HAND_SPREAD
            confidence = 0.9
        
        # Two-hand pinch (hands close, both pinching)
        elif (hand_distance < 0.15 and
              left_features["pinch_distance"] < 0.05 and
              right_features["pinch_distance"] < 0.05):
            gesture = GestureType.TWO_HAND_PINCH
            confidence = 0.85
        
        if gesture == GestureType.NONE:
            return None
        
        return GestureResult(
            gesture=gesture,
            confidence=confidence,
            hand_label=None,  # Both hands
            timestamp=current_time,
            features=combined_features
        )
    
    def _match_gesture_rules(self, features: Dict[str, float]) -> Tuple[GestureType, float]:
        """
        Match features to gesture using rule-based classification.
        
        Returns:
            Tuple of (GestureType, confidence_score)
        """
        fingers_extended = features["fingers_extended_count"]
        
        # PINCH: Thumb + Index touching, others curled
        if (features["pinch_distance"] < 0.05 and
            not features["middle_extended"] and
            not features["ring_extended"]):
            return GestureType.PINCH, 0.9
        
        # FIST: All fingers curled
        if fingers_extended == 0:
            return GestureType.FIST, 0.95
        
        # PALM: All fingers extended
        if fingers_extended == 5:
            return GestureType.PALM, 0.95
        
        # THUMBS UP: Only thumb extended
        if (fingers_extended == 1 and
            features["thumb_extended"]):
            return GestureType.THUMBS_UP, 0.85
        
        # PEACE: Index + Middle extended
        if (fingers_extended == 2 and
            features["index_extended"] and
            features["middle_extended"]):
            return GestureType.PEACE, 0.9
        
        # POINTING: Only index extended
        if (fingers_extended == 1 and
            features["index_extended"]):
            return GestureType.POINTING, 0.85
        
        # SWIPE detection based on hand movement
        # (Requires motion tracking - simplified here)
        hand_angle = features["hand_angle"]
        if fingers_extended >= 3:
            if -0.5 < hand_angle < 0.5:
                return GestureType.SWIPE_RIGHT, 0.7
            elif 2.6 < hand_angle or hand_angle < -2.6:
                return GestureType.SWIPE_LEFT, 0.7
        
        return GestureType.NONE, 0.0
    
    def _finalize_gesture(
        self,
        result: GestureResult,
        current_time: float
    ) -> Optional[GestureResult]:
        """
        Apply hold time requirement before confirming gesture.
        
        Prevents false positives from transient hand positions.
        """
        # Check if this is a new gesture candidate
        if self.current_candidate != result.gesture:
            self.current_candidate = result.gesture
            self.gesture_start_time = current_time
            return None
        
        # Check if gesture has been held long enough
        hold_duration = current_time - (self.gesture_start_time or current_time)
        
        if hold_duration >= self.config.gesture_hold_time:
            # Gesture confirmed!
            self.last_gesture = result.gesture
            self.last_gesture_time = current_time
            self.current_candidate = None
            self.gesture_start_time = None
            return result
        
        return None
    
    def reset(self) -> None:
        """Reset classifier state."""
        self.last_gesture = GestureType.NONE
        self.last_gesture_time = 0.0
        self.gesture_start_time = None
        self.current_candidate = None


if __name__ == "__main__":
    # Test gesture classifier
    print("Gesture Classifier Test - Check gesture_classifier module")
    print("Integration test available in main.py")
