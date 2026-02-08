"""
Webcam capture module for AccessAble.
Handles camera initialization, frame capture, and resource cleanup.
"""

import cv2
import numpy as np
from typing import Optional, Tuple
from config.constants import Constants


class Webcam:
    """
    Manages webcam access and frame capture for gesture detection.
    Designed for reliability and proper resource management.
    """
    
    def __init__(
        self,
        camera_index: int = Constants.CAMERA_INDEX,
        width: int = Constants.FRAME_WIDTH,
        height: int = Constants.FRAME_HEIGHT
    ):
        """
        Initialize webcam capture.
        
        Args:
            camera_index: Camera device index (0 for default camera)
            width: Desired frame width
            height: Desired frame height
        """
        self.camera_index = camera_index
        self.width = width
        self.height = height
        self.capture: Optional[cv2.VideoCapture] = None
        self.is_opened = False
    
    def start(self) -> bool:
        """
        Start the webcam capture.
        
        Returns:
            True if camera opened successfully, False otherwise
        """
        self.capture = cv2.VideoCapture(self.camera_index)
        
        if not self.capture.isOpened():
            print(f"Error: Could not open camera {self.camera_index}")
            return False
        
        # Configure camera properties
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.capture.set(cv2.CAP_PROP_FPS, Constants.TARGET_FPS)
        
        # Some cameras don't support all settings - verify actual values
        actual_width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        print(f"Camera initialized: {actual_width}x{actual_height}")
        
        self.is_opened = True
        return True
    
    def read_frame(self) -> Tuple[bool, Optional[np.ndarray]]:
        """
        Read a single frame from the camera.
        
        Returns:
            Tuple of (success, frame) where:
                success: True if frame was read successfully
                frame: The captured frame as numpy array, or None if failed
        """
        if not self.is_opened or self.capture is None:
            return False, None
        
        success, frame = self.capture.read()
        
        if not success:
            return False, None
        
        # Flip frame horizontally for mirror effect (more intuitive for users)
        # This makes the experience feel like looking in a mirror
        frame = cv2.flip(frame, 1)
        
        return True, frame
    
    def release(self) -> None:
        """
        Release camera resources.
        Always call this when done to free the camera for other applications.
        """
        if self.capture is not None:
            self.capture.release()
            self.is_opened = False
            print("Camera released")
    
    def __enter__(self):
        """Context manager entry - starts the camera."""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - releases the camera."""
        self.release()
