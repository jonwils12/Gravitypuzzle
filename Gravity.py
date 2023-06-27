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
BLUE = (0, 0, 255)

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
obstacle_width = 40
obstacle_height = 40

# Define maze layouts for each level
maze_layouts = [
    [
        "############",
        "#P         #",
        "#  ####### #",
        "#        # #",
        "#  ####### #",
        "#         E#",
        "############",
    ],
    [
        "############",
        "#P         #",
        "# #######  #",
        "#        # #",
        "#  ###   # #",
        "#  #E#     #",
        "############",
    ],
    [
        "############",
        "#P       E #",
        "# #######  #",
        "#        # #",
        "#  ###   # #",
        "#  #       #",
        "############",
    ],
]

# Load game fonts
font = pygame.font.Font(None, 36)

# Load maze images
maze_images = {
    "#": pygame.image.load("wall.png").convert(),
    "P": pygame.image.load("start.png").convert_alpha(),
    "E": pygame.image.load("end.png").convert_alpha(),
}

# Set image transparency
for image in maze_images.values():
    image.set_colorkey((255, 255, 255))

# Define game states
is_game_over = False
has_won = False

# Load the maze layout for the current level
maze_layout = maze_layouts[level - 1]
maze_width = len(maze_layout[0]) * obstacle_width
maze_height = len(maze_layout) * obstacle_height

# Create maze obstacles based on the layout
obstacles = []
for row_index, row in enumerate(maze_layout):
    for col_index, cell in enumerate(row):
        if cell != " ":
            x = col_index * obstacle_width
            y = row_index * obstacle_height
            obstacles.append(pygame.Rect(x, y, obstacle_width, obstacle_height))

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
                    maze_layout = maze_layouts[level - 1]
                    maze_width = len(maze_layout[0]) * obstacle_width
                    maze_height = len(maze_layout) * obstacle_height
                    obstacles.clear()
                    for row_index, row in enumerate(maze_layout):
                        for col_index, cell in enumerate(row):
                            if cell != " ":
                                x = col_index * obstacle_width
                                y = row_index * obstacle_height
                                obstacles.append(pygame.Rect(x, y, obstacle_width, obstacle_height))

    if not is_game_over:
        keys = pygame.key.get_pressed()
        player_vel += gravity

        # Move the player horizontally
        if keys[pygame.K_LEFT]:
            player_pos[0] -= move_speed * dt
        if keys[pygame.K_RIGHT]:
            player_pos[0] += move_speed * dt

        # Move the player vertically
        player_pos[1] += player_vel * dt

        # Check collision with maze obstacles
        player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)
        for obstacle in obstacles:
            if player_rect.colliderect(obstacle):
                if player_vel > 0:  # Player hits the obstacle from above
                    player_pos[1] = obstacle.top - player_size
                    player_vel = 0
                elif player_vel < 0:  # Player hits the obstacle from below
                    player_pos[1] = obstacle.bottom
                    player_vel = 0

        # Check if player reaches the end point
        end_rect = pygame.Rect(maze_width - obstacle_width, HEIGHT - obstacle_height, obstacle_width, obstacle_height)
        if player_rect.colliderect(end_rect):
            if level < max_levels:
                level += 1
                player_pos = [50, HEIGHT // 2]
                maze_layout = maze_layouts[level - 1]
                maze_width = len(maze_layout[0]) * obstacle_width
                maze_height = len(maze_layout) * obstacle_height
                obstacles.clear()
                for row_index, row in enumerate(maze_layout):
                    for col_index, cell in enumerate(row):
                        if cell != " ":
                            x = col_index * obstacle_width
                            y = row_index * obstacle_height
                            obstacles.append(pygame.Rect(x, y, obstacle_width, obstacle_height))
            else:
                has_won = True

        # Check if player falls off the screen
        if player_pos[1] > HEIGHT:
            is_game_over = True

    # Clear the window
    window.fill(WHITE)

    # Draw the maze obstacles
    for obstacle in obstacles:
        window.blit(maze_images["#"], obstacle)

    # Draw the player
    window.blit(maze_images["P"], (player_pos[0], player_pos[1]))

    # Draw the end point
    window.blit(maze_images["E"], (maze_width - obstacle_width, HEIGHT - obstacle_height))

    # Draw game text
    if is_game_over:
        game_over_text = font.render("Game Over! Press Space to Restart", True, BLACK)
        window.blit(game_over_text, (WIDTH // 2 - 200, HEIGHT // 2 - 50))
    elif has_won:
        win_text = font.render("You Win! Press Space to Restart", True, BLACK)
        window.blit(win_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))

    # Update the window
    pygame.display.update()
