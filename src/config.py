"""
Configuration file for GestureSnake
All constants and settings in one place
"""

# Screen settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
CAMERA_WIDTH = SCREEN_WIDTH // 2
GAME_WIDTH = SCREEN_WIDTH // 2
FPS = 30

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

# Snake settings
SNAKE_SIZE = 20
SNAKE_SPEED = 10
INITIAL_LENGTH = 3

# Gesture settings
GESTURE_CONFIDENCE = 0.7
CAMERA_INDEX = 0

# Gesture directions
UP = "UP"
DOWN = "DOWN"
LEFT = "LEFT"
RIGHT = "RIGHT"
NONE = "NONE"

# Font settings
FONT_SIZE = 36
SMALL_FONT_SIZE = 24