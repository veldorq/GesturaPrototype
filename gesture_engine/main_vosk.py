# main.py
# Entry point for Gestura with Vosk-based voice control.
# Runs gesture detection (OpenCV + MediaPipe) and voice control concurrently.

import cv2
import mediapipe as mp
import time
from gesture_engine import config
from gesture_engine.voice_controller import VoiceController


def run_gesture_loop() -> None:
    """
    Main gesture detection loop.
    Reads config.gesture_active to pause/resume detection.
    Reads config.running to know when to shut down.
    Replace the interior with your full GesturaPipeline if available.
    """
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[Gesture] ERROR: Could not open webcam.")
        with config.state_lock:
            config.running = False
        return

    mp_hands = mp.solutions.hands  # type: ignore
    mp_draw = mp.solutions.drawing_utils  # type: ignore

    with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.6,
    ) as hands:

        print("[Gesture] Starting gesture loop.")
        
        fps_counter = 0
        fps_start_time = time.time()
        current_fps = 0

        while config.running:
            ret, frame = cap.read()
            if not ret:
                print("[Gesture] Frame capture failed.")
                break

            frame = cv2.flip(frame, 1)

            # ── Pause gate ────────────────────────────────────────────────────
            # When voice says "pause gestura", skip all detection processing.
            with config.state_lock:
                active = config.gesture_active

            if not active:
                # Display paused message
                cv2.putText(
                    frame, 
                    "GESTURA PAUSED (Voice Control Active)", 
                    (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    1.0, 
                    (0, 0, 255), 
                    2
                )
                cv2.putText(
                    frame,
                    'Say "resume gestura" to continue',
                    (10, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 0, 255),
                    1
                )
                cv2.imshow("Gestura", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    with config.state_lock:
                        config.running = False
                continue

            # ── Gesture detection ─────────────────────────────────────────────
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_draw.draw_landmarks(
                        frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
                    )
                    # ── Plug your GesturaPipeline here ────────────────────────
                    # e.g. debug = pipeline.process_frame(frame)
                    # pipeline.draw_debug(frame, debug)

            # Calculate FPS
            fps_counter += 1
            if fps_counter >= 30:
                elapsed = time.time() - fps_start_time
                current_fps = fps_counter / elapsed if elapsed > 0 else 0
                fps_counter = 0
                fps_start_time = time.time()

            # Display status
            cv2.putText(
                frame,
                f"Gestura Active | FPS: {int(current_fps)}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )
            cv2.putText(
                frame,
                'Press "q" to quit | Say "pause gestura" to pause',
                (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1
            )

            cv2.imshow("Gestura", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                with config.state_lock:
                    config.running = False

    cap.release()
    cv2.destroyAllWindows()
    print("[Gesture] Loop exited.")


def main() -> None:
    """Main entry point for Gestura."""
    print("=" * 70)
    print("  GESTURA 3.0 — Gesture + Voice Control System (Vosk-based)")
    print("=" * 70)
    print()
    
    # Start voice controller in background thread
    voice = None
    try:
        voice = VoiceController()
        voice.start()
        print()
    except Exception as e:
        print(f"[Main] ⚠️  Voice control not available: {e}")
        print("[Main] Continuing with gestures only...")
        print()
    
    print("=" * 70)
    print("  VOICE COMMANDS AVAILABLE")
    print("=" * 70)
    from gesture_engine.voice_commands import list_commands
    list_commands()
    
    print("=" * 70)
    print("  STARTING GESTURE RECOGNITION")
    print("=" * 70)
    print()
    
    # Run gesture loop on main thread (OpenCV requires main thread on macOS/Windows)
    try:
        run_gesture_loop()
    except KeyboardInterrupt:
        print("\n[Main] ⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n[Main] ❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Ensure clean shutdown
    print()
    print("=" * 70)
    print("  SHUTTING DOWN")
    print("=" * 70)
    
    with config.state_lock:
        config.running = False

    if voice:
        voice.stop()
    
    print("[Main] ✅ Gestura shut down cleanly.")
    print()


if __name__ == "__main__":
    main()
