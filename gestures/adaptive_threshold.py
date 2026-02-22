"""
Adaptive thresholding system for gesture recognition.
Dynamically adjusts confidence thresholds based on user performance.
"""

from typing import Dict, Deque
from collections import deque
import numpy as np
from dataclasses import dataclass, field


@dataclass
class AdaptiveThresholds:
    """
    Manages adaptive confidence thresholds for gesture recognition.
    
    Tracks user's gesture execution success rate and adjusts
    thresholds to balance between false positives and false negatives.
    """
    
    # Configuration
    window_size: int = 50  # Number of recent gestures to consider
    min_confidence: float = 0.5  # Absolute minimum threshold
    max_confidence: float = 0.95  # Absolute maximum threshold
    adjustment_rate: float = 0.01  # How much to adjust per update
    
    # Tracking
    recent_confidences: Deque[float] = field(default_factory=lambda: deque(maxlen=50))
    successful_activations: int = 0
    false_positives: int = 0
    
    # Current threshold
    current_threshold: float = 0.75
    
    def record_activation(self, confidence: float, was_successful: bool) -> None:
        """
        Record a gesture activation and whether it was successful.
        
        Args:
            confidence: Confidence score of the activation
            was_successful: Whether the activation was intended by user
        """
        self.recent_confidences.append(confidence)
        
        if was_successful:
            self.successful_activations += 1
        else:
            self.false_positives += 1
        
        # Adjust threshold periodically
        if len(self.recent_confidences) >= 10:
            self._adjust_threshold()
    
    def _adjust_threshold(self) -> None:
        """
        Adjust confidence threshold based on recent performance.
        
        Strategy:
        - If many false positives → increase threshold
        - If few activations but hand visible → decrease threshold
        - Use exponential moving average for smoothness
        """
        total_activations = self.successful_activations + self.false_positives
        
        if total_activations < 10:
            return  # Not enough data yet
        
        false_positive_rate = self.false_positives / total_activations
        
        # If false positive rate is high, increase threshold
        if false_positive_rate > 0.2:  # More than 20% false positives
            self.current_threshold = min(
                self.current_threshold + self.adjustment_rate,
                self.max_confidence
            )
        # If false positive rate is very low, can decrease threshold
        elif false_positive_rate < 0.05:  # Less than 5% false positives
            self.current_threshold = max(
                self.current_threshold - self.adjustment_rate,
                self.min_confidence
            )
    
    def get_threshold(self) -> float:
        """Get current adaptive threshold."""
        return self.current_threshold
    
    def get_stats(self) -> Dict[str, float]:
        """Get statistics about threshold adaptation."""
        total = self.successful_activations + self.false_positives
        return {
            'current_threshold': self.current_threshold,
            'total_activations': total,
            'successful_rate': (self.successful_activations / total * 100) if total > 0 else 0,
            'false_positive_rate': (self.false_positives / total * 100) if total > 0 else 0,
            'avg_confidence': float(np.mean(list(self.recent_confidences))) if self.recent_confidences else 0.0,
        }
    
    def reset(self) -> None:
        """Reset adaptation state."""
        self.recent_confidences.clear()
        self.successful_activations = 0
        self.false_positives = 0
        self.current_threshold = 0.75  # Reset to default
