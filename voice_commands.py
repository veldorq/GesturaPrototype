"""
Voice command recognition for Gestura PROTOTYPE.PY
Enables hands-free control through speech recognition.

Author: Gestura Development Team
Version: 1.0
"""

import threading
import queue
import time
from typing import Optional, Dict, Callable

# Try to import speech recognition
try:
    import speech_recognition as sr
    SPEECH_AVAILABLE = True
    SR_MODULE = sr  # Store reference for type checking
except ImportError:
    SPEECH_AVAILABLE = False
    sr = None  # type: ignore
    SR_MODULE = None
    print("⚠️  speech_recognition not installed. Voice control disabled.")
    print("   Install with: pip install SpeechRecognition pyaudio")


class VoiceCommandController:
    """
    Background voice recognition for gesture system.
    Listens for voice commands and queues them for processing.
    """
    
    def __init__(self, language: str = "en-US"):
        """
        Initialize voice controller.
        
        Args:
            language: Language code for recognition (default: en-US)
        """
        if not SPEECH_AVAILABLE:
            self.available = False
            return
        
        self.available = True
        self.language = language
        
        # Command mapping
        self.commands = {
            "click": "click",
            "scroll up": "scroll_up",
            "scroll down": "scroll_down",
            "go back": "back",
            "go forward": "forward",
            "new tab": "new_tab",
            "close tab": "close_tab",
            "refresh": "refresh",
            "zoom in": "zoom_in",
            "zoom out": "zoom_out",
            "mute": "mute",
            "screenshot": "screenshot",
            "stop listening": "disable_voice",
            "help": "help",
        }
        
        # Initialize recognizer
        self.recognizer = sr.Recognizer()  # type: ignore
        self.microphone = None
        
        # Command queue
        self.command_queue: queue.Queue = queue.Queue()
        
        # Threading control
        self.is_listening = False
        self.listen_thread: Optional[threading.Thread] = None
        
        # Statistics
        self.commands_recognized = 0
        self.last_command_time = 0.0
        
        print("✅ Voice controller initialized")
    
    def start_listening(self) -> bool:
        """
        Start listening for voice commands in background thread.
        
        Returns:
            True if started successfully, False otherwise
        """
        if not self.available:
            print("❌ Voice control not available (speech_recognition not installed)")
            return False
        
        if self.is_listening:
            print("⚠️  Voice controller already listening")
            return True
        
        try:
            # Initialize microphone
            self.microphone = sr.Microphone()  # type: ignore
            
            # Calibrate for ambient noise
            print("🎤 Calibrating microphone...")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("✅ Microphone ready")
            
            # Start listening thread
            self.is_listening = True
            self.listen_thread = threading.Thread(
                target=self._listen_loop,
                daemon=True
            )
            self.listen_thread.start()
            
            print("🎤 Voice listening started")
            return True
            
        except Exception as e:
            print(f"❌ Failed to initialize microphone: {e}")
            return False
    
    def stop_listening(self) -> None:
        """Stop listening for voice commands."""
        if not self.is_listening:
            return
        
        self.is_listening = False
        
        if self.listen_thread:
            self.listen_thread.join(timeout=2.0)
        
        print("🔇 Voice listening stopped")
    
    def _listen_loop(self) -> None:
        """Background thread that continuously listens for commands."""
        if not self.microphone:
            print("⚠️  Microphone not initialized")
            return
        
        while self.is_listening:
            try:
                with self.microphone as source:
                    # Listen with timeout
                    audio = self.recognizer.listen(
                        source,
                        timeout=3.0,
                        phrase_time_limit=5.0
                    )
                    
                    # Recognize speech
                    try:
                        text = self.recognizer.recognize_google(  # type: ignore
                            audio,
                            language=self.language
                        ).lower()
                        
                        # Match to command
                        command = self._match_command(text)
                        if command:
                            self.command_queue.put((command, text))
                            self.commands_recognized += 1
                            self.last_command_time = time.time()
                            print(f"🎤 Voice command: {command} ('{text}')")
                    
                    except sr.UnknownValueError:  # type: ignore
                        pass  # Could not understand audio
                    except sr.RequestError as e:  # type: ignore
                        print(f"❌ Speech recognition error: {e}")
            
            except sr.WaitTimeoutError:  # type: ignore
                continue  # Normal timeout
            except Exception as e:
                print(f"⚠️  Error in voice listen loop: {e}")
                time.sleep(1)
    
    def _match_command(self, text: str) -> Optional[str]:
        """
        Match spoken text to a command.
        
        Args:
            text: Recognized text (lowercase)
            
        Returns:
            Command string if matched, None otherwise
        """
        # Exact match
        if text in self.commands:
            return self.commands[text]
        
        # Fuzzy match - check if any command phrase is in the text
        for phrase, command in self.commands.items():
            if phrase in text:
                return command
        
        return None
    
    def get_command(self) -> Optional[tuple]:
        """
        Get next command from queue (non-blocking).
        
        Returns:
            Tuple of (command, original_phrase) if available, None otherwise
        """
        try:
            return self.command_queue.get_nowait()
        except queue.Empty:
            return None
    
    def has_pending_commands(self) -> bool:
        """Check if there are pending commands in the queue."""
        return not self.command_queue.empty()
    
    def clear_queue(self) -> None:
        """Clear all pending commands from the queue."""
        while not self.command_queue.empty():
            try:
                self.command_queue.get_nowait()
            except queue.Empty:
                break


# Stub class for when speech recognition is not available
class VoiceCommandControllerStub:
    """Stub implementation when speech_recognition is not available."""
    
    def __init__(self, *args, **kwargs):
        self.available = False
        self.is_listening = False
    
    def start_listening(self) -> bool:
        return False
    
    def stop_listening(self) -> None:
        pass
    
    def get_command(self) -> None:
        return None
    
    def has_pending_commands(self) -> bool:
        return False
    
    def clear_queue(self) -> None:
        pass


# Export the appropriate class based on availability
if SPEECH_AVAILABLE:
    VoiceController = VoiceCommandController
else:
    VoiceController = VoiceCommandControllerStub
