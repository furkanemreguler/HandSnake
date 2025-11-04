"""
Snake Game Logic
Classic snake game implementation with Pygame
"""

import pygame
import random
from config import *


class Snake:
    def __init__(self, x, y):
        self.body = [(x, y)]
        self.direction = RIGHT
        self.grow = False
        
    def move(self):
        head_x, head_y = self.body[0]
        
        # Calculate new head position based on direction
        if self.direction == UP:
            new_head = (head_x, head_y - SNAKE_SIZE)
        elif self.direction == DOWN:
            new_head = (head_x, head_y + SNAKE_SIZE)
        elif self.direction == LEFT:
            new_head = (head_x - SNAKE_SIZE, head_y)
        elif self.direction == RIGHT:
            new_head = (head_x + SNAKE_SIZE, head_y)
        else:
            new_head = (head_x, head_y)
        
        # Insert new head
        self.body.insert(0, new_head)
        
        # Remove tail unless growing
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
    
    def change_direction(self, new_direction):
        # Prevent moving in opposite direction
        opposite_directions = {
            UP: DOWN,
            DOWN: UP,
            LEFT: RIGHT,
            RIGHT: LEFT
        }
        
        if new_direction != opposite_directions.get(self.direction):
            self.direction = new_direction
    
    def grow_snake(self):
        self.grow = True
    
    def check_collision(self, width, height):
        head_x, head_y = self.body[0]
        
        # Wall collision
        if head_x < 0 or head_x >= width or head_y < 0 or head_y >= height:
            return True
        
        # Self collision
        if self.body[0] in self.body[1:]:
            return True
        
        return False
    
    def draw(self, surface, offset_x=0):
        for i, (x, y) in enumerate(self.body):
            color = GREEN if i == 0 else CYAN  # Head is green, body is cyan
            pygame.draw.rect(surface, color, (x + offset_x, y, SNAKE_SIZE, SNAKE_SIZE))
            pygame.draw.rect(surface, BLACK, (x + offset_x, y, SNAKE_SIZE, SNAKE_SIZE), 1)


class Food:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.position = self.spawn()
    
    def spawn(self):
        x = random.randint(0, (self.width - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
        y = random.randint(0, (self.height - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
        return (x, y)
    
    def respawn(self, snake_body):
        while True:
            self.position = self.spawn()
            if self.position not in snake_body:
                break
    
    def draw(self, surface, offset_x=0):
        x, y = self.position
        pygame.draw.rect(surface, RED, (x + offset_x, y, SNAKE_SIZE, SNAKE_SIZE))
        pygame.draw.rect(surface, BLACK, (x + offset_x, y, SNAKE_SIZE, SNAKE_SIZE), 1)


class SnakeGame:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.reset()
        
        # Fonts
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.small_font = pygame.font.Font(None, SMALL_FONT_SIZE)
    
    def reset(self):
        start_x = self.width // 2
        start_y = self.height // 2
        self.snake = Snake(start_x, start_y)
        self.food = Food(self.width, self.height)
        self.score = 0
        self.game_over = False
    
    def update(self, direction=None):
        if self.game_over:
            return
        
        # Change direction if provided
        if direction:
            self.snake.change_direction(direction)
        
        # Move snake
        self.snake.move()
        
        # Check food collision
        if self.snake.body[0] == self.food.position:
            self.snake.grow_snake()
            self.food.respawn(self.snake.body)
            self.score += 10
        
        # Check collisions
        if self.snake.check_collision(self.width, self.height):
            self.game_over = True
    
    def draw(self, surface, offset_x=0):
        # Draw game area background
        game_area = pygame.Rect(offset_x, 0, self.width, self.height)
        pygame.draw.rect(surface, BLACK, game_area)
        
        # Draw grid lines (optional, for better visibility)
        for x in range(0, self.width, SNAKE_SIZE):
            pygame.draw.line(surface, (30, 30, 30), (offset_x + x, 0), (offset_x + x, self.height))
        for y in range(0, self.height, SNAKE_SIZE):
            pygame.draw.line(surface, (30, 30, 30), (offset_x, y), (offset_x + self.width, y))
        
        # Draw food and snake
        self.food.draw(surface, offset_x)
        self.snake.draw(surface, offset_x)
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        surface.blit(score_text, (offset_x + 10, 10))
        
        # Draw direction indicator
        direction_text = self.small_font.render(f"Direction: {self.snake.direction}", True, YELLOW)
        surface.blit(direction_text, (offset_x + 10, 50))
        
        # Draw game over message
        if self.game_over:
            game_over_text = self.font.render("GAME OVER!", True, RED)
            restart_text = self.small_font.render("Press R to Restart", True, WHITE)
            
            text_rect = game_over_text.get_rect(center=(offset_x + self.width // 2, self.height // 2))
            restart_rect = restart_text.get_rect(center=(offset_x + self.width // 2, self.height // 2 + 40))
            
            surface.blit(game_over_text, text_rect)
            surface.blit(restart_text, restart_rect)