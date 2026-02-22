"""
Voice Control Module

Integrates voice command recognition with gesture control system.
Supports offline speech recognition using speech_recognition library.

Author: Gestura Development Team
Version: 2.0.0
"""

import threading
import queue
import time
from typing import Optional, Callable, Dict, Any
from enum import Enum

try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    print("Warning: speech_recognition not installed. Voice control disabled.")

from gesture_engine.config import CONFIG


class VoiceCommand(Enum):
    """Recognized voice commands."""
    ENABLE_SCROLL = "enable_scroll"
    ENABLE_NAVIGATION = "enable_navigation"
    DISABLE_VOICE = "disable_voice"
    MOUSE_CLICK = "mouse_click"
    MOUSE_DOUBLE_CLICK = "mouse_double_click"
    BROWSER_BACK = "browser_back"
    BROWSER_FORWARD = "browser_forward"
    BROWSER_NEW_TAB = "browser_new_tab"
    BROWSER_CLOSE_TAB = "browser_close_tab"
    UNKNOWN = "unknown"


class VoiceController:
    """
    Voice command recognition and processing.
    
    Features:
    - Continuous background listening
    - Configurable command vocabulary
    - Timeout handling
    - Thread-safe command queue
    - Voice-triggered mode switching
    """
    
    def __init__(self, command_callback: Optional[Callable] = None):
        """
        Initialize voice controller.
        
        Args:
            command_callback: Function called when command recognized
                             Signature: callback(command: VoiceCommand, phrase: str)
        """
        if not SPEECH_RECOGNITION_AVAILABLE:
            raise RuntimeError("speech_recognition library not available")
        
        self.config = CONFIG.voice
        self.command_callback = command_callback
        
        # Speech recognizer
        self.recognizer = sr.Recognizer()  # type: ignore
        self.recognizer.energy_threshold = self.config.energy_threshold
        self.recognizer.pause_threshold = self.config.pause_threshold
        
        # Microphone
        self.microphone: Optional[sr.Microphone] = None  # type: ignore
        
        # Command mapping (phrase -> command)
        self.command_map: Dict[str, VoiceCommand] = {}
        self._load_command_map()
        
        # Listening state
        self.is_listening = False
        self.listen_thread: Optional[threading.Thread] = None
        self.command_queue: queue.Queue = queue.Queue()
        
        # Statistics
        self.commands_recognized = 0
        self.last_command_time = 0.0
    
    def _load_command_map(self) -> None:
        """Load command phrases from configuration."""
        for phrase, action in self.config.voice_commands.items():
            try:
                command = VoiceCommand(action)
                self.command_map[phrase.lower()] = command
            except ValueError:
                print(f"Warning: Unknown voice command action: {action}")
    
    def start_listening(self) -> bool:
        """
        Start background voice listening thread.
        
        Returns:
            True if started successfully, False otherwise
        """
        if self.is_listening:
            print("Already listening")
            return False
        
        # Initialize microphone
        try:
            self.microphone = sr.Microphone()  # type: ignore
            with self.microphone as source:
                print("Calibrating microphone for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Microphone ready")
        except Exception as e:
            print(f"Failed to initialize microphone: {e}")
            return False
        
        # Start listening thread
        self.is_listening = True
        self.listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.listen_thread.start()
        
        print("Voice listening started")
        return True
    
    def stop_listening(self) -> None:
        """Stop background voice listening."""
        self.is_listening = False
        if self.listen_thread:
            self.listen_thread.join(timeout=2.0)
        print("Voice listening stopped")
    
    def _listen_loop(self) -> None:
        """Background listening loop (runs in separate thread)."""
        if not self.microphone:
            print("Error: Microphone not initialized")
            return
        
        while self.is_listening:
            try:
                # Listen for audio
                with self.microphone as source:
                    print("Listening for command...")
                    audio = self.recognizer.listen(
                        source,
                        timeout=self.config.timeout_seconds,
                        phrase_time_limit=5.0
                    )
                
                # Recognize speech
                try:
                    # Use Google Speech Recognition (free, online)
                    text = self.recognizer.recognize_google(  # type: ignore
                        audio,
                        language=self.config.language
                    )
                    
                    print(f"Heard: '{text}'")
                    
                    # Process command
                    self._process_phrase(text)
                
                except sr.UnknownValueError:  # type: ignore
                    print("Could not understand audio")
                except sr.RequestError as e:  # type: ignore
                    print(f"Recognition service error: {e}")
            
            except sr.WaitTimeoutError:  # type: ignore
                # No speech detected, continue listening
                continue
            except Exception as e:
                print(f"Listening error: {e}")
                time.sleep(1)
    
    def _process_phrase(self, phrase: str) -> None:
        """
        Process recognized phrase and extract command.
        
        Args:
            phrase: Recognized text from speech
        """
        phrase_lower = phrase.lower().strip()
        
        # Match against command map
        command = VoiceCommand.UNKNOWN
        matched_phrase = None
        
        for cmd_phrase, cmd in self.command_map.items():
            if cmd_phrase in phrase_lower:
                command = cmd
                matched_phrase = cmd_phrase
                break
        
        if command != VoiceCommand.UNKNOWN:
            # Add to queue
            self.command_queue.put((command, phrase))
            self.commands_recognized += 1
            self.last_command_time = time.time()
            
            print(f"Command recognized: {command.value}")
            
            # Call callback if provided
            if self.command_callback:
                try:
                    self.command_callback(command, phrase)
                except Exception as e:
                    print(f"Callback error: {e}")
        else:
            print(f"No matching command for: '{phrase}'")
    
    def get_command(self, timeout: float = 0.0) -> Optional[tuple]:
        """
        Get next command from queue.
        
        Args:
            timeout: Maximum time to wait (0 = non-blocking)
            
        Returns:
            Tuple of (VoiceCommand, original_phrase) or None
        """
        try:
            if timeout > 0:
                return self.command_queue.get(timeout=timeout)
            else:
                return self.command_queue.get_nowait()
        except queue.Empty:
            return None
    
    def has_pending_commands(self) -> bool:
        """Check if commands are waiting in queue."""
        return not self.command_queue.empty()
    
    def clear_command_queue(self) -> None:
        """Clear all pending commands."""
        while not self.command_queue.empty():
            try:
                self.command_queue.get_nowait()
            except queue.Empty:
                break
    
    def add_custom_command(self, phrase: str, command: VoiceCommand) -> None:
        """
        Add custom voice command at runtime.
        
        Args:
            phrase: Voice phrase to recognize
            command: Command to trigger
        """
        self.command_map[phrase.lower()] = command
        print(f"Added custom command: '{phrase}' -> {command.value}")
    
    def remove_custom_command(self, phrase: str) -> bool:
        """
        Remove custom voice command.
        
        Args:
            phrase: Voice phrase to remove
            
        Returns:
            True if removed, False if not found
        """
        phrase_lower = phrase.lower()
        if phrase_lower in self.command_map:
            del self.command_map[phrase_lower]
            print(f"Removed command: '{phrase}'")
            return True
        return False
    
    def list_commands(self) -> Dict[str, str]:
        """Get all registered voice commands."""
        return {phrase: cmd.value for phrase, cmd in self.command_map.items()}
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get voice controller statistics."""
        return {
            "is_listening": self.is_listening,
            "commands_recognized": self.commands_recognized,
            "pending_commands": self.command_queue.qsize(),
            "last_command_time": self.last_command_time,
            "registered_commands": len(self.command_map)
        }


# Fallback implementation when speech_recognition not available
class VoiceControllerStub:
    """Stub implementation when voice control dependencies not available."""
    
    def __init__(self, command_callback: Optional[Callable] = None):
        print("Voice control disabled (dependencies not installed)")
        self.is_listening = False
    
    def start_listening(self) -> bool:
        print("Voice control not available")
        return False
    
    def stop_listening(self) -> None:
        pass
    
    def get_command(self, timeout: float = 0.0) -> Optional[tuple]:
        return None
    
    def has_pending_commands(self) -> bool:
        return False
    
    def clear_command_queue(self) -> None:
        pass
    
    def list_commands(self) -> Dict[str, str]:
        return {}
    
    def get_statistics(self) -> Dict[str, Any]:
        return {"is_listening": False, "error": "Not available"}


# Export appropriate class based on availability
if SPEECH_RECOGNITION_AVAILABLE:
    VoiceControllerClass = VoiceController
else:
    VoiceControllerClass = VoiceControllerStub


if __name__ == "__main__":
    # Test voice controller
    print("Voice Controller Test")
    print("=" * 50)
    
    if not SPEECH_RECOGNITION_AVAILABLE:
        print("ERROR: speech_recognition not installed")
        print("Install with: pip install SpeechRecognition pyaudio")
        exit(1)
    
    def on_command(command: VoiceCommand, phrase: str):
        print(f"\n>>> Command detected: {command.value}")
        print(f">>> Original phrase: '{phrase}'")
    
    controller = VoiceController(command_callback=on_command)
    
    print("\nAvailable commands:")
    for phrase, cmd in controller.list_commands().items():
        print(f"  '{phrase}' -> {cmd}")
    
    print("\nStarting voice listening...")
    print("Say a command or press Ctrl+C to stop\n")
    
    try:
        if controller.start_listening():
            # Keep running
            while True:
                time.sleep(1)
                
                # Check for commands in queue
                while controller.has_pending_commands():
                    cmd, phrase = controller.get_command()
                    print(f"Processed from queue: {cmd.value}")
    
    except KeyboardInterrupt:
        print("\nStopping...")
        controller.stop_listening()
    
    print("\nStatistics:")
    stats = controller.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
