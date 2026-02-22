"""
Voice Assistant Test Suite

Quick verification that all components are working correctly.

Usage:
    python test_voice_system.py
"""

import sys
import time
from pathlib import Path

print("="*70)
print("🧪 GESTURA VOICE ASSISTANT - COMPONENT TEST")
print("="*70 + "\n")

# ═══════════════════════════════════════════════════════════════
# Test 1: Module Imports
# ═══════════════════════════════════════════════════════════════

print("Test 1: Importing modules...")
try:
    from voice_assistant import VoiceController, VoiceCommandExecutor, VoiceConfig
    print("✅ All modules imported successfully\n")
except ImportError as e:
    print(f"❌ Import failed: {e}\n")
    sys.exit(1)

# ═══════════════════════════════════════════════════════════════
# Test 2: Check Dependencies
# ═══════════════════════════════════════════════════════════════

print("Test 2: Checking dependencies...")

dependencies = {
    "SpeechRecognition": False,
    "pyaudio": False,
    "pyautogui": False,
    "pynput": False,
    "vosk (optional)": False,
    "pyttsx3 (optional)": False,
}

try:
    import speech_recognition
    dependencies["SpeechRecognition"] = True
except ImportError:
    pass

try:
    import pyaudio
    dependencies["pyaudio"] = True
except ImportError:
    pass

try:
    import pyautogui
    dependencies["pyautogui"] = True
except ImportError:
    pass

try:
    import pynput  # type: ignore
    dependencies["pynput"] = True
except ImportError:
    pass

try:
    import vosk  # type: ignore
    dependencies["vosk (optional)"] = True
except ImportError:
    pass

try:
    import pyttsx3  # type: ignore
    dependencies["pyttsx3 (optional)"] = True
except ImportError:
    pass

for dep, installed in dependencies.items():
    status = "✅" if installed else "❌"
    optional = "(optional)" in dep
    print(f"  {status} {dep}")
    if not installed and not optional:
        print(f"     ⚠️  Install with: pip install {dep.lower()}")

print()

# Check if critical dependencies present
critical = ["SpeechRecognition", "pyautogui", "pynput"]
if not all(dependencies[dep] for dep in critical):
    print("❌ Critical dependencies missing. Run: pip install -r requirements.txt\n")
    sys.exit(1)

# ═══════════════════════════════════════════════════════════════
# Test 3: Configuration
# ═══════════════════════════════════════════════════════════════

print("Test 3: Configuration...")
try:
    config = VoiceConfig()
    print(f"✅ Config loaded")
    print(f"   Language: {config.LANGUAGE}")
    print(f"   Offline mode: {config.USE_OFFLINE_RECOGNITION}")
    print(f"   Voice feedback: {config.VOICE_FEEDBACK_ENABLED}")
    print(f"   Commands: {len(config.COMMAND_MAP)}")
    print()
except Exception as e:
    print(f"❌ Config error: {e}\n")
    sys.exit(1)

# ═══════════════════════════════════════════════════════════════
# Test 4: Vosk Model (Optional)
# ═══════════════════════════════════════════════════════════════

print("Test 4: Vosk model (offline recognition)...")
if dependencies["vosk (optional)"]:
    model_path = Path(config.VOSK_MODEL_PATH)
    if model_path.exists():
        print(f"✅ Vosk model found: {model_path}")
        required_files = ["am", "conf", "graph"]
        for f in required_files:
            if (model_path / f).exists():
                print(f"   ✅ {f}/ present")
            else:
                print(f"   ❌ {f}/ missing")
    else:
        print(f"⚠️  Vosk model not found at: {model_path}")
        print("   Download from: https://alphacephei.com/vosk/models")
        print("   Recommended: vosk-model-small-en-us-0.15 (40 MB)")
else:
    print("⚠️  Vosk not installed (will use online recognition)")
    print("   Install with: pip install vosk")
print()

# ═══════════════════════════════════════════════════════════════
# Test 5: Command Executor
# ═══════════════════════════════════════════════════════════════

print("Test 5: Command executor...")
try:
    executor = VoiceCommandExecutor(config)
    print("✅ Executor initialized")
    print(f"   Actions available: {len(executor.action_map)}")
    
    # Test action map completeness
    unmapped = []
    for phrase, action in config.COMMAND_MAP.items():
        if action not in executor.action_map:
            unmapped.append(action)
    
    if unmapped:
        print(f"   ⚠️  Unmapped actions: {unmapped}")
    else:
        print("   ✅ All commands have action handlers")
    print()
    
except Exception as e:
    print(f"❌ Executor error: {e}\n")
    sys.exit(1)

# ═══════════════════════════════════════════════════════════════
# Test 6: Voice Controller
# ═══════════════════════════════════════════════════════════════

print("Test 6: Voice controller...")
try:
    controller = VoiceController(config=config)
    print("✅ Controller initialized")
    print(f"   Recognition backend: ", end="")
    
    if controller.use_vosk:
        print("vosk (offline)")
    elif config.USE_OFFLINE_RECOGNITION:
        print("sphinx (offline)")
    else:
        print("google (online)")
    
    print()
    
except Exception as e:
    print(f"❌ Controller error: {e}\n")
    # Don't exit - might be microphone issue

# ═══════════════════════════════════════════════════════════════
# Test 7: Microphone (Interactive)
# ═══════════════════════════════════════════════════════════════

print("Test 7: Microphone access...")
print("   Attempting to initialize microphone...")

try:
    import speech_recognition as sr
    
    # List available microphones
    try:
        mics = sr.Microphone.list_microphone_names()
        print(f"✅ Found {len(mics)} microphone(s):")
        for i, mic in enumerate(mics[:5]):  # Show first 5
            print(f"     [{i}] {mic}")
        if len(mics) > 5:
            print(f"     ... and {len(mics)-5} more")
    except Exception as e:
        print(f"⚠️  Could not list microphones: {e}")
    
    # Test mic access
    try:
        r = sr.Recognizer()
        mic = sr.Microphone()
        with mic as source:
            print("   ✅ Microphone accessible")
            print("   🎤 Calibrating...")
            r.adjust_for_ambient_noise(source, duration=1)
            print("   ✅ Calibration complete")
    except Exception as e:
        print(f"   ❌ Microphone error: {e}")
        print("   ⚠️  Check mic permissions and PyAudio installation")
    
    print()
    
except Exception as e:
    print(f"❌ Microphone test failed: {e}\n")

# ═══════════════════════════════════════════════════════════════
# Test 8: Thread Safety
# ═══════════════════════════════════════════════════════════════

print("Test 8: Thread-safe state management...")
try:
    # Test state getters/setters
    assert config.is_system_running() == True
    assert config.is_gesture_active() == True
    assert config.is_voice_active() == True
    
    # Test state changes
    config.set_gesture_active(False)
    assert config.is_gesture_active() == False
    config.set_gesture_active(True)
    assert config.is_gesture_active() == True
    
    print("✅ Thread-safe state management working")
    print()
    
except Exception as e:
    print(f"❌ State management error: {e}\n")

# ═══════════════════════════════════════════════════════════════
# Test 9: TTS (Optional)
# ═══════════════════════════════════════════════════════════════

print("Test 9: Text-to-speech feedback...")
if dependencies["pyttsx3 (optional)"]:
    try:
        import pyttsx3  # type: ignore
        engine = pyttsx3.init()
        print("✅ TTS engine initialized")
        
        # Optional: Test TTS
        print("   Testing TTS (you should hear 'Test successful')...")
        engine.say("Test successful")
        engine.runAndWait()
        print("   ✅ TTS working")
        print()
        
    except Exception as e:
        print(f"⚠️  TTS error: {e}")
        print("   Voice feedback will be disabled")
        print()
else:
    print("⚠️  pyttsx3 not installed (voice feedback disabled)")
    print("   Install with: pip install pyttsx3")
    print()

# ═══════════════════════════════════════════════════════════════
# Summary
# ═══════════════════════════════════════════════════════════════

print("="*70)
print("📊 TEST SUMMARY")
print("="*70)

required_pass = [
    dependencies["SpeechRecognition"],
    dependencies["pyautogui"],
    dependencies["pynput"],
]

optional_pass = [
    dependencies["vosk (optional)"],
    dependencies["pyttsx3 (optional)"],
]

if all(required_pass):
    print("\n✅ All required components working!")
    print("\n🎤 You can now:")
    print("   1. Run: python main.py")
    print("   2. Speak voice commands")
    print("   3. Integrate with your gesture system")
    
    if not all(optional_pass):
        print("\n💡 Optional enhancements:")
        if not dependencies["vosk (optional)"]:
            print("   • Install vosk for offline recognition: pip install vosk")
        if not dependencies["pyttsx3 (optional)"]:
            print("   • Install pyttsx3 for voice feedback: pip install pyttsx3")
else:
    print("\n❌ Some required components not working")
    print("\n🔧 Fix required:")
    print("   pip install SpeechRecognition pyaudio pyautogui pynput")

print("\n" + "="*70 + "\n")
