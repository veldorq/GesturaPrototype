"""
AccessAble - Gesture-Based Web Navigation System
Main application orchestrator that integrates all modules.

A production-quality assistive technology for users with partial motor impairments.
"""

import cv2
import time
import sys
from typing import Optional

# Import all modules
from camera import Webcam
from hand_tracking import HandDetector
from gestures import GestureLibrary, GestureRecognizer
from actions import BrowserActions
from ui import OverlayRenderer
from config import Constants, Settings


class AccessAble:
    """
    Main application controller for AccessAble.
    
    Orchestrates the entire gesture-based navigation pipeline:
    1. Camera capture
    2. Hand detection
    3. Gesture recognition with stabilization
    4. Action execution
    5. Visual feedback
    """
    
    def __init__(self):
        """Initialize all application components."""
        print("=" * 60)
        print("AccessAble - Gesture-Based Web Navigation")
        print("=" * 60)
        print()
        
        # Load configuration
        self.settings = Settings()
        
        # Initialize camera
        print("Initializing camera...")
        self.camera = Webcam()
        
        # Initialize hand detector
        print("Initializing hand detection...")
        self.hand_detector = HandDetector()
        
        # Initialize gesture system
        print("Loading gesture library...")
        self.gesture_library = GestureLibrary()
        self.gesture_recognizer = GestureRecognizer(self.gesture_library)
        
        # Initialize action executor
        print("Initializing action system...")
        self.actions = BrowserActions()
        
        # Initialize UI overlay
        print("Initializing UI...")
        self.overlay = OverlayRenderer()
        
        # Application state
        self.is_running = False
        self.is_paused = False
        
        # Performance tracking
        self.fps = 0.0
        self.frame_times = []
        
        print("\nInitialization complete!")
        print()
    
    def run(self) -> None:
        """
        Main application loop.
        
        Continuously:
        1. Captures frames from camera
        2. Detects hand landmarks
        3. Recognizes gestures
        4. Executes actions
        5. Renders visual feedback
        """
        # Start camera
        if not self.camera.start():
            print("Error: Failed to start camera")
            return
        
        self.is_running = True
        
        print("Application started!")
        print()
        print("Controls:")
        print("  ESC   - Emergency stop (pause/resume)")
        print("  Q     - Quit application")
        print("  Space - Toggle pause")
        print()
        print("Default Gestures:")
        print("  Open Palm    - Pause (neutral)")
        print("  Fist         - Left Click")
        print("  Peace Sign   - Right Click")
        print("  Thumbs Up    - Scroll Up")
        print("  Thumbs Down  - Scroll Down")
        print()
        print("Ready! Show your hand to the camera...")
        print()
        
        last_frame_time = time.time()
        
        try:
            while self.is_running:
                frame_start = time.time()
                
                # Capture frame
                success, frame = self.camera.read_frame()
                if not success:
                    print("Warning: Failed to read frame")
                    continue
                
                # Process frame
                self._process_frame(frame)
                
                # Display frame
                cv2.imshow('AccessAble - Gesture Navigation', frame)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                self._handle_keyboard(key)
                
                # Calculate FPS
                frame_time = time.time() - frame_start
                self.frame_times.append(frame_time)
                if len(self.frame_times) > 30:
                    self.frame_times.pop(0)
                
                if self.frame_times:
                    avg_frame_time = sum(self.frame_times) / len(self.frame_times)
                    self.fps = 1.0 / avg_frame_time if avg_frame_time > 0 else 0.0
                
        except KeyboardInterrupt:
            print("\nInterrupted by user")
        
        finally:
            self._cleanup()
    
    def _process_frame(self, frame) -> None:
        """
        Process a single frame through the entire pipeline.
        
        Args:
            frame: Camera frame to process
        """
        current_time = time.time()
        
        # Detect hand landmarks
        hand_landmarks = self.hand_detector.detect(frame)
        
        gesture_name: Optional[str] = None
        action_name: Optional[str] = None
        confidence: float = 0.0
        dwell_progress: float = 0.0
        
        if hand_landmarks is not None:
            # Draw hand landmarks on frame
            self.hand_detector.draw_landmarks(frame, hand_landmarks)
            
            # Recognize gesture
            if not self.is_paused:
                gesture_name, confidence, should_activate = \
                    self.gesture_recognizer.recognize(hand_landmarks, current_time)
                
                if gesture_name:
                    # Get mapped action
                    action_name = self.settings.get_action_for_gesture(gesture_name)
                    
                    # Check for pause gesture
                    if gesture_name == 'open_palm' and action_name == 'none':
                        # Pause gesture detected - don't execute action
                        pass
                    elif should_activate and action_name:
                        # Execute action
                        success = self.actions.execute(action_name)
                        if success:
                            # Visual feedback for action execution
                            # (Could add notification here)
                            pass
                
                # Get dwell progress for UI
                dwell_progress = self.gesture_recognizer.get_dwell_progress()
        
        # Render UI overlay
        self.overlay.render_info_panel(
            frame,
            gesture_name,
            action_name,
            confidence,
            dwell_progress,
            self.is_paused
        )
        
        # Add help text
        self.overlay.render_help_text(frame)
        
        # Add FPS counter (bottom right)
        fps_text = f"FPS: {int(self.fps)}"
        cv2.putText(
            frame,
            fps_text,
            (frame.shape[1] - 120, frame.shape[0] - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            Constants.COLOR_TEXT,
            2
        )
    
    def _handle_keyboard(self, key: int) -> None:
        """
        Handle keyboard input for application control.
        
        Args:
            key: Key code from cv2.waitKey()
        """
        # Q - Quit
        if key == ord('q') or key == ord('Q'):
            print("\nQuitting...")
            self.is_running = False
        
        # ESC - Emergency stop / Toggle pause
        elif key == 27:  # ESC key
            self.is_paused = not self.is_paused
            status = "PAUSED" if self.is_paused else "RESUMED"
            print(f"\n>>> {status} <<<\n")
            self.gesture_recognizer.reset()
        
        # Space - Toggle pause
        elif key == ord(' '):
            self.is_paused = not self.is_paused
            status = "PAUSED" if self.is_paused else "RESUMED"
            print(f"\n>>> {status} <<<\n")
            self.gesture_recognizer.reset()
    
    def _cleanup(self) -> None:
        """Clean up resources and shut down gracefully."""
        print("\nShutting down...")
        
        # Release camera
        self.camera.release()
        
        # Release hand detector
        self.hand_detector.release()
        
        # Close all windows
        cv2.destroyAllWindows()
        
        # Save configuration
        self.settings.save()
        
        print("Cleanup complete. Goodbye!")


def main():
    """Application entry point."""
    try:
        app = AccessAble()
        app.run()
    except Exception as e:
        print(f"\nFatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
