"""
Test Pointer Movement Optimization
===================================
This tests the optimized pointer control.

Improvements:
- Reduced smoothing (0.15 from 0.3) = faster response
- Acceleration for large movements = covers screen faster
- Dead zone = no micro-jitter
- Edge dampening = no getting stuck at edges

Usage: python test_pointer.py
Point with index finger to move mouse
Press 'q' to quit
"""

import cv2
import mediapipe as mp
import pyautogui
import time

# Disable PyAutoGUI fail-safe for testing
pyautogui.FAILSAFE = False

# Config
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
MOUSE_SMOOTHING = 0.15
MOUSE_ACCELERATION = 1.5
MOUSE_DEAD_ZONE = 0.005
MOUSE_EDGE_PADDING = 50
INDEX_TIP = 8

# MediaPipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# Camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Initialize
prev_mouse_x = SCREEN_WIDTH // 2
prev_mouse_y = SCREEN_HEIGHT // 2

print("="*70)
print("  OPTIMIZED POINTER TEST")
print("="*70)
print("\nOptimizations active:")
print("  ✓ Faster response (smoothing: 0.15)")
print("  ✓ Acceleration for large movements (1.5x)")
print("  ✓ Dead zone (no micro-jitter)")
print("  ✓ Edge dampening (no stuck edges)")
print("\nPoint with INDEX FINGER to control mouse")
print("Press 'q' to quit\n")

frame_count = 0
last_print = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Get index finger position
            index_tip = hand_landmarks.landmark[INDEX_TIP]
            screen_x = int(index_tip.x * SCREEN_WIDTH)
            screen_y = int(index_tip.y * SCREEN_HEIGHT)
            
            # Calculate movement
            delta_x = screen_x - prev_mouse_x
            delta_y = screen_y - prev_mouse_y
            movement_magnitude = (delta_x**2 + delta_y**2) ** 0.5
            
            # Dead zone
            if movement_magnitude >= MOUSE_DEAD_ZONE * SCREEN_WIDTH:
                # Dynamic smoothing
                normalized_velocity = min(movement_magnitude / 100.0, 1.0)
                dynamic_smoothing = MOUSE_SMOOTHING * (1 - normalized_velocity * 0.5)
                
                # Acceleration
                if movement_magnitude > 50:
                    delta_x *= MOUSE_ACCELERATION
                    delta_y *= MOUSE_ACCELERATION
                    screen_x = int(prev_mouse_x + delta_x)
                    screen_y = int(prev_mouse_y + delta_y)
                
                # Smooth
                smooth_x = int(prev_mouse_x * dynamic_smoothing + 
                              screen_x * (1 - dynamic_smoothing))
                smooth_y = int(prev_mouse_y * dynamic_smoothing + 
                              screen_y * (1 - dynamic_smoothing))
                
                # Edge dampening
                edge_damping = 1.0
                if smooth_x < MOUSE_EDGE_PADDING:
                    edge_damping *= smooth_x / MOUSE_EDGE_PADDING
                elif smooth_x > SCREEN_WIDTH - MOUSE_EDGE_PADDING:
                    edge_damping *= (SCREEN_WIDTH - smooth_x) / MOUSE_EDGE_PADDING
                
                if smooth_y < MOUSE_EDGE_PADDING:
                    edge_damping *= smooth_y / MOUSE_EDGE_PADDING
                elif smooth_y > SCREEN_HEIGHT - MOUSE_EDGE_PADDING:
                    edge_damping *= (SCREEN_HEIGHT - smooth_y) / MOUSE_EDGE_PADDING
                
                if edge_damping < 1.0:
                    smooth_x = int(prev_mouse_x + (smooth_x - prev_mouse_x) * edge_damping)
                    smooth_y = int(prev_mouse_y + (smooth_y - prev_mouse_y) * edge_damping)
                
                # Clamp
                smooth_x = max(0, min(SCREEN_WIDTH - 1, smooth_x))
                smooth_y = max(0, min(SCREEN_HEIGHT - 1, smooth_y))
                
                # Move
                pyautogui.moveTo(smooth_x, smooth_y)
                
                prev_mouse_x = smooth_x
                prev_mouse_y = smooth_y
                
                # Print status every 0.5 seconds
                if time.time() - last_print >= 0.5:
                    speed_indicator = "FAST" if movement_magnitude > 50 else "normal"
                    print(f"Movement: {movement_magnitude:6.1f}px | Speed: {speed_indicator:5} | Edge damping: {edge_damping:.2f}")
                    last_print = time.time()
            
            # Visual feedback
            cv2.putText(frame, "POINTER MODE - Optimized", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"Movement: {movement_magnitude:.1f}", (10, 70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    
    cv2.imshow('Pointer Test', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
hands.close()
print("\nPointer test complete!")
