"""
Motion Smoothing and Filtering Module

Implements multiple smoothing algorithms to reduce jitter and noise in hand tracking:
- Moving Average Filter: Simple rolling window averaging
- Exponential Smoothing: Weighted average with decay
- Kalman Filter: Optimal state estimation with noise rejection

Author: Gestura Development Team
Version: 2.0.0
"""

import numpy as np
from typing import List, Optional, Tuple
from collections import deque
from dataclasses import dataclass


@dataclass
class LandmarkPoint:
    """Represents a 3D landmark point with smoothing history."""
    x: float
    y: float
    z: float
    
    def to_array(self) -> np.ndarray:
        """Convert to numpy array."""
        return np.array([self.x, self.y, self.z])
    
    @classmethod
    def from_array(cls, arr: np.ndarray) -> 'LandmarkPoint':
        """Create from numpy array."""
        return cls(x=arr[0], y=arr[1], z=arr[2])


class MovingAverageFilter:
    """
    Moving average filter using a rolling window.
    
    Reduces high-frequency noise by averaging landmark positions over N frames.
    Best for: General purpose smoothing, simple jitter reduction.
    """
    
    def __init__(self, window_size: int = 5):
        """
        Initialize moving average filter.
        
        Args:
            window_size: Number of frames to average (default: 5)
        """
        self.window_size = window_size
        self.history: deque = deque(maxlen=window_size)
    
    def smooth(self, landmark: LandmarkPoint) -> LandmarkPoint:
        """
        Apply moving average smoothing to a landmark point.
        
        Args:
            landmark: Current landmark position
            
        Returns:
            Smoothed landmark position
        """
        self.history.append(landmark.to_array())
        
        if len(self.history) < 2:
            return landmark
        
        # Calculate average of all points in window
        avg = np.mean(np.array(self.history), axis=0)
        return LandmarkPoint.from_array(avg)
    
    def reset(self) -> None:
        """Clear history buffer."""
        self.history.clear()


class ExponentialSmoothingFilter:
    """
    Exponential smoothing filter with configurable alpha parameter.
    
    Applies weighted average where recent values have more influence.
    Formula: smoothed = alpha * current + (1 - alpha) * previous
    
    Best for: Real-time responsiveness with moderate smoothing.
    """
    
    def __init__(self, alpha: float = 0.3):
        """
        Initialize exponential smoothing filter.
        
        Args:
            alpha: Smoothing factor (0.0-1.0). 
                  Lower = more smoothing, higher = more responsive
        """
        self.alpha = max(0.0, min(1.0, alpha))  # Clamp to [0, 1]
        self.previous: Optional[np.ndarray] = None
    
    def smooth(self, landmark: LandmarkPoint) -> LandmarkPoint:
        """
        Apply exponential smoothing to a landmark point.
        
        Args:
            landmark: Current landmark position
            
        Returns:
            Smoothed landmark position
        """
        current = landmark.to_array()
        
        if self.previous is None:
            self.previous = current
            return landmark
        
        # Exponential smoothing formula
        smoothed = self.alpha * current + (1 - self.alpha) * self.previous
        self.previous = smoothed
        
        return LandmarkPoint.from_array(smoothed)
    
    def reset(self) -> None:
        """Clear previous state."""
        self.previous = None


class KalmanFilter:
    """
    Kalman filter for optimal state estimation with noise rejection.
    
    Predicts future position based on motion model and corrects using measurements.
    Best for: Rejecting tremors, optimal estimation with sensor noise.
    
    State vector: [x, vx, y, vy, z, vz] (position + velocity for each axis)
    """
    
    def __init__(
        self, 
        process_noise: float = 0.01,
        measurement_noise: float = 0.1
    ):
        """
        Initialize Kalman filter.
        
        Args:
            process_noise: Process noise covariance (model uncertainty)
            measurement_noise: Measurement noise covariance (sensor noise)
        """
        # State dimension: 6 (x, vx, y, vy, z, vz)
        self.state_dim = 6
        
        # State vector [x, vx, y, vy, z, vz]
        self.state = np.zeros(self.state_dim)
        
        # Covariance matrix (uncertainty in state estimate)
        self.P = np.eye(self.state_dim) * 1.0
        
        # State transition matrix (constant velocity model)
        self.F = np.eye(self.state_dim)
        self.F[0, 1] = 1  # x = x + vx*dt
        self.F[2, 3] = 1  # y = y + vy*dt
        self.F[4, 5] = 1  # z = z + vz*dt
        
        # Measurement matrix (observe position only)
        self.H = np.zeros((3, self.state_dim))
        self.H[0, 0] = 1  # Measure x
        self.H[1, 2] = 1  # Measure y
        self.H[2, 4] = 1  # Measure z
        
        # Process noise covariance
        self.Q = np.eye(self.state_dim) * process_noise
        
        # Measurement noise covariance
        self.R = np.eye(3) * measurement_noise
        
        # Initialization flag
        self.initialized = False
    
    def smooth(self, landmark: LandmarkPoint) -> LandmarkPoint:
        """
        Apply Kalman filtering to a landmark point.
        
        Args:
            landmark: Current landmark measurement
            
        Returns:
            Filtered landmark position
        """
        measurement = landmark.to_array()
        
        if not self.initialized:
            # Initialize state with first measurement
            self.state[0] = measurement[0]  # x
            self.state[2] = measurement[1]  # y
            self.state[4] = measurement[2]  # z
            self.initialized = True
            return landmark
        
        # PREDICTION STEP
        # Predict state: x̂ₖ = F * x̂ₖ₋₁
        self.state = self.F @ self.state
        
        # Predict covariance: Pₖ = F * Pₖ₋₁ * F' + Q
        self.P = self.F @ self.P @ self.F.T + self.Q
        
        # UPDATE STEP
        # Innovation (measurement residual): y = z - H * x̂ₖ
        innovation = measurement - (self.H @ self.state)
        
        # Innovation covariance: S = H * Pₖ * H' + R
        S = self.H @ self.P @ self.H.T + self.R
        
        # Kalman gain: K = Pₖ * H' * S⁻¹
        K = self.P @ self.H.T @ np.linalg.inv(S)
        
        # Update state: x̂ₖ = x̂ₖ + K * y
        self.state = self.state + K @ innovation
        
        # Update covariance: Pₖ = (I - K * H) * Pₖ
        self.P = (np.eye(self.state_dim) - K @ self.H) @ self.P
        
        # Extract position from state
        filtered_pos = np.array([self.state[0], self.state[2], self.state[4]])
        
        return LandmarkPoint.from_array(filtered_pos)
    
    def reset(self) -> None:
        """Reset filter state."""
        self.state = np.zeros(self.state_dim)
        self.P = np.eye(self.state_dim) * 1.0
        self.initialized = False


class MultiLandmarkSmoother:
    """
    Smooths all 21 hand landmarks using configurable filter.
    
    Maintains separate filter instance for each landmark to preserve
    spatial relationships and gesture shapes.
    """
    
    def __init__(
        self, 
        filter_type: str = "exponential",
        **filter_params
    ):
        """
        Initialize multi-landmark smoother.
        
        Args:
            filter_type: Type of filter ("moving_avg", "exponential", "kalman")
            **filter_params: Parameters passed to filter constructor
        """
        self.filter_type = filter_type
        self.filter_params = filter_params
        
        # Create 21 independent filters (one per landmark)
        self.filters: List = []
        self._initialize_filters()
    
    def _initialize_filters(self) -> None:
        """Create filter instances for all 21 landmarks."""
        for _ in range(21):
            if self.filter_type == "moving_avg":
                window_size = self.filter_params.get("window_size", 5)
                self.filters.append(MovingAverageFilter(window_size))
            elif self.filter_type == "exponential":
                alpha = self.filter_params.get("alpha", 0.3)
                self.filters.append(ExponentialSmoothingFilter(alpha))
            elif self.filter_type == "kalman":
                process_noise = self.filter_params.get("process_noise", 0.01)
                measurement_noise = self.filter_params.get("measurement_noise", 0.1)
                self.filters.append(KalmanFilter(process_noise, measurement_noise))
            else:
                raise ValueError(f"Unknown filter type: {self.filter_type}")
    
    def smooth_landmarks(
        self, 
        landmarks: List[Tuple[float, float, float]]
    ) -> List[Tuple[float, float, float]]:
        """
        Smooth all 21 landmarks.
        
        Args:
            landmarks: List of 21 (x, y, z) tuples representing hand landmarks
            
        Returns:
            List of 21 smoothed (x, y, z) tuples
        """
        if len(landmarks) != 21:
            raise ValueError(f"Expected 21 landmarks, got {len(landmarks)}")
        
        smoothed = []
        for i, (x, y, z) in enumerate(landmarks):
            landmark = LandmarkPoint(x, y, z)
            smoothed_landmark = self.filters[i].smooth(landmark)
            smoothed.append((smoothed_landmark.x, smoothed_landmark.y, smoothed_landmark.z))
        
        return smoothed
    
    def reset(self) -> None:
        """Reset all filters."""
        for filter_inst in self.filters:
            filter_inst.reset()


if __name__ == "__main__":
    # Test smoothing filters
    import matplotlib.pyplot as plt
    
    # Generate noisy signal
    np.random.seed(42)
    t = np.linspace(0, 10, 100)
    signal = np.sin(t) + np.random.normal(0, 0.2, 100)
    
    # Test filters
    filters = {
        "Moving Average": MovingAverageFilter(window_size=5),
        "Exponential": ExponentialSmoothingFilter(alpha=0.3),
        "Kalman": KalmanFilter()
    }
    
    results = {"Original": signal}
    for name, f in filters.items():
        smoothed = []
        for val in signal:
            point = LandmarkPoint(val, 0, 0)
            smoothed_point = f.smooth(point)
            smoothed.append(smoothed_point.x)
        results[name] = smoothed
    
    # Plot comparison
    plt.figure(figsize=(12, 6))
    for name, data in results.items():
        plt.plot(t, data, label=name, alpha=0.7)
    plt.legend()
    plt.title("Smoothing Filter Comparison")
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.grid(True, alpha=0.3)
    plt.show()
