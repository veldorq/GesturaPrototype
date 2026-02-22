"""
Voice Controller - Microphone Input & Speech Recognition

Handles continuous background listening with support for:
- Offline recognition (vosk, sphinx)
- Online fallback (Google Speech API)
- Thread-safe command queuing
- Graceful error handling

Author: Gestura Development Team
"""

import threading
import queue
import time
import os
from typing import Optional, Callable
from pathlib import Path

# Speech recognition libraries
try:
    import speech_recognition as sr  # type: ignore
    SR_AVAILABLE = True
except ImportError:
    SR_AVAILABLE = False
    print("⚠️  speech_recognition not installed: pip install SpeechRecognition")

# Vosk for offline recognition
try:
    from vosk import Model, KaldiRecognizer  # type: ignore
    import json  # type: ignore
    VOSK_AVAILABLE = True
except ImportError:
    VOSK_AVAILABLE = False
    print("⚠️  vosk not installed: pip install vosk")

# Audio input
try:
    import sounddevice as sd
    SOUNDDEVICE_AVAILABLE = True
except ImportError:
    SOUNDDEVICE_AVAILABLE = False
    print("⚠️  sounddevice not installed: pip install sounddevice")

from .config import VoiceConfig


class VoiceController:
    """
    Voice recognition controller with offline-first approach.
    
    Recognition priority:
    1. Vosk (offline, fast, no internet needed)
    2. CMU Sphinx (offline, included with speech_recognition)
    3. Google Speech API (online fallback)
    
    Features:
    - Continuous non-blocking listening
    - Thread-safe command queue
    - Automatic mic calibration
    - Graceful degradation
    """
    
    def __init__(self, 
                 command_callback: Optional[Callable[[str, str], None]] = None,
                 config: Optional[VoiceConfig] = None):
        """
        Initialize voice controller.
        
        Args:
            command_callback: Called when command recognized (action, phrase)
            config: Voice configuration object (uses defaults if None)
        """
        if not SR_AVAILABLE:
            raise RuntimeError("speech_recognition library required")
        
        self.config = config or VoiceConfig()
        self.command_callback = command_callback
        
        # Speech recognizer
        self.recognizer = sr.Recognizer()  # type: ignore
        self.recognizer.energy_threshold = self.config.ENERGY_THRESHOLD
        self.recognizer.pause_threshold = self.config.PAUSE_THRESHOLD
        self.recognizer.dynamic_energy_threshold = True  # Auto-adjust to ambient noise
        self.recognizer.dynamic_energy_adjustment_damping = 0.15
        self.recognizer.dynamic_energy_ratio = 1.5
        
        # Microphone
        self.microphone: Optional[Any] = None  # type: ignore  # sr.Microphone
        
        # Voice status tracking
        self.last_recognized_text = "Waiting..."
        self.is_processing = False
        
        # Vosk offline model
        self.vosk_model: Optional['Model'] = None
        self.vosk_recognizer: Optional['KaldiRecognizer'] = None
        self.use_vosk = False
        
        # Command queue (thread-safe)
        self.command_queue: queue.Queue = queue.Queue()
        
        # Listening thread
        self.is_listening = False
        self.listen_thread: Optional[threading.Thread] = None
        
        # Statistics
        self.commands_recognized = 0
        self.recognition_errors = 0
        self.last_command_time = 0.0
        
        # Initialize recognition backend
        self._init_recognition_backend()
        
        print("✅ Voice controller initialized")
    
    def _init_recognition_backend(self) -> None:
        """Initialize speech recognition backend (offline preferred)."""
        
        # Try to load vosk offline model
        if self.config.USE_OFFLINE_RECOGNITION and VOSK_AVAILABLE:
            model_path = Path(self.config.VOSK_MODEL_PATH)
            if model_path.exists():
                try:
                    print(f"📦 Loading vosk model from {model_path}")
                    self.vosk_model = Model(str(model_path))  # type: ignore
                    self.vosk_recognizer = KaldiRecognizer(self.vosk_model, 16000)  # type: ignore
                    self.use_vosk = True
                    print("✅ Vosk offline recognition enabled")
                    return
                except Exception as e:
                    print(f"⚠️  Failed to load vosk model: {e}")
        
        # Fall back to sphinx (offline) or google (online)
        if self.config.USE_OFFLINE_RECOGNITION:
            print("📡 Using CMU Sphinx (offline recognition)")
        else:
            print("🌐 Using Google Speech API (online recognition)")
    
    def start_listening(self) -> bool:
        """
        Start continuous voice listening in background thread.
        
        Returns:
            True if started successfully, False otherwise
        """
        if self.is_listening:
            print("⚠️  Voice controller already listening")
            return True
        
        try:
            # Initialize microphone
            self.microphone = sr.Microphone()  # type: ignore
            
            # Calibrate for ambient noise
            if self.microphone:
                print("🎤 Calibrating microphone for ambient noise...")
                print("   Please stay quiet for 2 seconds...")
                with self.microphone as source:  # type: ignore
                    self.recognizer.adjust_for_ambient_noise(source, duration=2)  # type: ignore
                print(f"✅ Microphone calibrated (threshold: {self.recognizer.energy_threshold:.0f})")
                print(f"   📊 Ambient noise level measured. Sensitivity optimized.")
                print(f"   💡 Speak clearly and close to microphone for best results.")
            
            # Start listening thread
            self.is_listening = True
            self.listen_thread = threading.Thread(
                target=self._listen_loop,
                daemon=True,
                name="VoiceListenerThread"
            )
            self.listen_thread.start()
            
            print("🎤 Voice listening started")
            print(f"📝 {len(self.config.COMMAND_MAP)} commands available")
            return True
            
        except Exception as e:
            print(f"❌ Failed to start voice listening: {e}")
            return False
    
    def stop_listening(self) -> None:
        """Stop voice listening and clean up."""
        if not self.is_listening:
            return
        
        self.is_listening = False
        
        if self.listen_thread and self.listen_thread.is_alive():
            self.listen_thread.join(timeout=2.0)
        
        print("🔇 Voice listening stopped")
        print(f"📊 Commands recognized: {self.commands_recognized}")
    
    def _listen_loop(self) -> None:
        """
        Background listening loop (runs in separate thread).
        Continuously captures audio and recognizes speech.
        """
        if not self.microphone:
            print("❌ Microphone not initialized")
            return
        
        print("👂 Listening for voice commands...")
        
        while self.is_listening and self.config.is_voice_active():
            try:
                self.is_processing = False
                self.last_recognized_text = "🎤 Listening..."
                with self.microphone as source:
                    # Listen for audio with timeout
                    audio = self.recognizer.listen(
                        source,
                        timeout=self.config.PHRASE_TIMEOUT,
                        phrase_time_limit=10
                    )
                
                self.is_processing = True
                self.last_recognized_text = "⏳ Processing..."
                
                # Recognize speech (non-blocking)
                threading.Thread(
                    target=self._recognize_audio,
                    args=(audio,),
                    daemon=True
                ).start()
                
            except sr.WaitTimeoutError:  # type: ignore
                # No speech detected (normal, continue listening)
                continue
                
            except Exception as e:
                self.recognition_errors += 1
                if self.recognition_errors % 10 == 1:  # Log every 10th error
                    print(f"⚠️  Listening error: {e}")
                time.sleep(0.1)  # Prevent tight error loop
    
    def _recognize_audio(self, audio: 'sr.AudioData') -> None:
        """
        Recognize speech from audio data.
        
        Args:
            audio: Audio data captured from microphone
        """
        try:
            # Try offline recognition first
            if self.use_vosk and self.vosk_recognizer:
                text = self._recognize_vosk(audio)
            elif self.config.USE_OFFLINE_RECOGNITION:
                text = self.recognizer.recognize_sphinx(audio)  # type: ignore
            else:
                text = self.recognizer.recognize_google(audio, language=self.config.LANGUAGE)  # type: ignore
            
            if text:
                self.last_recognized_text = f"✓ {text}"
                self._process_recognized_text(text.lower())
            else:
                self.last_recognized_text = "❌ No speech detected"
                
        except sr.UnknownValueError:  # type: ignore
            # Speech not understood (normal, ignore)
            self.last_recognized_text = "❓ Speech unclear"
            if self.config.DEBUG_MODE:
                print("🎤 [DEBUG] Speech detected but not understood - try speaking more clearly")
            pass
            
        except sr.RequestError as e:  # type: ignore
            # API/network error
            print(f"⚠️  Recognition service error: {e}")
            
        except Exception as e:
            print(f"⚠️  Recognition error: {e}")
    
    def _recognize_vosk(self, audio: 'sr.AudioData') -> Optional[str]:
        """
        Recognize speech using vosk offline model.
        
        Args:
            audio: Audio data from microphone
            
        Returns:
            Recognized text or None
        """
        if not self.vosk_recognizer:
            return None
        
        # Convert audio to raw PCM 16kHz mono
        audio_data = audio.get_wav_data(convert_rate=16000)
        
        # Skip WAV header (44 bytes)
        pcm_data = audio_data[44:]
        
        # Process audio
        if self.vosk_recognizer.AcceptWaveform(pcm_data):
            result = json.loads(self.vosk_recognizer.Result())  # type: ignore
            return result.get("text", "")
        else:
            partial = json.loads(self.vosk_recognizer.PartialResult())  # type: ignore
            return partial.get("partial", "")
    
    def _process_recognized_text(self, text: str) -> None:
        """
        Process recognized text and match to commands.
        
        Args:
            text: Recognized text (lowercase)
        """
        # Check if text matches any command
        action = self.config.COMMAND_MAP.get(text)
        
        if action:
            # Valid command found
            self.commands_recognized += 1
            self.last_command_time = time.time()
            
            print(f"🎤 Voice command: '{text}' → {action}")
            
            # Add to queue
            self.command_queue.put((action, text))
            
            # Execute callback if provided
            if self.command_callback:
                try:
                    self.command_callback(action, text)
                except Exception as e:
                    print(f"⚠️  Command callback error: {e}")
        else:
            # Unrecognized phrase (don't spam logs)
            if len(text) > 2:  # Ignore very short noise
                print(f"🎤 Unrecognized: '{text}'")
    
    def get_command(self, timeout: Optional[float] = None) -> Optional[tuple]:
        """
        Get next command from queue (non-blocking or with timeout).
        
        Args:
            timeout: Max seconds to wait (None = no wait, 0 = wait forever)
            
        Returns:
            (action, phrase) tuple or None if queue empty
        """
        try:
            if timeout is None:
                return self.command_queue.get_nowait()
            else:
                return self.command_queue.get(timeout=timeout)
        except queue.Empty:
            return None
    
    def clear_queue(self) -> int:
        """
        Clear all pending commands from queue.
        
        Returns:
            Number of commands removed
        """
        count = 0
        while not self.command_queue.empty():
            try:
                self.command_queue.get_nowait()
                count += 1
            except queue.Empty:
                break
        return count
    
    def get_statistics(self) -> dict:
        """Get voice recognition statistics."""
        return {
            "commands_recognized": self.commands_recognized,
            "recognition_errors": self.recognition_errors,
            "queue_size": self.command_queue.qsize(),
            "is_listening": self.is_listening,
            "backend": "vosk" if self.use_vosk else "sphinx" if self.config.USE_OFFLINE_RECOGNITION else "google",
        }
