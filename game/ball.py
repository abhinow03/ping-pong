import pygame
import random
import math

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.speed = 5  # Base speed
        self.max_speed = 12  # Maximum speed
        self.velocity_x = random.choice([-1, 1]) * self.speed
        self.velocity_y = random.choice([-1, 1]) * self.speed * 0.6

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Bounce off top and bottom walls
        if self.y <= 0:
            self.y = 0
            self.velocity_y *= -1
        elif self.y + self.height >= self.screen_height:
            self.y = self.screen_height - self.height
            self.velocity_y *= -1

    def check_collision(self, player, ai):
        """
        Improved collision detection that prevents ball from getting stuck
        Returns True if collision occurred
        """
        ball_rect = self.rect()
        player_rect = player.rect()
        ai_rect = ai.rect()
        
        collision_occurred = False
        
        # Check player paddle collision
        if ball_rect.colliderect(player_rect) and self.velocity_x < 0:
            # Position ball just outside paddle
            self.x = player_rect.right
            
            # Calculate hit position for angle variation
            hit_pos = (self.y + self.height/2) - (player.y + player.height/2)
            normalized_hit = hit_pos / (player.height/2)  # -1 to 1
            
            # Reverse horizontal direction and add spin
            self.velocity_x = abs(self.velocity_x)
            self.velocity_y = normalized_hit * self.speed * 0.8
            
            # Increase speed slightly (with max cap)
            self.increase_speed()
            collision_occurred = True
        
        # Check AI paddle collision
        elif ball_rect.colliderect(ai_rect) and self.velocity_x > 0:
            # Position ball just outside paddle
            self.x = ai_rect.left - self.width
            
            # Calculate hit position for angle variation
            hit_pos = (self.y + self.height/2) - (ai.y + ai.height/2)
            normalized_hit = hit_pos / (ai.height/2)  # -1 to 1
            
            # Reverse horizontal direction and add spin
            self.velocity_x = -abs(self.velocity_x)
            self.velocity_y = normalized_hit * self.speed * 0.8
            
            # Increase speed slightly (with max cap)
            self.increase_speed()
            collision_occurred = True
        
        return collision_occurred

    def increase_speed(self):
        """Increase ball speed by 2% after each hit"""
        if self.speed < self.max_speed:
            # Increase speed by 2%
            self.velocity_x *= 1.02
            self.velocity_y *= 1.02
            # Update current speed
            self.speed = math.sqrt(self.velocity_x**2 + self.velocity_y**2)

    def reset(self):
        """Reset ball to center with random direction"""
        self.x = self.original_x
        self.y = self.original_y
        self.speed = 5  # Reset to base speed
        
        # Random direction with slight angle
        angle = random.uniform(-30, 30)  # Degrees
        direction = random.choice([-1, 1])
        
        self.velocity_x = direction * self.speed * math.cos(math.radians(angle))
        self.velocity_y = self.speed * math.sin(math.radians(angle))

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)