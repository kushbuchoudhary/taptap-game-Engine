"""
Flappy Bird Clone - Fully JSON-Configurable
A complete remake of Flappy Bird where ALL gameplay values are controlled by config.json
"""

import pygame
import json
import random
import sys

# ============================================================================
# LOAD CONFIGURATION FROM JSON
# ============================================================================
with open("config.json") as f:
    config = json.load(f)

# Load all game parameters from JSON
WIDTH = config["screen"]["width"]
HEIGHT = config["screen"]["height"]
FPS = config["screen"]["fps"]

GRAVITY = config["physics"]["gravity"]
JUMP_FORCE = config["physics"]["jump_force"]

PIPE_SPEED = config["pipes"]["speed"]
PIPE_WIDTH = config["pipes"]["width"]
PIPE_GAP = config["pipes"]["gap"]
PIPE_SPAWN_INTERVAL = config["pipes"]["spawn_interval"]

BIRD_SIZE = config["bird"]["size"]
BIRD_START_X = config["bird"]["start_x"]

# ============================================================================
# COLOR DEFINITIONS
# ============================================================================
SKY_BLUE = (135, 206, 250)
GROUND_BROWN = (139, 101, 58)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (34, 139, 34)
GOLD = (255, 215, 0)
YELLOW = (255, 255, 0)

# ============================================================================
# GAME STATE CLASS
# ============================================================================
class Game:
    """Main game controller"""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Flappy Bird - JSON Controlled")
        self.clock = pygame.time.Clock()
        
        # Fonts
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        
        # Game states
        self.MENU = 0
        self.PLAYING = 1
        self.GAME_OVER = 2
        
        self.reset_game()
        
        # Spawn pipe event
        self.SPAWN_PIPE_EVENT = pygame.USEREVENT
        pygame.time.set_timer(self.SPAWN_PIPE_EVENT, PIPE_SPAWN_INTERVAL)
        
        self.ground_level = HEIGHT - 50
    
    def reset_game(self):
        """Reset all game variables for a fresh start"""
        self.bird_x = BIRD_START_X
        self.bird_y = HEIGHT // 2
        self.bird_velocity = 0
        self.bird_rotation = 0
        
        self.pipes = []  # List to store all pipes
        self.score = 0
        self.pipes_passed = set()  # Track which pipes we've already scored
        
        self.game_state = self.MENU
    
    def handle_events(self):
        """Handle all user input and window events"""
        for event in pygame.event.get():
            # Window close
            if event.type == pygame.QUIT:
                return False
            
            # Window resize
            if event.type == pygame.VIDEORESIZE:
                global WIDTH, HEIGHT
                WIDTH, HEIGHT = event.w, event.h
                self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                self.ground_level = HEIGHT - 50
            
            # Keyboard input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    # Start game from menu
                    if self.game_state == self.MENU:
                        self.reset_game()
                        self.game_state = self.PLAYING
                    # Jump during gameplay
                    elif self.game_state == self.PLAYING:
                        self.bird_velocity = JUMP_FORCE
                    # Restart from game over
                    elif self.game_state == self.GAME_OVER:
                        self.reset_game()
                        self.game_state = self.PLAYING
            
            # Spawn pipes during gameplay
            if event.type == self.SPAWN_PIPE_EVENT and self.game_state == self.PLAYING:
                self.spawn_pipe()
        
        return True
    
    def spawn_pipe(self):
        """Create a new pair of pipes at random height"""
        # Random height for the gap between pipes
        gap_y = random.randint(100, self.ground_level - PIPE_GAP - 100)
        
        # Upper pipe (from top to gap)
        self.pipes.append({
            'x': WIDTH,
            'y': 0,
            'height': gap_y,
            'passed': False
        })
        
        # Lower pipe (from gap to ground)
        self.pipes.append({
            'x': WIDTH,
            'y': gap_y + PIPE_GAP,
            'height': self.ground_level - (gap_y + PIPE_GAP),
            'passed': False
        })
    
    def update_game(self):
        """Update game physics and logic"""
        if self.game_state != self.PLAYING:
            return
        
        # ===== BIRD PHYSICS =====
        # Apply gravity
        self.bird_velocity += GRAVITY
        
        # Terminal velocity (max falling speed)
        if self.bird_velocity > 8:
            self.bird_velocity = 8
        
        # Update bird position
        self.bird_y += self.bird_velocity
        
        # Update bird rotation based on velocity
        self.bird_rotation = min(max(self.bird_velocity * 2, -30), 90)
        
        # ===== PIPE LOGIC =====
        # Move pipes left
        for pipe in self.pipes:
            pipe['x'] -= PIPE_SPEED
        
        # Remove off-screen pipes
        self.pipes = [p for p in self.pipes if p['x'] > -PIPE_WIDTH]
        
        # ===== SCORING =====
        # Score when bird passes the center of pipes
        for i, pipe in enumerate(self.pipes):
            # Only count once per pipe pair (every 2nd pipe is the lower one)
            if pipe['x'] < self.bird_x and i not in self.pipes_passed and pipe['y'] > 0:
                self.score += 1
                self.pipes_passed.add(i)
        
        # ===== COLLISION DETECTION =====
        bird_rect = pygame.Rect(self.bird_x, self.bird_y, BIRD_SIZE, BIRD_SIZE)
        
        # Check collision with pipes
        for pipe in self.pipes:
            pipe_rect = pygame.Rect(pipe['x'], pipe['y'], PIPE_WIDTH, pipe['height'])
            if bird_rect.colliderect(pipe_rect):
                self.game_state = self.GAME_OVER
        
        # Check collision with ground and ceiling
        if self.bird_y >= self.ground_level - BIRD_SIZE or self.bird_y <= 0:
            self.game_state = self.GAME_OVER
    
    def draw_menu(self):
        """Draw main menu screen"""
        self.screen.fill(SKY_BLUE)
        
        # Title
        title = self.font_large.render("FLAPPY BIRD", True, WHITE)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
        
        # Instructions
        inst1 = self.font_small.render("Press SPACE to Start", True, BLACK)
        self.screen.blit(inst1, (WIDTH // 2 - inst1.get_width() // 2, HEIGHT // 2))
        
        inst2 = self.font_small.render("Press SPACE/UP to Jump", True, BLACK)
        self.screen.blit(inst2, (WIDTH // 2 - inst2.get_width() // 2, HEIGHT // 2 + 60))
        
        inst3 = self.font_small.render("Avoid the pipes!", True, RED)
        self.screen.blit(inst3, (WIDTH // 2 - inst3.get_width() // 2, HEIGHT // 2 + 120))
        
        # Info about JSON control
        info = self.font_small.render("Edit config.json to change difficulty!", True, GOLD)
        self.screen.blit(info, (WIDTH // 2 - info.get_width() // 2, HEIGHT - 100))
    
    def draw_game(self):
        """Draw game screen during gameplay"""
        self.screen.fill(SKY_BLUE)
        
        # Draw ground
        pygame.draw.line(self.screen, GROUND_BROWN, (0, self.ground_level), 
                        (WIDTH, self.ground_level), 5)
        
        # Draw score
        score_text = self.font_medium.render(str(self.score), True, WHITE)
        self.screen.blit(score_text, (20, 20))
        
        # Draw pipes
        for pipe in self.pipes:
            pygame.draw.rect(self.screen, GREEN, 
                           (pipe['x'], pipe['y'], PIPE_WIDTH, pipe['height']))
            
            # Add pipe styling (segmented look)
            pygame.draw.line(self.screen, (0, 100, 0),
                           (pipe['x'], pipe['y']),
                           (pipe['x'] + PIPE_WIDTH, pipe['y']), 3)
        
        # Draw bird
        self.draw_bird()
    
    def draw_game_over(self):
        """Draw game over screen overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Game over text
        go_text = self.font_large.render("GAME OVER", True, RED)
        self.screen.blit(go_text, (WIDTH // 2 - go_text.get_width() // 2, HEIGHT // 3))
        
        # Final score
        score_text = self.font_medium.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
        
        # Restart instruction
        restart_text = self.font_small.render("Press SPACE to Restart", True, WHITE)
        self.screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT - 100))
    
    def draw_bird(self):
        """Draw the bird with rotation"""
        # Create bird surface
        bird_surface = pygame.Surface((BIRD_SIZE, BIRD_SIZE), pygame.SRCALPHA)
        
        # Draw bird body (circle)
        pygame.draw.circle(bird_surface, GOLD, (BIRD_SIZE // 2, BIRD_SIZE // 2), 
                         BIRD_SIZE // 2)
        
        # Draw bird eye
        pygame.draw.circle(bird_surface, BLACK, (BIRD_SIZE // 2 + 8, BIRD_SIZE // 2 - 5), 3)
        
        # Draw bird beak
        pygame.draw.polygon(bird_surface, RED,
                          [(BIRD_SIZE - 2, BIRD_SIZE // 2 - 3),
                           (BIRD_SIZE - 2, BIRD_SIZE // 2 + 3),
                           (BIRD_SIZE + 4, BIRD_SIZE // 2)])
        
        # Rotate bird based on velocity
        rotated_bird = pygame.transform.rotate(bird_surface, -self.bird_rotation)
        bird_rect = rotated_bird.get_rect(center=(self.bird_x + BIRD_SIZE // 2,
                                                   self.bird_y + BIRD_SIZE // 2))
        
        self.screen.blit(rotated_bird, bird_rect)
    
    def render(self):
        """Render the appropriate screen based on game state"""
        if self.game_state == self.MENU:
            self.draw_menu()
        elif self.game_state == self.PLAYING:
            self.draw_game()
        elif self.game_state == self.GAME_OVER:
            self.draw_game()
            self.draw_game_over()
        
        pygame.display.update()
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            running = self.handle_events()
            self.update_game()
            self.render()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================
if __name__ == "__main__":
    game = Game()
    game.run()