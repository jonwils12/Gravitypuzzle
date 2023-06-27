import pygame
import random

# Constants
WIDTH = 800
HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLATFORM_COLOR = (0, 255, 0)

# Player properties
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_COLOR = (0, 0, 255)
PLAYER_GRAVITY = 1
PLAYER_JUMP_FORCE = 20
PLAYER_SPEED = 5

# Platform properties
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 20
PLATFORM_GAP_RANGE = (200, 300)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = HEIGHT // 2
        self.vel_y = 0
        self.is_jumping = False

    def update(self):
        self.vel_y += PLAYER_GRAVITY
        self.rect.y += self.vel_y

        # Check collision with platforms
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.is_jumping = False
                elif self.vel_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0

        # Handle player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.vel_y = -PLAYER_JUMP_FORCE
            self.is_jumping = True

        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED

    def reset(self):
        self.rect.x = 50
        self.rect.y = HEIGHT // 2
        self.vel_y = 0
        self.is_jumping = False

# Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, PLATFORM_HEIGHT))
        self.image.fill(PLATFORM_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Create sprite groups
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)

# Generate random level
def generate_level():
    platforms.empty()
    x = 0
    while x < WIDTH:
        gap = random.randint(*PLATFORM_GAP_RANGE)
        platform_width = random.randint(PLATFORM_WIDTH, PLATFORM_WIDTH + gap)
        platform = Platform(x, random.randint(100, HEIGHT - PLATFORM_HEIGHT), platform_width)
        platforms.add(platform)
        all_sprites.add(platform)
        x += platform_width + gap

# Generate initial level
generate_level()

running = True
while running:
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    # Check if player falls off the screen
    if player.rect.y > HEIGHT:
        player.reset()

    # Check if player reaches the end
    if player.rect.x > WIDTH:
        generate_level()
        player.reset()

    # Render
    screen.fill(WHITE)
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
