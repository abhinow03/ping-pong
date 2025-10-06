import pygame
import random

class Paddle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 7
        self.ai_reaction_delay = 0  # Frames to wait before reacting
        self.ai_error_margin = 15  # Pixels of intentional error

    def move(self, dy, screen_height):
        """Move paddle with boundary checking"""
        self.y += dy
        self.y = max(0, min(self.y, screen_height - self.height))

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def auto_track(self, ball, screen_height):
        """
        AI tracking with difficulty settings - not perfect!
        Makes occasional mistakes and has reaction delay
        """
        # Add reaction delay (AI doesn't react instantly)
        if self.ai_reaction_delay > 0:
            self.ai_reaction_delay -= 1
            return
        
        # Calculate target position with error margin
        target_y = ball.y - self.height // 2
        error = random.randint(-self.ai_error_margin, self.ai_error_margin)
        target_y += error
        
        # Calculate center of paddle
        paddle_center = self.y + self.height // 2
        ball_center = ball.y + ball.height // 2
        
        # Only move if ball is moving towards AI (right direction)
        if ball.velocity_x > 0:
            # Move towards ball with some imperfection
            if ball_center < paddle_center - 10:
                self.move(-self.speed, screen_height)
            elif ball_center > paddle_center + 10:
                self.move(self.speed, screen_height)
            
            # Randomly add small reaction delay
            if random.random() < 0.05:  # 5% chance each frame
                self.ai_reaction_delay = random.randint(2, 8)
        else:
            # Return to center when ball is moving away (less aggressive)
            center_screen = screen_height // 2 - self.height // 2
            if self.y < center_screen - 20:
                self.move(self.speed // 2, screen_height)
            elif self.y > center_screen + 20:
                self.move(-self.speed // 2, screen_height)