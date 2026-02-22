"""
Voice command recognition for AccessAble.
Enables hands-free control through speech recognition.
"""

import speech_recognition as sr
import threading
import queue
import time
from typing import Optional, Dict, Callable
from enum import Enum
from utils import get_logger

logger = get_logger(__name__)


class VoiceCommand(Enum):
    """Available voice commands."""
    SCROLL_MODE = "scroll_mode"
    NAVIGATION_MODE = "navigation_mode"
    CLICK = "click"
    GO_BACK = "go_back"
    GO_FORWARD = "go_forward"
    NEW_TAB = "new_tab"
    CLOSE_TAB = "close_tab"
    REFRESH = "refresh"
    DISABLE_VOICE = "disable_voice"
    HELP = "help"


class VoiceController:
    """
    Background voice recognition controller.
    
    Listens for voice commands in a separate thread and queues them
    for the main application to process.
    """
    
    def __init__(
        self,
        command_map: Optional[Dict[str, VoiceCommand]] = None,
        language: str = "en-US"
    ):
        """
        Initialize voice controller.
        
        Args:
            command_map: Dictionary mapping phrases to commands
            language: Language code for recognition (default: en-US)
        """
        self.language = language
        
        # Default command mapping
        if command_map is None:
            self.command_map = {
                "scroll mode": VoiceCommand.SCROLL_MODE,
                "navigation mode": VoiceCommand.NAVIGATION_MODE,
                "click": VoiceCommand.CLICK,
                "go back": VoiceCommand.GO_BACK,
                "go forward": VoiceCommand.GO_FORWARD,
                "new tab": VoiceCommand.NEW_TAB,
                "close tab": VoiceCommand.CLOSE_TAB,
                "refresh": VoiceCommand.REFRESH,
                "disable voice": VoiceCommand.DISABLE_VOICE,
                "help": VoiceCommand.HELP,
            }
        else:
            self.command_map = command_map
        
        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()
        self.microphone = None
        
        # Command queue for thread-safe communication
        self.command_queue: queue.Queue = queue.Queue()
        
        # Threading control
        self.is_listening = False
        self.listen_thread: Optional[threading.Thread] = None
        
        # Statistics
        self.commands_recognized = 0
        self.last_command_time = 0.0
        
        logger.info("Voice controller initialized")
    
    def start_listening(self) -> bool:
        """
        Start listening for voice commands in background thread.
        
        Returns:
            True if started successfully, False otherwise
        """
        if self.is_listening:
            logger.warning("Voice controller already listening")
            return True
        
        try:
            # Initialize microphone
            self.microphone = sr.Microphone()
            
            # Calibrate for ambient noise
            logger.info("Calibrating microphone for ambient noise...")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            logger.info("Microphone ready")
            
            # Start listening thread
            self.is_listening = True
            self.listen_thread = threading.Thread(
                target=self._listen_loop,
                daemon=True
            )
            self.listen_thread.start()
            
            logger.info("Voice listening started")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize microphone: {e}")
            return False
    
    def stop_listening(self) -> None:
        """Stop listening for voice commands."""
        if not self.is_listening:
            return
        
        self.is_listening = False
        
        # Wait for listener thread to finish
        if self.listen_thread:
            self.listen_thread.join(timeout=2.0)
        
        logger.info("Voice listening stopped")
    
    def _listen_loop(self) -> None:
        """
        Background thread that continuously listens for commands.
        Runs until is_listening is set to False.
        """
        if not self.microphone:
            logger.error("Microphone not initialized")
            return
        
        while self.is_listening:
            try:
                with self.microphone as source:
                    logger.debug("Listening for command...")
                    
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
                        
                        logger.debug(f"Heard: '{text}'")
                        
                        # Match to command
                        command = self._match_command(text)
                        if command:
                            self.command_queue.put((command, text))
                            self.commands_recognized += 1
                            self.last_command_time = time.time()
                            logger.info(f"Command recognized: {command.value}")
                        else:
                            logger.debug(f"No matching command for: '{text}'")
                    
                    except sr.UnknownValueError:
                        logger.debug("Could not understand audio")
                    except sr.RequestError as e:
                        logger.error(f"Speech recognition error: {e}")
            
            except sr.WaitTimeoutError:
                # Normal timeout, continue listening
                continue
            except Exception as e:
                logger.error(f"Error in listen loop: {e}")
                time.sleep(1)  # Avoid tight loop on errors
    
    def _match_command(self, text: str) -> Optional[VoiceCommand]:
        """
        Match spoken text to a voice command.
        
        Args:
            text: Recognized text (lowercase)
            
        Returns:
            VoiceCommand if matched, None otherwise
        """
        # Exact match
        if text in self.command_map:
            return self.command_map[text]
        
        # Fuzzy match - check if any command phrase is in the text
        for phrase, command in self.command_map.items():
            if phrase in text:
                return command
        
        return None
    
    def get_command(self) -> Optional[tuple[VoiceCommand, str]]:
        """
        Get next command from queue (non-blocking).
        
        Returns:
            Tuple of (VoiceCommand, original_phrase) if available, None otherwise
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


class VoiceControllerStub:
    """
    Stub implementation when speech_recognition is not available.
    Provides same interface but does nothing.
    """
    
    def __init__(self, *args, **kwargs):
        logger.warning("VoiceController stub active (speech_recognition not available)")
    
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


# Try to use real controller, fall back to stub if dependencies missing
try:
    import speech_recognition
    VoiceControllerClass = VoiceController
except ImportError:
    logger.warning("speech_recognition not found, voice control will be disabled")
    VoiceControllerClass = VoiceControllerStub
