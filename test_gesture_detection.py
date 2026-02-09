"""
Quick Gesture Detection Test
=============================
Tests if your camera and gesture recognition are working.
Shows real-time gesture detection to help diagnose issues.
"""

import cv2
import mediapipe as mp
import sys
import time

def test_camera_and_gestures():
    """Test camera and basic gesture detection"""
    
    print("\n" + "="*70)
    print("  GESTURE DETECTION DIAGNOSTIC TEST")
    print("="*70)
    print("\nThis test will:")
    print("  1. Open your webcam")
    print("  2. Detect your hand using MediaPipe")
    print("  3. Count extended fingers")
    print("  4. Show real-time detection feedback")
    print("\nPress 'q' to quit")
    print("="*70 + "\n")
    
    # Initialize MediaPipe
    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils
    
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    )
    
    # Open camera
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("[ERROR] Cannot open camera!")
        print("Please check:")
        print("  - Camera is connected")
        print("  - No other app is using the camera")
        print("  - Camera permissions are granted")
        return
    
    print("[OK] Camera opened successfully")
    print("\nShow your hand to the camera...")
    print("Try these gestures:")
    print("  - Open palm (5 fingers extended)")
    print("  - Closed fist (0 fingers extended)")
    print("  - Index finger only (1 finger extended)")
    print("  - Peace sign (2 fingers extended)")
    print("\n")
    
    frame_count = 0
    hand_detected_count = 0
    
    try:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                print("[WARNING] Failed to capture frame")
                continue
            
            frame_count += 1
            
            # Flip for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Convert to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process frame
            results = hands.process(rgb_frame)
            
            # Draw on frame
            status_text = "No hand detected"
            status_color = (0, 0, 255)  # Red
            
            if results.multi_hand_landmarks:
                hand_detected_count += 1
                hand_landmarks = results.multi_hand_landmarks[0]
                
                # Draw hand landmarks
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                # Count extended fingers
                landmarks = hand_landmarks.landmark
                
                # Simple finger counting logic
                finger_tips = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky
                finger_pips = [6, 10, 14, 18]
                
                extended_count = 0
                
                # Check each finger
                for tip, pip in zip(finger_tips, finger_pips):
                    if landmarks[tip].y < landmarks[pip].y:
                        extended_count += 1
                
                # Check thumb (different logic)
                if landmarks[4].x < landmarks[3].x:  # Assuming right hand
                    extended_count += 1
                
                status_text = f"Hand detected! Fingers extended: {extended_count}"
                status_color = (0, 255, 0)  # Green
                
                # Gesture interpretation
                gesture_name = "Unknown"
                if extended_count == 0:
                    gesture_name = "CLOSED FIST (Scroll Up)"
                elif extended_count == 1:
                    gesture_name = "ONE FINGER (Pointer/Click)"
                elif extended_count == 2:
                    gesture_name = "TWO FINGERS (Peace/Click)"
                elif extended_count == 5:
                    gesture_name = "OPEN PALM (Scroll Down)"
                else:
                    gesture_name = f"{extended_count} FINGERS"
                
                # Display gesture
                cv2.putText(frame, gesture_name, (20, 120),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
            
            # Display status
            cv2.putText(frame, status_text, (20, 40),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)
            
            # Display instructions
            cv2.putText(frame, "Press 'q' to quit", (20, 80),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
            
            # Show frame
            cv2.imshow('Gesture Detection Test', frame)
            
            # Check for quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    except KeyboardInterrupt:
        print("\n[INTERRUPTED] Test stopped by user")
    
    finally:
        # Cleanup
        cap.release()
        cv2.destroyAllWindows()
        hands.close()
        
        # Print statistics
        print("\n" + "="*70)
        print("  TEST RESULTS")
        print("="*70)
        print(f"Total frames processed: {frame_count}")
        print(f"Frames with hand detected: {hand_detected_count}")
        
        if hand_detected_count > 0:
            detection_rate = (hand_detected_count / frame_count) * 100
            print(f"Detection rate: {detection_rate:.1f}%")
            
            if detection_rate > 80:
                print("\n✓ EXCELLENT - Hand detection working well!")
            elif detection_rate > 50:
                print("\n✓ GOOD - Hand detection working, but could be better")
                print("  Tips: Ensure good lighting, clear background, hand in frame")
            else:
                print("\n⚠ POOR - Hand detection struggling")
                print("  Tips:")
                print("    - Improve lighting")
                print("    - Use plain background")
                print("    - Keep hand in center of frame")
                print("    - Move hand closer or farther from camera")
        else:
            print("\n✗ NO HAND DETECTED")
            print("  Possible issues:")
            print("    - Hand not in camera view")
            print("    - Poor lighting")
            print("    - Camera issue")
            print("    - MediaPipe not working properly")
        
        print("="*70 + "\n")


if __name__ == "__main__":
    test_camera_and_gestures()
