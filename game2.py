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
BLOCK_SIZE = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)

def draw_text(text, x, y):
    img = font.render(text, True, WHITE)
    screen.blit(img, (x, y))

class Snake:
    def __init__(self):
        self.body = [[WIDTH//2, HEIGHT//2]]
        self.direction = [0, -BLOCK_SIZE]
        self.grow = False

    def move(self):
        head = [self.body[0][0] + self.direction[0], self.body[0][1] + self.direction[1]]
        self.body.insert(0, head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def change_direction(self, new_dir):
        if new_dir[0] * -1 != self.direction[0] or new_dir[1] * -1 != self.direction[1]:
            self.direction = new_dir

    def check_collision(self):
        head = self.body[0]
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            return True
        for segment in self.body[1:]:
            if head == segment:
                return True
        return False

    def draw(self):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))

class Food:
    def __init__(self):
        self.position = [random.randint(0, (WIDTH//BLOCK_SIZE)-1)*BLOCK_SIZE, random.randint(0, (HEIGHT//BLOCK_SIZE)-1)*BLOCK_SIZE]

    def draw(self):
        pygame.draw.rect(screen, RED, (self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE))

def main():
    snake = Snake()
    food = Food()
    score = 0
    speed = 10
    obstacles = []
    power_ups = []  # New: power-ups
    power_up_timer = 0

    while True:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    snake.change_direction([-BLOCK_SIZE, 0])
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction([BLOCK_SIZE, 0])
                elif event.key == pygame.K_UP:
                    snake.change_direction([0, -BLOCK_SIZE])
                elif event.key == pygame.K_DOWN:
                    snake.change_direction([0, BLOCK_SIZE])

        snake.move()

        if snake.body[0] == food.position:
            snake.grow = True
            food = Food()
            score += 1
            speed += 0.5
            if score % 5 == 0:
                obstacles.append([random.randint(0, (WIDTH//BLOCK_SIZE)-1)*BLOCK_SIZE, random.randint(0, (HEIGHT//BLOCK_SIZE)-1)*BLOCK_SIZE])
            # Add power-up every 10 points
            if score % 10 == 0:
                power_ups.append([random.randint(0, (WIDTH//BLOCK_SIZE)-1)*BLOCK_SIZE, random.randint(0, (HEIGHT//BLOCK_SIZE)-1)*BLOCK_SIZE])

        # Check power-up collision
        for pu in power_ups[:]:
            if snake.body[0] == pu:
                power_ups.remove(pu)
                speed += 2  # Speed boost
                power_up_timer = 300  # 5 seconds at 60 FPS

        if power_up_timer > 0:
            power_up_timer -= 1
            if power_up_timer == 0:
                speed = max(10, speed - 2)

        if snake.check_collision():
            draw_text("Game Over! Score: " + str(score), WIDTH//2 - 100, HEIGHT//2)
            pygame.display.update()
            pygame.time.wait(2000)
            return

        for obs in obstacles:
            if snake.body[0] == obs:
                draw_text("Game Over! Score: " + str(score), WIDTH//2 - 100, HEIGHT//2)
                pygame.display.update()
                pygame.time.wait(2000)
                return

        snake.draw()
        food.draw()
        for obs in obstacles:
            pygame.draw.rect(screen, WHITE, (obs[0], obs[1], BLOCK_SIZE, BLOCK_SIZE))
        for pu in power_ups:
            pygame.draw.rect(screen, YELLOW, (pu[0], pu[1], BLOCK_SIZE, BLOCK_SIZE))  # Yellow for power-up

        draw_text("Score: " + str(score), 10, 10)
        if power_up_timer > 0:
            draw_text("Speed Boost!", 10, 40)

        pygame.display.update()
        clock.tick(speed)

if __name__ == "__main__":
    main()