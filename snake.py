import pygame # type: ignore
import sys
import random

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 640, 480
BLOCK_SIZE = 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Set up the font
font = pygame.font.Font(None, 36)

# Set up the snake and food
snake = [(200, 200), (220, 200), (240, 200)]
food = (400, 300)

# Set up the score and direction
score = 0
direction = "right"

# Game loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
            sys.exit    ()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != "down":
                direction = "up"
            elif event.key == pygame.K_DOWN and direction != "up":
                direction = "down"
            elif event.key == pygame.K_LEFT and direction != "right":
                direction = "left"
            elif event.key == pygame.K_RIGHT and direction != "left":
                direction = "right"

    # Move the snake
    head = snake[-1]
    if direction == "up":
        new_head = (head[0], head[1] - BLOCK_SIZE)
    elif direction == "down":
        new_head = (head[0], head[1] + BLOCK_SIZE)
    elif direction == "left":
        new_head = (head[0] - BLOCK_SIZE, head[1])
    elif direction == "right":
        new_head = (head[0] + BLOCK_SIZE, head[1])
    snake.append(new_head)

    # Check for collision with food
    if snake[-1] == food:
        score += 1
        food = (random.randint(0, WIDTH - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE,
                random.randint(0, HEIGHT - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE)
    else:
        snake.pop(0)

    # Check for collision with self or wall
    if (snake[-1][0] < 0 or snake[-1][0] >= WIDTH or
            snake[-1][1] < 0 or snake[-1][1] >= HEIGHT or
            snake[-1] in snake[:-1]):
        # Game over! Show score and retry button    
        screen.fill(BLACK)
        text = font.render(f"Game Over! Score: {score}", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        retry_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
        pygame.draw.rect(screen, GREEN, retry_button)
        text = font.render("Retry", True, BLACK)
        screen.blit(text, (retry_button.centerx - text.get_width() // 2, retry_button.centery - text.get_height() // 2))
        pygame.display.flip()

        # Wait for retry button click
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if retry_button.collidepoint(event.pos):
                        waiting = False
                        score = 0
                        snake = [(200, 200), (220, 200), (240, 200)]
                        food = (400, 300)
                        direction = "right"

    # Draw everything
    screen.fill(BLACK)
    for pos in snake:
        pygame.draw.rect(screen, WHITE, (pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, RED, (food[0], food[1], BLOCK_SIZE, BLOCK_SIZE))
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(10)