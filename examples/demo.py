"""
HandSnake - Demo Script
Simple demonstration of hand detection without the full game
"""

import cv2
import mediapipe as mp
import sys
import os

# Add parent directory to path to import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import *


def main():
    """Run simple hand detection demo"""
    print("=" * 50)
    print("HandSnake - Hand Detection Demo")
    print("=" * 50)
    print("\nThis demo shows hand tracking without the game.")
    print("Move your hand to see detection in action.")
    print("Press 'q' to quit\n")
    
    # Initialize MediaPipe
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    )
    mp_draw = mp.solutions.drawing_utils
    
    # Initialize camera
    cap = cv2.VideoCapture(CAMERA_INDEX)
    
    if not cap.isOpened():
        print("Error: Cannot open camera")
        print("Try changing CAMERA_INDEX in config.py")
        return
    
    print("Camera opened successfully!")
    print("Showing hand detection...")
    
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error reading frame")
            break
        
        # Flip frame horizontally
        frame = cv2.flip(frame, 1)
        
        # Convert to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process frame
        results = hands.process(rgb_frame)
        
        # Draw hand landmarks
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw landmarks
                mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )
                
                # Get wrist position
                wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                h, w, _ = frame.shape
                
                wrist_x = int(wrist.x * w)
                wrist_y = int(wrist.y * h)
                
                # Draw wrist position
                cv2.circle(frame, (wrist_x, wrist_y), 10, (0, 255, 0), -1)
                
                # Calculate direction
                center_x, center_y = w // 2, h // 2
                rel_x = (wrist_x - center_x) / w
                rel_y = (wrist_y - center_y) / h
                
                direction = "NONE"
                if abs(rel_x) > abs(rel_y):
                    if rel_x > 0.15:
                        direction = "RIGHT"
                    elif rel_x < -0.15:
                        direction = "LEFT"
                else:
                    if rel_y > 0.15:
                        direction = "DOWN"
                    elif rel_y < -0.15:
                        direction = "UP"
                
                # Display direction
                cv2.putText(frame, f"Direction: {direction}", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, "Hand Detected!", (10, 70),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "No Hand Detected", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        # Draw center crosshair
        h, w, _ = frame.shape
        center_x, center_y = w // 2, h // 2
        cv2.line(frame, (center_x - 30, center_y), (center_x + 30, center_y), (255, 255, 255), 2)
        cv2.line(frame, (center_x, center_y - 30), (center_x, center_y + 30), (255, 255, 255), 2)
        
        # Show FPS
        frame_count += 1
        cv2.putText(frame, f"Frame: {frame_count}", (10, h - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Display frame
        cv2.imshow('HandSnake - Demo', frame)
        
        # Check for quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Cleanup
    cap.release()
    hands.close()
    cv2.destroyAllWindows()
    
    print("\nDemo finished!")
    print(f"Total frames processed: {frame_count}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()