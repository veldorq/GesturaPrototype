"""
Gesture CNN Inference Wrapper for Gestura
==========================================
Author: Senior Python Accessibility Engineer
Date: February 8, 2026

Purpose:
    Safe inference wrapper for CNN gesture classification.
    Enforces strict confidence thresholding and temporal voting.

Critical Design:
    - CNN output NEVER directly triggers actions
    - All predictions pass through confidence filter
    - Temporal voting for stability (last N frames)
    - Output format: (gesture_label, confidence_score)

Safety Guarantees:
    - Low confidence predictions ignored
    - Single-frame predictions never propagated
    - Consistent frame buffer before classification
"""

import numpy as np
import cv2
import pickle
from pathlib import Path
from collections import deque

try:
    import tensorflow as tf
    from tensorflow import keras
    CNN_AVAILABLE = True
except ImportError:
    CNN_AVAILABLE = False
    print(f"WARNING: TensorFlow not available - CNN inference disabled")


class GestureInferenceConfig:
    """Configuration for CNN inference"""
    
    # Model paths
    MODEL_PATH = "models/gesture_cnn_model.h5"
    LABEL_ENCODER_PATH = "models/label_encoder.pkl"
    
    # Input settings
    IMAGE_SIZE = (64, 64)
    
    # Confidence thresholding (CRITICAL for anti-glitch)
    # TUNED: Higher threshold (0.80) reduces false positives for accessibility
    MIN_CONFIDENCE_THRESHOLD = 0.80  # Ignore predictions below 80% (was 75%)
    HIGH_CONFIDENCE_THRESHOLD = 0.88  # Strong confidence threshold (was 85%)
    
    # Temporal voting (CRITICAL for stability)
    # TUNED: Longer window (7 frames) for shaky hand tolerance
    VOTING_WINDOW_SIZE = 7  # Last 7 frames must agree (was 5)
    VOTING_CONSISTENCY_THRESHOLD = 0.85  # 85% of frames must show same gesture (was 80%)
    
    # Safety
    ENABLE_CONFIDENCE_FILTER = True  # Must be True for production
    ENABLE_TEMPORAL_VOTING = True    # Must be True for production


class CNNGestureClassifier:
    """
    CNN-based gesture classifier with safety mechanisms.
    
    This class ONLY performs gesture classification.
    It does NOT execute actions - that's handled by the state machine.
    """
    
    def __init__(self):
        """Initialize CNN classifier"""
        self.model = None
        self.label_encoder = None
        self.is_loaded = False
        
        # Temporal voting buffer
        self.prediction_buffer = deque(maxlen=GestureInferenceConfig.VOTING_WINDOW_SIZE)
        self.confidence_buffer = deque(maxlen=GestureInferenceConfig.VOTING_WINDOW_SIZE)
        
        # Statistics
        self.total_predictions = 0
        self.filtered_predictions = 0
        
    def load_model(self):
        """
        Load trained CNN model and label encoder.
        
        Returns:
            bool: True if loaded successfully
        """
        if not CNN_AVAILABLE:
            print("[ERROR] TensorFlow not available - CNN classifier disabled")
            return False
        
        model_path = Path(GestureInferenceConfig.MODEL_PATH)
        encoder_path = Path(GestureInferenceConfig.LABEL_ENCODER_PATH)
        
        if not model_path.exists():
            print(f"[ERROR] Model not found: {model_path}")
            print("   Train model first using: python train_gesture_model.py")
            return False
        
        if not encoder_path.exists():
            print(f"[ERROR] Label encoder not found: {encoder_path}")
            return False
        
        try:
            # Load model
            self.model = keras.models.load_model(str(model_path))
            print(f"[SUCCESS] CNN model loaded: {model_path}")
            
            # Load label encoder
            with open(encoder_path, 'rb') as f:
                self.label_encoder = pickle.load(f)
            print(f"[SUCCESS] Label encoder loaded: {encoder_path}")
            
            # Verify model input shape
            input_shape = self.model.input_shape
            expected_shape = (None, 64, 64, 1)
            if input_shape != expected_shape:
                print(f"WARNING: Unexpected input shape: {input_shape}")
            
            self.is_loaded = True
            return True
        
        except Exception as e:
            print(f"[ERROR] Error loading model: {e}")
            return False
    
    def preprocess_hand_roi(self, hand_roi):
        """
        Preprocess hand ROI for CNN inference.
        
        Args:
            hand_roi: Hand region extracted from frame
        
        Returns:
            Preprocessed image ready for model (1, 64, 64, 1)
        """
        # Convert to grayscale if needed
        if len(hand_roi.shape) == 3:
            hand_gray = cv2.cvtColor(hand_roi, cv2.COLOR_BGR2GRAY)
        else:
            hand_gray = hand_roi
        
        # Resize to model input size
        hand_resized = cv2.resize(hand_gray, GestureInferenceConfig.IMAGE_SIZE)
        
        # Normalize to [0, 1]
        hand_normalized = hand_resized.astype('float32') / 255.0
        
        # Reshape for model: (1, 64, 64, 1)
        hand_input = hand_normalized.reshape(1, 64, 64, 1)
        
        return hand_input
    
    def predict_single_frame(self, hand_roi):
        """
        Predict gesture from single frame (RAW - no filtering).
        
        IMPORTANT: This is RAW prediction. Use classify() for filtered output.
        
        Args:
            hand_roi: Hand region image
        
        Returns:
            tuple: (gesture_label, confidence_score) or (None, 0.0)
        """
        if not self.is_loaded or self.model is None:
            return None, 0.0
        
        if hand_roi is None or hand_roi.size == 0:
            return None, 0.0
        
        try:
            # Preprocess
            hand_input = self.preprocess_hand_roi(hand_roi)
            
            # Predict
            predictions = self.model.predict(hand_input, verbose=0)[0]
            
            # Get best prediction
            best_idx = np.argmax(predictions)
            confidence = float(predictions[best_idx])
            gesture_label = self.label_encoder.get(best_idx, 'unknown')
            
            self.total_predictions += 1
            
            return gesture_label, confidence
        
        except Exception as e:
            print(f"WARNING: Prediction error: {e}")
            return None, 0.0
    
    def apply_confidence_filter(self, gesture_label, confidence):
        """
        Apply confidence threshold filtering.
        
        SAFETY MECHANISM: Reject low-confidence predictions.
        
        Args:
            gesture_label: Predicted gesture
            confidence: Confidence score (0-1)
        
        Returns:
            tuple: (filtered_gesture, confidence) or (None, 0.0)
        """
        if not GestureInferenceConfig.ENABLE_CONFIDENCE_FILTER:
            return gesture_label, confidence
        
        # Reject low confidence
        if confidence < GestureInferenceConfig.MIN_CONFIDENCE_THRESHOLD:
            self.filtered_predictions += 1
            return None, 0.0
        
        return gesture_label, confidence
    
    def apply_temporal_voting(self, gesture_label, confidence):
        """
        Apply temporal voting for stability.
        
        SAFETY MECHANISM: Require consistent predictions over N frames.
        
        DataFlair-based anti-flicker logic:
            1. Add current prediction to buffer
            2. Check if buffer is full (prevents premature detection)
            3. Find most common gesture in buffer
            4. Check if it appears in ≥85% of frames (strict consistency)
            5. Return only if consistent, else None (false negative > false positive)
        
        Args:
            gesture_label: Current gesture prediction
            confidence: Current confidence score
        
        Returns:
            tuple: (stable_gesture, avg_confidence) or (None, 0.0)
        """
        if not GestureInferenceConfig.ENABLE_TEMPORAL_VOTING:
            return gesture_label, confidence
        
        # Add to buffers
        self.prediction_buffer.append(gesture_label)
        self.confidence_buffer.append(confidence)
        
        # Wait for buffer to fill
        if len(self.prediction_buffer) < GestureInferenceConfig.VOTING_WINDOW_SIZE:
            return None, 0.0
        
        # Count gesture occurrences
        gesture_counts = {}
        for g in self.prediction_buffer:
            if g is not None:
                gesture_counts[g] = gesture_counts.get(g, 0) + 1
        
        if not gesture_counts:
            return None, 0.0
        
        # Find most common gesture
        most_common_gesture = max(gesture_counts, key=gesture_counts.get)
        occurrence_ratio = gesture_counts[most_common_gesture] / len(self.prediction_buffer)
        
        # Check consistency threshold
        if occurrence_ratio >= GestureInferenceConfig.VOTING_CONSISTENCY_THRESHOLD:
            # Calculate average confidence for this gesture
            avg_confidence = np.mean([
                conf for g, conf in zip(self.prediction_buffer, self.confidence_buffer)
                if g == most_common_gesture
            ])
            return most_common_gesture, float(avg_confidence)
        
        return None, 0.0
    
    def classify(self, hand_roi):
        """
        Main classification method with full safety pipeline.
        
        Pipeline:
            Hand ROI
            → CNN Prediction (raw)
            → Confidence Filter (threshold)
            → Temporal Voting (stability)
            → Output: (gesture_label, confidence) or (None, 0.0)
        
        GUARANTEED: This method NEVER returns unstable or low-confidence predictions.
        
        Args:
            hand_roi: Hand region image
        
        Returns:
            tuple: (gesture_label, confidence_score) or (None, 0.0)
        """
        # Step 1: Raw CNN prediction
        gesture_raw, confidence_raw = self.predict_single_frame(hand_roi)
        
        # Step 2: Confidence filtering
        gesture_filtered, confidence_filtered = self.apply_confidence_filter(
            gesture_raw, confidence_raw
        )
        
        # Step 3: Temporal voting
        gesture_stable, confidence_stable = self.apply_temporal_voting(
            gesture_filtered, confidence_filtered
        )
        
        return gesture_stable, confidence_stable
    
    def reset_buffers(self):
        """Reset temporal voting buffers (call when hand lost or mode switches)"""
        self.prediction_buffer.clear()
        self.confidence_buffer.clear()
    
    def get_statistics(self):
        """Get classifier statistics"""
        filter_rate = (self.filtered_predictions / self.total_predictions * 100) if self.total_predictions > 0 else 0
        
        return {
            'total_predictions': self.total_predictions,
            'filtered_predictions': self.filtered_predictions,
            'filter_rate': filter_rate,
            'buffer_size': len(self.prediction_buffer)
        }


class HybridGestureSystem:
    """
    Hybrid gesture recognition combining CNN and MediaPipe.
    
    Division of labor:
        - CNN: Gesture classification (scroll, swipe, pinch, etc.)
        - MediaPipe: Pointer movement, pinch distance measurement
    
    This ensures smooth pointer control while using CNN for action gestures.
    """
    
    def __init__(self):
        """Initialize hybrid system"""
        self.cnn_classifier = CNNGestureClassifier()
        self.use_cnn = False
    
    def initialize(self):
        """Initialize the hybrid system"""
        print("\n🔧 Initializing Hybrid Gesture System...")
        
        # Try to load CNN model
        if self.cnn_classifier.load_model():
            self.use_cnn = True
            print("[SUCCESS] CNN classifier active")
        else:
            print("WARNING: CNN classifier not available - using rule-based fallback")
            self.use_cnn = False
        
        return self.use_cnn
    
    def classify_gesture(self, hand_roi, hand_landmarks=None):
        """
        Classify gesture using hybrid approach.
        
        Args:
            hand_roi: Hand region for CNN
            hand_landmarks: MediaPipe landmarks (optional, for pointer mode detection)
        
        Returns:
            tuple: (gesture_label, confidence_score)
        """
        if self.use_cnn:
            return self.cnn_classifier.classify(hand_roi)
        else:
            # Fallback to rule-based (existing system)
            return None, 0.0
    
    def is_pointer_mode(self, hand_landmarks):
        """
        Detect if in pointer mode (single index finger extended).
        
        Uses MediaPipe landmarks, NOT CNN (for smooth pointer control).
        """
        # This should be implemented using existing rule-based logic
        # Left as placeholder for integration
        return False


def test_inference():
    """Test CNN inference wrapper"""
    print("\n" + "="*70)
    print("  CNN INFERENCE TEST")
    print("="*70 + "\n")
    
    classifier = CNNGestureClassifier()
    
    if classifier.load_model():
        print("\n[SUCCESS] Model loaded successfully")
        
        # Create dummy hand ROI
        dummy_roi = np.random.randint(0, 255, (100, 100), dtype=np.uint8)
        
        print("\nTesting classification pipeline...")
        gesture, confidence = classifier.classify(dummy_roi)
        
        print(f"  Result: gesture={gesture}, confidence={confidence:.4f}")
        
        stats = classifier.get_statistics()
        print(f"\nStatistics:")
        print(f"  Total predictions: {stats['total_predictions']}")
        print(f"  Filtered predictions: {stats['filtered_predictions']}")
        print(f"  Filter rate: {stats['filter_rate']:.2f}%")
    else:
        print("\n[ERROR] Model not loaded - cannot test inference")


if __name__ == "__main__":
    test_inference()
