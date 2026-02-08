"""
AccessAble - CONFLICT-FREE Gesture-Based Web Navigation System
Main application with mutually exclusive gesture detection.

CRITICAL IMPROVEMENTS:
1. Mutually exclusive gesture classification with confidence scores
2. State machine for temporal stability (NONE → CANDIDATE → CONFIRMED → COOLDOWN)
3. Guaranteed single gesture per frame
4. Action cooldown prevents rapid re-triggering
5. Proper separation: detection → classification → state → action
"""

import cv2
import time
import sys
from typing import Optional

# Import all modules
from camera import Webcam
from hand_tracking import HandDetector
from gesture_classification import MutuallyExclusiveGestureClassifier
from gesture_state_machine import GestureStateMachine, GestureState
from actions import BrowserActions
from ui import OverlayRenderer
from config import Constants, Settings


class AccessAbleConflictFree:
    """
    Main application controller with conflict-free gesture pipeline.
    
    PIPELINE ARCHITECTURE:
    1. Camera → Frame capture
    2. Hand Detector → Landmark extraction
    3. Gesture Classifier → Single gesture + confidence
    4. State Machine → Temporal stability + dwell time
    5. Settings → Gesture-to-action mapping
    6. Actions → Browser control
    7. UI → Visual feedback
    
    CONFLICT PREVENTION:
    - Classifier guarantees ONE gesture per frame
    - State machine blocks rapid re-triggering
    - COOLDOWN state prevents action spam
    - Dwell time prevents accidental triggers
    """
    
    def __init__(self):
        """Initialize all application components."""
        print("=" * 60)
        print("AccessAble - CONFLICT-FREE Edition")
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
        
        # Initialize CONFLICT-FREE gesture classifier
        print("Loading conflict-free gesture classifier...")
        self.gesture_classifier = MutuallyExclusiveGestureClassifier()
        
        # Initialize state machine
        print("Initializing gesture state machine...")
        self.state_machine = GestureStateMachine()
        
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
        self._print_instructions()
    
    def _print_instructions(self):
        """Print usage instructions."""
        print("=" * 60)
        print("CONTROLS:")
        print("=" * 60)
        print("  ESC   - Emergency stop (pause/resume)")
        print("  Q     - Quit application")
        print("  Space - Toggle pause")
        print()
        print("GESTURES (Mutually Exclusive):")
        print("=" * 60)
        print("  Open Palm    → Pause (neutral gesture)")
        print("  Fist         → Left Click")
        print("  Peace Sign   → Right Click")
        print("  Thumbs Up    → Scroll Up")
        print("  Thumbs Down  → Scroll Down")
        print("  Pointing     → (Reserved for future use)")
        print()
        print("STATE MACHINE:")
        print("=" * 60)
        print("  NONE      → No gesture detected")
        print("  CANDIDATE → Gesture detected, checking stability")
        print("  CONFIRMED → Gesture stable, action triggered")
        print("  COOLDOWN  → Blocking gestures after action")
        print()
        print("CONFLICT PREVENTION:")
        print("=" * 60)
        print("  • Only ONE gesture detected per frame")
        print("  • Confidence-based selection (highest wins)")
        print("  • Dwell time: Hold gesture for 1.5 seconds")
        print("  • Cooldown: 0.5s block after action")
        print("  • Stability: 80% consistency over 5 frames")
        print("=" * 60)
        print()
    
    def run(self) -> None:
        """
        Main application loop with conflict-free pipeline.
        """
        # Start camera
        if not self.camera.start():
            print("Error: Failed to start camera")
            return
        
        self.is_running = True
        
        print("Application started!")
        print("Ready! Show your hand to the camera...")
        print()
        
        last_frame_time = time.time()
        
        try:
            while self.is_running:
                frame_start = time.time()
                current_time = time.time()
                
                # STEP 1: Capture frame
                success, frame = self.camera.read_frame()
                if not success:
                    print("Warning: Failed to read frame")
                    continue
                
                # STEP 2: Process through conflict-free pipeline
                self._process_frame_conflict_free(frame, current_time)
                
                # Display frame
                cv2.imshow('AccessAble - Conflict-Free Mode', frame)
                
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
    
    def _process_frame_conflict_free(self, frame, current_time: float) -> None:
        """
        Process frame through the conflict-free pipeline.
        
        PIPELINE STEPS:
        1. Detect hand landmarks
        2. Classify into SINGLE gesture with confidence
        3. Update state machine (stability + dwell)
        4. Map gesture to action (if confirmed)
        5. Execute action (with cooldown)
        6. Render visual feedback
        
        Args:
            frame: Camera frame to process
            current_time: Current timestamp
        """
        # STEP 2: Detect hand landmarks
        hand_landmarks = self.hand_detector.detect(frame)
        
        # Initialize variables
        gesture_result = None
        action_name = None
        state_info = None
        
        if hand_landmarks is not None:
            # Draw hand landmarks
            self.hand_detector.draw_landmarks(frame, hand_landmarks)
            
            if not self.is_paused:
                # STEP 3: Classify gesture (MUTUALLY EXCLUSIVE)
                gesture_result = self.gesture_classifier.classify(hand_landmarks)
                
                # STEP 4: Update state machine
                should_trigger_action = self.state_machine.update(
                    gesture_result,
                    current_time
                )
                
                # STEP 5: Get gesture-to-action mapping
                if gesture_result.gesture_name:
                    action_name = self.settings.get_action_for_gesture(
                        gesture_result.gesture_name
                    )
                
                # STEP 6: Execute action if state machine confirms
                if should_trigger_action and action_name and action_name != 'none':
                    self._execute_action_safe(action_name, gesture_result.gesture_name)
                
                # Get state info for UI
                state_info = self.state_machine.get_state_info(current_time)
        else:
            # No hand detected - still need to update state machine
            if not self.is_paused:
                # Create an empty gesture result
                from gesture_classification import GestureResult
                empty_result = GestureResult(
                    gesture_name=None,
                    confidence=0.0,
                    reason="No hand detected"
                )
                self.state_machine.update(empty_result, current_time)
                state_info = self.state_machine.get_state_info(current_time)
        
        # STEP 7: Render UI overlay
        gesture_name = gesture_result.gesture_name if gesture_result else None
        confidence = gesture_result.confidence if gesture_result else 0.0
        dwell_progress = state_info.get('dwell_progress', 0.0) if state_info else 0.0
        
        self.overlay.render_info_panel(
            frame,
            gesture_name,
            action_name,
            confidence,
            dwell_progress,
            self.is_paused,
            state_info
        )
        
        # Add help text
        self.overlay.render_help_text(frame)
        
        # Add FPS counter
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
        
        # Add conflict-free badge
        cv2.putText(
            frame,
            "CONFLICT-FREE",
            (frame.shape[1] - 220, 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            Constants.COLOR_PRIMARY,
            2
        )
    
    def _execute_action_safe(self, action_name: str, gesture_name: str) -> None:
        """
        Execute action with safety checks and logging.
        
        Args:
            action_name: Action to execute
            gesture_name: Gesture that triggered it
        """
        try:
            success = self.actions.execute(action_name)
            if success:
                print(f"✓ [{gesture_name}] → {action_name}")
            else:
                print(f"✗ [{gesture_name}] → {action_name} FAILED")
        except Exception as e:
            print(f"✗ Error executing {action_name}: {e}")
    
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
            self.state_machine.reset()
        
        # Space - Toggle pause
        elif key == ord(' '):
            self.is_paused = not self.is_paused
            status = "PAUSED" if self.is_paused else "RESUMED"
            print(f"\n>>> {status} <<<\n")
            self.state_machine.reset()
        
        # D - Debug info
        elif key == ord('d') or key == ord('D'):
            self._print_debug_info()
    
    def _print_debug_info(self) -> None:
        """Print debug information."""
        print("\n" + "=" * 60)
        print("DEBUG INFO")
        print("=" * 60)
        state_info = self.state_machine.get_state_info(time.time())
        for key, value in state_info.items():
            print(f"{key}: {value}")
        print("=" * 60 + "\n")
    
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
        app = AccessAbleConflictFree()
        app.run()
    except Exception as e:
        print(f"\nFatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
