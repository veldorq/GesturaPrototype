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
from config import Constants, Settings, ConfigValidator, ConfigValidationError
from utils import setup_logging, get_logger, PerformanceMetrics
from voice_control import VoiceControllerClass, VoiceCommand

# Initialize logging
setup_logging(log_level="INFO", enable_file_logging=True)
logger = get_logger(__name__)


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
        logger.info("=" * 60)
        logger.info("AccessAble - Gesture-Based Web Navigation")
        logger.info("=" * 60)
        
        try:
            # Validate configuration
            logger.info("Validating configuration...")
            warnings = ConfigValidator.validate_constants(Constants)
            for warning in warnings:
                logger.warning(f"Config warning: {warning}")
            
            # Load settings
            self.settings = Settings()
            
            # Initialize performance metrics
            self.metrics = PerformanceMetrics()
            logger.info("Performance monitoring enabled")
            
            # Initialize camera
            logger.info("Initializing camera...")
            self.camera = Webcam()
            
            # Initialize hand detector
            logger.info("Initializing hand detection...")
            self.hand_detector = HandDetector(
                use_smoothing=Constants.USE_SMOOTHING,
                smoothing_type=Constants.SMOOTHING_TYPE
            )
            
            # Initialize gesture system
            logger.info("Loading gesture library...")
            self.gesture_library = GestureLibrary()
            self.gesture_recognizer = GestureRecognizer(self.gesture_library)
            
            # Initialize action executor
            logger.info("Initializing action system...")
            self.actions = BrowserActions()
            
            # Initialize UI overlay
            logger.info("Initializing UI...")
            self.overlay = OverlayRenderer()
            
            # Initialize voice control (optional)
            self.voice_controller = None
            if Constants.ENABLE_VOICE_CONTROL:
                logger.info("Initializing voice control...")
                try:
                    self.voice_controller = VoiceControllerClass(
                        language=Constants.VOICE_LANGUAGE
                    )
                    if self.voice_controller.start_listening():
                        logger.info("Voice control enabled")
                    else:
                        self.voice_controller = None
                        logger.warning("Voice control initialization failed")
                except Exception as e:
                    logger.warning(f"Voice control unavailable: {e}")
                    self.voice_controller = None
            else:
                logger.info("Voice control disabled in config")
            
            # Application state
            self.is_running = False
            self.is_paused = False
            
            logger.info("Initialization complete!")
            
        except ConfigValidationError as e:
            logger.error(f"Configuration validation failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Initialization failed: {e}", exc_info=True)
            raise
    
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
        try:
            # Start camera
            if not self.camera.start():
                logger.error("Failed to start camera")
                return
            
            self.is_running = True
            
            logger.info("Application started!")
            logger.info("Controls: ESC/Space=Pause, Q=Quit")
            logger.info("Default Gestures: Open Palm=Pause, Fist=Left Click, Peace=Right Click")
            logger.info("Ready! Show your hand to the camera...")
            
            while self.is_running:
                frame_start = time.time()
                
                try:
                    # Capture frame
                    success, frame = self.camera.read_frame()
                    if not success:
                        logger.warning("Failed to read frame")
                        continue
                    
                    # Process frame
                    self._process_frame(frame)
                    
                    # Process voice commands if enabled
                    if self.voice_controller:
                        self._process_voice_commands()
                    
                    # Display frame
                    cv2.imshow('AccessAble - Gesture Navigation', frame)
                    
                    # Handle keyboard input
                    key = cv2.waitKey(1) & 0xFF
                    self._handle_keyboard(key)
                    
                    # Record frame metrics
                    frame_time = time.time() - frame_start
                    self.metrics.record_frame_time(frame_time)
                    
                except Exception as e:
                    logger.error(f"Error processing frame: {e}", exc_info=True)
                    continue
                    
        except KeyboardInterrupt:
            logger.info("Interrupted by user")
        except Exception as e:
            logger.error(f"Fatal error in main loop: {e}", exc_info=True)
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
        detection_start = time.time()
        hand_landmarks = self.hand_detector.detect(frame)
        detection_time = time.time() - detection_start
        self.metrics.record_detection_time(detection_time, hand_landmarks is not None)
        
        gesture_name: Optional[str] = None
        action_name: Optional[str] = None
        confidence: float = 0.0
        dwell_progress: float = 0.0
        
        if hand_landmarks is not None:
            # Draw hand landmarks on frame
            self.hand_detector.draw_landmarks(frame, hand_landmarks)
            
            # Recognize gesture
            if not self.is_paused:
                recognition_start = time.time()
                gesture_name, confidence, should_activate = \
                    self.gesture_recognizer.recognize(hand_landmarks, current_time)
                recognition_time = time.time() - recognition_start
                self.metrics.record_recognition_time(recognition_time, gesture_name is not None)
                
                if gesture_name:
                    # Get mapped action
                    action_name = self.settings.get_action_for_gesture(gesture_name)
                    
                    # Check for pause gesture
                    if gesture_name == 'open_palm' and action_name == 'none':
                        # Pause gesture detected - don't execute action
                        pass
                    elif should_activate and action_name:
                        # Execute action
                        try:
                            success = self.actions.execute(action_name)
                            if success:
                                self.metrics.record_action_execution()
                                logger.debug(f"Executed action: {action_name}")
                        except Exception as e:
                            logger.error(f"Failed to execute action {action_name}: {e}")
                
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
        
        # Add FPS counter and metrics (bottom right)
        fps = self.metrics.get_fps()
        fps_text = f"FPS: {int(fps)}"
        cv2.putText(
            frame,
            fps_text,
            (frame.shape[1] - 120, frame.shape[0] - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            Constants.COLOR_TEXT,
            2
        )
    
    def _process_voice_commands(self) -> None:
        """
        Process any pending voice commands.
        Executes corresponding actions for recognized voice commands.
        """
        while self.voice_controller.has_pending_commands():
            command_data = self.voice_controller.get_command()
            if not command_data:
                break
            
            command, phrase = command_data
            logger.info(f"Voice command: {command.value} ('{phrase}')")
            
            # Handle voice commands
            if command == VoiceCommand.CLICK:
                self.actions.execute('left_click')
            elif command == VoiceCommand.GO_BACK:
                self.actions.execute('browser_back')
            elif command == VoiceCommand.GO_FORWARD:
                self.actions.execute('browser_forward')
            elif command == VoiceCommand.NEW_TAB:
                self.actions.execute('new_tab')
            elif command == VoiceCommand.CLOSE_TAB:
                self.actions.execute('close_tab')
            elif command == VoiceCommand.REFRESH:
                self.actions.execute('refresh')
            elif command == VoiceCommand.DISABLE_VOICE:
                self.voice_controller.stop_listening()
                logger.info("Voice control disabled by voice command")
            elif command == VoiceCommand.HELP:
                logger.info("Voice Commands: click, go back, go forward, new tab, close tab, refresh, disable voice")
    
    def _handle_keyboard(self, key: int) -> None:
        """
        Handle keyboard input for application control.
        
        Args:
            key: Key code from cv2.waitKey()
        """
        # Q - Quit
        if key == ord('q') or key == ord('Q'):
            logger.info("Quit requested by user")
            self.is_running = False
        
        # ESC - Emergency stop / Toggle pause
        elif key == 27:  # ESC key
            self.is_paused = not self.is_paused
            status = "PAUSED" if self.is_paused else "RESUMED"
            logger.info(f">>> {status} <<<")
            self.gesture_recognizer.reset()
        
        # Space - Toggle pause
        elif key == ord(' '):
            self.is_paused = not self.is_paused
            status = "PAUSED" if self.is_paused else "RESUMED"
            logger.info(f">>> {status} <<<")
            self.gesture_recognizer.reset()
        
        # M - Print metrics
        elif key == ord('m') or key == ord('M'):
            metrics = self.metrics.get_summary()
            logger.info("=== Performance Metrics ===")
            for key, value in metrics.items():
                logger.info(f"{key}: {value:.2f}")
        
        # V - Toggle voice control
        elif key == ord('v') or key == ord('V'):
            if self.voice_controller:
                if self.voice_controller.is_listening:
                    self.voice_controller.stop_listening()
                    logger.info("Voice control disabled")
                else:
                    if self.voice_controller.start_listening():
                        logger.info("Voice control enabled")
            else:
                logger.warning("Voice control not available")
    
    def _cleanup(self) -> None:
        """Clean up resources and shut down gracefully."""
        logger.info("Shutting down...")
        
        try:
            # Print final metrics
            metrics = self.metrics.get_summary()
            logger.info("=== Final Performance Metrics ===")
            for key, value in metrics.items():
                logger.info(f"{key}: {value:.2f}")
            
            # Release camera
            self.camera.release()
            
            # Release hand detector
            self.hand_detector.release()
            
            # Release voice controller
            if self.voice_controller:
                self.voice_controller.stop_listening()
            
            # Close all windows
            cv2.destroyAllWindows()
            
            # Save configuration
            self.settings.save()
            
            logger.info("Cleanup complete. Goodbye!")
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}", exc_info=True)


def main():
    """Application entry point."""
    try:
        app = AccessAble()
        app.run()
    except ConfigValidationError as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.critical(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
