"""
Voice Controller - Vosk-Based Offline Speech Recognition

Handles microphone input, Vosk speech recognition, and command dispatch.
Runs entirely in a background daemon thread — never blocks main thread.

Author: Gestura Development Team
Version: 3.0.0 (Vosk-based)
"""

import json
import threading
import queue

try:
    import sounddevice as sd  # type: ignore
    SOUNDDEVICE_AVAILABLE = True
except ImportError:
    SOUNDDEVICE_AVAILABLE = False
    print("[Voice] Warning: sounddevice not installed. Install with: pip install sounddevice")

try:
    from vosk import Model, KaldiRecognizer  # type: ignore
    VOSK_AVAILABLE = True
except ImportError:
    VOSK_AVAILABLE = False
    print("[Voice] Warning: vosk not installed. Install with: pip install vosk")

from gesture_engine import config
from gesture_engine.voice_commands import dispatch


class VoiceController:
    """
    Continuously listens via microphone, recognises speech using Vosk (offline),
    and dispatches matched commands via voice_commands.dispatch().
    
    Features:
    - Offline speech recognition (no internet required)
    - Non-blocking background thread
    - Thread-safe command execution
    - Graceful error handling
    """

    def __init__(self):
        """Initialize voice controller with Vosk model."""
        if not VOSK_AVAILABLE:
            raise RuntimeError(
                "[Voice] Vosk not available. Install with: pip install vosk\n"
                "Download model from: https://alphacephei.com/vosk/models"
            )
        
        if not SOUNDDEVICE_AVAILABLE:
            raise RuntimeError(
                "[Voice] sounddevice not available. Install with: pip install sounddevice"
            )
        
        self._audio_queue: queue.Queue = queue.Queue()
        self._thread: Optional[threading.Thread] = None  # type: ignore
        self._model: Optional[Any] = None  # type: ignore  # Model class from vosk
        
        print("[Voice] Loading Vosk model...")
        try:
            self._model = Model(config.VOSK_MODEL_PATH)  # type: ignore
            print("[Voice] ✅ Vosk model loaded successfully")
        except Exception as e:
            raise RuntimeError(
                f"[Voice] Failed to load Vosk model at '{config.VOSK_MODEL_PATH}'.\n"
                f"Download it from https://alphacephei.com/vosk/models\n"
                f"Recommended: vosk-model-small-en-us-0.15 (40 MB)\n"
                f"Original error: {e}"
            )

    # ── Public API ────────────────────────────────────────────────────────────

    def start(self) -> None:
        """Start the background listening thread."""
        if self._thread and self._thread.is_alive():
            print("[Voice] Already listening")
            return
        
        self._thread = threading.Thread(
            target=self._listen_loop,
            name="VoiceControllerThread",
            daemon=True,   # Exits automatically when main thread exits
        )
        self._thread.start()
        print("[Voice] 🎤 Listening started (Vosk offline recognition)")

    def stop(self) -> None:
        """Signal the listening loop to stop (config.running handles this)."""
        print("[Voice] Stopping listener...")
        with config.state_lock:
            config.running = False

    def is_running(self) -> bool:
        """Check if voice controller is actively listening."""
        return self._thread is not None and self._thread.is_alive()

    # ── Internal ──────────────────────────────────────────────────────────────

    def _audio_callback(
        self,
        indata,
        frames: int,
        time,
        status,
    ) -> None:
        """
        Called by sounddevice on each audio block.
        Puts raw bytes into the queue for the recognition loop to consume.
        """
        if status:
            # Log device warnings without crashing
            print(f"[Voice] Audio status: {status}")
        self._audio_queue.put(bytes(indata))

    def _listen_loop(self) -> None:
        """
        Main recognition loop. Runs in background thread.
        Reads audio blocks from the queue and feeds them to Vosk.
        """
        recogniser = KaldiRecognizer(self._model, config.SAMPLE_RATE)  # type: ignore
        
        print("[Voice] Initializing microphone stream...")

        try:
            with sd.RawInputStream(  # type: ignore
                samplerate=config.SAMPLE_RATE,
                blocksize=config.AUDIO_BLOCK_SIZE,
                dtype="int16",
                channels=1,
                callback=self._audio_callback,
            ):
                print("[Voice] ✅ Microphone stream open. Listening for commands...")
                
                while config.running:
                    try:
                        # Block briefly to avoid burning CPU, then check config.running
                        audio_block = self._audio_queue.get(timeout=0.5)
                    except queue.Empty:
                        continue

                    if recogniser.AcceptWaveform(audio_block):
                        # Complete phrase recognized
                        result = json.loads(recogniser.Result())
                        text = result.get("text", "").strip()

                        if text:
                            print(f"[Voice] 🎤 Heard: '{text}'")
                            matched = dispatch(text)
                            if not matched:
                                # Unrecognised — log once, don't spam
                                print(f"[Voice] ⚠️  No command matched for: '{text}'")
                    else:
                        # Partial result (ongoing speech)
                        partial = json.loads(recogniser.PartialResult())
                        partial_text = partial.get("partial", "").strip()
                        if partial_text:
                            # Optional: show partial results for debugging
                            # print(f"[Voice] Partial: '{partial_text}'", end='\r')
                            pass

                print("[Voice] Listen loop exited normally")

        except Exception as e:  # type: ignore  # catches all errors including sd.PortAudioError
            print(f"[Voice] ❌ Microphone error: {e}")
            print("[Voice] Possible causes:")
            print("  - Microphone not connected")
            print("  - Microphone permissions denied")
            print("  - Another application is using the microphone")
            import traceback
            traceback.print_exc()
        finally:
            print("[Voice] Microphone stream closed")


if __name__ == "__main__":
    # Quick test
    print("Testing Voice Controller...")
    try:
        controller = VoiceController()
        print("✅ Controller initialized")
        
        from gesture_engine.voice_commands import list_commands
        list_commands()
        
        print("\n▶️  Starting voice recognition...")
        print("   Speak one of the commands above")
        print("   Press Ctrl+C to stop\n")
        
        controller.start()
        
        # Keep running until interrupted
        import time
        while config.running:
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        print("\n👋 Test complete")
