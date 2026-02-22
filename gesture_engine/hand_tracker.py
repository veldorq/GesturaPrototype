"""
Two-Hand Tracking Module using MediaPipe

Provides simultaneous tracking of left and right hands with independent state management.
Integrates with smoothing filters to reduce jitter and improve tracking quality.

Author: Gestura Development Team
Version: 2.0.0
"""

import cv2
import mediapipe as mp
import numpy as np
from typing import Optional, List, Tuple, Dict
from dataclasses import dataclass
from enum import Enum

from gesture_engine.smoothing import MultiLandmarkSmoother
from gesture_engine.config import CONFIG


class HandLabel(Enum):
    """Hand identification labels."""
    LEFT = "Left"
    RIGHT = "Right"
    UNKNOWN = "Unknown"


@dataclass
class HandData:
    """
    Complete data structure for a single hand.
    
    Attributes:
        label: Hand identification (Left/Right)
        landmarks: List of 21 (x, y, z) landmark coordinates (normalized 0-1)
        landmarks_px: List of 21 (x, y) pixel coordinates
        world_landmarks: List of 21 (x, y, z) real-world coordinates (meters)
        confidence: Detection confidence score (0-1)
        is_visible: Whether hand is currently in frame
        frame_id: Frame number when hand was last detected
    """
    label: HandLabel
    landmarks: List[Tuple[float, float, float]]
    landmarks_px: List[Tuple[int, int]]
    world_landmarks: List[Tuple[float, float, float]]
    confidence: float
    is_visible: bool
    frame_id: int
    
    def get_landmark(self, idx: int) -> Optional[Tuple[float, float, float]]:
        """Get specific landmark by index (0-20)."""
        if 0 <= idx < len(self.landmarks):
            return self.landmarks[idx]
        return None
    
    def get_landmark_px(self, idx: int) -> Optional[Tuple[int, int]]:
        """Get specific landmark in pixel coordinates."""
        if 0 <= idx < len(self.landmarks_px):
            return self.landmarks_px[idx]
        return None
    
    def to_feature_vector(self) -> np.ndarray:
        """Convert landmarks to flat feature vector for ML models."""
        return np.array(self.landmarks).flatten()


class TwoHandTracker:
    """
    Tracks both hands simultaneously using MediaPipe Hands.
    
    Features:
    - Independent tracking of left and right hands
    - Configurable smoothing (moving average, exponential, Kalman)
    - Hand state management with entry/exit detection
    - Real-world and pixel coordinate systems
    - Performance optimized for real-time operation (30+ FPS)
    """
    
    def __init__(self, use_smoothing: bool = True, smoothing_type: str = "exponential"):
        """
        Initialize two-hand tracker.
        
        Args:
            use_smoothing: Enable landmark smoothing (default: True)
            smoothing_type: Type of smoothing filter ("moving_avg", "exponential", "kalman")
        """
        # Load configuration
        self.config = CONFIG.hand_tracking
        
        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=self.config.max_num_hands,
            min_detection_confidence=self.config.min_detection_confidence,
            min_tracking_confidence=self.config.min_tracking_confidence,
            model_complexity=self.config.model_complexity
        )
        
        # Smoothing filters for each hand
        self.use_smoothing = use_smoothing
        self.smoothers: Dict[HandLabel, MultiLandmarkSmoother] = {}
        
        if use_smoothing:
            smoothing_params = self._get_smoothing_params(smoothing_type)
            self.smoothers[HandLabel.LEFT] = MultiLandmarkSmoother(
                filter_type=smoothing_type,
                **smoothing_params
            )
            self.smoothers[HandLabel.RIGHT] = MultiLandmarkSmoother(
                filter_type=smoothing_type,
                **smoothing_params
            )
        
        # Hand state tracking
        self.left_hand: Optional[HandData] = None
        self.right_hand: Optional[HandData] = None
        self.frame_count = 0
        
        # Camera properties (set during processing)
        self.frame_width = self.config.frame_width
        self.frame_height = self.config.frame_height
    
    def _get_smoothing_params(self, smoothing_type: str) -> Dict:
        """Get smoothing parameters from configuration."""
        if smoothing_type == "moving_avg":
            return {"window_size": CONFIG.smoothing.moving_avg_window}
        elif smoothing_type == "exponential":
            return {"alpha": CONFIG.smoothing.exp_smoothing_alpha}
        elif smoothing_type == "kalman":
            return {
                "process_noise": CONFIG.smoothing.kalman_process_noise,
                "measurement_noise": CONFIG.smoothing.kalman_measurement_noise
            }
        return {}
    
    def process_frame(self, frame: np.ndarray) -> Tuple[np.ndarray, Dict[HandLabel, HandData]]:
        """
        Process a single frame and detect hands.
        
        Args:
            frame: BGR image from camera (numpy array)
            
        Returns:
            Tuple of (annotated_frame, hand_data_dict)
            - annotated_frame: Frame with hand landmarks drawn
            - hand_data_dict: Dictionary mapping HandLabel to HandData
        """
        self.frame_count += 1
        
        # Update frame dimensions
        h, w, _ = frame.shape
        self.frame_height, self.frame_width = h, w
        
        # Convert BGR to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process frame with MediaPipe
        results = self.hands.process(rgb_frame)
        
        # Reset hand visibility
        if self.left_hand:
            self.left_hand.is_visible = False
        if self.right_hand:
            self.right_hand.is_visible = False
        
        detected_hands = {}
        
        if results.multi_hand_landmarks and results.multi_handedness:
            for hand_landmarks, handedness in zip(
                results.multi_hand_landmarks,
                results.multi_handedness
            ):
                # Determine hand label
                # MediaPipe returns labels from camera perspective (mirrored)
                # So we swap: "Left" from camera = Right hand of user
                hand_label_str = handedness.classification[0].label
                hand_label = HandLabel.RIGHT if hand_label_str == "Left" else HandLabel.LEFT
                confidence = handedness.classification[0].score
                
                # Extract landmarks
                landmarks = self._extract_landmarks(hand_landmarks)
                landmarks_px = self._landmarks_to_pixels(landmarks)
                
                # Extract world landmarks if available
                world_landmarks = []
                if results.multi_hand_world_landmarks:
                    for wl in results.multi_hand_world_landmarks[0].landmark:
                        world_landmarks.append((wl.x, wl.y, wl.z))
                else:
                    world_landmarks = landmarks  # Fallback
                
                # Apply smoothing
                if self.use_smoothing and hand_label in self.smoothers:
                    landmarks = self.smoothers[hand_label].smooth_landmarks(landmarks)
                    landmarks_px = self._landmarks_to_pixels(landmarks)
                
                # Create HandData object
                hand_data = HandData(
                    label=hand_label,
                    landmarks=landmarks,
                    landmarks_px=landmarks_px,
                    world_landmarks=world_landmarks,
                    confidence=confidence,
                    is_visible=True,
                    frame_id=self.frame_count
                )
                
                # Update state
                if hand_label == HandLabel.LEFT:
                    self.left_hand = hand_data
                elif hand_label == HandLabel.RIGHT:
                    self.right_hand = hand_data
                
                detected_hands[hand_label] = hand_data
                
                # Draw landmarks on frame
                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style()
                )
                
                # Draw hand label
                wrist_px = landmarks_px[0]
                cv2.putText(
                    frame,
                    f"{hand_label.value} ({confidence:.2f})",
                    (wrist_px[0] - 40, wrist_px[1] - 20),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0) if hand_label == HandLabel.LEFT else (255, 0, 0),
                    2
                )
        
        return frame, detected_hands
    
    def _extract_landmarks(self, hand_landmarks) -> List[Tuple[float, float, float]]:
        """Extract normalized landmark coordinates (0-1 range)."""
        return [(lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark]
    
    def _landmarks_to_pixels(
        self, 
        landmarks: List[Tuple[float, float, float]]
    ) -> List[Tuple[int, int]]:
        """Convert normalized landmarks to pixel coordinates."""
        return [
            (int(x * self.frame_width), int(y * self.frame_height))
            for x, y, z in landmarks
        ]
    
    def get_hand(self, label: HandLabel) -> Optional[HandData]:
        """
        Get data for specific hand.
        
        Args:
            label: HandLabel.LEFT or HandLabel.RIGHT
            
        Returns:
            HandData if hand is visible, None otherwise
        """
        if label == HandLabel.LEFT:
            return self.left_hand if self.left_hand and self.left_hand.is_visible else None
        elif label == HandLabel.RIGHT:
            return self.right_hand if self.right_hand and self.right_hand.is_visible else None
        return None
    
    def get_both_hands(self) -> Tuple[Optional[HandData], Optional[HandData]]:
        """
        Get data for both hands.
        
        Returns:
            Tuple of (left_hand_data, right_hand_data)
            Either can be None if hand is not visible
        """
        left = self.left_hand if self.left_hand and self.left_hand.is_visible else None
        right = self.right_hand if self.right_hand and self.right_hand.is_visible else None
        return left, right
    
    def are_both_hands_visible(self) -> bool:
        """Check if both hands are currently visible."""
        return (
            self.left_hand is not None and self.left_hand.is_visible and
            self.right_hand is not None and self.right_hand.is_visible
        )
    
    def get_hand_distance(self) -> Optional[float]:
        """
        Calculate distance between hands (when both visible).
        
        Returns:
            Normalized distance (0-1) or None if both hands not visible
        """
        if not self.are_both_hands_visible():
            return None
        
        # Use wrist landmarks (index 0)
        left_wrist = np.array(self.left_hand.landmarks[0])
        right_wrist = np.array(self.right_hand.landmarks[0])
        
        return np.linalg.norm(left_wrist - right_wrist)
    
    def reset_smoothing(self) -> None:
        """Reset smoothing filters (e.g., when hand re-enters frame)."""
        for smoother in self.smoothers.values():
            smoother.reset()
    
    def release(self) -> None:
        """Release MediaPipe resources."""
        self.hands.close()
    
    def __del__(self):
        """Cleanup on object destruction."""
        self.release()


if __name__ == "__main__":
    # Test hand tracking with webcam
    print("Two-Hand Tracker Test")
    print("Press 'q' to quit, 's' to toggle smoothing, 'r' to reset")
    
    tracker = TwoHandTracker(use_smoothing=True, smoothing_type="exponential")
    cap = cv2.VideoCapture(CONFIG.hand_tracking.camera_index)
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CONFIG.hand_tracking.frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CONFIG.hand_tracking.frame_height)
    
    use_smoothing = True
    
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            continue
        
        # Process frame
        annotated_frame, hands = tracker.process_frame(frame)
        
        # Display info
        info_text = []
        left, right = tracker.get_both_hands()
        
        if left:
            info_text.append(f"Left: {left.confidence:.2f}")
        if right:
            info_text.append(f"Right: {right.confidence:.2f}")
        
        if tracker.are_both_hands_visible():
            distance = tracker.get_hand_distance()
            info_text.append(f"Distance: {distance:.3f}")
        
        # Draw info
        y_offset = 30
        for text in info_text:
            cv2.putText(annotated_frame, text, (10, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            y_offset += 30
        
        cv2.putText(annotated_frame, f"Smoothing: {'ON' if use_smoothing else 'OFF'}",
                   (10, annotated_frame.shape[0] - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        
        cv2.imshow("Two-Hand Tracker Test", annotated_frame)
        
        # Handle keys
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            use_smoothing = not use_smoothing
            tracker.use_smoothing = use_smoothing
        elif key == ord('r'):
            tracker.reset_smoothing()
            print("Smoothing filters reset")
    
    cap.release()
    cv2.destroyAllWindows()
    tracker.release()
