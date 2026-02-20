"""
Performance metrics collection and monitoring.
Tracks FPS, latency, and other key performance indicators.
"""

import time
from collections import deque
from typing import Dict, Optional
from dataclasses import dataclass, field


@dataclass
class PerformanceMetrics:
    """
    Collects and calculates performance metrics for the application.
    """
    
    # Configuration
    window_size: int = 30  # Number of samples for moving average
    
    # Frame timing
    frame_times: deque = field(default_factory=lambda: deque(maxlen=30))
    detection_times: deque = field(default_factory=lambda: deque(maxlen=30))
    recognition_times: deque = field(default_factory=lambda: deque(maxlen=30))
    
    # Counters
    total_frames: int = 0
    successful_detections: int = 0
    gesture_recognitions: int = 0
    action_executions: int = 0
    
    # Timestamps
    start_time: float = field(default_factory=time.time)
    last_frame_time: float = field(default_factory=time.time)
    
    def record_frame_time(self, duration: float) -> None:
        """Record time taken to process a frame."""
        self.frame_times.append(duration)
        self.total_frames += 1
        self.last_frame_time = time.time()
    
    def record_detection_time(self, duration: float, success: bool) -> None:
        """Record time taken for hand detection."""
        self.detection_times.append(duration)
        if success:
            self.successful_detections += 1
    
    def record_recognition_time(self, duration: float, recognized: bool) -> None:
        """Record time taken for gesture recognition."""
        self.recognition_times.append(duration)
        if recognized:
            self.gesture_recognitions += 1
    
    def record_action_execution(self) -> None:
        """Record that an action was executed."""
        self.action_executions += 1
    
    def get_fps(self) -> float:
        """Calculate current FPS from frame times."""
        if not self.frame_times:
            return 0.0
        avg_time = sum(self.frame_times) / len(self.frame_times)
        return 1.0 / avg_time if avg_time > 0 else 0.0
    
    def get_avg_detection_time(self) -> float:
        """Get average detection time in milliseconds."""
        if not self.detection_times:
            return 0.0
        return (sum(self.detection_times) / len(self.detection_times)) * 1000
    
    def get_avg_recognition_time(self) -> float:
        """Get average recognition time in milliseconds."""
        if not self.recognition_times:
            return 0.0
        return (sum(self.recognition_times) / len(self.recognition_times)) * 1000
    
    def get_detection_rate(self) -> float:
        """Get percentage of frames with successful hand detection."""
        if self.total_frames == 0:
            return 0.0
        return (self.successful_detections / self.total_frames) * 100
    
    def get_uptime(self) -> float:
        """Get application uptime in seconds."""
        return time.time() - self.start_time
    
    def get_summary(self) -> Dict[str, float]:
        """Get a summary of all metrics."""
        return {
            'fps': self.get_fps(),
            'avg_detection_ms': self.get_avg_detection_time(),
            'avg_recognition_ms': self.get_avg_recognition_time(),
            'detection_rate': self.get_detection_rate(),
            'total_frames': self.total_frames,
            'gestures_recognized': self.gesture_recognitions,
            'actions_executed': self.action_executions,
            'uptime_seconds': self.get_uptime(),
        }
    
    def reset(self) -> None:
        """Reset all metrics."""
        self.frame_times.clear()
        self.detection_times.clear()
        self.recognition_times.clear()
        self.total_frames = 0
        self.successful_detections = 0
        self.gesture_recognitions = 0
        self.action_executions = 0
        self.start_time = time.time()
