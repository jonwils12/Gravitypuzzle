import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 800
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity Puzzle Game")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Define game variables
clock = pygame.time.Clock()
gravity = 0.5
jump_force = 10
move_speed = 200  # Pixels per second
player_size = 30
player_pos = [50, HEIGHT // 2]
player_vel = 0
level = 1
max_levels = 3
goal_pos = [WIDTH - 50, HEIGHT - 50]
obstacle_pos = [WIDTH // 2, HEIGHT - 50]
obstacle_width = 100
obstacle_height = 20

# Define game states
is_game_over = False
has_won = False

# Load game fonts
font = pygame.font.Font(None, 36)

# Game loop
while True:
    dt = clock.tick(60) / 1000.0  # Time elapsed in seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not is_game_over:
                    player_vel = -jump_force
                else:
                    is_game_over = False
                    has_won = False
                    level = 1
                    player_pos = [50, HEIGHT // 2]

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] -= move_speed * dt
    if keys[pygame.K_RIGHT]:
        player_pos[0] += move_speed * dt
    if keys[pygame.K_UP]:
        player_pos[1] -= move_speed * dt
    if keys[pygame.K_DOWN]:
        player_pos[1] += move_speed * dt

    # Apply gravity to the player
    player_vel += gravity * dt
    player_pos[1] += player_vel * dt

    # Check for collision with obstacles
    if player_pos[1] >= HEIGHT - player_size:
        player_pos[1] = HEIGHT - player_size
        player_vel = 0

    # Check for collision with the goal
    if player_pos[0] + player_size >= goal_pos[0] and player_pos[1] + player_size >= goal_pos[1]:
        if level == max_levels:
            has_won = True
        else:
            level += 1
            player_pos = [50, HEIGHT // 2]

    # Check for collision with the obstacle
    if player_pos[0] + player_size >= obstacle_pos[0] and player_pos[0] <= obstacle_pos[0] + obstacle_width:
        if player_pos[1] + player_size >= obstacle_pos[1] and player_pos[1] <= obstacle_pos[1] + obstacle_height:
            is_game_over = True

    # Clear the window
    window.fill(WHITE)

    # Draw the player
    pygame.draw.rect(window, BLACK, (player_pos[0], player_pos[1], player_size, player_size))

    # Draw the goal
    pygame.draw.rect(window, GREEN, (goal_pos[0], goal_pos[1], player_size, player_size))

    # Draw the obstacle
    pygame.draw.rect(window, RED, (obstacle_pos[0], obstacle_pos[1], obstacle_width, obstacle_height))

    # Draw game text
    if is_game_over:
        game_over_text = font.render("Game Over! Press Space to Restart", True, BLACK)
        window.blit(game_over_text, (WIDTH // 2 - 200, HEIGHT // 2 - 50))
    elif has_won:
        win_text = font.render("You Win! Press Space to Restart", True, BLACK)
        window.blit(win_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))

    # Update the window
    pygame.display.update()
