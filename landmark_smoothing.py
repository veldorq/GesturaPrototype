"""
Motion smoothing filters for hand landmark tracking.
Reduces jitter and improves gesture recognition stability for PROTOTYPE.PY.

Author: Gestura Development Team
Version: 1.0
"""

import numpy as np
from typing import List, Tuple, Optional
from collections import deque


class LandmarkPoint:
    """A single 3D landmark point."""
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z


class MovingAverageFilter:
    """
    Simple moving average filter for landmark smoothing.
    Averages the last N frames to reduce jitter.
    """
    
    def __init__(self, window_size: int = 5):
        self.window_size = window_size
        self.history: deque = deque(maxlen=window_size)
    
    def smooth(self, point: LandmarkPoint) -> LandmarkPoint:
        """Apply moving average smoothing."""
        self.history.append((point.x, point.y, point.z))
        
        if len(self.history) == 0:
            return point
        
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
        Args:
            alpha: Smoothing factor (0-1). Lower = more smoothing, higher = more responsive
        """
        self.alpha = alpha
        self.prev_point: Optional[LandmarkPoint] = None
    
    def smooth(self, point: LandmarkPoint) -> LandmarkPoint:
        """Apply exponential smoothing."""
        if self.prev_point is None:
            self.prev_point = point
            return point
        
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
    
    def __init__(self, process_noise: float = 0.01, measurement_noise: float = 0.1):
        # State vector: [x, vx, y, vy, z, vz]
        self.state = np.zeros(6)
        self.covariance = np.eye(6) * 1000
        self.process_noise = np.eye(6) * process_noise
        self.measurement_noise = np.eye(3) * measurement_noise
        
        # State transition matrix (constant velocity model)
        self.transition = np.array([
            [1, 1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 0],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 1],
            [0, 0, 0, 0, 0, 1],
        ])
        
        # Measurement matrix
        self.measurement = np.array([
            [1, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 0],
        ])
        
        self.initialized = False
    
    def smooth(self, point: LandmarkPoint) -> LandmarkPoint:
        """Apply Kalman filtering."""
        measurement = np.array([point.x, point.y, point.z])
        
        if not self.initialized:
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
    Applies selected filter type to each landmark independently.
    """
    
    def __init__(self, filter_type: str = "exponential", **filter_params):
        """
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
    
    def smooth_landmarks(self, landmarks) -> list:
        """
        Apply smoothing to all landmarks.
        
        Args:
            landmarks: MediaPipe hand_landmarks.landmark list
            
        Returns:
            Smoothed landmarks (modifies in place)
        """
        smoothed = []
        
        for i, landmark in enumerate(landmarks):
            point = LandmarkPoint(landmark.x, landmark.y, landmark.z)
            smoothed_point = self.filters[i].smooth(point)
            
            # Update landmark in place
            landmark.x = smoothed_point.x
            landmark.y = smoothed_point.y
            landmark.z = smoothed_point.z
            
            smoothed.append(landmark)
        
        return smoothed
    
    def reset(self):
        """Reset all filters."""
        for filter_obj in self.filters:
            filter_obj.reset()


# Convenience function for easy integration
def create_landmark_smoother(smoothing_type: str = "exponential", alpha: float = 0.3, 
                            window_size: int = 5) -> LandmarkSmoother:
    """
    Factory function to create a landmark smoother with common presets.
    
    Args:
        smoothing_type: 'exponential' (default), 'moving_avg', or 'kalman'
        alpha: For exponential smoothing (0.2-0.5 recommended)
        window_size: For moving average (3-7 recommended)
    
    Returns:
        Configured LandmarkSmoother instance
    """
    if smoothing_type == "exponential":
        return LandmarkSmoother(filter_type="exponential", alpha=alpha)
    elif smoothing_type == "moving_avg":
        return LandmarkSmoother(filter_type="moving_avg", window_size=window_size)
    elif smoothing_type == "kalman":
        return LandmarkSmoother(filter_type="kalman", process_noise=0.01, measurement_noise=0.1)
    else:
        raise ValueError(f"Unknown smoothing type: {smoothing_type}")
