"""
Motion smoothing filters for hand landmark tracking.
Reduces jitter and improves gesture recognition stability.
"""

import numpy as np
from typing import List, Tuple, Optional
from collections import deque
from dataclasses import dataclass


@dataclass
class LandmarkPoint:
    """A single 3D landmark point."""
    x: float
    y: float
    z: float


class MovingAverageFilter:
    """
    Simple moving average filter for landmark smoothing.
    Averages the last N frames to reduce jitter.
    """
    
    def __init__(self, window_size: int = 5):
        """
        Initialize moving average filter.
        
        Args:
            window_size: Number of frames to average
        """
        self.window_size = window_size
        self.history: deque = deque(maxlen=window_size)
    
    def smooth(self, point: LandmarkPoint) -> LandmarkPoint:
        """
        Apply moving average smoothing.
        
        Args:
            point: Current landmark point
            
        Returns:
            Smoothed landmark point
        """
        self.history.append((point.x, point.y, point.z))
        
        if len(self.history) == 0:
            return point
        
        # Calculate average
        avg_x = sum(p[0] for p in self.history) / len(self.history)
        avg_y = sum(p[1] for p in self.history) / len(self.history)
        avg_z = sum(p[2] for p in self.history) / len(self.history)
        
        return LandmarkPoint(avg_x, avg_y, avg_z)
    
    def reset(self):
        """Clear the history buffer."""
        self.history.clear()


class ExponentialSmoothingFilter:
    """
    Exponential smoothing filter for landmark tracking.
    More responsive than moving average while still reducing jitter.
    """
    
    def __init__(self, alpha: float = 0.3):
        """
        Initialize exponential smoothing filter.
        
        Args:
            alpha: Smoothing factor (0-1). Lower = more smoothing, higher = more responsive
        """
        self.alpha = alpha
        self.prev_point: Optional[LandmarkPoint] = None
    
    def smooth(self, point: LandmarkPoint) -> LandmarkPoint:
        """
        Apply exponential smoothing.
        
        Args:
            point: Current landmark point
            
        Returns:
            Smoothed landmark point
        """
        if self.prev_point is None:
            self.prev_point = point
            return point
        
        # Exponentially weighted average
        smoothed_x = self.alpha * point.x + (1 - self.alpha) * self.prev_point.x
        smoothed_y = self.alpha * point.y + (1 - self.alpha) * self.prev_point.y
        smoothed_z = self.alpha * point.z + (1 - self.alpha) * self.prev_point.z
        
        smoothed = LandmarkPoint(smoothed_x, smoothed_y, smoothed_z)
        self.prev_point = smoothed
        
        return smoothed
    
    def reset(self):
        """Reset the filter state."""
        self.prev_point = None


class KalmanFilter:
    """
    Kalman filter for landmark tracking with velocity estimation.
    Provides predictive smoothing that can anticipate motion.
    """
    
    def __init__(
        self,
        process_noise: float = 0.01,
        measurement_noise: float = 0.1
    ):
        """
        Initialize Kalman filter.
        
        Args:
            process_noise: Process noise covariance (lower = trust model more)
            measurement_noise: Measurement noise covariance (lower = trust measurements more)
        """
        # State vector: [x, vx, y, vy, z, vz]
        self.state = np.zeros(6)
        
        # State covariance matrix
        self.covariance = np.eye(6) * 1000
        
        # Process noise
        self.process_noise = np.eye(6) * process_noise
        
        # Measurement noise
        self.measurement_noise = np.eye(3) * measurement_noise
        
        # State transition matrix (constant velocity model)
        self.transition = np.array([
            [1, 1, 0, 0, 0, 0],  # x = x + vx
            [0, 1, 0, 0, 0, 0],  # vx = vx
            [0, 0, 1, 1, 0, 0],  # y = y + vy
            [0, 0, 0, 1, 0, 0],  # vy = vy
            [0, 0, 0, 0, 1, 1],  # z = z + vz
            [0, 0, 0, 0, 0, 1],  # vz = vz
        ])
        
        # Measurement matrix (we only observe position)
        self.measurement = np.array([
            [1, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 0],
        ])
        
        self.initialized = False
    
    def smooth(self, point: LandmarkPoint) -> LandmarkPoint:
        """
        Apply Kalman filtering.
        
        Args:
            point: Current landmark point
            
        Returns:
            Smoothed and predicted landmark point
        """
        measurement = np.array([point.x, point.y, point.z])
        
        if not self.initialized:
            # Initialize state with first measurement
            self.state[0] = point.x
            self.state[2] = point.y
            self.state[4] = point.z
            self.initialized = True
            return point
        
        # Prediction step
        self.state = self.transition @ self.state
        self.covariance = (
            self.transition @ self.covariance @ self.transition.T
            + self.process_noise
        )
        
        # Update step
        innovation = measurement - self.measurement @ self.state
        innovation_cov = (
            self.measurement @ self.covariance @ self.measurement.T
            + self.measurement_noise
        )
        kalman_gain = (
            self.covariance @ self.measurement.T @ np.linalg.inv(innovation_cov)
        )
        
        self.state = self.state + kalman_gain @ innovation
        self.covariance = (
            (np.eye(6) - kalman_gain @ self.measurement) @ self.covariance
        )
        
        return LandmarkPoint(self.state[0], self.state[2], self.state[4])
    
    def reset(self):
        """Reset the filter state."""
        self.state = np.zeros(6)
        self.covariance = np.eye(6) * 1000
        self.initialized = False


class LandmarkSmoother:
    """
    Manages smoothing for all 21 hand landmarks.
    """
    
    def __init__(self, filter_type: str = "exponential", **filter_params):
        """
        Initialize landmark smoother.
        
        Args:
            filter_type: Type of filter ('moving_avg', 'exponential', 'kalman')
            **filter_params: Parameters for the selected filter
        """
        self.filter_type = filter_type
        self.filters = []
        
        # Create a filter for each of the 21 landmarks
        for _ in range(21):
            if filter_type == "moving_avg":
                window_size = filter_params.get('window_size', 5)
                self.filters.append(MovingAverageFilter(window_size))
            elif filter_type == "exponential":
                alpha = filter_params.get('alpha', 0.3)
                self.filters.append(ExponentialSmoothingFilter(alpha))
            elif filter_type == "kalman":
                process_noise = filter_params.get('process_noise', 0.01)
                measurement_noise = filter_params.get('measurement_noise', 0.1)
                self.filters.append(KalmanFilter(process_noise, measurement_noise))
            else:
                raise ValueError(f"Unknown filter type: {filter_type}")
    
    def smooth_landmarks(
        self,
        landmarks: List[Tuple[float, float, float]]
    ) -> List[Tuple[float, float, float]]:
        """
        Apply smoothing to all landmarks.
        
        Args:
            landmarks: List of 21 (x, y, z) landmark tuples
            
        Returns:
            Smoothed landmarks in the same format
        """
        smoothed = []
        
        for i, (x, y, z) in enumerate(landmarks):
            point = LandmarkPoint(x, y, z)
            smoothed_point = self.filters[i].smooth(point)
            smoothed.append((smoothed_point.x, smoothed_point.y, smoothed_point.z))
        
        return smoothed
    
    def reset(self):
        """Reset all filters."""
        for filter_obj in self.filters:
            filter_obj.reset()
