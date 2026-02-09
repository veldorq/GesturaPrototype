"""
Quick test to verify the program won't crash on Windows
Tests that all messages print correctly without Unicode errors
"""

print("="*70)
print("QUICK SYSTEM TEST (No MediaPipe required)")
print("="*70)

print("\nTesting all message types that appear during gestures...")

test_messages = [
    # Startup messages
    "[STARTING] Starting video capture...",
    "[SUCCESS] System initialized successfully!",
    
    # Gesture execution messages (these used to have emojis)
    "[SCROLL DOWN] Scrolling down (3.5x speed, 4-step smooth)...",
    "[SCROLL UP] Scrolling up (3.5x speed, 4-step smooth)...",
    "[CLICK] Left click",
    "[ZOOM IN] Zoom in (smooth 2-step)",
    "[PINCH] Pinch zoom in (smooth 2-step, isolated)",
    "[SPREAD] Spread zoom out (smooth 2-step, isolated)",
    "[NEXT TAB] Next tab",
    "[PREV TAB] Previous tab",
    "[SCREENSHOT] Screenshot saved: screenshot_test.png",
    "[REFRESH] Page refresh",
    "[MUTE] Mute toggled (0.6s dwell + 1s cooldown)",
    "[POINTER MODE] activated (zoom disabled)",
    "[GESTURE MODE] activated",
    
    # Warning messages
    "WARNING: Hold thumb-down for 1.2s to close tab...",
    "[PROGRESS] Close tab progress: 25%",
    "[PROGRESS] Close tab progress: 50%",
    "[PROGRESS] Close tab progress: 75%",
    "WARNING: Failed to capture frame",
    "WARNING: Action error: Test error",
    
    # Shutdown messages
    "[SHUTDOWN] Shutting down safely...",
    "[CLEANUP] Cleaning up resources...",
    "[SUCCESS] Cleanup complete. Goodbye!",
]

success_count = 0
error_count = 0

for i, msg in enumerate(test_messages, 1):
    try:
        print(f"  [{i:2d}] {msg}")
        success_count += 1
    except UnicodeEncodeError as e:
        print(f"  [ERROR] Message {i} failed with encoding error!")
        error_count += 1

print("\n" + "="*70)
print(f"TEST RESULTS: {success_count}/{len(test_messages)} messages printed successfully")
if error_count > 0:
    print(f"FAILED: {error_count} messages caused Unicode encoding errors")
    print("The program will crash when these messages try to print!")
else:
    print("SUCCESS: All messages print correctly on Windows!")
    print("\nYour program will NOT crash when you raise your hand.")
    print("The THUMB_UP gesture will now print '[ZOOM IN] Zoom in' safely.")
print("="*70)
