"""
Voice Command Executor - Maps Commands to System Actions

Handles execution of voice commands using pyautogui/pynput for:
- Mouse control (click, double click, right click)
- Keyboard control (scrolling, navigation)
- Browser actions (tabs, navigation, zoom)
- System control (pause/resume gestures)

Author: Gestura Development Team
"""

import time
from typing import Optional

# System control libraries
try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
    # Safety settings
    pyautogui.FAILSAFE = True  # Move mouse to corner to abort
    pyautogui.PAUSE = 0.1  # Small delay between actions
except ImportError:
    PYAUTOGUI_AVAILABLE = False
    print("⚠️  pyautogui not installed: pip install pyautogui")

try:
    from pynput.keyboard import Key, Controller as KeyboardController  # type: ignore
    from pynput.mouse import Button, Controller as MouseController  # type: ignore
    PYNPUT_AVAILABLE = True
except ImportError:
    PYNPUT_AVAILABLE = False
    print("⚠️  pynput not installed: pip install pynput")

# Text-to-speech for voice feedback
try:
    import pyttsx3  # type: ignore
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("⚠️  pyttsx3 not installed: pip install pyttsx3")

from .config import VoiceConfig


class VoiceCommandExecutor:
    """
    Executes voice commands as system actions.
    
    Features:
    - Mouse control (click, scroll)
    - Keyboard shortcuts (navigation, zoom)
    - Browser actions
    - System state control (pause/resume gestures)
    - Optional TTS feedback
    """
    
    def __init__(self, config: Optional[VoiceConfig] = None):
        """
        Initialize command executor.
        
        Args:
            config: Voice configuration object
        """
        if not (PYAUTOGUI_AVAILABLE or PYNPUT_AVAILABLE):
            raise RuntimeError("Either pyautogui or pynput required")
        
        self.config = config or VoiceConfig()
        
        # Input controllers
        self.keyboard = KeyboardController() if PYNPUT_AVAILABLE else None  # type: ignore
        self.mouse = MouseController() if PYNPUT_AVAILABLE else None  # type: ignore
        
        # TTS engine
        self.tts_engine: Optional['pyttsx3.Engine'] = None
        if TTS_AVAILABLE and self.config.VOICE_FEEDBACK_ENABLED:
            self._init_tts()
        
        # Command dispatch map
        self.action_map = {
            # Mouse actions
            "click": self.action_click,
            "double_click": self.action_double_click,
            "right_click": self.action_right_click,
            
            # Scrolling
            "scroll_up": self.action_scroll_up,
            "scroll_down": self.action_scroll_down,
            "page_up": self.action_page_up,
            "page_down": self.action_page_down,
            
            # Browser navigation
            "browser_back": self.action_browser_back,
            "browser_forward": self.action_browser_forward,
            "new_tab": self.action_new_tab,
            "close_tab": self.action_close_tab,
            "refresh": self.action_refresh,
            
            # Zoom
            "zoom_in": self.action_zoom_in,
            "zoom_out": self.action_zoom_out,
            "reset_zoom": self.action_reset_zoom,
            
            # Media
            "mute": self.action_mute,
            "unmute": self.action_unmute,
            "volume_up": self.action_volume_up,
            "volume_down": self.action_volume_down,
            
            # Screenshot
            "screenshot": self.action_screenshot,
            
            # System control
            "pause_gestures": self.action_pause_gestures,
            "resume_gestures": self.action_resume_gestures,
            "stop_gestures": self.action_stop_system,
            "show_help": self.action_show_help,
        }
        
        print("✅ Voice command executor initialized")
    
    def _init_tts(self) -> None:
        """Initialize text-to-speech engine."""
        try:
            self.tts_engine = pyttsx3.init()  # type: ignore
            if self.tts_engine:
                self.tts_engine.setProperty('rate', self.config.TTS_RATE)  # type: ignore
                self.tts_engine.setProperty('volume', self.config.TTS_VOLUME)  # type: ignore
            print("🔊 TTS feedback enabled")
        except Exception as e:
            print(f"⚠️  TTS initialization failed: {e}")
            self.tts_engine = None
    
    def speak(self, text: str) -> None:
        """
        Speak text using TTS (non-blocking).
        
        Args:
            text: Text to speak
        """
        if self.tts_engine and self.config.VOICE_FEEDBACK_ENABLED:
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception as e:
                print(f"⚠️  TTS error: {e}")
    
    def execute(self, action: str, phrase: str = "") -> bool:
        """
        Execute voice command action.
        
        Args:
            action: Action identifier from command map
            phrase: Original spoken phrase (for logging)
            
        Returns:
            True if executed successfully, False otherwise
        """
        handler = self.action_map.get(action)
        
        if not handler:
            print(f"⚠️  Unknown action: {action}")
            return False
        
        try:
            # Execute action
            handler()
            
            # Provide voice feedback if configured
            feedback_message = self.config.FEEDBACK_MESSAGES.get(action)
            if feedback_message:
                self.speak(feedback_message)
            
            return True
            
        except Exception as e:
            print(f"⚠️  Action execution error ({action}): {e}")
            return False
    
    # ═══════════════════════════════════════════════════════════════
    # MOUSE ACTIONS
    # ═══════════════════════════════════════════════════════════════
    
    def action_click(self) -> None:
        """Perform left mouse click."""
        if PYAUTOGUI_AVAILABLE:
            pyautogui.click()  # type: ignore
        elif self.mouse:
            self.mouse.click(Button.left)  # type: ignore
        print("🖱️  Click")
    
    def action_double_click(self) -> None:
        """Perform double click."""
        if PYAUTOGUI_AVAILABLE:
            pyautogui.doubleClick()  # type: ignore
        elif self.mouse:
            self.mouse.click(Button.left, 2)  # type: ignore
        print("🖱️  Double click")
    
    def action_right_click(self) -> None:
        """Perform right mouse click."""
        if PYAUTOGUI_AVAILABLE:
            pyautogui.rightClick()  # type: ignore
        elif self.mouse:
            self.mouse.click(Button.right)  # type: ignore
        print("🖱️  Right click")
    
    # ═══════════════════════════════════════════════════════════════
    # SCROLLING ACTIONS
    # ═══════════════════════════════════════════════════════════════
    
    def action_scroll_up(self) -> None:
        """Scroll up."""
        if PYAUTOGUI_AVAILABLE:
            pyautogui.scroll(300)  # type: ignore
        elif self.mouse:
            self.mouse.scroll(0, 3)
        print("📜 Scroll up")
    
    def action_scroll_down(self) -> None:
        """Scroll down."""
        if PYAUTOGUI_AVAILABLE:
            pyautogui.scroll(-300)  # type: ignore
        elif self.mouse:
            self.mouse.scroll(0, -3)
        print("📜 Scroll down")
    
    def action_page_up(self) -> None:
        """Page up."""
        if PYAUTOGUI_AVAILABLE:
            pyautogui.press('pageup')  # type: ignore
        elif self.keyboard:
            self.keyboard.press(Key.page_up)  # type: ignore
            self.keyboard.release(Key.page_up)  # type: ignore
        print("📜 Page up")
    
    def action_page_down(self) -> None:
        """Page down."""
        if PYAUTOGUI_AVAILABLE:
            pyautogui.press('pagedown')  # type: ignore
        elif self.keyboard:
            self.keyboard.press(Key.page_down)  # type: ignore
            self.keyboard.release(Key.page_down)  # type: ignore
        print("📜 Page down")
    
    # ═══════════════════════════════════════════════════════════════
    # BROWSER ACTIONS
    # ═══════════════════════════════════════════════════════════════
    
    def action_browser_back(self) -> None:
        """Browser back."""
        if PYAUTOGUI_AVAILABLE:
            pyautogui.hotkey('alt', 'left')  # type: ignore
        elif self.keyboard:
            with self.keyboard.pressed(Key.alt):  # type: ignore
                self.keyboard.press(Key.left)  # type: ignore
                self.keyboard.release(Key.left)  # type: ignore
        print("⬅️  Browser back")
    
    def action_browser_forward(self) -> None:
        """Browser forward."""
        if PYAUTOGUI_AVAILABLE:
            pyautogui.hotkey('alt', 'right')  # type: ignore
        elif self.keyboard:
            with self.keyboard.pressed(Key.alt):  # type: ignore
                self.keyboard.press(Key.right)  # type: ignore
                self.keyboard.release(Key.right)  # type: ignore
        print("➡️  Browser forward")
    
    def action_new_tab(self) -> None:
        """Open new browser tab."""
        if PYAUTOGUI_AVAILABLE:
            pyautogui.hotkey('ctrl', 't')  # type: ignore
        elif self.keyboard:
            with self.keyboard.pressed(Key.ctrl):  # type: ignore
                self.keyboard.tap('t')
        print("📑 New tab")
    
    def action_close_tab(self) -> None:
        """Close current browser tab."""
        if PYAUTOGUI_AVAILABLE:
            pyautogui.hotkey('ctrl', 'w')  # type: ignore
        elif self.keyboard:
            with self.keyboard.pressed(Key.ctrl):  # type: ignore
                self.keyboard.tap('w')
        print("✖️  Close tab")
    
    def action_refresh(self) -> None:
        """Refresh page."""
        if PYAUTOGUI_AVAILABLE:
            pyautogui.press('f5')  # type: ignore
        elif self.keyboard:
            self.keyboard.press(Key.f5)  # type: ignore
            self.keyboard.release(Key.f5)  # type: ignore
        print("🔄 Refresh")
    
    # ═══════════════════════════════════════════════════════════════
    # ZOOM ACTIONS
    # ═══════════════════════════════════════════════════════════════
    
    def action_zoom_in(self) -> None:
        """Zoom in."""
        if PYAUTOGUI_AVAILABLE:
            pyautogui.hotkey('ctrl', '+')  # type: ignore
        elif self.keyboard:
            with self.keyboard.pressed(Key.ctrl):  # type: ignore
                self.keyboard.tap('+')
        print("🔍 Zoom in")
    
    def action_zoom_out(self) -> None:
        """Zoom out."""
        if PYAUTOGUI_AVAILABLE:
            pyautogui.hotkey('ctrl', '-')  # type: ignore
        elif self.keyboard:
            with self.keyboard.pressed(Key.ctrl):  # type: ignore
                self.keyboard.tap('-')
        print("🔍 Zoom out")
    
    def action_reset_zoom(self) -> None:
        """Reset zoom to 100%."""
        if PYAUTOGUI_AVAILABLE:
            pyautogui.hotkey('ctrl', '0')  # type: ignore
        elif self.keyboard:
            with self.keyboard.pressed(Key.ctrl):  # type: ignore
                self.keyboard.tap('0')
        print("🔍 Reset zoom")
    
    # ═══════════════════════════════════════════════════════════════
    # MEDIA CONTROLS
    # ═══════════════════════════════════════════════════════════════
    
    def action_mute(self) -> None:
        """Mute/unmute audio."""
        if PYAUTOGUI_AVAILABLE:
            pyautogui.press('volumemute')  # type: ignore
        elif self.keyboard:
            self.keyboard.press(Key.media_volume_mute)  # type: ignore
            self.keyboard.release(Key.media_volume_mute)  # type: ignore
        print("🔇 Mute toggle")
    
    def action_unmute(self) -> None:
        """Unmute (same as mute toggle)."""
        self.action_mute()
    
    def action_volume_up(self) -> None:
        """Increase volume."""
        if PYAUTOGUI_AVAILABLE:
            pyautogui.press('volumeup')  # type: ignore
        elif self.keyboard:
            self.keyboard.press(Key.media_volume_up)  # type: ignore
            self.keyboard.release(Key.media_volume_up)  # type: ignore
        print("🔊 Volume up")
    
    def action_volume_down(self) -> None:
        """Decrease volume."""
        if PYAUTOGUI_AVAILABLE:
            pyautogui.press('volumedown')  # type: ignore
        elif self.keyboard:
            self.keyboard.press(Key.media_volume_down)  # type: ignore
            self.keyboard.release(Key.media_volume_down)  # type: ignore
        print("🔉 Volume down")
    
    # ═══════════════════════════════════════════════════════════════
    # SCREENSHOT
    # ═══════════════════════════════════════════════════════════════
    
    def action_screenshot(self) -> None:
        """Take screenshot."""
        if PYAUTOGUI_AVAILABLE:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            pyautogui.screenshot(filename)  # type: ignore
            print(f"📸 Screenshot saved: {filename}")
        else:
            # Use system shortcut
            if self.keyboard:
                with self.keyboard.pressed(Key.cmd):  # type: ignore  # Windows key
                    with self.keyboard.pressed(Key.shift):  # type: ignore
                        self.keyboard.tap('s')
            print("📸 Screenshot")
    
    # ═══════════════════════════════════════════════════════════════
    # SYSTEM CONTROL
    # ═══════════════════════════════════════════════════════════════
    
    def action_pause_gestures(self) -> None:
        """Pause gesture recognition system."""
        self.config.set_gesture_active(False)
        print("⏸️  Gestures paused")
    
    def action_resume_gestures(self) -> None:
        """Resume gesture recognition system."""
        self.config.set_gesture_active(True)
        print("▶️  Gestures resumed")
    
    def action_stop_system(self) -> None:
        """Stop entire Gestura system."""
        self.config.stop_system()
        print("🛑 Stopping Gestura")
    
    def action_show_help(self) -> None:
        """Show available voice commands."""
        print("\n" + "="*60)
        print("📋 AVAILABLE VOICE COMMANDS")
        print("="*60)
        
        categories = {
            "Mouse": ["click", "double click", "right click"],
            "Scrolling": ["scroll up", "scroll down", "page up", "page down"],
            "Browser": ["go back", "go forward", "new tab", "close tab", "refresh"],
            "Zoom": ["zoom in", "zoom out", "reset zoom"],
            "Media": ["mute", "unmute", "volume up", "volume down"],
            "Screenshot": ["screenshot", "take screenshot"],
            "System": ["pause gestura", "resume gestura", "stop gestura"],
        }
        
        for category, commands in categories.items():
            print(f"\n{category}:")
            for cmd in commands:
                action = self.config.COMMAND_MAP.get(cmd)
                if action:
                    print(f"  • \"{cmd}\"")
        
        print("="*60 + "\n")
