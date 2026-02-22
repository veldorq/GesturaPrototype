"""
User calibration system for personalized gesture recognition.
Allows users to record their specific hand characteristics.
"""

import json
import numpy as np
from typing import Dict, List, Optional
from pathlib import Path
from dataclasses import dataclass, field

from hand_tracking.detector import HandLandmarks
from gestures.recognizer import GestureRecognizer


@dataclass
class CalibrationProfile:
    """
    Stores user-specific calibration data.
    """
    user_id: str = "default"
    hand_size_scale: float = 1.0  # Relative hand size compared to average
    finger_extension_bias: Dict[str, float] = field(default_factory=dict)
    confidence_multiplier: float = 1.0
    preferred_dwell_time: float = 1.5
    samples_count: int = 0


class CalibrationSystem:
    """
    Manages user calibration for improved gesture recognition.
    
    Performs a guided calibration where users perform known gestures
    multiple times to establish their specific patterns.
    """
    
    def __init__(self, profile_path: str = "user_calibration.json"):
        """
        Initialize calibration system.
        
        Args:
            profile_path: Path to save/load calibration profile
        """
        self.profile_path = Path(profile_path)
        self.profile = CalibrationProfile()
        self.calibration_samples: Dict[str, List[Dict]] = {}
        self.is_calibrating = False
        
        # Load existing profile if available
        if self.profile_path.exists():
            self.load_profile()
    
    def start_calibration(self, gesture_name: str, num_samples: int = 5) -> None:
        """
        Start calibration for a specific gesture.
        
        Args:
            gesture_name: Name of gesture to calibrate
            num_samples: Number of samples to collect
        """
        self.is_calibrating = True
        self.calibration_samples[gesture_name] = []
        self.current_gesture = gesture_name
        self.target_samples = num_samples
    
    def add_calibration_sample(
        self,
        gesture_name: str,
        landmarks: HandLandmarks,
        features: Dict[str, float]
    ) -> bool:
        """
        Add a calibration sample for a gesture.
        
        Args:
            gesture_name: Name of the gesture
            landmarks: Hand landmarks for the sample
            features: Extracted features
            
        Returns:
            True if sample was added successfully
        """
        if gesture_name not in self.calibration_samples:
            self.calibration_samples[gesture_name] = []
        
        sample = {
            'features': features,
            'landmarks': [(lm[0], lm[1], lm[2]) for lm in landmarks.landmarks]
        }
        
        self.calibration_samples[gesture_name].append(sample)
        return True
    
    def finish_calibration(self) -> CalibrationProfile:
        """
        Complete calibration and compute personalized profile.
        
        Returns:
            Computed calibration profile
        """
        self.is_calibrating = False
        
        # Analyze collected samples
        self._analyze_hand_characteristics()
        self._compute_feature_adjustments()
        
        # Save profile
        self.save_profile()
        
        return self.profile
    
    def _analyze_hand_characteristics(self) -> None:
        """
        Analyze user's hand size and proportions.
        
        Computes average hand size relative to expected norms
        to adjust feature extraction accordingly.
        """
        all_palm_sizes = []
        
        for gesture_samples in self.calibration_samples.values():
            for sample in gesture_samples:
                landmarks = sample['landmarks']
                wrist = np.array(landmarks[0][:2])
                middle_base = np.array(landmarks[9][:2])
                palm_size = np.linalg.norm(middle_base - wrist)
                all_palm_sizes.append(palm_size)
        
        if all_palm_sizes:
            avg_palm_size = np.mean(all_palm_sizes)
            # Assume average palm size is around 0.2 (normalized coordinates)
            self.profile.hand_size_scale = float(avg_palm_size / 0.2)
            self.profile.samples_count = len(all_palm_sizes)
    
    def _compute_feature_adjustments(self) -> None:
        """
        Compute adjustments to feature extraction for this user.
        
        Some users may naturally extend fingers differently,
        have different thumb angles, etc.
        """
        # Compute average features per gesture
        for gesture_name, samples in self.calibration_samples.items():
            if not samples:
                continue
            
            # Average all features
            feature_sums = {}
            count = len(samples)
            
            for sample in samples:
                for feat_name, feat_value in sample['features'].items():
                    if feat_name not in feature_sums:
                        feature_sums[feat_name] = 0
                    feature_sums[feat_name] += feat_value
            
            # Store average features (could be used to adjust gesture templates)
            avg_features = {k: v / count for k, v in feature_sums.items()}
            
            # Compute finger extension bias
            for finger in ['thumb', 'index', 'middle', 'ring', 'pinky']:
                key = f'{finger}_extended'
                if key in avg_features:
                    # Store deviation from expected (0.0 or 1.0)
                    expected = 1.0 if avg_features[key] > 0.5 else 0.0
                    bias = avg_features[key] - expected
                    self.profile.finger_extension_bias[key] = bias
    
    def apply_calibration(
        self,
        features: Dict[str, float]
    ) -> Dict[str, float]:
        """
        Apply calibration adjustments to extracted features.
        
        Args:
            features: Raw extracted features
            
        Returns:
            Adjusted features based on user calibration
        """
        adjusted = features.copy()
        
        # Apply finger extension bias
        for feat_name, bias in self.profile.finger_extension_bias.items():
            if feat_name in adjusted:
                adjusted[feat_name] = np.clip(
                    adjusted[feat_name] - bias,
                    0.0,
                    1.0
                )
        
        return adjusted
    
    def get_confidence_multiplier(self) -> float:
        """
        Get confidence multiplier based on calibration quality.
        
        Better calibrated users get a boost in confidence scores.
        """
        if self.profile.samples_count < 10:
            return 1.0  # Not enough calibration
        
        # Boost confidence for well-calibrated users
        return min(1.1, 1.0 + (self.profile.samples_count / 100))
    
    def save_profile(self) -> None:
        """Save calibration profile to file."""
        data = {
            'user_id': self.profile.user_id,
            'hand_size_scale': self.profile.hand_size_scale,
            'finger_extension_bias': self.profile.finger_extension_bias,
            'confidence_multiplier': self.profile.confidence_multiplier,
            'preferred_dwell_time': self.profile.preferred_dwell_time,
            'samples_count': self.profile.samples_count,
        }
        
        with open(self.profile_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_profile(self) -> bool:
        """
        Load calibration profile from file.
        
        Returns:
            True if profile was loaded successfully
        """
        try:
            with open(self.profile_path, 'r') as f:
                data = json.load(f)
            
            self.profile.user_id = data.get('user_id', 'default')
            self.profile.hand_size_scale = data.get('hand_size_scale', 1.0)
            self.profile.finger_extension_bias = data.get('finger_extension_bias', {})
            self.profile.confidence_multiplier = data.get('confidence_multiplier', 1.0)
            self.profile.preferred_dwell_time = data.get('preferred_dwell_time', 1.5)
            self.profile.samples_count = data.get('samples_count', 0)
            
            return True
            
        except Exception:
            return False
    
    def reset_profile(self) -> None:
        """Reset calibration profile to defaults."""
        self.profile = CalibrationProfile()
        self.calibration_samples.clear()
        
        if self.profile_path.exists():
            self.profile_path.unlink()
