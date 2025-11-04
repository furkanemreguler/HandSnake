"""
Gesture Controller
Hand detection and gesture recognition using MediaPipe
"""

import cv2
import mediapipe as mp
import numpy as np
from config import *


class GestureController:
    def __init__(self):
        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=GESTURE_CONFIDENCE,
            min_tracking_confidence=GESTURE_CONFIDENCE
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # Initialize camera
        self.cap = cv2.VideoCapture(CAMERA_INDEX)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, SCREEN_HEIGHT)
        
        # Gesture detection settings
        self.last_direction = NONE
        self.gesture_threshold = 0.15  # Minimum movement to register gesture
    
    def detect_gesture(self, frame):
        """
        Detect hand gesture and return direction
        Returns: (direction, annotated_frame)
        """
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame
        results = self.hands.process(rgb_frame)
        
        direction = NONE
        
        # Draw hand landmarks and detect gesture
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw landmarks
                self.mp_draw.draw_landmarks(
                    frame, 
                    hand_landmarks, 
                    self.mp_hands.HAND_CONNECTIONS
                )
                
                # Get direction from hand position
                direction = self._get_direction_from_hand(hand_landmarks, frame.shape)
        
        # Draw direction indicator
        self._draw_direction_indicator(frame, direction)
        
        return direction, frame
    
    def _get_direction_from_hand(self, hand_landmarks, frame_shape):
        """
        Determine direction based on hand position
        Uses the position of the hand center (wrist) relative to frame center
        """
        height, width, _ = frame_shape
        
        # Get wrist position (landmark 0)
        wrist = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
        
        # Convert normalized coordinates to pixel coordinates
        wrist_x = wrist.x * width
        wrist_y = wrist.y * height
        
        # Calculate center of frame
        center_x = width / 2
        center_y = height / 2
        
        # Calculate relative position
        rel_x = (wrist_x - center_x) / width
        rel_y = (wrist_y - center_y) / height
        
        # Determine direction based on position
        # Prioritize horizontal movement over vertical
        if abs(rel_x) > abs(rel_y):
            if rel_x > self.gesture_threshold:
                return RIGHT
            elif rel_x < -self.gesture_threshold:
                return LEFT
        else:
            if rel_y > self.gesture_threshold:
                return DOWN
            elif rel_y < -self.gesture_threshold:
                return UP
        
        return NONE
    
    def _draw_direction_indicator(self, frame, direction):
        """
        Draw direction text and visual indicator on frame
        """
        height, width, _ = frame.shape
        
        # Draw direction text
        if direction != NONE:
            color = (0, 255, 0)  # Green
            text = f"Direction: {direction}"
        else:
            color = (0, 0, 255)  # Red
            text = "No Direction"
        
        cv2.putText(frame, text, (10, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        
        # Draw center crosshair
        center_x, center_y = width // 2, height // 2
        cv2.line(frame, (center_x - 20, center_y), (center_x + 20, center_y), (255, 255, 255), 2)
        cv2.line(frame, (center_x, center_y - 20), (center_x, center_y + 20), (255, 255, 255), 2)
        
        # Draw zone indicators
        self._draw_zones(frame, width, height)
    
    def _draw_zones(self, frame, width, height):
        """
        Draw colored zones to help user understand gesture areas
        """
        zone_size = int(width * self.gesture_threshold)
        center_x, center_y = width // 2, height // 2
        
        # Semi-transparent overlay
        overlay = frame.copy()
        alpha = 0.3
        
        # Left zone (blue)
        cv2.rectangle(overlay, (0, 0), (center_x - zone_size, height), (255, 0, 0), -1)
        
        # Right zone (blue)
        cv2.rectangle(overlay, (center_x + zone_size, 0), (width, height), (255, 0, 0), -1)
        
        # Up zone (green)
        cv2.rectangle(overlay, (0, 0), (width, center_y - zone_size), (0, 255, 0), -1)
        
        # Down zone (green)
        cv2.rectangle(overlay, (0, center_y + zone_size), (width, height), (0, 255, 0), -1)
        
        # Blend overlay with original frame
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
        
        # Draw zone labels
        cv2.putText(frame, "LEFT", (20, center_y), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, "RIGHT", (width - 100, center_y), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, "UP", (center_x - 20, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, "DOWN", (center_x - 40, height - 20), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    def release(self):
        """Release camera resources"""
        self.cap.release()
        self.hands.close()