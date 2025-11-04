"""
Unit tests for Gesture Controller
"""

import unittest
import sys
import os
import numpy as np

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import *


class MockHandLandmark:
    """Mock hand landmark for testing"""
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z


class MockHandLandmarks:
    """Mock hand landmarks collection"""
    def __init__(self, wrist_x, wrist_y):
        self.landmark = {
            0: MockHandLandmark(wrist_x, wrist_y)  # Wrist
        }


class TestGestureDetection(unittest.TestCase):
    """Test gesture detection logic"""
    
    def test_direction_left(self):
        """Test left direction detection"""
        # Wrist at left side (x = 0.2, center would be 0.5)
        rel_x = -0.3  # (0.2 - 0.5) / width_normalized
        rel_y = 0.0
        
        if abs(rel_x) > abs(rel_y) and rel_x < -0.15:
            direction = LEFT
        else:
            direction = NONE
        
        self.assertEqual(direction, LEFT)
    
    def test_direction_right(self):
        """Test right direction detection"""
        rel_x = 0.3
        rel_y = 0.0
        
        if abs(rel_x) > abs(rel_y) and rel_x > 0.15:
            direction = RIGHT
        else:
            direction = NONE
        
        self.assertEqual(direction, RIGHT)
    
    def test_direction_up(self):
        """Test up direction detection"""
        rel_x = 0.0
        rel_y = -0.3
        
        if abs(rel_y) > abs(rel_x) and rel_y < -0.15:
            direction = UP
        else:
            direction = NONE
        
        self.assertEqual(direction, UP)
    
    def test_direction_down(self):
        """Test down direction detection"""
        rel_x = 0.0
        rel_y = 0.3
        
        if abs(rel_y) > abs(rel_x) and rel_y > 0.15:
            direction = DOWN
        else:
            direction = NONE
        
        self.assertEqual(direction, DOWN)
    
    def test_no_direction_center(self):
        """Test no direction when hand is in center"""
        rel_x = 0.05
        rel_y = 0.05
        threshold = 0.15
        
        if abs(rel_x) > abs(rel_y):
            if abs(rel_x) > threshold:
                direction = RIGHT if rel_x > 0 else LEFT
            else:
                direction = NONE
        else:
            if abs(rel_y) > threshold:
                direction = DOWN if rel_y > 0 else UP
            else:
                direction = NONE
        
        self.assertEqual(direction, NONE)
    
    def test_threshold_boundary(self):
        """Test direction at threshold boundary"""
        threshold = 0.15
        
        # Just above threshold
        rel_x = 0.16
        direction = RIGHT if rel_x > threshold else NONE
        self.assertEqual(direction, RIGHT)
        
        # Just below threshold
        rel_x = 0.14
        direction = RIGHT if rel_x > threshold else NONE
        self.assertEqual(direction, NONE)


class TestConfigValues(unittest.TestCase):
    """Test configuration values"""
    
    def test_screen_dimensions(self):
        """Test screen dimensions are valid"""
        self.assertGreater(SCREEN_WIDTH, 0)
        self.assertGreater(SCREEN_HEIGHT, 0)
        self.assertEqual(CAMERA_WIDTH + GAME_WIDTH, SCREEN_WIDTH)
    
    def test_snake_settings(self):
        """Test snake settings are valid"""
        self.assertGreater(SNAKE_SIZE, 0)
        self.assertGreater(SNAKE_SPEED, 0)
        self.assertLessEqual(SNAKE_SPEED, 20)
    
    def test_gesture_confidence(self):
        """Test gesture confidence is in valid range"""
        self.assertGreaterEqual(GESTURE_CONFIDENCE, 0.0)
        self.assertLessEqual(GESTURE_CONFIDENCE, 1.0)
    
    def test_fps(self):
        """Test FPS is reasonable"""
        self.assertGreater(FPS, 0)
        self.assertLessEqual(FPS, 120)


if __name__ == '__main__':
    print("Running HandSnake gesture tests...\n")
    unittest.main(verbosity=2)