import pygame
import random
import sys

pygame.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [(0, 255, 255), (255, 255, 0), (128, 0, 128), (0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 165, 0)]

# Screen dimensions
WIDTH = 800
HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]],  # L
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]]   # Z
]

class Tetris:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.score = 0
        self.level = 1
        self.fall_time = 0
        self.fall_speed = 500  # ms, decrease for hardness

    def new_piece(self):
        shape = random.choice(SHAPES)
        color = random.randint(1, len(COLORS))
        return {'shape': shape, 'color': color, 'x': GRID_WIDTH//2 - len(shape[0])//2, 'y': 0}

    def rotate(self, piece):
        piece['shape'] = [list(reversed(col)) for col in zip(*piece['shape'])]

    def valid_move(self, piece, dx=0, dy=0):
        for y, row in enumerate(piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    nx, ny = piece['x'] + x + dx, piece['y'] + y + dy
                    if nx < 0 or nx >= GRID_WIDTH or ny >= GRID_HEIGHT or (ny >= 0 and self.grid[ny][nx]):
                        return False
        return True

    def place_piece(self, piece):
        for y, row in enumerate(piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[piece['y'] + y][piece['x'] + x] = piece['color']
        self.clear_lines()

    def clear_lines(self):
        lines = 0
        for y in range(GRID_HEIGHT):
            if all(self.grid[y]):
                del self.grid[y]
                self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
                lines += 1
        self.score += lines ** 2 * 100
        self.level = self.score // 1000 + 1
        self.fall_speed = max(50, 500 - (self.level - 1) * 50)  # Faster for hardness

    def draw(self):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x]:
                    pygame.draw.rect(screen, COLORS[self.grid[y][x]-1], (x*BLOCK_SIZE + 100, y*BLOCK_SIZE + 50, BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(screen, WHITE, (x*BLOCK_SIZE + 100, y*BLOCK_SIZE + 50, BLOCK_SIZE, BLOCK_SIZE), 1)

        # Draw current piece
        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, COLORS[self.current_piece['color']-1], ((self.current_piece['x'] + x)*BLOCK_SIZE + 100, (self.current_piece['y'] + y)*BLOCK_SIZE + 50, BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(screen, WHITE, ((self.current_piece['x'] + x)*BLOCK_SIZE + 100, (self.current_piece['y'] + y)*BLOCK_SIZE + 50, BLOCK_SIZE, BLOCK_SIZE), 1)

def draw_text(text, x, y):
    img = font.render(text, True, WHITE)
    screen.blit(img, (x, y))

game = Tetris()

while True:
    screen.fill(BLACK)

    dt = clock.tick(60)
    game.fall_time += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and game.valid_move(game.current_piece, -1, 0):
                game.current_piece['x'] -= 1
            if event.key == pygame.K_RIGHT and game.valid_move(game.current_piece, 1, 0):
                game.current_piece['x'] += 1
            if event.key == pygame.K_DOWN and game.valid_move(game.current_piece, 0, 1):
                game.current_piece['y'] += 1
            if event.key == pygame.K_UP:
                game.rotate(game.current_piece)
                if not game.valid_move(game.current_piece):
                    game.rotate(game.current_piece)  # Rotate back if invalid

    if game.fall_time >= game.fall_speed:
        if game.valid_move(game.current_piece, 0, 1):
            game.current_piece['y'] += 1
        else:
            game.place_piece(game.current_piece)
            game.current_piece = game.next_piece
            game.next_piece = game.new_piece()
            if not game.valid_move(game.current_piece):
                draw_text("Game Over! Score: " + str(game.score), WIDTH//2 - 100, HEIGHT//2)
                pygame.display.update()
                pygame.time.wait(2000)
                sys.exit()
        game.fall_time = 0

    game.draw()
    draw_text("Score: " + str(game.score), 10, 10)
    draw_text("Level: " + str(game.level), 10, 40)

    pygame.display.update()
<parameter name="filePath">c:\Users\bhasker\Downloads\taptap-game-Engine-main\taptap-game-Engine-main\game5.py