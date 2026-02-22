"""
Gesture Engine Main Integration Module

Orchestrates all components of the Gestura 2.0 gesture recognition system:
- Two-hand tracking with MediaPipe
- Real-time gesture classification
- Custom gesture training
- Motion smoothing (moving average, exponential, Kalman)
- Voice command integration
- Unified command execution

Author: Gestura Development Team
Version: 2.0.0

INTEGRATION INSTRUCTIONS:
========================

1. Install Dependencies:
   pip install opencv-python mediapipe numpy pyautogui SpeechRecognition pyaudio

2. Configure System:
   Edit gesture_engine/config.py to customize:
   - Camera settings (index, resolution, FPS)
   - Smoothing parameters (window size, alpha, Kalman noise)
   - Recognition thresholds (confidence, hold time, cooldown)
   - Voice commands and action mappings

3. Run Gesture Engine:
   python gesture_engine/main.py

4. Keyboard Controls:
   - 'q': Quit
   - 's': Toggle smoothing
   - 'v': Toggle voice control
   - 't': Enter training mode
   - 'r': Reset smoothing filters
   - 'h': Show help
   - 'p': Pause/resume gesture recognition
   - 'f': Toggle FPS display

5. Training Mode:
   - Press 't' to enter training mode
   - Follow on-screen instructions to record custom gestures
   - Trained gestures saved to config/trained_gestures.json

6. Integration with Existing Gestura:
   - Import GestureEngine class
   - Initialize: engine = GestureEngine()
   - Process frames: engine.process_frame(camera_frame)
   - Access results: engine.get_last_gesture()
   
Example:
    from gesture_engine.main import GestureEngine
    
    engine = GestureEngine(use_smoothing=True, enable_voice=True)
    engine.start()
    
    # Engine runs in background, access results as needed
    gesture = engine.get_last_gesture()
    if gesture:
        print(f"Detected: {gesture.gesture.value} ({gesture.confidence:.2f})")
"""

import cv2
import time
import numpy as np
import sys
from typing import Optional, Dict
from dataclasses import dataclass
from enum import Enum

# Import gesture engine modules
from gesture_engine.config import CONFIG
from gesture_engine.hand_tracker import TwoHandTracker, HandData, HandLabel
from gesture_engine.gesture_classifier import GestureClassifier, GestureResult, GestureType
from gesture_engine.gesture_trainer import GestureTrainer
# VoiceController is new Vosk-based system - VoiceControllerClass/VoiceCommand no longer exist
from gesture_engine.command_executor import CommandExecutor


class EngineMode(Enum):
    """Operating modes for gesture engine."""
    RUNNING = "running"
    PAUSED = "paused"
    TRAINING = "training"


@dataclass
class EngineState:
    """Current state of gesture engine."""
    mode: EngineMode
    smoothing_enabled: bool
    voice_enabled: bool
    fps: float
    frame_count: int
    gestures_detected: int
    voice_commands_received: int


class GestureEngine:
    """
    Main gesture engine coordinator.
    
    Integrates all subsystems for production-ready gesture control.
    """
    
    def __init__(
        self,
        camera_index: int = 0,
        use_smoothing: bool = True,
        smoothing_type: str = "exponential",
        enable_voice: bool = True,
        enable_gui: bool = True
    ):
        """
        Initialize gesture engine.
        
        Args:
            camera_index: Camera device index (default: 0)
            use_smoothing: Enable motion smoothing (default: True)
            smoothing_type: Type of smoothing ("moving_avg", "exponential", "kalman")
            enable_voice: Enable voice control (default: True)
            enable_gui: Show GUI window (default: True)
        """
        print("=" * 60)
        print("GESTURA 2.0 - GESTURE ENGINE")
        print("=" * 60)
        
        self.enable_gui = enable_gui
        
        # Initialize subsystems
        print("\n[1/6] Initializing hand tracker...")
        self.tracker = TwoHandTracker(
            use_smoothing=use_smoothing,
            smoothing_type=smoothing_type
        )
        
        print("[2/6] Initializing gesture classifier...")
        self.classifier = GestureClassifier()
        
        print("[3/6] Initializing gesture trainer...")
        self.trainer = GestureTrainer()
        
        print("[4/6] Initializing command executor...")
        self.executor = CommandExecutor()
        
        print("[5/6] Voice controller disabled (replaced with new Vosk system in main_vosk.py)")
        self.voice_controller = None
        # Old voice controller removed - use gesture_engine/main_vosk.py instead
        # if enable_voice:
        #     try:
        #         self.voice_controller = VoiceControllerClass(
        #             command_callback=self._on_voice_command
        #         )
        #     except Exception as e:
        #         print(f"Voice control initialization failed: {e}")
        #         self.voice_controller = None
        
        print("[6/6] Initializing camera...")
        self.cap = cv2.VideoCapture(camera_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, CONFIG.hand_tracking.frame_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CONFIG.hand_tracking.frame_height)
        self.cap.set(cv2.CAP_PROP_FPS, CONFIG.hand_tracking.target_fps)
        
        # Engine state
        self.state = EngineState(
            mode=EngineMode.RUNNING,
            smoothing_enabled=use_smoothing,
            voice_enabled=enable_voice and self.voice_controller is not None,
            fps=0.0,
            frame_count=0,
            gestures_detected=0,
            voice_commands_received=0
        )
        
        # Runtime variables
        self.last_gesture: Optional[GestureResult] = None
        self.last_frame_time = time.time()
        self.frame_times = []
        self.show_fps = CONFIG.performance.show_fps
        
        # Training state
        self.training_hand: Optional[HandLabel] = None
        self.training_gesture_name: Optional[str] = None
        
        print("\n✓ Gesture Engine initialized successfully!")
        print("\nPress 'h' for help\n")
    
    def start(self) -> None:
        """Start the gesture engine main loop."""
        # Start voice listening if enabled
        if self.state.voice_enabled and self.voice_controller:
            self.voice_controller.start_listening()
        
        print("Engine started. Processing frames...")
        
        try:
            self._main_loop()
        except KeyboardInterrupt:
            print("\nInterrupted by user")
        finally:
            self.stop()
    
    def _main_loop(self) -> None:
        """Main processing loop."""
        while self.cap.isOpened():
            # Read frame
            success, frame = self.cap.read()
            if not success:
                print("Failed to read camera frame")
                continue
            
            # Process frame
            frame = self.process_frame(frame)
            
            # Update FPS
            self._update_fps()
            
            # Display
            if self.enable_gui:
                cv2.imshow("Gestura 2.0 - Gesture Engine", frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            if not self._handle_key(key):
                break
    
    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Process a single frame through the gesture pipeline.
        
        Args:
            frame: Input BGR frame from camera
            
        Returns:
            Annotated frame with visualizations
        """
        self.state.frame_count += 1
        
        # Track hands
        annotated_frame, detected_hands = self.tracker.process_frame(frame)
        
        # Extract hand data
        left_hand = detected_hands.get(HandLabel.LEFT)
        right_hand = detected_hands.get(HandLabel.RIGHT)
        
        # Handle different modes
        if self.state.mode == EngineMode.RUNNING:
            # Classify gesture
            gesture_result = self.classifier.classify(left_hand, right_hand)
            
            if gesture_result:
                self.last_gesture = gesture_result
                self.state.gestures_detected += 1
                
                # Execute gesture action
                action_result = self.executor.execute_gesture(gesture_result.gesture)
                
                # Draw gesture on frame
                if action_result:
                    self._draw_gesture_feedback(
                        annotated_frame,
                        gesture_result.gesture.value,
                        gesture_result.confidence
                    )
            
            # Check for custom trained gestures
            if right_hand:
                match = self.trainer.match_gesture(right_hand, HandLabel.RIGHT)
                if match:
                    gesture_name, confidence = match
                    self._draw_trained_gesture_feedback(
                        annotated_frame,
                        gesture_name,
                        confidence
                    )
        
        elif self.state.mode == EngineMode.TRAINING:
            # Training mode
            if self.training_hand == HandLabel.LEFT and left_hand:
                complete, collected, target = self.trainer.record_sample(
                    left_hand, 
                    self.state.frame_count
                )
                self._draw_training_progress(annotated_frame, collected, target, complete)
                
                if complete:
                    self.state.mode = EngineMode.RUNNING
                    self.training_hand = None
                    self.training_gesture_name = None
            
            elif self.training_hand == HandLabel.RIGHT and right_hand:
                complete, collected, target = self.trainer.record_sample(
                    right_hand,
                    self.state.frame_count
                )
                self._draw_training_progress(annotated_frame, collected, target, complete)
                
                if complete:
                    self.state.mode = EngineMode.RUNNING
                    self.training_hand = None
                    self.training_gesture_name = None
        
        # Draw UI overlays
        self._draw_ui(annotated_frame)
        
        return annotated_frame
    
    def _on_voice_command(self, command: str, phrase: str) -> None:  # type: ignore
        """
        Callback for voice commands.
        
        Args:
            command: Recognized voice command (string, not enum anymore)
            phrase: Original phrase spoken
        """
        self.state.voice_commands_received += 1
        
        # Execute voice command
        if self.state.mode == EngineMode.RUNNING:
            action_result = self.executor.execute_voice_command(command)
            
            # Handle special mode switches
            if command == "disable_voice":  # Changed from VoiceCommand enum
                if self.voice_controller:
                    # voice_controller.stop_listening() method may not exist in new system
                    self.state.voice_enabled = False
                    print("Voice control disabled")
    
    def _handle_key(self, key: int) -> bool:
        """
        Handle keyboard input.
        
        Args:
            key: Key code
            
        Returns:
            True to continue, False to quit
        """
        if key == ord('q'):
            return False
        
        elif key == ord('s'):
            # Toggle smoothing
            self.state.smoothing_enabled = not self.state.smoothing_enabled
            self.tracker.use_smoothing = self.state.smoothing_enabled
            print(f"Smoothing: {'ON' if self.state.smoothing_enabled else 'OFF'}")
        
        elif key == ord('v'):
            # Toggle voice
            if self.voice_controller:
                if self.state.voice_enabled:
                    self.voice_controller.stop_listening()
                    self.state.voice_enabled = False
                    print("Voice control disabled")
                else:
                    self.voice_controller.start_listening()
                    self.state.voice_enabled = True
                    print("Voice control enabled")
        
        elif key == ord('t'):
            # Enter training mode
            self._enter_training_mode()
        
        elif key == ord('r'):
            # Reset smoothing
            self.tracker.reset_smoothing()
            print("Smoothing filters reset")
        
        elif key == ord('p'):
            # Pause/resume
            if self.state.mode == EngineMode.RUNNING:
                self.state.mode = EngineMode.PAUSED
                print("Paused")
            elif self.state.mode == EngineMode.PAUSED:
                self.state.mode = EngineMode.RUNNING
                print("Resumed")
        
        elif key == ord('f'):
            # Toggle FPS display
            self.show_fps = not self.show_fps
        
        elif key == ord('h'):
            # Show help
            self._show_help()
        
        return True
    
    def _enter_training_mode(self) -> None:
        """Enter gesture training mode."""
        print("\n" + "=" * 60)
        print("TRAINING MODE")
        print("=" * 60)
        
        # Get gesture name
        gesture_name = input("Enter gesture name: ").strip()
        if not gesture_name:
            print("Cancelled")
            return
        
        # Get hand selection
        hand_choice = input("Which hand? (L/R): ").strip().upper()
        if hand_choice not in ['L', 'R']:
            print("Invalid selection")
            return
        
        hand_label = HandLabel.LEFT if hand_choice == 'L' else HandLabel.RIGHT
        
        # Start recording
        self.trainer.start_recording(gesture_name, hand_label)
        self.state.mode = EngineMode.TRAINING
        self.training_hand = hand_label
        self.training_gesture_name = gesture_name
        
        print(f"\nPerform the '{gesture_name}' gesture repeatedly")
        print("Hold each pose for ~0.5 seconds")
    
    def _draw_gesture_feedback(self, frame: np.ndarray, gesture: str, confidence: float) -> None:
        """Draw gesture detection feedback on frame."""
        text = f"{gesture}: {confidence:.2f}"
        cv2.putText(
            frame, text, (10, 120),
            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2
        )
    
    def _draw_trained_gesture_feedback(self, frame: np.ndarray, gesture: str, confidence: float) -> None:
        """Draw trained gesture match feedback."""
        text = f"Custom: {gesture} ({confidence:.2f})"
        cv2.putText(
            frame, text, (10, 160),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 165, 0), 2
        )
    
    def _draw_training_progress(self, frame: np.ndarray, collected: int, target: int, complete: bool) -> None:
        """Draw training progress bar."""
        if complete:
            text = "Training complete!"
            color = (0, 255, 0)
        else:
            text = f"Recording: {collected}/{target}"
            color = (0, 165, 255)
        
        cv2.putText(
            frame, text, (10, frame.shape[0] - 20),
            cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 2
        )
        
        # Progress bar
        bar_width = 400
        bar_height = 30
        x, y = 10, frame.shape[0] - 70
        
        # Background
        cv2.rectangle(frame, (x, y), (x + bar_width, y + bar_height), (50, 50, 50), -1)
        
        # Progress
        progress = min(collected / target, 1.0)
        cv2.rectangle(
            frame, (x, y),
            (x + int(bar_width * progress), y + bar_height),
            color, -1
        )
    
    def _draw_ui(self, frame: np.ndarray) -> None:
        """Draw UI overlays."""
        # Mode
        mode_text = f"Mode: {self.state.mode.value.upper()}"
        cv2.putText(frame, mode_text, (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # FPS
        if self.show_fps:
            fps_text = f"FPS: {self.state.fps:.1f}"
            cv2.putText(frame, fps_text, (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Status indicators
        y_offset = 90
        
        if self.state.smoothing_enabled:
            cv2.putText(frame, "Smoothing: ON", (frame.shape[1] - 200, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        if self.state.voice_enabled:
            cv2.putText(frame, "Voice: ON", (frame.shape[1] - 200, y_offset + 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    
    def _update_fps(self) -> None:
        """Update FPS calculation."""
        current_time = time.time()
        frame_time = current_time - self.last_frame_time
        self.last_frame_time = current_time
        
        self.frame_times.append(frame_time)
        if len(self.frame_times) > 30:
            self.frame_times.pop(0)
        
        if self.frame_times:
            avg_frame_time = sum(self.frame_times) / len(self.frame_times)
            self.state.fps = 1.0 / avg_frame_time if avg_frame_time > 0 else 0.0
    
    def _show_help(self) -> None:
        """Display help information."""
        print("\n" + "=" * 60)
        print("KEYBOARD CONTROLS")
        print("=" * 60)
        print("q - Quit")
        print("s - Toggle smoothing")
        print("v - Toggle voice control")
        print("t - Enter training mode")
        print("r - Reset smoothing filters")
        print("p - Pause/resume gesture recognition")
        print("f - Toggle FPS display")
        print("h - Show this help")
        print("=" * 60 + "\n")
    
    def stop(self) -> None:
        """Stop gesture engine and release resources."""
        print("\nStopping gesture engine...")
        
        if self.voice_controller and self.state.voice_enabled:
            self.voice_controller.stop_listening()
        
        self.cap.release()
        cv2.destroyAllWindows()
        self.tracker.release()
        
        # Print statistics
        print("\n" + "=" * 60)
        print("SESSION STATISTICS")
        print("=" * 60)
        print(f"Frames processed: {self.state.frame_count}")
        print(f"Gestures detected: {self.state.gestures_detected}")
        print(f"Voice commands: {self.state.voice_commands_received}")
        print(f"Average FPS: {self.state.fps:.1f}")
        print(f"Actions executed: {self.executor.actions_executed}")
        print("=" * 60 + "\n")
    
    def get_last_gesture(self) -> Optional[GestureResult]:
        """Get the most recently detected gesture."""
        return self.last_gesture
    
    def get_state(self) -> EngineState:
        """Get current engine state."""
        return self.state


def main():
    """Main entry point."""
    # Create and start engine
    engine = GestureEngine(
        camera_index=CONFIG.hand_tracking.camera_index,
        use_smoothing=True,
        smoothing_type="exponential",
        enable_voice=True,
        enable_gui=True
    )
    
    engine.start()


if __name__ == "__main__":
    main()
