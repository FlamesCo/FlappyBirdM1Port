import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
BIRD_SIZE = 20
PIPE_WIDTH = 100
PIPE_GAP = 200
GRAVITY = 1
JUMP_STRENGTH = -15
PIPE_SPEED = 5
PIPE_FREQUENCY = 1500  # milliseconds between pipe generation

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Setup the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

def reset_game():
    global bird_pos, bird_vel, pipes, last_pipe
    bird_pos = [SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2]
    bird_vel = 0
    pipes = []
    last_pipe = pygame.time.get_ticks()  # Reset the last pipe timer

def check_collision(pipe):
    bird_rect = pygame.Rect(bird_pos[0] - BIRD_SIZE // 2, bird_pos[1] - BIRD_SIZE // 2, BIRD_SIZE, BIRD_SIZE)
    upper_pipe_rect = pygame.Rect(pipe[0], 0, PIPE_WIDTH, pipe[1])
    lower_pipe_rect = pygame.Rect(pipe[0], pipe[1] + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - pipe[1] - PIPE_GAP)
    
    return bird_rect.colliderect(upper_pipe_rect) or bird_rect.colliderect(lower_pipe_rect)

# Initial game setup
reset_game()

# Game loop
running = True
while running:
    screen.fill(WHITE)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bird_vel = JUMP_STRENGTH

    # Bird mechanics
    bird_vel += GRAVITY
    bird_pos[1] += bird_vel

    # Draw bird
    pygame.draw.circle(screen, RED, (int(bird_pos[0]), int(bird_pos[1])), BIRD_SIZE)

    # Generate and move pipes
    time_now = pygame.time.get_ticks()
    if time_now - last_pipe > PIPE_FREQUENCY:
        pipe_height = random.randint(200, SCREEN_HEIGHT - 200 - PIPE_GAP)
        pipes.append([SCREEN_WIDTH, pipe_height])
        last_pipe = time_now

    for pipe in pipes[:]:
        pipe[0] -= PIPE_SPEED
        if pipe[0] < -PIPE_WIDTH:
            pipes.remove(pipe)

        pygame.draw.rect(screen, GREEN, (pipe[0], 0, PIPE_WIDTH, pipe[1]))
        pygame.draw.rect(screen, GREEN, (pipe[0], pipe[1] + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - pipe[1] - PIPE_GAP))

        if check_collision(pipe):
            reset_game()
            break

    # Update display and maintain FPS
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
