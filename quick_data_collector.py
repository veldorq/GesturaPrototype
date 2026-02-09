"""
FAST GESTURE DATA COLLECTION (Turbo Mode)
==========================================
Faster alternative to collect_gesture_dataset.py

This captures images automatically (no need to press 's'):
- Just show the gesture and hold it steady
- Images are captured automatically every 0.05 seconds
- Much faster data collection (100 images in ~10 seconds per gesture)

Usage: python quick_data_collector.py
"""

import cv2
import mediapipe as mp
import numpy as np
import os
import time
from pathlib import Path

class QuickCollector:
    """Fast automated data collector"""
    
    def __init__(self):
        """Initialize"""
        self.dataset_root = "dataset"
        self.gestures = [
            'scroll_up',
            'scroll_down',
            'swipe_left',
            'swipe_right',
            'pinch_zoom',
            'thumb_down_close',
            'mute_toggle'
        ]
        
        self.target_per_gesture = 150  # Quick target
        self.capture_interval = 0.05  # 50ms = 20 images/second
        
        # Setup
        self.setup_folders()
        
        # MediaPipe
        self.mp_hands = mp.solutions.hands  # type: ignore
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils  # type: ignore
        
        # Camera
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        self.current_gesture_idx = 0
        self.last_capture_time = 0
        self.session_count = 0
        
        print("✅ Quick Collector Ready!")
    
    def setup_folders(self):
        """Create dataset folders"""
        Path(self.dataset_root).mkdir(exist_ok=True)
        for gesture in self.gestures:
            (Path(self.dataset_root) / gesture).mkdir(exist_ok=True)
    
    def count_images(self, gesture):
        """Count existing images"""
        path = Path(self.dataset_root) / gesture
        return len(list(path.glob("*.jpg")))
    
    def extract_hand_roi(self, frame, landmarks):
        """Extract hand ROI (same as main collector)"""
        h, w = frame.shape[:2]
        
        x_coords = [lm.x * w for lm in landmarks]
        y_coords = [lm.y * h for lm in landmarks]
        
        x_min, x_max = int(min(x_coords)), int(max(x_coords))
        y_min, y_max = int(min(y_coords)), int(max(y_coords))
        
        padding_x = int((x_max - x_min) * 0.2)
        padding_y = int((y_max - y_min) * 0.2)
        
        x_min = max(0, x_min - padding_x)
        y_min = max(0, y_min - padding_y)
        x_max = min(w, x_max + padding_x)
        y_max = min(h, y_max + padding_y)
        
        if x_max <= x_min or y_max <= y_min:
            return None, None
        
        roi = frame[y_min:y_max, x_min:x_max]
        
        if roi.size == 0:
            return None, None
        
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        normalized = cv2.equalizeHist(gray)
        resized = cv2.resize(normalized, (64, 64))
        
        return resized, (x_min, y_min, x_max, y_max)
    
    def run(self):
        """Main loop with auto-capture"""
        print("\n" + "="*70)
        print("  TURBO MODE DATA COLLECTION")
        print("="*70)
        print("\nAuto-capture enabled - just show your hand!")
        print("Images captured automatically every 50ms")
        print("\nGestures:")
        for i, g in enumerate(self.gestures):
            count = self.count_images(g)
            print(f"  {i+1}. {g:<20} ({count} images)")
        
        print(f"\nTarget: {self.target_per_gesture} images per gesture")
        print("\nControls:")
        print("  'n' - Next gesture")
        print("  'q' - Quit")
        print("\nStarting in 3 seconds...")
        time.sleep(3)
        
        try:
            while self.cap.isOpened():
                success, frame = self.cap.read()
                if not success:
                    continue
                
                frame = cv2.flip(frame, 1)
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.hands.process(rgb)
                
                current_gesture = self.gestures[self.current_gesture_idx]
                existing = self.count_images(current_gesture)
                total = existing + self.session_count
                
                # Auto-capture when hand detected
                if results.multi_hand_landmarks:
                    hand_lm = results.multi_hand_landmarks[0]
                    
                    # Draw landmarks
                    self.mp_draw.draw_landmarks(
                        frame, hand_lm, self.mp_hands.HAND_CONNECTIONS
                    )
                    
                    roi, bbox = self.extract_hand_roi(frame, hand_lm.landmark)
                    
                    if roi is not None and bbox is not None:
                        # Draw bbox
                        x1, y1, x2, y2 = bbox
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        
                        # AUTO-CAPTURE if enough time passed
                        now = time.time()
                        if total < self.target_per_gesture:
                            if now - self.last_capture_time >= self.capture_interval:
                                # Save
                                gesture_path = Path(self.dataset_root) / current_gesture
                                filename = f"{current_gesture}_{int(now*1000)}.jpg"
                                cv2.imwrite(str(gesture_path / filename), roi)
                                
                                self.session_count += 1
                                self.last_capture_time = now
                        
                        # Show ROI
                        roi_display = cv2.resize(roi, (150, 150))
                        frame[10:160, frame.shape[1]-160:frame.shape[1]-10] = cv2.cvtColor(roi_display, cv2.COLOR_GRAY2BGR)
                
                # Draw UI
                h, w = frame.shape[:2]
                
                # Status box
                cv2.rectangle(frame, (10, 10), (450, 150), (0, 0, 0), -1)
                cv2.rectangle(frame, (10, 10), (450, 150), (0, 255, 0), 2)
                
                cv2.putText(frame, f"Gesture: {current_gesture}", (20, 40),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                cv2.putText(frame, f"Captured: {total}/{self.target_per_gesture}", (20, 75),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                if total >= self.target_per_gesture:
                    cv2.putText(frame, "COMPLETE! Press 'n' for next", (20, 110),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                else:
                    cv2.putText(frame, "Show gesture - Auto-capturing...", (20, 110),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                
                # Progress bar
                progress = min(1.0, total / self.target_per_gesture)
                bar_width = 420
                cv2.rectangle(frame, (20, 120), (20 + int(bar_width * progress), 135), (0, 255, 0), -1)
                cv2.rectangle(frame, (20, 120), (20 + bar_width, 135), (255, 255, 255), 1)
                
                cv2.imshow('Quick Collector (Turbo Mode)', frame)
                
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('n'):
                    self.session_count = 0
                    self.current_gesture_idx = (self.current_gesture_idx + 1) % len(self.gestures)
                    print(f"\n➡️  Next: {self.gestures[self.current_gesture_idx]}")
        
        except KeyboardInterrupt:
            print("\n⚠️  Interrupted")
        
        finally:
            self.cap.release()
            cv2.destroyAllWindows()
            self.hands.close()
            
            # Summary
            print("\n" + "="*70)
            print("  COLLECTION SUMMARY")
            print("="*70)
            for gesture in self.gestures:
                count = self.count_images(gesture)
                status = "✓" if count >= self.target_per_gesture else "○"
                print(f"  {status} {gesture:<20} {count} images")
            print("="*70 + "\n")

if __name__ == "__main__":
    collector = QuickCollector()
    collector.run()
