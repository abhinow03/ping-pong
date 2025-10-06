import pygame
import random
from game.game_engine import GameEngine

# Initialize pygame/Start application
pygame.init()

# Load custom font
try:
    # Try to load from file first
    FONT_PATH = "fonts/PressStart2P-Regular.ttf"
    def get_font(size):
        return pygame.font.Font(FONT_PATH, size)
except:
    # Fallback to system font if custom font not found
    print("Custom font not found. Using system font.")
    def get_font(size):
        return pygame.font.SysFont("Arial", size, bold=True)

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("⭐ COSMIC PONG ⭐")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BLUE = (10, 10, 30)
CYAN = (0, 255, 255)
PURPLE = (138, 43, 226)
GOLD = (255, 215, 0)
GRAY = (100, 100, 100)

# Star field for background
class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = random.randint(1, 3)
        self.speed = random.uniform(0.1, 0.5)
        self.brightness = random.randint(100, 255)
    
    def update(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = 0
            self.x = random.randint(0, WIDTH)
    
    def draw(self, screen):
        color = (self.brightness, self.brightness, self.brightness)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.size)

# Create starfield
stars = [Star() for _ in range(100)]

# Clock
clock = pygame.time.Clock()
FPS = 60

# Game loop
engine = GameEngine(WIDTH, HEIGHT)

# Set winning score if not already set
if not hasattr(engine, 'winning_score'):
    engine.winning_score = 10

def draw_pause_screen():
    """Draw pause overlay with glow effect"""
    # Semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(150)
    overlay.fill(DARK_BLUE)
    SCREEN.blit(overlay, (0, 0))
    
    # Glowing title effect
    title_font = get_font(40)
    subtitle_font = get_font(16)
    
    # Draw glow
    for offset in range(5, 0, -1):
        glow_color = (CYAN[0]//offset, CYAN[1]//offset, CYAN[2]//offset)
        pause_glow = title_font.render("PAUSED", True, glow_color)
        SCREEN.blit(pause_glow, (WIDTH//2 - pause_glow.get_width()//2 + offset, HEIGHT//2 - 60 + offset))
    
    pause_text = title_font.render("PAUSED", True, CYAN)
    resume_text = subtitle_font.render("Press ESC to Resume", True, WHITE)
    
    SCREEN.blit(pause_text, (WIDTH//2 - pause_text.get_width()//2, HEIGHT//2 - 60))
    SCREEN.blit(resume_text, (WIDTH//2 - resume_text.get_width()//2, HEIGHT//2 + 30))

def draw_game_winner_screen(winner, engine):
    """Draw screen when a single game is won (not the full series)"""
    # Semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(160)
    overlay.fill(DARK_BLUE)
    SCREEN.blit(overlay, (0, 0))
    
    title_font = get_font(32)
    subtitle_font = get_font(18)
    info_font = get_font(16)
    
    winner_color = GOLD if winner == "PLAYER" else PURPLE
    
    # Draw glow effect for game winner
    for offset in range(4, 0, -1):
        glow_color = (winner_color[0]//offset, winner_color[1]//offset, winner_color[2]//offset)
        winner_glow = title_font.render(f"{winner} Wins!", True, glow_color)
        SCREEN.blit(winner_glow, (WIDTH//2 - winner_glow.get_width()//2 + offset, HEIGHT//2 - 120 + offset))
    
    game_text = title_font.render(f"{winner} Wins!", True, winner_color)
    SCREEN.blit(game_text, (WIDTH//2 - game_text.get_width()//2, HEIGHT//2 - 120))
    
    # Show series score
    series_score_text = subtitle_font.render(f"Series Score", True, WHITE)
    SCREEN.blit(series_score_text, (WIDTH//2 - series_score_text.get_width()//2, HEIGHT//2 - 30))
    
    score_text = info_font.render(f"Player {engine.player_games_won} - {engine.ai_games_won} AI", True, CYAN)
    SCREEN.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 + 20))
    
    # Show what's needed to win
    games_needed = engine.games_to_win_series
    info_text = get_font(12).render(f"First to {games_needed} wins", True, (150, 150, 150))
    SCREEN.blit(info_text, (WIDTH//2 - info_text.get_width()//2, HEIGHT//2 + 60))
    
    # Continue message
    continue_font = get_font(14)
    continue_text = continue_font.render("Press SPACE", True, (150, 255, 150))
    SCREEN.blit(continue_text, (WIDTH//2 - continue_text.get_width()//2, HEIGHT//2 + 100))

def draw_game_over_screen(winner, is_series_over=False, engine=None):
    """Draw game over screen with celebration effect"""
    # Semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)
    overlay.fill(DARK_BLUE)
    SCREEN.blit(overlay, (0, 0))
    
    title_font = get_font(36)
    subtitle_font = get_font(18)
    option_font = get_font(14)
    info_font = get_font(12)
    
    # Winner color
    winner_color = GOLD if winner == "PLAYER" else PURPLE
    
    # Different text for series winner vs single game winner
    winner_text = f"{winner} WINS!" if is_series_over else f"{winner} WINS!"
    
    # Draw glow effect
    for offset in range(5, 0, -1):
        glow_color = (winner_color[0]//offset, winner_color[1]//offset, winner_color[2]//offset)
        winner_glow = title_font.render(winner_text, True, glow_color)
        SCREEN.blit(winner_glow, (WIDTH//2 - winner_glow.get_width()//2 + offset, HEIGHT//2 - 200 + offset))
    
    game_over_text = title_font.render(winner_text, True, winner_color)
    SCREEN.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 200))
    
    # Show final series score if it was a series
    if is_series_over and engine:
        final_score = info_font.render(f"Score: {engine.player_games_won} - {engine.ai_games_won}", True, WHITE)
        SCREEN.blit(final_score, (WIDTH//2 - final_score.get_width()//2, HEIGHT//2 - 140))
    
    play_again_text = subtitle_font.render("Choose Mode", True, WHITE)
    SCREEN.blit(play_again_text, (WIDTH//2 - play_again_text.get_width()//2, HEIGHT//2 - 90))
    
    # Draw options with better spacing and styling
    options = [
        ("3", "Best of 3", (100, 200, 255), HEIGHT//2 - 30),
        ("5", "Best of 5", (180, 100, 255), HEIGHT//2 + 20),
        ("7", "Best of 7", (255, 180, 100), HEIGHT//2 + 70),
        ("0", "First to 10", (255, 100, 150), HEIGHT//2 + 120)
    ]
    
    for key, text, color, y_pos in options:
        # Draw glow box
        box_width = 320
        box_height = 40
        box_x = WIDTH//2 - box_width//2
        
        # Outer glow
        for i in range(3, 0, -1):
            glow_rect = pygame.Rect(box_x - i*2, y_pos - i*2, box_width + i*4, box_height + i*4)
            glow_color = (color[0]//2, color[1]//2, color[2]//2)
            pygame.draw.rect(SCREEN, glow_color, glow_rect, border_radius=10)
        
        # Filled box with border
        pygame.draw.rect(SCREEN, (color[0]//3, color[1]//3, color[2]//3), (box_x, y_pos, box_width, box_height), border_radius=8)
        pygame.draw.rect(SCREEN, color, (box_x, y_pos, box_width, box_height), 3, border_radius=8)
        
        option_text = option_font.render(f"[{key}] {text}", True, color)
        SCREEN.blit(option_text, (WIDTH//2 - option_text.get_width()//2, y_pos + 10))
    
    # Exit option at bottom
    exit_font = get_font(10)
    exit_text = exit_font.render("ESC to Exit", True, (150, 150, 150))
    SCREEN.blit(exit_text, (WIDTH//2 - exit_text.get_width()//2, HEIGHT - 50))

def main():
    running = True
    paused = False
    game_over_state = False  # Single game finished
    series_over_state = False  # Entire series finished
    winner = ""
    game_winner = ""
    
    while running:
        # Draw starfield background
        SCREEN.fill(DARK_BLUE)
        for star in stars:
            star.update()
            star.draw(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                # Pause toggle (only during active play)
                if event.key == pygame.K_ESCAPE and not series_over_state and not game_over_state:
                    paused = not paused
                
                # Continue to next game after winning a game
                if event.key == pygame.K_SPACE and game_over_state and not series_over_state:
                    game_over_state = False
                    engine.reset_game()
                
                # Series/Game mode selection menu
                if series_over_state:
                    if event.key == pygame.K_3:
                        engine.start_series('best_of_3')
                        series_over_state = False
                        game_over_state = False
                        winner = ""
                    elif event.key == pygame.K_5:
                        engine.start_series('best_of_5')
                        series_over_state = False
                        game_over_state = False
                        winner = ""
                    elif event.key == pygame.K_7:
                        engine.start_series('best_of_7')
                        series_over_state = False
                        game_over_state = False
                        winner = ""
                    elif event.key == pygame.K_0:
                        engine.start_series('single')
                        series_over_state = False
                        game_over_state = False
                        winner = ""
                    elif event.key == pygame.K_ESCAPE:
                        running = False
        
        # Game logic (only runs when not paused and game is active)
        if not paused and not game_over_state and not series_over_state:
            engine.handle_input()
            engine.update()
            
            # Check if current game is won
            game_winner = engine.check_game_winner()
            if game_winner:
                # Record the game win
                engine.record_game_win(game_winner)
                
                # Check if series is over (early termination)
                series_winner = engine.check_series_winner()
                
                if series_winner:
                    # Series is won! No more games needed
                    series_over_state = True
                    winner = series_winner
                elif engine.series_mode == 'single':
                    # Single game mode - go directly to series over
                    series_over_state = True
                    winner = game_winner
                else:
                    # Series continues - show game winner screen
                    game_over_state = True
        
        # Render game
        engine.render(SCREEN)
        
        # Draw overlays
        if paused:
            draw_pause_screen()
        
        if game_over_state and not series_over_state:
            draw_game_winner_screen(game_winner, engine)
        
        if series_over_state:
            is_series = engine.series_mode != 'single'
            draw_game_over_screen(winner, is_series, engine)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()