import pygame
from .paddle import Paddle
from .ball import Ball

# Game Engine

WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
PURPLE = (138, 43, 226)
GOLD = (255, 215, 0)
LIGHT_BLUE = (100, 149, 237)
PINK = (255, 105, 180)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100
        self.points_per_game = 5  # Points needed to win a single game in a series
        
        # Series tracking
        self.series_mode = None  # 'best_of_3', 'best_of_5', 'best_of_7', or 'single'
        self.player_games_won = 0  # Games won in current series
        self.ai_games_won = 0      # Games won in current series
        self.games_to_win_series = 0  # Games needed to win the series (2 for bo3, 3 for bo5, etc)
        self.current_game_number = 1

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        
        # Load custom font
        try:
            FONT_PATH = "fonts/PressStart2P-Regular.ttf"
            self.font = pygame.font.Font(FONT_PATH, 40)
            self.small_font = pygame.font.Font(FONT_PATH, 12)
            self.title_font = pygame.font.Font(FONT_PATH, 16)
        except:
            # Fallback to system font
            self.font = pygame.font.SysFont("Arial", 60, bold=True)
            self.small_font = pygame.font.SysFont("Arial", 22)
            self.title_font = pygame.font.SysFont("Arial", 28, bold=True)
        
        # Sound effects (optional - will work if sound files exist)
        self.sounds_enabled = True
        try:
            self.paddle_sound = pygame.mixer.Sound("sounds/paddle.wav")
            self.wall_sound = pygame.mixer.Sound("sounds/wall.wav")
            self.score_sound = pygame.mixer.Sound("sounds/score.wav")
        except:
            self.sounds_enabled = False

    def play_sound(self, sound_type):
        """Play sound effect if enabled"""
        if not self.sounds_enabled:
            return
        
        try:
            if sound_type == "paddle":
                self.paddle_sound.play()
            elif sound_type == "wall":
                self.wall_sound.play()
            elif sound_type == "score":
                self.score_sound.play()
        except:
            pass

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.player.move(10, self.height)

    def update(self):
        # Check for wall collision before moving
        old_y = self.ball.y
        self.ball.move()
        
        # Play wall bounce sound
        if (self.ball.y <= 0 or self.ball.y + self.ball.height >= self.height) and old_y != self.ball.y:
            self.play_sound("wall")
        
        # Check paddle collisions
        collision = self.ball.check_collision(self.player, self.ai)
        if collision:
            self.play_sound("paddle")

        # Check scoring
        if self.ball.x <= 0:
            self.ai_score += 1
            self.play_sound("score")
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.play_sound("score")
            self.ball.reset()

        # AI movement with difficulty (not perfect tracking)
        self.ai.auto_track(self.ball, self.height)

    def render(self, screen):
        # Draw paddles with glow effect
        # Player paddle (left) - Cyan glow
        for i in range(3, 0, -1):
            glow_rect = pygame.Rect(self.player.x - i, self.player.y - i, 
                                   self.paddle_width + i*2, self.paddle_height + i*2)
            glow_color = (0, 255//i, 255//i)
            pygame.draw.rect(screen, glow_color, glow_rect, border_radius=5)
        pygame.draw.rect(screen, CYAN, self.player.rect(), border_radius=5)
        
        # AI paddle (right) - Purple glow
        for i in range(3, 0, -1):
            glow_rect = pygame.Rect(self.ai.x - i, self.ai.y - i, 
                                   self.paddle_width + i*2, self.paddle_height + i*2)
            glow_color = (138//i, 43//i, 226//i)
            pygame.draw.rect(screen, glow_color, glow_rect, border_radius=5)
        pygame.draw.rect(screen, PURPLE, self.ai.rect(), border_radius=5)
        
        # Draw ball with glow effect
        ball_center = (int(self.ball.x + self.ball.width//2), int(self.ball.y + self.ball.height//2))
        for i in range(5, 0, -1):
            pygame.draw.circle(screen, (255//i, 215//i, 0), ball_center, self.ball.width//2 + i)
        pygame.draw.circle(screen, GOLD, ball_center, self.ball.width//2)
        
        # Draw fancy center line
        for i in range(0, self.height, 25):
            pygame.draw.rect(screen, LIGHT_BLUE, (self.width//2 - 3, i, 6, 15), border_radius=3)

        # Draw score with glow
        player_score_str = str(self.player_score)
        ai_score_str = str(self.ai_score)
        
        # Player score glow (cyan)
        for offset in range(3, 0, -1):
            glow_color = (0, 255//(offset+1), 255//(offset+1))
            player_glow = self.font.render(player_score_str, True, glow_color)
            screen.blit(player_glow, (self.width//4 - player_glow.get_width()//2 + offset, 30 + offset))
        
        player_text = self.font.render(player_score_str, True, CYAN)
        screen.blit(player_text, (self.width//4 - player_text.get_width()//2, 30))
        
        # AI score glow (purple)
        for offset in range(3, 0, -1):
            glow_color = (138//(offset+1), 43//(offset+1), 226//(offset+1))
            ai_glow = self.font.render(ai_score_str, True, glow_color)
            screen.blit(ai_glow, (self.width * 3//4 - ai_glow.get_width()//2 + offset, 30 + offset))
        
        ai_text = self.font.render(ai_score_str, True, PURPLE)
        screen.blit(ai_text, (self.width * 3//4 - ai_text.get_width()//2, 30))
        
        # Draw controls hint
        controls_text = self.small_font.render("W/S or Arrows - ESC Pause", True, LIGHT_BLUE)
        screen.blit(controls_text, (self.width//2 - controls_text.get_width()//2, self.height - 35))
        
        # Draw series info with fancy styling
        if self.series_mode == 'best_of_3':
            games_played = self.player_games_won + self.ai_games_won
            target_text = self.title_font.render(f"Best of 3 - Game {games_played + 1}", True, PINK)
        elif self.series_mode == 'best_of_5':
            games_played = self.player_games_won + self.ai_games_won
            target_text = self.title_font.render(f"Best of 5 - Game {games_played + 1}", True, PINK)
        elif self.series_mode == 'best_of_7':
            games_played = self.player_games_won + self.ai_games_won
            target_text = self.title_font.render(f"Best of 7 - Game {games_played + 1}", True, PINK)
        else:
            target_text = self.title_font.render(f"First to {self.points_per_game}", True, PINK)
        screen.blit(target_text, (self.width//2 - target_text.get_width()//2, 110))
        
        # Draw series score if in series mode
        if self.series_mode != 'single':
            series_text = self.small_font.render(f"Series: Player {self.player_games_won} - {self.ai_games_won} AI", True, LIGHT_BLUE)
            screen.blit(series_text, (self.width//2 - series_text.get_width()//2, 140))

    def reset_game(self):
        """Reset only the current game (keep series score)"""
        self.player_score = 0
        self.ai_score = 0
        self.player.y = self.height // 2 - 50
        self.ai.y = self.height // 2 - 50
        self.ball.reset()
        self.ball.speed = 5  # Reset ball speed
    
    def reset_series(self):
        """Reset the entire series"""
        self.player_games_won = 0
        self.ai_games_won = 0
        self.current_game_number = 1
        self.reset_game()
    
    def start_series(self, series_type):
        """Start a new series with specified format"""
        self.series_mode = series_type
        
        if series_type == 'best_of_3':
            self.games_to_win_series = 2  # Need 2 games to win best of 3
            self.points_per_game = 5
        elif series_type == 'best_of_5':
            self.games_to_win_series = 3  # Need 3 games to win best of 5
            self.points_per_game = 5
        elif series_type == 'best_of_7':
            self.games_to_win_series = 4  # Need 4 games to win best of 7
            self.points_per_game = 5
        else:  # Single game mode
            self.series_mode = 'single'
            self.games_to_win_series = 1
            self.points_per_game = 10
        
        self.reset_series()
    
    def check_game_winner(self):
        """Check if someone won the current game (not the series)"""
        if self.player_score >= self.points_per_game:
            return "PLAYER"
        elif self.ai_score >= self.points_per_game:
            return "AI"
        return None
    
    def record_game_win(self, winner):
        """Record a game win and update series status"""
        if winner == "PLAYER":
            self.player_games_won += 1
        else:
            self.ai_games_won += 1
        self.current_game_number += 1
    
    def check_series_winner(self):
        """Check if someone won the series (early termination logic)"""
        # Series ends as soon as someone reaches required games
        if self.player_games_won >= self.games_to_win_series:
            return "PLAYER"
        elif self.ai_games_won >= self.games_to_win_series:
            return "AI"
        return None
    
    def get_series_status(self):
        """Get current series status for display"""
        if self.series_mode == 'single':
            return "Single Game"
        
        total_games = self.player_games_won + self.ai_games_won
        if self.series_mode == 'best_of_3':
            return f"Best of 3 - Game {total_games + 1}"
        elif self.series_mode == 'best_of_5':
            return f"Best of 5 - Game {total_games + 1}"
        elif self.series_mode == 'best_of_7':
            return f"Best of 7 - Game {total_games + 1}"
        return ""