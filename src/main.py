"""
HandSnake - Main Application
Control Snake game with hand gestures
"""

import cv2
import pygame
import numpy as np
from snake_game import SnakeGame
from gesture_controller import GestureController
from config import *


class HandSnake:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("HandSnake - Control Snake with Hand Gestures")
        
        # Initialize game and gesture controller
        self.snake_game = SnakeGame(GAME_WIDTH, SCREEN_HEIGHT)
        self.gesture_controller = GestureController()
        
        # Game state
        self.running = True
        self.paused = False
        self.clock = pygame.time.Clock()
        self.current_direction = None
        
        # Frame counter for game update speed
        self.frame_count = 0
        self.update_frequency = FPS // SNAKE_SPEED
        
    def process_camera(self):
        """Process camera feed and detect gestures"""
        ret, frame = self.gesture_controller.cap.read()
        if not ret:
            return None
            
        # Flip frame horizontally for mirror effect
        frame = cv2.flip(frame, 1)
        
        # Detect gesture
        direction, annotated_frame = self.gesture_controller.detect_gesture(frame)
        
        if direction != NONE:
            self.current_direction = direction
        
        # Resize frame to fit half screen
        annotated_frame = cv2.resize(annotated_frame, (CAMERA_WIDTH, SCREEN_HEIGHT))
        
        return annotated_frame
    
    def draw_camera_feed(self, frame):
        """Draw camera feed on left side of screen"""
        if frame is not None:
            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Rotate frame for Pygame (OpenCV uses different coordinate system)
            frame_rgb = np.rot90(frame_rgb)
            frame_rgb = np.flipud(frame_rgb)
            
            # Convert to Pygame surface
            frame_surface = pygame.surfarray.make_surface(frame_rgb)
            
            # Draw on screen (left side)
            self.screen.blit(frame_surface, (0, 0))
    
    def draw_instructions(self):
        """Draw instructions overlay"""
        font = pygame.font.Font(None, 24)
        instructions = [
            "Move your hand to control the snake:",
            "LEFT - Move hand to left",
            "RIGHT - Move hand to right", 
            "UP - Move hand up",
            "DOWN - Move hand down",
            "",
            "Press P - Pause/Resume",
            "Press R - Restart Game",
            "Press ESC - Quit"
        ]
        
        y_offset = SCREEN_HEIGHT - 220
        for i, instruction in enumerate(instructions):
            text = font.render(instruction, True, WHITE)
            # Draw text with shadow for better visibility
            shadow = font.render(instruction, True, BLACK)
            self.screen.blit(shadow, (12, y_offset + i * 25 + 2))
            self.screen.blit(text, (10, y_offset + i * 25))
    
    def draw_separator(self):
        """Draw vertical line separating camera and game"""
        pygame.draw.line(self.screen, WHITE, 
                        (CAMERA_WIDTH, 0), 
                        (CAMERA_WIDTH, SCREEN_HEIGHT), 3)
    
    def handle_events(self):
        """Handle keyboard events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                # Quit game
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                
                # Restart game
                elif event.key == pygame.K_r:
                    self.snake_game.reset()
                    self.current_direction = None
                
                # Pause game
                elif event.key == pygame.K_p:
                    self.paused = not self.paused
                
                # Manual controls (for testing)
                elif event.key == pygame.K_UP:
                    self.current_direction = UP
                elif event.key == pygame.K_DOWN:
                    self.current_direction = DOWN
                elif event.key == pygame.K_LEFT:
                    self.current_direction = LEFT
                elif event.key == pygame.K_RIGHT:
                    self.current_direction = RIGHT
    
    def run(self):
        """Main game loop"""
        print("HandSnake Started!")
        print("Move your hand in front of the camera to control the snake")
        print("Press ESC to quit")
        
        while self.running:
            # Handle events
            self.handle_events()
            
            # Process camera feed
            camera_frame = self.process_camera()
            
            # Update game (at controlled speed)
            if not self.paused and not self.snake_game.game_over:
                self.frame_count += 1
                if self.frame_count >= self.update_frequency:
                    self.snake_game.update(self.current_direction)
                    self.frame_count = 0
            
            # Draw everything
            self.screen.fill(BLACK)
            
            # Draw camera feed (left side)
            self.draw_camera_feed(camera_frame)
            
            # Draw separator
            self.draw_separator()
            
            # Draw game (right side)
            self.snake_game.draw(self.screen, offset_x=CAMERA_WIDTH)
            
            # Draw instructions
            self.draw_instructions()
            
            # Draw pause indicator
            if self.paused:
                font = pygame.font.Font(None, 72)
                pause_text = font.render("PAUSED", True, YELLOW)
                text_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                self.screen.blit(pause_text, text_rect)
            
            # Update display
            pygame.display.flip()
            
            # Control frame rate
            self.clock.tick(FPS)
        
        # Cleanup
        self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        self.gesture_controller.release()
        pygame.quit()
        print("HandSnake closed. Thanks for playing!")


def main():
    """Entry point"""
    try:
        game = HandSnake()
        game.run()
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()