"""
Quick Test for Closed Fist Detection
=====================================
This script helps test if closed fist (scroll up) is being detected properly.

It shows:
- Finger count (should be 0 for closed fist)  
- Which fingers are detected as extended
- When CLOSED_FIST gesture is recognized

Usage: python test_closed_fist.py
Press 'q' to quit
"""

import cv2
import mediapipe as mp
import time

# MediaPipe setup
mp_hands = mp.solutions.hands  # type: ignore
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils  # type: ignore

# Open camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Landmark indices
INDEX_TIP = 8
INDEX_DIP = 7
INDEX_MCP = 5
MIDDLE_TIP = 12
MIDDLE_DIP = 11
MIDDLE_MCP = 9
RING_TIP = 16
RING_DIP = 15
RING_MCP = 13
PINKY_TIP = 20
PINKY_DIP = 19
PINKY_MCP = 17
THUMB_TIP = 4
THUMB_IP = 3
WRIST = 0

FINGER_EXTENSION_THRESHOLD = 0.02  # Same as PROTOTYPE.PY

def is_finger_extended(landmarks, finger_tip, finger_dip, finger_mcp):
    """Check if finger is extended using improved threshold logic"""
    tip_y = landmarks[finger_tip].y
    dip_y = landmarks[finger_dip].y
    mcp_y = landmarks[finger_mcp].y
    
    is_tip_above_dip = (tip_y + FINGER_EXTENSION_THRESHOLD) < dip_y
    is_dip_above_mcp = (dip_y + FINGER_EXTENSION_THRESHOLD) < mcp_y
    
    return is_tip_above_dip and is_dip_above_mcp

def is_thumb_extended(landmarks):
    """Check if thumb is extended"""
    thumb_tip = landmarks[THUMB_TIP]
    thumb_ip = landmarks[THUMB_IP]
    thumb_mcp = landmarks[2]
    wrist = landmarks[WRIST]
    
    tip_dist = ((thumb_tip.x - wrist.x)**2 + (thumb_tip.y - wrist.y)**2) ** 0.5
    ip_dist = ((thumb_ip.x - wrist.x)**2 + (thumb_ip.y - wrist.y)**2) ** 0.5
    mcp_dist = ((thumb_mcp.x - wrist.x)**2 + (thumb_mcp.y - wrist.y)**2) ** 0.5
    
    return tip_dist > ip_dist and ip_dist > mcp_dist * 0.8

def count_fingers(landmarks):
    """Count extended fingers (thumb ignored by default)"""
    fingers = {
        'index': is_finger_extended(landmarks, INDEX_TIP, INDEX_DIP, INDEX_MCP),
        'middle': is_finger_extended(landmarks, MIDDLE_TIP, MIDDLE_DIP, MIDDLE_MCP),
        'ring': is_finger_extended(landmarks, RING_TIP, RING_DIP, RING_MCP),
        'pinky': is_finger_extended(landmarks, PINKY_TIP, PINKY_DIP, PINKY_MCP),
        'thumb': is_thumb_extended(landmarks)
    }
    
    # Count without thumb (default mode)
    count_no_thumb = sum([fingers['index'], fingers['middle'], fingers['ring'], fingers['pinky']])
    
    return count_no_thumb, fingers

print("="*70)
print("  CLOSED FIST DETECTION TEST")
print("="*70)
print("\nMake a CLOSED FIST (all fingers folded)")
print("  → Should show: Count = 0")
print("  → Should detect: CLOSED_FIST ✓")
print("\nPress 'q' to quit\n")

frame_count = 0
last_gesture = None
gesture_start_time = None

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    
    # Draw hand landmarks
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            landmarks = hand_landmarks.landmark
            count, fingers = count_fingers(landmarks)
            
            # Print status every 10 frames
            frame_count += 1
            if frame_count % 10 == 0:
                extended = [k for k, v in fingers.items() if v and k != 'thumb']
                print(f"Finger count: {count} | Extended: {extended if extended else 'None'}")
                
                if count == 0:
                    print("  → CLOSED_FIST ✓ (Ready for scroll up)")
                    if last_gesture != 'CLOSED_FIST':
                        gesture_start_time = time.time()
                        last_gesture = 'CLOSED_FIST'
                        print("  → Hold for 0.15s to trigger scroll...")
                    elif gesture_start_time is not None and time.time() - gesture_start_time >= 0.15:
                        print("  → [SCROLL UP] Would trigger now!")
                else:
                    last_gesture = None
            
            # Display info on frame
            text = f"Fingers: {count}"
            cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            if count == 0:
                status = "CLOSED_FIST - Ready for scroll up!"
                color = (0, 255, 0)
            else:
                status = f"Not closed fist (fingers: {count})"
                color = (0, 0, 255)
            
            cv2.putText(frame, status, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    
    cv2.imshow('Closed Fist Test', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
hands.close()
print("\nTest complete!")
