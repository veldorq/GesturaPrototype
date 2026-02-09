"""
Gesture Dataset Collection Tool for Gestura
============================================
Author: Senior Python Accessibility Engineer
Date: February 8, 2026

Purpose:
    Collect hand gesture images for CNN training using OpenCV and MediaPipe.
    Captures hand ROI only (no background) with normalized lighting and scale.

Usage:
    python collect_gesture_dataset.py

Dataset Structure:
    dataset/
    ├── scroll_up/
    ├── scroll_down/
    ├── swipe_left/
    ├── swipe_right/
    ├── pinch_zoom/
    ├── thumb_down_close/
    └── mute_toggle/

Controls:
    's' - Start/Stop capturing current gesture
    'n' - Move to next gesture
    'q' - Quit
"""

import cv2
import mediapipe as mp
import numpy as np
import os
import time
from pathlib import Path

# Configuration
class DatasetConfig:
    """Dataset collection configuration"""
    DATASET_ROOT = "dataset"
    IMAGE_SIZE = (64, 64)  # Small size for lightweight CNN
    TARGET_IMAGES_PER_GESTURE = 1000  # ~800-1500 recommended
    
    # Gestures to collect (minimal, non-overlapping set)
    GESTURES = [
        'scroll_up',
        'scroll_down',
        'swipe_left',
        'swipe_right',
        'pinch_zoom',
        'thumb_down_close',
        'mute_toggle'
    ]
    
    # Camera settings
    CAMERA_INDEX = 0
    FRAME_WIDTH = 1280
    FRAME_HEIGHT = 720
    
    # MediaPipe settings
    MIN_DETECTION_CONFIDENCE = 0.7
    MIN_TRACKING_CONFIDENCE = 0.7


class GestureDataCollector:
    """Collects hand gesture images for CNN training"""
    
    def __init__(self):
        """Initialize the data collector"""
        print("🚀 Initializing Gesture Dataset Collector...")
        
        # Create dataset folders
        self.setup_dataset_folders()
        
        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=DatasetConfig.MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=DatasetConfig.MIN_TRACKING_CONFIDENCE
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # Initialize camera
        self.cap = cv2.VideoCapture(DatasetConfig.CAMERA_INDEX)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, DatasetConfig.FRAME_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, DatasetConfig.FRAME_HEIGHT)
        
        # Collection state
        self.current_gesture_idx = 0
        self.is_capturing = False
        self.capture_count = 0
        self.last_capture_time = 0
        self.capture_delay = 0.1  # 100ms between captures (prevents duplicates)
        
        print("✅ Collector initialized successfully!")
        self.print_instructions()
    
    def setup_dataset_folders(self):
        """Create dataset directory structure"""
        Path(DatasetConfig.DATASET_ROOT).mkdir(exist_ok=True)
        
        for gesture in DatasetConfig.GESTURES:
            gesture_path = Path(DatasetConfig.DATASET_ROOT) / gesture
            gesture_path.mkdir(exist_ok=True)
        
        print(f"📁 Dataset folders created at: {DatasetConfig.DATASET_ROOT}/")
    
    def print_instructions(self):
        """Print usage instructions"""
        print("\n" + "="*70)
        print("GESTURE DATA COLLECTION INSTRUCTIONS")
        print("="*70)
        print("\nGestures to collect:")
        for i, gesture in enumerate(DatasetConfig.GESTURES):
            existing_count = self.count_existing_images(gesture)
            print(f"  {i+1}. {gesture:<20} (currently: {existing_count} images)")
        
        print(f"\nTarget: {DatasetConfig.TARGET_IMAGES_PER_GESTURE} images per gesture")
        print("\nControls:")
        print("  's' - Start/Stop capturing current gesture")
        print("  'n' - Move to next gesture")
        print("  'q' - Quit")
        print("\nTips:")
        print("  - Hold your hand steady in different positions")
        print("  - Vary hand distance from camera slightly")
        print("  - Keep background lighting consistent")
        print("  - Only your hand should be visible in the ROI")
        print("="*70 + "\n")
    
    def count_existing_images(self, gesture):
        """Count existing images for a gesture"""
        gesture_path = Path(DatasetConfig.DATASET_ROOT) / gesture
        if gesture_path.exists():
            return len(list(gesture_path.glob('*.jpg')))
        return 0
    
    def extract_hand_roi(self, frame, hand_landmarks):
        """
        Extract hand region of interest (ROI) with padding.
        
        CRITICAL: This preprocessing MUST match inference exactly.
        DataFlair consistency requirements:
            - Same bounding box calculation (min/max with 20% padding)
            - Same grayscale conversion
            - Same normalization (histogram equalization)
            - Same resize (64x64)
        
        Returns normalized, grayscale hand image ready for CNN training.
        """
        h, w, _ = frame.shape
        
        # Get bounding box of hand landmarks
        x_min, y_min = w, h
        x_max, y_max = 0, 0
        
        for landmark in hand_landmarks.landmark:
            x, y = int(landmark.x * w), int(landmark.y * h)
            x_min = min(x_min, x)
            y_min = min(y_min, y)
            x_max = max(x_max, x)
            y_max = max(y_max, y)
        
        # Add padding (20%)
        padding_x = int((x_max - x_min) * 0.2)
        padding_y = int((y_max - y_min) * 0.2)
        
        x_min = max(0, x_min - padding_x)
        y_min = max(0, y_min - padding_y)
        x_max = min(w, x_max + padding_x)
        y_max = min(h, y_max + padding_y)
        
        # Extract ROI
        hand_roi = frame[y_min:y_max, x_min:x_max]
        
        if hand_roi.size == 0:
            return None, None
        
        # Convert to grayscale
        hand_gray = cv2.cvtColor(hand_roi, cv2.COLOR_BGR2GRAY)
        
        # Normalize lighting (histogram equalization)
        hand_normalized = cv2.equalizeHist(hand_gray)
        
        # Resize to target size
        hand_resized = cv2.resize(hand_normalized, DatasetConfig.IMAGE_SIZE)
        
        return hand_resized, (x_min, y_min, x_max, y_max)
    
    def save_gesture_image(self, hand_image, gesture_name):
        """Save captured gesture image to dataset"""
        gesture_path = Path(DatasetConfig.DATASET_ROOT) / gesture_name
        
        # Generate unique filename with timestamp
        timestamp = int(time.time() * 1000)
        filename = f"{gesture_name}_{timestamp}.jpg"
        filepath = gesture_path / filename
        
        # Save image
        cv2.imwrite(str(filepath), hand_image)
        self.capture_count += 1
        
        return filepath
    
    def run(self):
        """Main collection loop"""
        print("🎥 Starting data collection...\n")
        
        try:
            while self.cap.isOpened():
                success, frame = self.cap.read()
                if not success:
                    print("⚠️  Failed to capture frame")
                    continue
                
                # Flip for mirror effect
                frame = cv2.flip(frame, 1)
                
                # Convert to RGB for MediaPipe
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Process with MediaPipe
                results = self.hands.process(rgb_frame)
                
                # Current gesture
                current_gesture = DatasetConfig.GESTURES[self.current_gesture_idx]
                existing_count = self.count_existing_images(current_gesture)
                
                # Draw hand landmarks and extract ROI
                hand_roi_display = None
                if results.multi_hand_landmarks:
                    hand_landmarks = results.multi_hand_landmarks[0]
                    
                    # Draw landmarks on frame
                    self.mp_draw.draw_landmarks(
                        frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                    )
                    
                    # Extract hand ROI
                    hand_roi, bbox = self.extract_hand_roi(frame, hand_landmarks)
                    
                    if hand_roi is not None:
                        # Draw bounding box
                        x_min, y_min, x_max, y_max = bbox
                        color = (0, 255, 0) if self.is_capturing else (255, 0, 0)
                        cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), color, 2)
                        
                        # Display ROI in corner
                        hand_roi_display = cv2.resize(hand_roi, (200, 200))
                        
                        # Capture if enabled
                        current_time = time.time()
                        if self.is_capturing and (current_time - self.last_capture_time) >= self.capture_delay:
                            filepath = self.save_gesture_image(hand_roi, current_gesture)
                            self.last_capture_time = current_time
                            print(f"✅ Captured: {filepath.name} ({existing_count + self.capture_count}/{DatasetConfig.TARGET_IMAGES_PER_GESTURE})")
                
                # Draw UI
                self.draw_ui(frame, current_gesture, existing_count, hand_roi_display)
                
                # Display
                cv2.imshow('Gestura Dataset Collector', frame)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    print("\n👋 Exiting dataset collector...")
                    break
                elif key == ord('s'):
                    self.is_capturing = not self.is_capturing
                    self.capture_count = 0
                    status = "STARTED" if self.is_capturing else "STOPPED"
                    print(f"\n📸 Capture {status} for: {current_gesture}")
                elif key == ord('n'):
                    if self.is_capturing:
                        print("⚠️  Stop capturing before switching gestures")
                    else:
                        self.current_gesture_idx = (self.current_gesture_idx + 1) % len(DatasetConfig.GESTURES)
                        print(f"\n➡️  Switched to: {DatasetConfig.GESTURES[self.current_gesture_idx]}")
        
        except KeyboardInterrupt:
            print("\n⚠️  Interrupted by user")
        
        except Exception as e:
            print(f"\n❌ Error: {e}")
        
        finally:
            self.cleanup()
    
    def draw_ui(self, frame, current_gesture, existing_count, hand_roi_display):
        """Draw user interface on frame"""
        h, w, _ = frame.shape
        
        # Status panel
        panel_height = 200
        cv2.rectangle(frame, (10, 10), (500, panel_height), (0, 0, 0), -1)
        cv2.rectangle(frame, (10, 10), (500, panel_height), (0, 255, 0), 2)
        
        # Current gesture
        cv2.putText(frame, f"Gesture: {current_gesture}", (20, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Count
        total_count = existing_count + self.capture_count
        progress = (total_count / DatasetConfig.TARGET_IMAGES_PER_GESTURE) * 100
        count_color = (0, 255, 0) if total_count >= DatasetConfig.TARGET_IMAGES_PER_GESTURE else (0, 255, 255)
        cv2.putText(frame, f"Count: {total_count}/{DatasetConfig.TARGET_IMAGES_PER_GESTURE} ({progress:.1f}%)", 
                   (20, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.6, count_color, 2)
        
        # Capture status
        status_text = "CAPTURING..." if self.is_capturing else "PAUSED"
        status_color = (0, 255, 0) if self.is_capturing else (0, 0, 255)
        cv2.putText(frame, f"Status: {status_text}", (20, 110),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2)
        
        # Controls
        cv2.putText(frame, "s: Start/Stop | n: Next | q: Quit", (20, 145),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        # Gesture list
        cv2.putText(frame, f"Gesture {self.current_gesture_idx + 1}/{len(DatasetConfig.GESTURES)}", 
                   (20, 175), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        # Display hand ROI preview
        if hand_roi_display is not None:
            # Convert grayscale to BGR for display
            hand_roi_bgr = cv2.cvtColor(hand_roi_display, cv2.COLOR_GRAY2BGR)
            frame[10:210, w-220:w-20] = hand_roi_bgr
            cv2.rectangle(frame, (w-220, 10), (w-20, 210), (255, 255, 255), 2)
            cv2.putText(frame, "Hand ROI", (w-180, 230),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    def cleanup(self):
        """Clean up resources"""
        print("🧹 Cleaning up resources...")
        self.cap.release()
        cv2.destroyAllWindows()
        self.hands.close()
        print("✅ Cleanup complete!")
        
        # Print summary
        print("\n" + "="*70)
        print("COLLECTION SUMMARY")
        print("="*70)
        for gesture in DatasetConfig.GESTURES:
            count = self.count_existing_images(gesture)
            status = "✅ COMPLETE" if count >= DatasetConfig.TARGET_IMAGES_PER_GESTURE else "⚠️  INCOMPLETE"
            print(f"  {gesture:<20}: {count:>4} images {status}")
        print("="*70 + "\n")


def main():
    """Entry point"""
    print("\n" + "="*70)
    print("  GESTURA DATASET COLLECTION TOOL")
    print("="*70 + "\n")
    
    collector = GestureDataCollector()
    collector.run()


if __name__ == "__main__":
    main()
