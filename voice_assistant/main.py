"""
Gestura Main - Integrated Gesture + Voice Control

Demonstrates concurrent execution of gesture recognition and voice control
using shared thread-safe state for seamless interaction.

Author: Gestura Development Team
Version: 3.0.0

Usage:
    python main.py

Requirements:
    pip install opencv-python mediapipe speech_recognition pyautogui pyttsx3 vosk sounddevice
"""

import cv2
import time
import threading
from typing import Optional

# Import voice assistant modules
from voice_assistant import VoiceController, VoiceCommandExecutor, VoiceConfig

# Placeholder for gesture system (replace with your actual implementation)
class GestureSystem:
    """
    Placeholder for your existing gesture recognition system.
    Replace this with your actual MediaPipe + OpenCV gesture code.
    """
    
    def __init__(self, config: VoiceConfig):
        """Initialize gesture recognition system."""
        self.config = config
        self.camera: Optional[cv2.VideoCapture] = None
        self.is_running = False
        
        print("✅ Gesture system initialized")
    
    def start(self) -> bool:
        """Start gesture recognition."""
        try:
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                print("❌ Failed to open camera")
                return False
            
            self.is_running = True
            print("📹 Gesture recognition started")
            return True
            
        except Exception as e:
            print(f"❌ Gesture system error: {e}")
            return False
    
    def stop(self) -> None:
        """Stop gesture recognition."""
        self.is_running = False
        if self.camera:
            self.camera.release()
        cv2.destroyAllWindows()
        print("📹 Gesture recognition stopped")
    
    def process_frame(self) -> bool:
        """
        Process one frame of gesture recognition.
        
        Returns:
            True if should continue, False to stop
        """
        if not self.camera:
            return False
        
        # Check if system should continue running
        if not self.config.is_system_running():
            return False
        
        # Check if gestures are paused by voice command
        if not self.config.is_gesture_active():
            # Display "PAUSED" message but keep capturing
            ret, frame = self.camera.read()
            if ret:
                cv2.putText(
                    frame,
                    "GESTURES PAUSED (Voice Control Active)",
                    (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.0,
                    (0, 0, 255),
                    2
                )
                cv2.imshow("Gestura", frame)
            
            # Check for quit key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                return False
            
            time.sleep(0.03)  # ~30 FPS when paused
            return True
        
        # ========================================
        # YOUR GESTURE RECOGNITION CODE HERE
        # ========================================
        # This is where you would:
        # 1. Read frame from camera
        # 2. Detect hands with MediaPipe
        # 3. Recognize gestures
        # 4. Execute actions
        # ========================================
        
        ret, frame = self.camera.read()
        if not ret:
            return False
        
        # Example: Display frame
        cv2.putText(
            frame,
            f"Gestura Active | FPS: {int(30)}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )
        
        cv2.imshow("Gestura", frame)
        
        # Check for quit key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return False
        
        return True


class GesturaApp:
    """
    Main application controller - Runs gesture and voice systems concurrently.
    
    Architecture:
    - Main thread: Gesture recognition (OpenCV loop)
    - Background thread: Voice listening (continuous)
    - Shared state: VoiceConfig (thread-safe flags)
    """
    
    def __init__(self):
        """Initialize Gestura application."""
        print("\n" + "="*70)
        print("🚀 GESTURA - Gesture + Voice Control System")
        print("="*70 + "\n")
        
        # Shared configuration (thread-safe state)
        self.config = VoiceConfig()
        
        # Initialize systems
        self.gesture_system = GestureSystem(self.config)
        self.voice_controller = VoiceController(
            command_callback=self.on_voice_command,
            config=self.config
        )
        self.voice_executor = VoiceCommandExecutor(self.config)
        
        print("✅ All systems initialized\n")
    
    def on_voice_command(self, action: str, phrase: str) -> None:
        """
        Callback for voice commands (called from voice thread).
        
        Args:
            action: Action identifier
            phrase: Original spoken phrase
        """
        # Execute command through executor
        self.voice_executor.execute(action, phrase)
    
    def run(self) -> None:
        """
        Main application loop.
        
        Runs gesture recognition on main thread,
        voice listening on background thread.
        """
        try:
            # Start voice listening (background thread)
            if not self.voice_controller.start_listening():
                print("⚠️  Voice control not available, continuing with gestures only")
            
            # Start gesture recognition (main thread)
            if not self.gesture_system.start():
                print("❌ Failed to start gesture system")
                return
            
            print("\n" + "="*70)
            print("✅ GESTURA RUNNING")
            print("="*70)
            print("🎤 Voice commands active (speak naturally)")
            print("📹 Gesture recognition active (show hand to camera)")
            print("💬 Say 'show help' for list of voice commands")
            print("⏸️  Say 'pause gestura' to pause gesture recognition")
            print("▶️  Say 'resume gestura' to resume gesture recognition")
            print("🛑 Say 'stop gestura' or press 'q' to quit")
            print("="*70 + "\n")
            
            # Main loop (gesture recognition)
            while self.config.is_system_running():
                if not self.gesture_system.process_frame():
                    break
                
                # Process any pending voice commands
                self._process_voice_commands()
            
            print("\n🛑 Shutting down...")
            
        except KeyboardInterrupt:
            print("\n⚠️  Interrupted by user")
        
        except Exception as e:
            print(f"\n❌ Error: {e}")
        
        finally:
            self.shutdown()
    
    def _process_voice_commands(self) -> None:
        """Process pending voice commands from queue."""
        # Get all pending commands
        while True:
            command = self.voice_controller.get_command(timeout=None)
            if not command:
                break
            
            action, phrase = command
            # Command already executed by callback, just log it
            # (optional: additional processing here)
    
    def shutdown(self) -> None:
        """Clean shutdown of all systems."""
        print("\n" + "="*70)
        print("🧹 CLEANUP")
        print("="*70)
        
        # Stop voice listening
        self.voice_controller.stop_listening()
        
        # Stop gesture recognition
        self.gesture_system.stop()
        
        # Display statistics
        stats = self.voice_controller.get_statistics()
        print(f"\n📊 Voice Statistics:")
        print(f"   Commands recognized: {stats['commands_recognized']}")
        print(f"   Recognition backend: {stats['backend']}")
        print(f"   Recognition errors: {stats['recognition_errors']}")
        
        print("\n✅ Gestura stopped successfully")
        print("="*70 + "\n")


def main():
    """Entry point for Gestura application."""
    app = GesturaApp()
    app.run()


if __name__ == "__main__":
    main()
