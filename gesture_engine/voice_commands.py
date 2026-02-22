# voice_commands.py
# Maps recognised voice command strings to system actions.
# Each command function is self-contained and independently callable.

import pyautogui
import pyttsx3  # type: ignore
from gesture_engine import config

# Initialise TTS engine once at module level to avoid repeated startup cost
try:
    _tts_engine = pyttsx3.init()
    _tts_engine.setProperty("rate", 165)   # Words per minute
    _tts_engine.setProperty("volume", 1.0)
    TTS_AVAILABLE = True
except Exception as e:
    print(f"[Voice Commands] TTS not available: {e}")
    _tts_engine = None
    TTS_AVAILABLE = False


def _speak(text: str) -> None:
    """Speak text aloud if voice feedback is enabled."""
    if config.VOICE_FEEDBACK_ENABLED and TTS_AVAILABLE and _tts_engine:
        try:
            _tts_engine.say(text)
            _tts_engine.runAndWait()
        except Exception as e:
            print(f"[Voice Commands] TTS error: {e}")


# ── Action functions ──────────────────────────────────────────────────────────

def cmd_click() -> None:
    """Execute mouse click."""
    pyautogui.click()
    print("[Voice Commands] Click executed")

def cmd_double_click() -> None:
    """Execute double click."""
    pyautogui.doubleClick()
    print("[Voice Commands] Double click executed")

def cmd_scroll_up() -> None:
    """Scroll up."""
    pyautogui.scroll(300)
    print("[Voice Commands] Scroll up")

def cmd_scroll_down() -> None:
    """Scroll down."""
    pyautogui.scroll(-300)
    print("[Voice Commands] Scroll down")

def cmd_new_tab() -> None:
    """Open new browser tab."""
    pyautogui.hotkey('ctrl', 't')
    print("[Voice Commands] New tab")

def cmd_close_tab() -> None:
    """Close current browser tab."""
    pyautogui.hotkey('ctrl', 'w')
    print("[Voice Commands] Close tab")

def cmd_go_back() -> None:
    """Browser back."""
    pyautogui.hotkey('alt', 'left')
    print("[Voice Commands] Go back")

def cmd_go_forward() -> None:
    """Browser forward."""
    pyautogui.hotkey('alt', 'right')
    print("[Voice Commands] Go forward")

def cmd_refresh() -> None:
    """Refresh page."""
    pyautogui.press('f5')
    print("[Voice Commands] Refresh")

def cmd_zoom_in() -> None:
    """Zoom in."""
    pyautogui.hotkey('ctrl', '+')
    print("[Voice Commands] Zoom in")

def cmd_zoom_out() -> None:
    """Zoom out."""
    pyautogui.hotkey('ctrl', '-')
    print("[Voice Commands] Zoom out")

def cmd_mute() -> None:
    """Mute/unmute."""
    pyautogui.press('volumemute')
    print("[Voice Commands] Mute toggle")

def cmd_screenshot() -> None:
    """Take screenshot."""
    import time
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.png"
    pyautogui.screenshot(filename)
    print(f"[Voice Commands] Screenshot saved: {filename}")

def cmd_pause_gestura() -> None:
    """Pause gesture detection."""
    with config.state_lock:
        config.gesture_active = False
    print("[Voice Commands] Gesture detection paused.")
    _speak("Gestura paused")

def cmd_resume_gestura() -> None:
    """Resume gesture detection."""
    with config.state_lock:
        config.gesture_active = True
    print("[Voice Commands] Gesture detection resumed.")
    _speak("Gestura resumed")

def cmd_stop_gestura() -> None:
    """Stop entire Gestura system."""
    with config.state_lock:
        config.running = False
    print("[Voice Commands] Shutting down Gestura.")
    _speak("Stopping Gestura")


# ── Command registry ──────────────────────────────────────────────────────────
# Maps the exact recognised text to its handler function.
# Add new commands here without touching any other file.

COMMAND_MAP: dict = {
    "click":           cmd_click,
    "double click":    cmd_double_click,
    "scroll up":       cmd_scroll_up,
    "scroll down":     cmd_scroll_down,
    "new tab":         cmd_new_tab,
    "close tab":       cmd_close_tab,
    "go back":         cmd_go_back,
    "go forward":      cmd_go_forward,
    "refresh":         cmd_refresh,
    "zoom in":         cmd_zoom_in,
    "zoom out":        cmd_zoom_out,
    "mute":            cmd_mute,
    "screenshot":      cmd_screenshot,
    "pause gestura":   cmd_pause_gestura,
    "resume gestura":  cmd_resume_gestura,
    "stop gestura":    cmd_stop_gestura,
}


def dispatch(recognised_text: str) -> bool:
    """
    Look up and execute a command from recognised_text.
    Returns True if a command was matched and executed, False otherwise.
    """
    text = recognised_text.strip().lower()
    handler = COMMAND_MAP.get(text)
    if handler:
        try:
            handler()
            return True
        except Exception as e:
            print(f"[Voice Commands] Error executing '{text}': {e}")
            return False
    return False


def list_commands() -> None:
    """Print all available voice commands."""
    print("\n" + "="*60)
    print("📋 AVAILABLE VOICE COMMANDS")
    print("="*60)
    
    categories = {
        "Mouse Control": ["click", "double click"],
        "Scrolling": ["scroll up", "scroll down"],
        "Browser Navigation": ["go back", "go forward", "new tab", "close tab", "refresh"],
        "Zoom": ["zoom in", "zoom out"],
        "Media": ["mute"],
        "Screenshot": ["screenshot"],
        "System Control": ["pause gestura", "resume gestura", "stop gestura"],
    }
    
    for category, commands in categories.items():
        print(f"\n{category}:")
        for cmd in commands:
            if cmd in COMMAND_MAP:
                print(f"  • \"{cmd}\"")
    
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    # Test command listing
    list_commands()
