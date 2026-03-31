import pygame
import random
import json
import sys

pygame.init()

def load_config(filename):
    global config
    with open(filename) as f:
        config = json.load(f)

# Load default config
load_config("config.json")

WIDTH = config["screen"]["width"]
HEIGHT = config["screen"]["height"]
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Hub 🎮")
clock = pygame.time.Clock()

font_large = pygame.font.Font(None, 72)
font_medium = pygame.font.Font(None, 48)
font_small = pygame.font.Font(None, 36)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# States
MENU = 0
FLAPPY = 1
ARROW = 2
BREAKOUT = 3
SNAKE = 4
SPACE = 5

state = MENU

# Menu variables
def draw_button(text, x, y, width, height, color, hover_color):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(screen, hover_color, (x, y, width, height))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, color, (x, y, width, height))
    pygame.draw.rect(screen, WHITE, (x, y, width, height), 2)
    # Create smaller font for button text
    btn_font = pygame.font.Font(None, 24)
    img = btn_font.render(text, True, BLACK)
    # Center text in button
    text_rect = img.get_rect()
    text_x = x + (width - text_rect.width) // 2
    text_y = y + (height - text_rect.height) // 2
    screen.blit(img, (text_x, text_y))
    return False

def draw_text(text, x, y, font=font_medium, color=WHITE):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# Flappy variables
bird_x = config["flappy"]["bird"]["start_x"]
bird_y = HEIGHT // 2
bird_velocity = 0
pipes = []
score = 0
ground_level = HEIGHT - 50
pipe_timer = 0

# Arrow variables
arrows = []
targets = []
arrow_speed = config["arrow"]["arrow_speed"]
target_speed = config["arrow"]["target_speed"]
arrow_score = 0
arrow_miss = 0
shooter_x = WIDTH//2

# Breakout variables
paddle = [WIDTH//2 - 50, HEIGHT - 30]
ball_pos = [WIDTH//2, HEIGHT//2]
ball_vel = [config["breakout"]["ball_speed"], -config["breakout"]["ball_speed"]]
bricks = []
for i in range(config["breakout"]["brick_rows"]):
    for j in range(config["breakout"]["brick_cols"]):
        bricks.append([j*80 + 10, i*30 + 50])
breakout_won = False
breakout_lost = False

# Snake variables
snake = []
direction = [0, -config["snake"]["segment_size"]]
food = []
snake_score = 0
snake_timer = 0

# Space Invaders variables
player_x = WIDTH//2
bullets = []
aliens = []
alien_speed = 2
alien_dir = 1
space_score = 0
space_timer = 0
missed_bullets = 0
space_missed = 0

def reset_flappy():
    global bird_x, bird_y, bird_velocity, pipes, score, pipe_timer
    bird_x = config["flappy"]["bird"]["start_x"]
    bird_y = HEIGHT // 2
    bird_velocity = 0
    pipes = []
    score = 0
    pipe_timer = 0

def reset_arrow():
    global arrows, targets, arrow_score, arrow_miss, shooter_x
    arrows = []
    targets = []
    arrow_score = 0
    arrow_miss = 0
    shooter_x = WIDTH//2
    for i in range(5):
        targets.append([random.randint(50, WIDTH-50), random.randint(50, HEIGHT//2)])

def reset_breakout():
    global paddle, ball_pos, ball_vel, bricks, breakout_won, breakout_lost
    paddle = [WIDTH//2 - 50, HEIGHT - 30]
    ball_pos = [WIDTH//2, HEIGHT//2]
    ball_vel = [config["breakout"]["ball_speed"], -config["breakout"]["ball_speed"]]
    bricks = []
    for i in range(config["breakout"]["brick_rows"]):
        for j in range(config["breakout"]["brick_cols"]):
            bricks.append([j*80 + 10, i*30 + 50])
    breakout_won = False
    breakout_lost = False

def reset_snake():
    global snake, direction, food, snake_score, snake_timer
    snake = [[WIDTH//2, HEIGHT//2]]
    direction = [0, -config["snake"]["segment_size"]]
    food = [random.randint(0, (WIDTH//config["snake"]["segment_size"])-1)*config["snake"]["segment_size"], random.randint(0, (HEIGHT//config["snake"]["segment_size"])-1)*config["snake"]["segment_size"]]
    snake_score = 0
    snake_timer = 0

def reset_space():
    global player_x, bullets, aliens, alien_speed, alien_dir, space_score, space_timer, missed_bullets, space_missed
    player_x = WIDTH//2
    bullets = []
    aliens = []
    for i in range(config["space"]["alien_rows"]):
        for j in range(config["space"]["alien_cols"]):
            aliens.append([50 + j*60, 50 + i*40])
    alien_speed = config["space"]["alien_speed"]
    alien_dir = 1
    space_score = 0
    space_timer = 0
    missed_bullets = 0
    space_missed = 0

def draw_bird(x, y):
    # Draw bird body (larger, oval)
    pygame.draw.ellipse(screen, YELLOW, (x + 10, y + 10, 20, 15))
    # Draw wings (flapping)
    pygame.draw.ellipse(screen, (255, 215, 0), (x + 5, y + 8, 15, 8))
    pygame.draw.ellipse(screen, (255, 215, 0), (x + 20, y + 8, 15, 8))
    # Eye
    pygame.draw.circle(screen, BLACK, (x + 25, y + 12), 2)
    # Pupil
    pygame.draw.circle(screen, WHITE, (x + 26, y + 11), 1)
    # Beak
    pygame.draw.polygon(screen, RED, [(x + 30, y + 13), (x + 35, y + 12), (x + 35, y + 14)])
    # Tail
    pygame.draw.polygon(screen, (255, 140, 0), [(x + 5, y + 20), (x, y + 15), (x, y + 25)])
    # Legs
    pygame.draw.line(screen, RED, (x + 15, y + 25), (x + 13, y + 30), 2)
    pygame.draw.line(screen, RED, (x + 20, y + 25), (x + 22, y + 30), 2)

while True:
    screen.fill(BLACK)

    if state == MENU:
        draw_text("GAME HUB", 300, 50, font_large, WHITE)
        draw_text("Select Difficulty:", 50, 120, font_medium, WHITE)
        if draw_button("Easy", 50, 160, 120, 50, GREEN, WHITE):
            load_config("easy.json")
        if draw_button("Medium", 200, 160, 120, 50, YELLOW, WHITE):
            load_config("medium.json")
        if draw_button("Hard", 350, 160, 120, 50, RED, WHITE):
            load_config("hard.json")
        draw_text("Select Game:", 50, 240, font_medium, WHITE)
        if draw_button("Flappy Bird", 50, 280, 180, 50, BLUE, WHITE):
            state = FLAPPY
            reset_flappy()
        if draw_button("Arrow Shooter", 270, 280, 180, 50, GREEN, WHITE):
            state = ARROW
            reset_arrow()
        if draw_button("Breakout", 50, 350, 180, 50, RED, WHITE):
            state = BREAKOUT
            reset_breakout()
        if draw_button("Snake", 270, 350, 180, 50, PURPLE, WHITE):
            state = SNAKE
            reset_snake()
        if draw_button("Space Invaders", 490, 280, 180, 50, YELLOW, WHITE):
            state = SPACE
            reset_space()
        draw_text("Click buttons to play!", 250, 450, font_small, WHITE)

    elif state == FLAPPY:
        # Flappy logic - endless
        bird_velocity += config["flappy"]["physics"]["gravity"]
        bird_y += bird_velocity
        if bird_y < 0 or bird_y > ground_level - 20:
            bird_y = HEIGHT // 2  # Reset bird
            bird_velocity = 0
        pipe_timer += 1
        if pipe_timer > 50:  # Spawn pipes more frequently
            gap_y = random.randint(50, HEIGHT - config["flappy"]["pipes"]["gap"] - 50)
            pipes.append([WIDTH, gap_y, False])
            pipe_timer = 0
        for pipe in pipes:
            pipe[0] -= config["flappy"]["pipes"]["speed"]
            if pipe[0] + config["flappy"]["pipes"]["width"] < bird_x and not pipe[2]:
                score += 1
                pipe[2] = True
            if bird_x + 20 > pipe[0] and bird_x < pipe[0] + config["flappy"]["pipes"]["width"]:
                if bird_y < pipe[1] or bird_y + 20 > pipe[1] + config["flappy"]["pipes"]["gap"]:
                    state = MENU
        pipes = [p for p in pipes if p[0] > -config["flappy"]["pipes"]["width"]]
        draw_bird(bird_x, bird_y)
        for pipe in pipes:
            pygame.draw.rect(screen, BLUE, (pipe[0], 0, config["flappy"]["pipes"]["width"], pipe[1]))
            pygame.draw.rect(screen, BLUE, (pipe[0], pipe[1] + config["flappy"]["pipes"]["gap"], config["flappy"]["pipes"]["width"], HEIGHT - pipe[1] - config["flappy"]["pipes"]["gap"]))
        draw_text("Score: " + str(score), 10, 10)

    elif state == ARROW:
        # Arrow logic
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and shooter_x > 0:
            shooter_x -= 5
        if keys[pygame.K_RIGHT] and shooter_x < WIDTH - 30:
            shooter_x += 5
        if keys[pygame.K_SPACE] and not arrows:
            arrows.append([shooter_x + 15, HEIGHT - 50])
        for a in arrows[:]:
            a[1] += arrow_speed
            if a[1] < 0:
                arrows.remove(a)
                arrow_miss += 1
                if arrow_miss >= config["arrow"]["miss_limit"]:
                    state = MENU
        for target in targets[:]:
            target[0] += target_speed
            if target[0] > WIDTH:
                target[0] = 0
            for arrow in arrows[:]:
                if target[0] < arrow[0] < target[0] + 30 and target[1] < arrow[1] < target[1] + 30:
                    arrows.remove(arrow)
                    targets.remove(target)
                    arrow_score += 1
                    targets.append([random.randint(50, WIDTH-50), random.randint(50, HEIGHT//2)])
                    break
        pygame.draw.polygon(screen, WHITE, [(shooter_x, HEIGHT - 50), (shooter_x+15, HEIGHT - 70), (shooter_x+30, HEIGHT - 50)])
        for a in arrows:
            # Arrow shaft
            pygame.draw.line(screen, (139, 69, 19), (a[0], a[1]), (a[0], a[1] + 15), 3)
            # Arrowhead
            pygame.draw.polygon(screen, (192, 192, 192), [(a[0], a[1]), (a[0]-3, a[1]+5), (a[0]+3, a[1]+5)])
            # Fletching
            pygame.draw.polygon(screen, RED, [(a[0], a[1]+12), (a[0]-2, a[1]+15), (a[0]+2, a[1]+15)])
            pygame.draw.polygon(screen, WHITE, [(a[0], a[1]+10), (a[0]-2, a[1]+13), (a[0]+2, a[1]+13)])
        for t in targets:
            pygame.draw.ellipse(screen, RED, (t[0], t[1], 30, 30))
        draw_text("Score: " + str(arrow_score), 10, 10)

    elif state == BREAKOUT:
        # Breakout logic
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle[0] > 0:
            paddle[0] -= config["breakout"]["paddle_speed"]
        if keys[pygame.K_RIGHT] and paddle[0] < WIDTH - 100:
            paddle[0] += config["breakout"]["paddle_speed"]
        ball_pos[0] += ball_vel[0]
        ball_pos[1] += ball_vel[1]
        if ball_pos[0] <= 0 or ball_pos[0] >= WIDTH - 10:
            ball_vel[0] = -ball_vel[0]
        if ball_pos[1] <= 0:
            ball_vel[1] = -ball_vel[1]
        if ball_pos[1] >= HEIGHT - 50 and paddle[0] <= ball_pos[0] <= paddle[0] + 100:
            ball_vel[1] = -ball_vel[1]
        elif ball_pos[1] >= HEIGHT:
            state = MENU
        for brick in bricks[:]:
            if brick[0] <= ball_pos[0] <= brick[0] + 80 and brick[1] <= ball_pos[1] <= brick[1] + 30:
                bricks.remove(brick)
                ball_vel[1] = -ball_vel[1]
                break
        if not bricks and not breakout_won:
            breakout_won = True
        pygame.draw.rect(screen, WHITE, (paddle[0], paddle[1], 100, 10))
        pygame.draw.ellipse(screen, WHITE, (ball_pos[0], ball_pos[1], 10, 10))
        for brick in bricks:
            pygame.draw.rect(screen, RED, (brick[0], brick[1], 80, 30))
        if breakout_won:
            draw_text("You Won!", WIDTH//2 - 50, HEIGHT//2, font_large, GREEN)
        elif breakout_lost:
            draw_text("You Lost!", WIDTH//2 - 50, HEIGHT//2, font_large, RED)

    elif state == SNAKE:
        # Snake logic
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and direction != [config["snake"]["segment_size"], 0]:
            direction = [-config["snake"]["segment_size"], 0]
        if keys[pygame.K_RIGHT] and direction != [-config["snake"]["segment_size"], 0]:
            direction = [config["snake"]["segment_size"], 0]
        if keys[pygame.K_UP] and direction != [0, config["snake"]["segment_size"]]:
            direction = [0, -config["snake"]["segment_size"]]
        if keys[pygame.K_DOWN] and direction != [0, -config["snake"]["segment_size"]]:
            direction = [0, config["snake"]["segment_size"]]
        
        snake_timer += 1
        if snake_timer >= config["snake"]["speed"]:
            snake_timer = 0
            # Move snake
            head = [snake[0][0] + direction[0], snake[0][1] + direction[1]]
            
            # Check wall collision
            if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
                state = MENU
            
            # Check self collision
            if head in snake:
                state = MENU
            
            snake.insert(0, head)
            
            # Check food
            if head == food:
                snake_score += 1
                food = [random.randint(0, (WIDTH//config["snake"]["segment_size"])-1)*config["snake"]["segment_size"], random.randint(0, (HEIGHT//config["snake"]["segment_size"])-1)*config["snake"]["segment_size"]]
            else:
                snake.pop()
        
        # Draw
        for i, segment in enumerate(snake):
            if i == 0:  # Head
                pygame.draw.ellipse(screen, GREEN, (segment[0], segment[1], config["snake"]["segment_size"], config["snake"]["segment_size"] - 2))
                # Eyes
                pygame.draw.circle(screen, BLACK, (segment[0] + 5, segment[1] + 5), 2)
                pygame.draw.circle(screen, BLACK, (segment[0] + 15, segment[1] + 5), 2)
                # Tongue
                pygame.draw.line(screen, RED, (segment[0] + 10, segment[1] + 15), (segment[0] + 10, segment[1] + 20), 1)
                pygame.draw.circle(screen, RED, (segment[0] + 10, segment[1] + 21), 1)
            else:  # Body (curved)
                pygame.draw.ellipse(screen, GREEN, (segment[0], segment[1], config["snake"]["segment_size"], config["snake"]["segment_size"] - 2))
        pygame.draw.ellipse(screen, RED, (food[0], food[1], config["snake"]["segment_size"], config["snake"]["segment_size"]))
        draw_text("Score: " + str(snake_score), 10, 10)

    elif state == SPACE:
        # Space Invaders logic
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= config["space"]["player_speed"]
        if keys[pygame.K_RIGHT] and player_x < WIDTH - 30:
            player_x += config["space"]["player_speed"]
        if keys[pygame.K_SPACE]:
            bullets.append([player_x + 15, HEIGHT - 50])
        
        for b in bullets[:]:
            b[1] += config["space"]["bullet_speed"]
            if b[1] < 0:
                bullets.remove(b)
                missed_bullets += 1
                if missed_bullets >= config["space"]["miss_limit"]:
                    state = MENU
        
        move_down = False
        for alien in aliens:
            alien[0] += config["space"]["alien_speed"] * alien_dir
            if alien[0] <= 0 or alien[0] >= WIDTH - 30:
                move_down = True
        
        if move_down:
            alien_dir *= -1
            for alien in aliens:
                alien[1] += 20
            alien_speed += 0.5
        
        for bullet in bullets[:]:
            for alien in aliens[:]:
                if alien[0] < bullet[0] < alien[0] + 30 and alien[1] < bullet[1] < alien[1] + 20:
                    if bullet in bullets:
                        bullets.remove(bullet)
                    if alien in aliens:
                        aliens.remove(alien)
                    space_score += 10
                    break
        
        for alien in aliens:
            if alien[1] >= HEIGHT - 50:
                space_missed += 1
                if space_missed >= config["space"]["miss_limit"]:
                    state = MENU
                else:
                    aliens = []
                    for i in range(config["space"]["alien_rows"]):
                        for j in range(config["space"]["alien_cols"]):
                            aliens.append([50 + j*60, 50 + i*40])
                break
        
        pygame.draw.rect(screen, WHITE, (player_x, HEIGHT - 50, 30, 20))
        for b in bullets:
            pygame.draw.rect(screen, GREEN, (b[0], b[1], 5, 10))
        for a in aliens:
            pygame.draw.rect(screen, RED, (a[0], a[1], 30, 20))
        draw_text("Score: " + str(space_score), 10, 10)
        draw_text("Missed Bullets: " + str(missed_bullets) + "/" + str(config["space"]["miss_limit"]), WIDTH - 320, 10)
        draw_text("Aliens Reached Bottom: " + str(space_missed) + "/" + str(config["space"]["miss_limit"]), WIDTH - 420, 40)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if state == MENU:
                pygame.quit()
                sys.exit()
            else:
                state = MENU
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                state = MENU
            if state == FLAPPY and event.key == pygame.K_SPACE:
                bird_velocity = config["flappy"]["physics"]["jump_force"]

    pygame.display.update()
    clock.tick(60)