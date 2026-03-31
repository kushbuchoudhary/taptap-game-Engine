import pygame
import sys

pygame.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Screen dimensions
WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)

# Paddle dimensions
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
BALL_SIZE = 10

# Initial positions
left_paddle = [50, HEIGHT//2 - PADDLE_HEIGHT//2]
right_paddle = [WIDTH - 50 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2]
balls = [[WIDTH//2, HEIGHT//2]]  # List of balls
ball_velocities = [[5, 5]]

left_score = 0
right_score = 0

def draw_text(text, x, y):
    img = font.render(text, True, WHITE)
    screen.blit(img, (x, y))

def reset_ball():
    global balls, ball_velocities
    balls = [[WIDTH//2, HEIGHT//2]]
    ball_velocities = [[random.choice([-5, 5]), random.choice([-5, 5])]]

import random

while True:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and left_paddle[1] > 0:
        left_paddle[1] -= 5
    if keys[pygame.K_s] and left_paddle[1] < HEIGHT - PADDLE_HEIGHT:
        left_paddle[1] += 5

    # AI for right paddle
    if balls:
        target_y = balls[0][1]  # Track first ball
        if target_y < right_paddle[1] + PADDLE_HEIGHT//2 and right_paddle[1] > 0:
            right_paddle[1] -= 4
        if target_y > right_paddle[1] + PADDLE_HEIGHT//2 and right_paddle[1] < HEIGHT - PADDLE_HEIGHT:
            right_paddle[1] += 4

    # Move balls
    for i, ball in enumerate(balls):
        ball[0] += ball_velocities[i][0]
        ball[1] += ball_velocities[i][1]

        # Ball collision with top/bottom
        if ball[1] <= 0 or ball[1] >= HEIGHT - BALL_SIZE:
            ball_velocities[i][1] = -ball_velocities[i][1]

        # Ball collision with paddles
        if (ball[0] <= left_paddle[0] + PADDLE_WIDTH and left_paddle[1] <= ball[1] <= left_paddle[1] + PADDLE_HEIGHT) or \
           (ball[0] + BALL_SIZE >= right_paddle[0] and right_paddle[1] <= ball[1] <= right_paddle[1] + PADDLE_HEIGHT):
            ball_velocities[i][0] = -ball_velocities[i][0]
            ball_velocities[i][0] *= 1.1

        # Score
        if ball[0] < 0:
            right_score += 1
            reset_ball()
            break
        if ball[0] > WIDTH:
            left_score += 1
            reset_ball()
            break

    # Add more balls every 5 points
    if left_score + right_score > 0 and (left_score + right_score) % 5 == 0 and len(balls) == 1:
        balls.append([WIDTH//2, HEIGHT//2])
        ball_velocities.append([random.choice([-5, 5]), random.choice([-5, 5])])

    # Draw paddles
    pygame.draw.rect(screen, WHITE, (left_paddle[0], left_paddle[1], PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(screen, WHITE, (right_paddle[0], right_paddle[1], PADDLE_WIDTH, PADDLE_HEIGHT))

    # Draw balls
    for ball in balls:
        pygame.draw.ellipse(screen, WHITE, (ball[0], ball[1], BALL_SIZE, BALL_SIZE))

    # Draw scores
    draw_text(str(left_score), WIDTH//4, 20)
    draw_text(str(right_score), 3*WIDTH//4, 20)

    pygame.display.update()
    clock.tick(60)