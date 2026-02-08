"""
Hand detection and landmark tracking using MediaPipe.
Extracts hand landmarks for gesture recognition.
"""

import cv2
import mediapipe as mp
import numpy as np
from typing import Optional, List, Tuple
from dataclasses import dataclass
from config.constants import Constants


@dataclass
class HandLandmarks:
    """
    Represents detected hand landmarks with metadata.
    
    MediaPipe provides 21 3D landmarks per hand:
    - 0: Wrist
    - 1-4: Thumb (CMC, MCP, IP, Tip)
    - 5-8: Index finger (MCP, PIP, DIP, Tip)
    - 9-12: Middle finger (MCP, PIP, DIP, Tip)
    - 13-16: Ring finger (MCP, PIP, DIP, Tip)
    - 17-20: Pinky (MCP, PIP, DIP, Tip)
    """
    landmarks: List[Tuple[float, float, float]]  # (x, y, z) normalized coordinates
    handedness: str  # 'Left' or 'Right'
    confidence: float  # Detection confidence score
    
    def get_landmark(self, index: int) -> Tuple[float, float, float]:
        """
        Get a specific landmark by index.
        
        Args:
            index: Landmark index (0-20)
            
        Returns:
            (x, y, z) coordinates normalized to [0, 1]
        """
        return self.landmarks[index]
    
    def get_finger_tip(self, finger: str) -> Tuple[float, float, float]:
        """
        Get the tip landmark for a specific finger.
        
        Args:
            finger: One of 'thumb', 'index', 'middle', 'ring', 'pinky'
            
        Returns:
            (x, y, z) coordinates of the fingertip
        """
        tip_indices = {
            'thumb': 4,
            'index': 8,
            'middle': 12,
            'ring': 16,
            'pinky': 20
        }
        return self.landmarks[tip_indices[finger]]
    
    def get_pixel_coords(
        self,
        index: int,
        frame_width: int,
        frame_height: int
    ) -> Tuple[int, int]:
        """
        Convert normalized landmark to pixel coordinates.
        
        Args:
            index: Landmark index
            frame_width: Width of the frame
            frame_height: Height of the frame
            
        Returns:
            (x, y) pixel coordinates
        """
        x, y, _ = self.landmarks[index]
        return int(x * frame_width), int(y * frame_height)


class HandDetector:
    """
    Detects hands and extracts landmarks using MediaPipe Hands.
    Optimized for single-hand detection with high reliability.
    """
    
    def __init__(
        self,
        max_hands: int = Constants.MAX_NUM_HANDS,
        detection_confidence: float = Constants.MIN_DETECTION_CONFIDENCE,
        tracking_confidence: float = Constants.MIN_TRACKING_CONFIDENCE
    ):
        """
        Initialize MediaPipe hand detector.
        
        Args:
            max_hands: Maximum number of hands to detect
            detection_confidence: Minimum confidence for initial detection
            tracking_confidence: Minimum confidence for tracking across frames
        """
        self.max_hands = max_hands
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence
        
        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # Create Hands object with specified parameters
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,  # Video stream mode for better performance
            max_num_hands=self.max_hands,
            min_detection_confidence=self.detection_confidence,
            min_tracking_confidence=self.tracking_confidence
        )
    
    def detect(self, frame: np.ndarray) -> Optional[HandLandmarks]:
        """
        Detect hand landmarks in a frame.
        
        Args:
            frame: BGR image from camera
            
        Returns:
            HandLandmarks object if hand detected, None otherwise
        """
        # Convert BGR to RGB (MediaPipe requires RGB)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process frame to detect hands
        results = self.hands.process(rgb_frame)
        
        # Return None if no hands detected
        if not results.multi_hand_landmarks:
            return None
        
        # Extract first hand only (accessibility focus)
        hand_landmarks = results.multi_hand_landmarks[0]
        hand_handedness = results.multi_handedness[0]
        
        # Extract landmark coordinates
        landmarks = [
            (lm.x, lm.y, lm.z)
            for lm in hand_landmarks.landmark
        ]
        
        # Extract handedness and confidence
        handedness = hand_handedness.classification[0].label
        confidence = hand_handedness.classification[0].score
        
        return HandLandmarks(
            landmarks=landmarks,
            handedness=handedness,
            confidence=confidence
        )
    
    def draw_landmarks(
        self,
        frame: np.ndarray,
        hand_landmarks: HandLandmarks
    ) -> np.ndarray:
        """
        Draw hand landmarks on frame for visual feedback.
        
        Args:
            frame: Frame to draw on
            hand_landmarks: Detected hand landmarks
            
        Returns:
            Frame with landmarks drawn
        """
        # Convert our HandLandmarks back to MediaPipe format for drawing
        mp_landmark_list = self.mp_hands.HandLandmark
        
        # Create a MediaPipe-compatible landmark structure
        from mediapipe.framework.formats import landmark_pb2
        
        hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        for x, y, z in hand_landmarks.landmarks:
            landmark = hand_landmarks_proto.landmark.add()
            landmark.x = x
            landmark.y = y
            landmark.z = z
        
        # Draw landmarks with connections
        self.mp_drawing.draw_landmarks(
            frame,
            hand_landmarks_proto,
            self.mp_hands.HAND_CONNECTIONS,
            self.mp_drawing_styles.get_default_hand_landmarks_style(),
            self.mp_drawing_styles.get_default_hand_connections_style()
        )
        
        return frame
    
    def release(self) -> None:
        """Release MediaPipe resources."""
        if self.hands:
            self.hands.close()
