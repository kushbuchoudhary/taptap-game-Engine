import pygame
import random
import sys

pygame.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Screen dimensions
WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)

# Player
player = [WIDTH//2, HEIGHT - 50]
player_speed = 5

# Bullets
bullets = []
bullet_speed = -7

# Aliens
aliens = []
alien_speed = 2
alien_direction = 1
for i in range(5):
    for j in range(10):
        aliens.append([50 + j*60, 50 + i*40])

def draw_text(text, x, y):
    img = font.render(text, True, WHITE)
    screen.blit(img, (x, y))

score = 0
lives = 3
bullet_speed = -7
power_ups = []  # New: power-ups for faster shooting

while True:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append([player[0] + 15, player[1]])

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player[0] > 0:
        player[0] -= player_speed
    if keys[pygame.K_RIGHT] and player[0] < WIDTH - 30:
        player[0] += player_speed

    # Move bullets
    bullets = [b for b in bullets if b[1] > 0]
    for b in bullets:
        b[1] += bullet_speed

    # Move aliens
    move_down = False
    for alien in aliens:
        alien[0] += alien_speed * alien_direction
        if alien[0] <= 0 or alien[0] >= WIDTH - 30:
            move_down = True
    if move_down:
        alien_direction *= -1
        for alien in aliens:
            alien[1] += 20
        alien_speed += 0.5
        # Add power-up when aliens move down
        if random.random() < 0.3:  # 30% chance
            power_ups.append([random.randint(0, WIDTH-30), 0])

    # Move power-ups
    power_ups = [p for p in power_ups if p[1] < HEIGHT]
    for p in power_ups:
        p[1] += 3

    # Check collisions
    for bullet in bullets[:]:
        for alien in aliens[:]:
            if alien[0] < bullet[0] < alien[0] + 30 and alien[1] < bullet[1] < alien[1] + 20:
                bullets.remove(bullet)
                aliens.remove(alien)
                score += 10
                break

    # Check power-up collision
    for p in power_ups[:]:
        if player[0] < p[0] < player[0] + 30 and player[1] < p[1] < player[1] + 20:
            power_ups.remove(p)
            bullet_speed -= 1  # Faster bullets

    # Check if aliens reach bottom
    for alien in aliens:
        if alien[1] >= HEIGHT - 50:
            lives -= 1
            aliens = []
            for i in range(5):
                for j in range(10):
                    aliens.append([50 + j*60, 50 + i*40])
            break

    if lives <= 0:
        draw_text("Game Over! Score: " + str(score), WIDTH//2 - 100, HEIGHT//2)
        pygame.display.update()
        pygame.time.wait(2000)
        sys.exit()

    # Draw player
    pygame.draw.rect(screen, WHITE, (player[0], player[1], 30, 20))

    # Draw bullets
    for b in bullets:
        pygame.draw.rect(screen, GREEN, (b[0], b[1], 5, 10))

    # Draw aliens
    for a in aliens:
        pygame.draw.rect(screen, RED, (a[0], a[1], 30, 20))

    # Draw power-ups
    for p in power_ups:
        pygame.draw.rect(screen, YELLOW, (p[0], p[1], 10, 10))

    draw_text("Score: " + str(score), 10, 10)
    draw_text("Lives: " + str(lives), WIDTH - 100, 10)

    pygame.display.update()
    clock.tick(60)
<parameter name="filePath">c:\Users\bhasker\Downloads\taptap-game-Engine-main\taptap-game-Engine-main\game4.py