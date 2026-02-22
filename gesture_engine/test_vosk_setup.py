"""
Vosk Voice Control - Installation Verification

This script checks if all dependencies are installed and
the Vosk model is properly configured.

Usage:
    python test_vosk_setup.py
"""

import sys
from pathlib import Path

print("="*70)
print("  VOSK VOICE CONTROL - INSTALLATION VERIFICATION")
print("="*70)
print()

# ══════════════════════════════════════════════════════════════════
# Test 1: Check Python Version
# ══════════════════════════════════════════════════════════════════

print("Test 1: Python Version")
if sys.version_info >= (3, 8):
    print(f"  ✅ Python {sys.version_info.major}.{sys.version_info.minor} (OK)")
else:
    print(f"  ❌ Python {sys.version_info.major}.{sys.version_info.minor} (Need 3.8+)")
    sys.exit(1)
print()

# ══════════════════════════════════════════════════════════════════
# Test 2: Check Dependencies
# ══════════════════════════════════════════════════════════════════

print("Test 2: Required Dependencies")

dependencies = {
    "vosk": False,
    "sounddevice": False,
    "pyautogui": False,
    "pyttsx3": False,
    "cv2 (opencv-python)": False,
    "mediapipe": False,
}

try:
    import vosk  # type: ignore
    dependencies["vosk"] = True
except ImportError:
    pass

try:
    import sounddevice
    dependencies["sounddevice"] = True
except ImportError:
    pass

try:
    import pyautogui
    dependencies["pyautogui"] = True
except ImportError:
    pass

try:
    import pyttsx3  # type: ignore
    dependencies["pyttsx3"] = True
except ImportError:
    pass

try:
    import cv2
    dependencies["cv2 (opencv-python)"] = True
except ImportError:
    pass

try:
    import mediapipe
    dependencies["mediapipe"] = True
except ImportError:
    pass

all_installed = True
for dep, installed in dependencies.items():
    status = "✅" if installed else "❌"
    print(f"  {status} {dep}")
    if not installed:
        all_installed = False

if not all_installed:
    print()
    print("  ⚠️  Missing dependencies detected!")
    print("  Install with: pip install -r requirements_vosk.txt")
    print()
print()

# ══════════════════════════════════════════════════════════════════
# Test 3: Check Vosk Model
# ══════════════════════════════════════════════════════════════════

print("Test 3: Vosk Model")

# Check from gesture_engine import config
try:
    from gesture_engine import config
    model_path = Path(config.VOSK_MODEL_PATH)
    
    print(f"  Model path: {model_path}")
    
    if model_path.exists():
        print(f"  ✅ Model directory found")
        
        # Check required subdirectories
        required_dirs = ["am", "conf", "graph", "ivector"]
        all_present = True
        
        for dir_name in required_dirs:
            dir_path = model_path / dir_name
            if dir_path.exists():
                print(f"    ✅ {dir_name}/ present")
            else:
                print(f"    ❌ {dir_name}/ missing")
                all_present = False
        
        if not all_present:
            print()
            print("  ⚠️  Model appears incomplete!")
            print("  Download: https://alphacephei.com/vosk/models")
            print("  Recommended: vosk-model-small-en-us-0.15.zip (40 MB)")
            print()
    else:
        print(f"  ❌ Model directory not found at: {model_path}")
        print()
        print("  📥 Download Vosk model:")
        print("    1. Visit: https://alphacephei.com/vosk/models")
        print("    2. Download: vosk-model-small-en-us-0.15.zip (40 MB)")
        print(f"    3. Extract to: {model_path.absolute()}")
        print()

except ImportError as e:
    print(f"  ❌ Could not import config: {e}")
    print()
except Exception as e:
    print(f"  ❌ Error checking model: {e}")
    print()
print()

# ══════════════════════════════════════════════════════════════════
# Test 4: Check Microphone
# ══════════════════════════════════════════════════════════════════

print("Test 4: Microphone Access")

if dependencies["sounddevice"]:
    try:
        import sounddevice as sd
        devices = sd.query_devices()
        
        # Find input devices
        input_devices = [d for d in devices if d['max_input_channels'] > 0]
        
        if input_devices:
            print(f"  ✅ Found {len(input_devices)} microphone(s):")
            for i, dev in enumerate(input_devices[:3]):  # Show first 3
                print(f"    • {dev['name']}")
            if len(input_devices) > 3:
                print(f"    ... and {len(input_devices)-3} more")
        else:
            print("  ❌ No microphones detected")
            print("  Connect a microphone and try again")
    except Exception as e:
        print(f"  ⚠️  Error checking microphones: {e}")
else:
    print("  ⚠️  Skipped (sounddevice not installed)")
print()

# ══════════════════════════════════════════════════════════════════
# Test 5: Test TTS
# ══════════════════════════════════════════════════════════════════

print("Test 5: Text-to-Speech")

if dependencies["pyttsx3"]:
    try:
        import pyttsx3  # type: ignore
        engine = pyttsx3.init()
        print("  ✅ TTS engine initialized")
        
        # Optionally test speaking
        user_input = input("  Test TTS? (y/n): ").strip().lower()
        if user_input == 'y':
            print("  🔊 Speaking test message...")
            engine.say("Voice control test successful")
            engine.runAndWait()
            print("  ✅ TTS test complete")
    except Exception as e:
        print(f"  ⚠️  TTS error: {e}")
else:
    print("  ⚠️  Skipped (pyttsx3 not installed)")
print()

# ══════════════════════════════════════════════════════════════════
# Test 6: Test Voice Controller (Optional)
# ══════════════════════════════════════════════════════════════════

print("Test 6: Voice Controller")

if all_installed and Path(config.VOSK_MODEL_PATH).exists():  # type: ignore
    user_input = input("  Test voice recognition? (y/n): ").strip().lower()
    if user_input == 'y':
        try:
            print()
            print("  " + "="*66)
            print("  Starting voice controller...")
            print("  Speak a command from the list below:")
            print("  " + "="*66)
            
            from gesture_engine.voice_commands import list_commands
            list_commands()
            
            from gesture_engine.voice_controller import VoiceController
            controller = VoiceController()
            controller.start()
            
            print("  🎤 Listening... (Press Ctrl+C to stop)")
            print()
            
            # Listen for 10 seconds
            import time
            for i in range(10, 0, -1):
                if not config.running:  # type: ignore
                    break
                print(f"  ⏱️  {i} seconds remaining...", end='\r')
                time.sleep(1)
            
            print()
            print("  ✅ Voice test complete")
            
            with config.state_lock:  # type: ignore
                config.running = False  # type: ignore
            
        except KeyboardInterrupt:
            print()
            print("  ⚠️  Test interrupted")
        except Exception as e:
            print(f"  ❌ Error: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("  ⏭️  Skipped by user")
else:
    print("  ⏭️  Skipped (dependencies or model missing)")
print()

# ══════════════════════════════════════════════════════════════════
# Summary
# ══════════════════════════════════════════════════════════════════

print("="*70)
print("  SUMMARY")
print("="*70)

if all_installed and Path(config.VOSK_MODEL_PATH).exists():  # type: ignore
    print()
    print("✅ All requirements satisfied!")
    print()
    print("🚀 You can now:")
    print("  1. Test voice controller: python gesture_engine/voice_controller.py")
    print("  2. Run gesture + voice: python gesture_engine/main_vosk.py")
    print("  3. Integrate with PROTOTYPE.PY")
    print()
else:
    print()
    print("⚠️  Setup incomplete. Please:")
    if not all_installed:
        print("  • Install dependencies: pip install -r requirements_vosk.txt")
    if not Path(config.VOSK_MODEL_PATH).exists():  # type: ignore
        print("  • Download Vosk model: https://alphacephei.com/vosk/models")
    print()

print("="*70)
print()
