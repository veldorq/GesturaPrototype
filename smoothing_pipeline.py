"""
Smoothing Pipeline for Real-Time Gesture Recognition
=====================================================
Author: Senior Python Accessibility Engineer & Performance Optimizer
Date: February 9, 2026

Purpose:
    Reduce jitter, flicker, and confidence oscillation in real-time gesture detection
    using filterpy (Kalman) and scipy.signal (Savitzky-Golay) filtering.

Integration Point:
    Post-CNN prediction, pre-state machine (does NOT replace state machine)

Safety Guarantees:
    - Filtered outputs never trigger actions directly
    - All values pass through existing state machine
    - No architectural changes to existing pipeline
    - Graceful degradation if libraries unavailable
"""

import numpy as np
from collections import deque
import warnings
warnings.filterwarnings('ignore')

# Optional imports with graceful fallback
try:
    from filterpy.kalman import KalmanFilter  # type: ignore
    from filterpy.common import Q_discrete_white_noise  # type: ignore
    FILTERPY_AVAILABLE = True
except ImportError:
    FILTERPY_AVAILABLE = False
    KalmanFilter = None  # type: ignore
    Q_discrete_white_noise = None  # type: ignore
    print("WARNING: filterpy not installed - confidence smoothing disabled")
    print("   Install with: pip install filterpy")

try:
    from scipy.signal import savgol_filter  # type: ignore
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    savgol_filter = None  # type: ignore
    print("WARNING: scipy not installed - jitter reduction disabled")
    print("   Install with: pip install scipy")


class SmoothingConfig:
    """Configuration for smoothing pipeline"""
    
    # Kalman filter settings (confidence smoothing)
    KALMAN_PROCESS_VARIANCE = 0.01   # Lower = smoother but slower response
    KALMAN_MEASUREMENT_VARIANCE = 0.1  # Lower = trust measurements more
    
    # Savitzky-Golay filter settings (jitter reduction)
    SAVGOL_WINDOW_LENGTH = 5   # Must be odd, larger = smoother
    SAVGOL_POLYORDER = 2        # Polynomial order (2 or 3 recommended)
    
    # Smoothing buffer sizes
    CONFIDENCE_BUFFER_SIZE = 10  # For Savitzky-Golay on confidence
    LANDMARK_BUFFER_SIZE = 7     # For coordinate smoothing
    
    # Enable/disable flags (for A/B testing)
    ENABLE_KALMAN_SMOOTHING = True
    ENABLE_SAVGOL_SMOOTHING = True
    ENABLE_COORDINATE_SMOOTHING = True


class ConfidenceKalmanFilter:
    """
    Kalman filter for CNN confidence score smoothing.
    
    Purpose:
        - Reduce confidence oscillation (e.g., 0.78 → 0.82 → 0.79 → ...)
        - Smooth out frame-to-frame noise
        - Maintain responsiveness to genuine changes
    
    Integration:
        CNN raw confidence → Kalman filter → Smoothed confidence → State machine
    """
    
    def __init__(self):
        """Initialize Kalman filter for 1D confidence tracking"""
        self.enabled = FILTERPY_AVAILABLE and SmoothingConfig.ENABLE_KALMAN_SMOOTHING
        
        if self.enabled:
            # Create 1D Kalman filter (state = [confidence, confidence_velocity])
            self.kf = KalmanFilter(dim_x=2, dim_z=1)  # type: ignore
            
            # State transition matrix (constant velocity model)
            self.kf.F = np.array([[1., 1.],   # confidence(t+1) = confidence(t) + velocity(t)
                                  [0., 1.]])   # velocity(t+1) = velocity(t)
            
            # Measurement matrix (we only observe confidence directly)
            self.kf.H = np.array([[1., 0.]])  # type: ignore
            
            # Process noise (how much confidence can change frame-to-frame)
            self.kf.Q = Q_discrete_white_noise(dim=2, dt=1./30.,  # type: ignore
                                              var=SmoothingConfig.KALMAN_PROCESS_VARIANCE)
            
            # Measurement noise (uncertainty in CNN confidence readings)
            self.kf.R = np.array([[SmoothingConfig.KALMAN_MEASUREMENT_VARIANCE]])
            
            # Initial state covariance
            self.kf.P *= 1.0
            
            # Initial state (will be set on first measurement)
            self.kf.x = np.array([[0.5], [0.]])  # Start at neutral confidence
            self.initialized = False
        else:
            self.kf = None
            self.initialized = False
    
    def update(self, confidence_raw):
        """
        Update filter with new confidence measurement.
        
        Args:
            confidence_raw: Raw CNN confidence (0-1)
        
        Returns:
            float: Smoothed confidence (0-1) or raw if filtering disabled
        """
        if not self.enabled or confidence_raw is None:
            return confidence_raw
        
        # Initialize on first measurement
        if not self.initialized and self.kf is not None:
            self.kf.x = np.array([[confidence_raw], [0.]])
            self.initialized = True
            return confidence_raw
        
        if self.kf is None:
            return confidence_raw
        
        # Predict next state
        self.kf.predict()
        
        # Update with measurement
        self.kf.update(np.array([[confidence_raw]]))
        
        # Extract smoothed confidence (clip to [0, 1])
        smoothed = float(self.kf.x[0])
        return np.clip(smoothed, 0.0, 1.0)
    
    def reset(self):
        """Reset filter state (call when hand lost or gesture changes)"""
        if self.enabled:
            self.initialized = False


class SavitzkyGolayJitterReducer:
    """
    Savitzky-Golay filter for micro-jitter reduction.
    
    Purpose:
        - Smooth short-term oscillations in confidence/coordinates
        - Preserve genuine signal changes (edge-preserving)
        - Reduce high-frequency noise without lag
    
    Integration:
        After Kalman filter, before state machine
    """
    
    def __init__(self, buffer_size=SmoothingConfig.CONFIDENCE_BUFFER_SIZE):
        """Initialize Savitzky-Golay filter"""
        self.enabled = SCIPY_AVAILABLE and SmoothingConfig.ENABLE_SAVGOL_SMOOTHING
        self.buffer = deque(maxlen=buffer_size)
        self.buffer_size = buffer_size
    
    def add_value(self, value):
        """
        Add new value to buffer.
        
        Args:
            value: Confidence score or coordinate (float)
        """
        if value is not None:
            self.buffer.append(value)
    
    def get_smoothed_value(self):
        """
        Apply Savitzky-Golay filter to buffer.
        
        Returns:
            float: Smoothed value or None if buffer too small
        """
        if not self.enabled:
            return self.buffer[-1] if self.buffer else None
        
        # Need at least window_length samples
        if len(self.buffer) < SmoothingConfig.SAVGOL_WINDOW_LENGTH:
            return self.buffer[-1] if self.buffer else None
        
        # Convert buffer to array
        buffer_array = np.array(list(self.buffer))
        
        # Apply Savitzky-Golay filter
        try:
            smoothed_array = savgol_filter(  # type: ignore
                buffer_array,
                window_length=SmoothingConfig.SAVGOL_WINDOW_LENGTH,
                polyorder=SmoothingConfig.SAVGOL_POLYORDER,
                mode='nearest'
            )
            # Return most recent smoothed value
            return float(smoothed_array[-1])
        except Exception:
            # Fallback to raw value on error
            return buffer_array[-1]
    
    def reset(self):
        """Clear buffer"""
        self.buffer.clear()


class CoordinateStabilizer:
    """
    Stabilize hand landmark coordinates using exponential moving average.
    
    Purpose:
        - Reduce hand tremor in pointer mode
        - Smooth ROI center for CNN extraction
        - Improve swipe detection consistency
    
    Integration:
        MediaPipe landmarks → Coordinate stabilizer → Gesture recognition
    """
    
    def __init__(self, alpha=0.3):
        """
        Initialize coordinate stabilizer.
        
        Args:
            alpha: Smoothing factor (0=no smoothing, 1=no filtering)
                  Lower = smoother but slower response
        """
        self.enabled = SmoothingConfig.ENABLE_COORDINATE_SMOOTHING
        self.alpha = alpha
        self.prev_coords = None
    
    def smooth_coordinates(self, current_coords):
        """
        Apply exponential moving average to coordinates.
        
        Args:
            current_coords: Array of (x, y) coordinates [(x1,y1), (x2,y2), ...]
        
        Returns:
            Smoothed coordinates or raw if filtering disabled
        """
        if not self.enabled or current_coords is None:
            return current_coords
        
        # Initialize on first frame
        if self.prev_coords is None:
            self.prev_coords = np.array(current_coords)
            return current_coords
        
        # Apply exponential moving average: smoothed = alpha * current + (1-alpha) * previous
        smoothed = self.alpha * np.array(current_coords) + (1 - self.alpha) * self.prev_coords
        
        # Update previous
        self.prev_coords = smoothed
        
        return smoothed.tolist()
    
    def reset(self):
        """Reset stabilizer state"""
        self.prev_coords = None


class GestureSmoothingPipeline:
    """
    Complete smoothing pipeline for gesture recognition.
    
    Pipeline flow:
        CNN → Kalman (confidence) → Savitzky-Golay (confidence) → State machine
        MediaPipe → EMA (coordinates) → Gesture recognition
    
    Safety:
        - Does NOT replace state machine
        - Does NOT trigger actions
        - Only smooths values, preserves logic
    """
    
    def __init__(self):
        """Initialize complete smoothing pipeline"""
        # Confidence smoothing
        self.kalman_filter = ConfidenceKalmanFilter()
        self.savgol_filter = SavitzkyGolayJitterReducer()
        
        # Coordinate smoothing
        self.coord_stabilizer = CoordinateStabilizer(alpha=0.3)
        
        # Statistics
        self.frames_processed = 0
        self.smoothing_active = (FILTERPY_AVAILABLE or SCIPY_AVAILABLE)
        
        print(f"\nSmoothing Pipeline Initialized:")
        print(f"   - Kalman filter: {'[ENABLED]' if self.kalman_filter.enabled else '[DISABLED]'}")
        print(f"   - Savitzky-Golay filter: {'[ENABLED]' if self.savgol_filter.enabled else '[DISABLED]'}")
        print(f"   - Coordinate stabilizer: {'[ENABLED]' if self.coord_stabilizer.enabled else '[DISABLED]'}")
    
    def smooth_confidence(self, confidence_raw):
        """
        Apply two-stage confidence smoothing.
        
        Pipeline: Raw confidence → Kalman → Savitzky-Golay → Smoothed
        
        Args:
            confidence_raw: Raw CNN confidence (0-1)
        
        Returns:
            float: Smoothed confidence (0-1)
        """
        if confidence_raw is None:
            return None
        
        # Stage 1: Kalman filtering
        confidence_kalman = self.kalman_filter.update(confidence_raw)
        
        # Stage 2: Savitzky-Golay filtering
        self.savgol_filter.add_value(confidence_kalman)
        confidence_smoothed = self.savgol_filter.get_smoothed_value()
        
        self.frames_processed += 1
        
        return confidence_smoothed if confidence_smoothed is not None else confidence_kalman
    
    def smooth_landmarks(self, landmarks_raw):
        """
        Smooth hand landmark coordinates.
        
        Args:
            landmarks_raw: List of MediaPipe landmarks (with .x, .y attributes)
        
        Returns:
            None (modifies landmarks in-place)
        """
        if landmarks_raw is None:
            return None
        
        # Extract coordinates
        coords = [(lm.x, lm.y) for lm in landmarks_raw]
        
        # Smooth coordinates
        smoothed_coords = self.coord_stabilizer.smooth_coordinates(coords)
        
        # Update landmarks in-place (preserve z coordinate)
        # Use try-except to handle protobuf read-only fields gracefully
        try:
            for i in range(len(landmarks_raw)):
                landmarks_raw[i].x = smoothed_coords[i][0]
                landmarks_raw[i].y = smoothed_coords[i][1]
        except (AttributeError, TypeError) as e:
            # If landmarks are read-only, skip smoothing
            # This can happen with certain protobuf versions
            pass
        
        return None
    
    def reset_all(self):
        """Reset all filters (call when hand lost or major scene change)"""
        self.kalman_filter.reset()
        self.savgol_filter.reset()
        self.coord_stabilizer.reset()
    
    def get_statistics(self):
        """Get smoothing pipeline statistics"""
        return {
            'frames_processed': self.frames_processed,
            'smoothing_active': self.smoothing_active,
            'kalman_enabled': self.kalman_filter.enabled,
            'savgol_enabled': self.savgol_filter.enabled,
            'coord_stabilizer_enabled': self.coord_stabilizer.enabled
        }


def test_smoothing():
    """Test smoothing pipeline with synthetic data"""
    print("\n" + "="*70)
    print("  SMOOTHING PIPELINE TEST")
    print("="*70 + "\n")
    
    pipeline = GestureSmoothingPipeline()
    
    # Simulate noisy confidence values
    print("Testing confidence smoothing with noisy signal:")
    noisy_confidences = [0.78, 0.82, 0.77, 0.83, 0.79, 0.84, 0.80, 0.85, 0.81]
    smoothed_confidences = []
    
    for i, conf_raw in enumerate(noisy_confidences):
        conf_smoothed = pipeline.smooth_confidence(conf_raw)
        smoothed_confidences.append(conf_smoothed)
        print(f"  Frame {i+1}: Raw={conf_raw:.3f} → Smoothed={conf_smoothed:.3f}")
    
    # Calculate variance reduction
    var_raw = np.var(noisy_confidences)
    var_smoothed = np.var(smoothed_confidences)
    reduction = (1 - var_smoothed/var_raw) * 100
    
    print(f"\nVariance reduction: {reduction:.1f}%")
    print(f"Raw variance: {var_raw:.6f}")
    print(f"Smoothed variance: {var_smoothed:.6f}")
    
    stats = pipeline.get_statistics()
    print(f"\nStatistics:")
    print(f"  Frames processed: {stats['frames_processed']}")
    print(f"  Smoothing active: {stats['smoothing_active']}")


if __name__ == "__main__":
    test_smoothing()
