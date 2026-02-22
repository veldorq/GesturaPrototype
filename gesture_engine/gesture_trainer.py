"""
Gesture Training Module

Allows users to record, train, save, and load custom gestures.
Gestures are stored as feature vectors with confidence thresholds.

Author: Gestura Development Team
Version: 2.0.0
"""

import json
import numpy as np
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import pickle

from gesture_engine.hand_tracker import HandData, HandLabel
from gesture_engine.gesture_classifier import GeometricFeatureExtractor
from gesture_engine.config import CONFIG


@dataclass
class TrainedGesture:
    """
    Represents a trained custom gesture.
    
    Attributes:
        name: Gesture name/identifier
        feature_vectors: List of feature vectors from training samples
        mean_vector: Average feature vector
        std_vector: Standard deviation of features
        confidence_threshold: Minimum similarity score to match
        hand_label: Which hand (Left/Right/Both)
        timestamp: When gesture was trained
        sample_count: Number of training samples
    """
    name: str
    feature_vectors: List[np.ndarray]
    mean_vector: np.ndarray
    std_vector: np.ndarray
    confidence_threshold: float
    hand_label: str
    timestamp: float
    sample_count: int
    
    def to_dict(self) -> Dict:
        """Convert to JSON-serializable dictionary."""
        return {
            "name": self.name,
            "feature_vectors": [fv.tolist() for fv in self.feature_vectors],
            "mean_vector": self.mean_vector.tolist(),
            "std_vector": self.std_vector.tolist(),
            "confidence_threshold": self.confidence_threshold,
            "hand_label": self.hand_label,
            "timestamp": self.timestamp,
            "sample_count": self.sample_count
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'TrainedGesture':
        """Create from dictionary."""
        return cls(
            name=data["name"],
            feature_vectors=[np.array(fv) for fv in data["feature_vectors"]],
            mean_vector=np.array(data["mean_vector"]),
            std_vector=np.array(data["std_vector"]),
            confidence_threshold=data["confidence_threshold"],
            hand_label=data["hand_label"],
            timestamp=data["timestamp"],
            sample_count=data["sample_count"]
        )


class GestureTrainer:
    """
    Trains and manages custom gestures.
    
    Features:
    - Record gesture samples over multiple frames
    - Calculate feature statistics (mean, std)
    - Save/load gestures to/from file
    - Match live gestures against trained templates
    - Manage gesture library (add, delete, list)
    """
    
    def __init__(self, gestures_file: Optional[str] = None):
        """
        Initialize gesture trainer.
        
        Args:
            gestures_file: Path to gestures storage file (default: from config)
        """
        self.config = CONFIG.training
        self.gestures_file = gestures_file or self.config.gestures_file
        
        # Trained gestures library
        self.trained_gestures: Dict[str, TrainedGesture] = {}
        
        # Recording state
        self.is_recording = False
        self.recording_name: Optional[str] = None
        self.recording_samples: List[Dict[str, float]] = []
        self.recording_hand_label: Optional[str] = None
        self.samples_collected = 0
        
        # Feature extractor
        self.feature_extractor = GeometricFeatureExtractor()
        
        # Load existing gestures
        self.load_gestures()
    
    def start_recording(self, gesture_name: str, hand_label: HandLabel) -> None:
        """
        Start recording a new gesture.
        
        Args:
            gesture_name: Name for the gesture
            hand_label: Which hand to use (LEFT/RIGHT)
        """
        if self.is_recording:
            raise RuntimeError("Already recording a gesture")
        
        self.is_recording = True
        self.recording_name = gesture_name
        self.recording_hand_label = hand_label.value
        self.recording_samples = []
        self.samples_collected = 0
        
        print(f"Started recording gesture: '{gesture_name}' ({hand_label.value} hand)")
        print(f"Target samples: {self.config.training_samples_per_gesture}")
    
    def record_sample(
        self,
        hand_data: HandData,
        frame_count: int
    ) -> Tuple[bool, int, int]:
        """
        Record a single gesture sample.
        
        Args:
            hand_data: Hand landmark data
            frame_count: Current frame number
            
        Returns:
            Tuple of (recording_complete, samples_collected, target_samples)
        """
        if not self.is_recording:
            return False, 0, 0
        
        # Sample at configured rate
        if frame_count % self.config.training_sample_rate != 0:
            return False, self.samples_collected, self.config.training_samples_per_gesture
        
        # Extract features
        features = self.feature_extractor.extract_features(hand_data)
        self.recording_samples.append(features)
        self.samples_collected += 1
        
        # Check if recording complete
        if self.samples_collected >= self.config.training_samples_per_gesture:
            self._finalize_recording()
            return True, self.samples_collected, self.config.training_samples_per_gesture
        
        return False, self.samples_collected, self.config.training_samples_per_gesture
    
    def _finalize_recording(self) -> None:
        """Process recorded samples and create trained gesture."""
        if not self.recording_samples:
            print("No samples recorded!")
            self.is_recording = False
            return
        
        # Convert feature dictionaries to consistent vectors
        # Use same feature keys for all samples
        feature_keys = sorted(self.recording_samples[0].keys())
        feature_vectors = []
        
        for sample in self.recording_samples:
            vector = np.array([sample[key] for key in feature_keys])
            feature_vectors.append(vector)
        
        feature_vectors = np.array(feature_vectors)
        
        # Calculate statistics
        mean_vector = np.mean(feature_vectors, axis=0)
        std_vector = np.std(feature_vectors, axis=0)
        
        # Create trained gesture
        trained_gesture = TrainedGesture(
            name=self.recording_name,
            feature_vectors=list(feature_vectors),
            mean_vector=mean_vector,
            std_vector=std_vector,
            confidence_threshold=self.config.match_threshold,
            hand_label=self.recording_hand_label,
            timestamp=time.time(),
            sample_count=len(feature_vectors)
        )
        
        # Add to library
        self.trained_gestures[self.recording_name] = trained_gesture
        
        print(f"Gesture '{self.recording_name}' trained successfully!")
        print(f"Samples: {trained_gesture.sample_count}")
        
        # Save automatically
        self.save_gestures()
        
        # Reset recording state
        self.is_recording = False
        self.recording_name = None
        self.recording_samples = []
        self.recording_hand_label = None
        self.samples_collected = 0
    
    def cancel_recording(self) -> None:
        """Cancel current recording session."""
        self.is_recording = False
        self.recording_name = None
        self.recording_samples = []
        self.recording_hand_label = None
        self.samples_collected = 0
        print("Recording cancelled")
    
    def match_gesture(
        self,
        hand_data: HandData,
        hand_label: HandLabel
    ) -> Optional[Tuple[str, float]]:
        """
        Match hand data against trained gestures.
        
        Args:
            hand_data: Current hand landmark data
            hand_label: Which hand
            
        Returns:
            Tuple of (gesture_name, confidence) or None if no match
        """
        if not self.trained_gestures:
            return None
        
        # Extract features from current hand
        current_features = self.feature_extractor.extract_features(hand_data)
        feature_keys = sorted(current_features.keys())
        current_vector = np.array([current_features[key] for key in feature_keys])
        
        best_match = None
        best_confidence = 0.0
        
        # Compare against all trained gestures
        for gesture_name, trained_gesture in self.trained_gestures.items():
            # Skip if wrong hand
            if trained_gesture.hand_label != hand_label.value:
                continue
            
            # Calculate similarity using cosine similarity and euclidean distance
            mean_vec = trained_gesture.mean_vector
            
            # Ensure vectors have same length
            if len(current_vector) != len(mean_vec):
                continue
            
            # Cosine similarity
            cosine_sim = np.dot(current_vector, mean_vec) / (
                np.linalg.norm(current_vector) * np.linalg.norm(mean_vec) + 1e-8
            )
            
            # Normalized euclidean distance
            euclidean_dist = np.linalg.norm(current_vector - mean_vec)
            max_dist = np.linalg.norm(mean_vec) + 1e-8
            similarity = 1.0 - (euclidean_dist / max_dist)
            
            # Combined confidence score
            confidence = (cosine_sim * 0.6 + similarity * 0.4)
            
            # Check threshold
            if confidence >= trained_gesture.confidence_threshold:
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_match = gesture_name
        
        if best_match:
            return best_match, best_confidence
        
        return None
    
    def save_gestures(self, backup: bool = True) -> None:
        """
        Save trained gestures to file.
        
        Args:
            backup: Create backup of existing file
        """
        # Create directory if needed
        gesture_path = Path(self.gestures_file)
        gesture_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Backup existing file
        if backup and gesture_path.exists():
            backup_path = Path(self.config.backup_file)
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            import shutil
            shutil.copy2(gesture_path, backup_path)
        
        # Convert to serializable format
        data = {
            "version": "2.0.0",
            "timestamp": time.time(),
            "gesture_count": len(self.trained_gestures),
            "gestures": {
                name: gesture.to_dict()
                for name, gesture in self.trained_gestures.items()
            }
        }
        
        # Save to JSON
        with open(gesture_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Saved {len(self.trained_gestures)} gestures to {self.gestures_file}")
    
    def load_gestures(self) -> int:
        """
        Load trained gestures from file.
        
        Returns:
            Number of gestures loaded
        """
        gesture_path = Path(self.gestures_file)
        
        if not gesture_path.exists():
            print(f"No gestures file found at {self.gestures_file}")
            return 0
        
        try:
            with open(gesture_path, 'r') as f:
                data = json.load(f)
            
            self.trained_gestures = {}
            for name, gesture_data in data.get("gestures", {}).items():
                self.trained_gestures[name] = TrainedGesture.from_dict(gesture_data)
            
            print(f"Loaded {len(self.trained_gestures)} gestures from {self.gestures_file}")
            return len(self.trained_gestures)
        
        except Exception as e:
            print(f"Error loading gestures: {e}")
            return 0
    
    def delete_gesture(self, gesture_name: str) -> bool:
        """
        Delete a trained gesture.
        
        Args:
            gesture_name: Name of gesture to delete
            
        Returns:
            True if deleted, False if not found
        """
        if gesture_name in self.trained_gestures:
            del self.trained_gestures[gesture_name]
            self.save_gestures()
            print(f"Deleted gesture: {gesture_name}")
            return True
        
        print(f"Gesture not found: {gesture_name}")
        return False
    
    def list_gestures(self) -> List[str]:
        """Get list of all trained gesture names."""
        return list(self.trained_gestures.keys())
    
    def get_gesture_info(self, gesture_name: str) -> Optional[Dict]:
        """Get detailed information about a trained gesture."""
        if gesture_name not in self.trained_gestures:
            return None
        
        gesture = self.trained_gestures[gesture_name]
        return {
            "name": gesture.name,
            "hand": gesture.hand_label,
            "samples": gesture.sample_count,
            "threshold": gesture.confidence_threshold,
            "trained_at": time.ctime(gesture.timestamp)
        }


if __name__ == "__main__":
    # Test gesture trainer
    print("Gesture Trainer Test")
    print("=" * 50)
    
    trainer = GestureTrainer()
    
    print(f"\nLoaded gestures: {trainer.list_gestures()}")
    
    for gesture_name in trainer.list_gestures():
        info = trainer.get_gesture_info(gesture_name)
        print(f"\n{gesture_name}:")
        for key, value in info.items():
            print(f"  {key}: {value}")
