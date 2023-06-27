import pygame
import random

# Constants
WIDTH = 800
HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

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
PLATFORM_COLOR = (0, 255, 0)

# Game variables
level = 1
score = 0

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
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

        # Check if player falls off the screen or lands on the bottom boundary
        if self.rect.y > HEIGHT or self.rect.top > HEIGHT:
            self.kill()

    def jump(self):
        if not self.is_jumping:
            self.vel_y = -PLAYER_JUMP_FORCE
            self.is_jumping = True

    def move_left(self):
        self.rect.x -= PLAYER_SPEED

    def move_right(self):
        self.rect.x += PLAYER_SPEED

# Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(PLATFORM_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Create sprite groups
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()

# Create player
player = Player(100, HEIGHT // 2)
all_sprites.add(player)

# Generate random platforms for the initial level
def generate_platforms():
    platforms.empty()
    for i in range(level * 10):
        x = random.randint(0, WIDTH - PLATFORM_WIDTH)
        y = random.randint(100, HEIGHT - 100)
        platform = Platform(x, y)
        all_sprites.add(platform)
        platforms.add(platform)

generate_platforms()

running = True
left_pressed = False
right_pressed = False

while running:
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()
            elif event.key == pygame.K_LEFT:
                left_pressed = True
            elif event.key == pygame.K_RIGHT:
                right_pressed = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left_pressed = False
            elif event.key == pygame.K_RIGHT:
                right_pressed = False

    # Update
    all_sprites.update()

    if left_pressed:
        player.move_left()
    if right_pressed:
        player.move_right()

    # Check if player reaches the end of the level
    if player.rect.right >= WIDTH:
        score += 1
        level += 1
        generate_platforms()

    # Check if player collides with the bottom boundary
    if pygame.sprite.spritecollide(player, platforms, False):
        player.kill()

    # Render
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # Draw score and level
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, BLACK)
    level_text = font.render(f"Level: {level}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 50))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
