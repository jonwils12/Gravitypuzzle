import pygame

# Initialize Pygame
pygame.init()

# Game window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Player properties
PLAYER_WIDTH = 20
PLAYER_HEIGHT = 20
PLAYER_COLOR = BLUE
PLAYER_JUMP_FORCE = -10
PLAYER_GRAVITY = 0.5

# Platform properties
PLATFORM_WIDTH = 150
PLATFORM_HEIGHT = 20
PLATFORM_COLOR = GRAY

# Obstacle properties
OBSTACLE_WIDTH = 30
OBSTACLE_HEIGHT = 30
OBSTACLE_COLOR = RED
OBSTACLE_VELOCITY = 2

# End goal properties
GOAL_WIDTH = 50
GOAL_HEIGHT = 50
GOAL_COLOR = GREEN

# Create the game window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Gravity Puzzle Game")

clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity_y = 0
        self.is_jumping = False

    def update(self):
        self.gravity()
        self.rect.y += self.velocity_y

    def jump(self):
        if not self.is_jumping:
            self.velocity_y = PLAYER_JUMP_FORCE
            self.is_jumping = True

    def gravity(self):
        self.velocity_y += PLAYER_GRAVITY

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(PLATFORM_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        self.image.fill(OBSTACLE_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity_x = OBSTACLE_VELOCITY

    def update(self):
        self.rect.x += self.velocity_x

class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((GOAL_WIDTH, GOAL_HEIGHT))
        self.image.fill(GOAL_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Create player object
player = Player(50, 50)
player_group = pygame.sprite.Group()
player_group.add(player)

# Create platform objects
platforms = [
    Platform(0, WINDOW_HEIGHT - PLATFORM_HEIGHT),  # Start platform
    Platform(200, 300),
    Platform(500, 200)
]
platform_group = pygame.sprite.Group()
platform_group.add(platforms)

# Create obstacle objects
obstacles = [
    Obstacle(400, 100),
    Obstacle(600, 150)
]
obstacle_group = pygame.sprite.Group()
obstacle_group.add(obstacles)

# Create end goal object
goal = Goal(WINDOW_WIDTH - GOAL_WIDTH, WINDOW_HEIGHT - GOAL_HEIGHT)
goal_group = pygame.sprite.Group()
goal_group.add(goal)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.rect.x -= 5
    if keys[pygame.K_RIGHT]:
        player.rect.x += 5

    # Check collision with platforms
    collision_platform = pygame.sprite.spritecollide(player, platform_group, False)
    if collision_platform:
        player.rect.bottom = collision_platform[0].rect.top
        player.velocity_y = 0
        player.is_jumping = False

    # Check collision with obstacles
    collision_obstacle = pygame.sprite.spritecollide(player, obstacle_group, False)
    if collision_obstacle:
        running = False

    # Check collision with goal
    collision_goal = pygame.sprite.spritecollide(player, goal_group, False)
    if collision_goal:
        print("Player reached the goal!")
        # Add your code here to handle winning condition

    # Update game objects
    player_group.update()
    obstacle_group.update()

    # Draw game objects
    window.fill(BLACK)
    player_group.draw(window)
    platform_group.draw(window)
    obstacle_group.draw(window)
    goal_group.draw(window)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
