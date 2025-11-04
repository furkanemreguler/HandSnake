"""
Unit tests for Snake Game
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.snake_game import Snake, Food
from src.config import *


class TestSnake(unittest.TestCase):
    """Test Snake class"""
    
    def setUp(self):
        """Set up test snake"""
        self.snake = Snake(100, 100)
    
    def test_initial_position(self):
        """Test snake initial position"""
        self.assertEqual(len(self.snake.body), 1)
        self.assertEqual(self.snake.body[0], (100, 100))
    
    def test_initial_direction(self):
        """Test snake initial direction"""
        self.assertEqual(self.snake.direction, RIGHT)
    
    def test_move_right(self):
        """Test moving right"""
        initial_x = self.snake.body[0][0]
        self.snake.move()
        new_x = self.snake.body[0][0]
        self.assertEqual(new_x, initial_x + SNAKE_SIZE)
    
    def test_move_up(self):
        """Test moving up"""
        self.snake.direction = UP
        initial_y = self.snake.body[0][1]
        self.snake.move()
        new_y = self.snake.body[0][1]
        self.assertEqual(new_y, initial_y - SNAKE_SIZE)
    
    def test_change_direction(self):
        """Test changing direction"""
        self.snake.change_direction(UP)
        self.assertEqual(self.snake.direction, UP)
    
    def test_prevent_opposite_direction(self):
        """Test that snake cannot move in opposite direction"""
        self.snake.direction = RIGHT
        self.snake.change_direction(LEFT)
        self.assertEqual(self.snake.direction, RIGHT)  # Should not change
    
    def test_grow(self):
        """Test snake growth"""
        initial_length = len(self.snake.body)
        self.snake.grow_snake()
        self.snake.move()
        new_length = len(self.snake.body)
        self.assertEqual(new_length, initial_length + 1)
    
    def test_wall_collision(self):
        """Test collision with wall"""
        # Move snake to left edge
        self.snake.body = [(0, 100)]
        self.snake.direction = LEFT
        self.snake.move()
        collision = self.snake.check_collision(640, 480)
        self.assertTrue(collision)
    
    def test_self_collision(self):
        """Test collision with self"""
        # Create a snake that will collide with itself
        self.snake.body = [(100, 100), (80, 100), (60, 100), (60, 80), (80, 80), (100, 80)]
        self.snake.direction = DOWN
        self.snake.move()
        collision = self.snake.check_collision(640, 480)
        self.assertTrue(collision)


class TestFood(unittest.TestCase):
    """Test Food class"""
    
    def setUp(self):
        """Set up test food"""
        self.food = Food(640, 480)
    
    def test_food_position(self):
        """Test food spawns within bounds"""
        x, y = self.food.position
        self.assertGreaterEqual(x, 0)
        self.assertGreaterEqual(y, 0)
        self.assertLess(x, 640)
        self.assertLess(y, 480)
    
    def test_food_alignment(self):
        """Test food aligns with grid"""
        x, y = self.food.position
        self.assertEqual(x % SNAKE_SIZE, 0)
        self.assertEqual(y % SNAKE_SIZE, 0)
    
    def test_respawn_avoids_snake(self):
        """Test food respawns away from snake"""
        snake_body = [(100, 100), (80, 100), (60, 100)]
        self.food.respawn(snake_body)
        self.assertNotIn(self.food.position, snake_body)


if __name__ == '__main__':
    print("Running HandSnake unit tests...\n")
    unittest.main(verbosity=2)