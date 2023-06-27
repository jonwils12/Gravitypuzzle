import pygame
import random

# Game dimensions
WIDTH = 800
HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Platform settings
PLATFORM_WIDTH = 80
PLATFORM_HEIGHT = 20
PLATFORM_GAP_RANGE = (100, 200)

# Player settings
PLAYER_WIDTH = 20
PLAYER_HEIGHT = 40
PLAYER_VELOCITY = 5
PLAYER_JUMP_VELOCITY = 10
GRAVITY = 0.5

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer Game")

clock = pygame.time.Clock()

platforms = pygame.sprite.Group()
level_sprites = pygame.sprite.Group()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.velocity = pygame.Vector2(0, 0)
        self.jump = False

    def update(self):
        self.velocity.y += GRAVITY
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        platform_collisions = pygame.sprite.spritecollide(self, platforms, False)
        for platform in platform_collisions:
            if self.velocity.y > 0 and self.rect.bottom <= platform.rect.top:
                self.rect.bottom = platform.rect.top
                self.velocity.y = 0
                self.jump = False

    def jump_action(self):
        if not self.jump:
            self.velocity.y = -PLAYER_JUMP_VELOCITY
            self.jump = True

    def move_left(self):
        self.velocity.x = -PLAYER_VELOCITY

    def move_right(self):
        self.velocity.x = PLAYER_VELOCITY

    def stop_movement(self):
        self.velocity.x = 0

def generate_level():
    level_sprites.empty()
    platforms.empty()
    x = 0
    while x < WIDTH:
        gap = random.randint(*PLATFORM_GAP_RANGE)
        platform_width = random.randint(PLATFORM_WIDTH, PLATFORM_WIDTH + gap)
        platform = Platform(x, random.randint(100, HEIGHT - PLATFORM_HEIGHT), platform_width)
        platforms.add(platform)
        level_sprites.add(platform)
        x += platform_width + gap

    # Increase the number of platforms by 25%
    num_platforms = len(platforms)
    additional_platforms = int(num_platforms * 0.25)

    for _ in range(additional_platforms):
        gap = random.randint(*PLATFORM_GAP_RANGE)
        platform_width = random.randint(PLATFORM_WIDTH, PLATFORM_WIDTH + gap)
        platform = Platform(random.randint(0, WIDTH), random.randint(100, HEIGHT - PLATFORM_HEIGHT), platform_width)
        platforms.add(platform)
        level_sprites.add(platform)

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        super().__init__()
        self.image = pygame.Surface((width, PLATFORM_HEIGHT))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x -= PLAYER_VELOCITY

        if self.rect.right < 0:
            self.kill()

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

generate_level()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump_action()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move_left()
    elif keys[pygame.K_RIGHT]:
        player.move_right()
    else:
        player.stop_movement()

    all_sprites.update()

    screen.fill(WHITE)

    for sprite in all_sprites:
        screen.blit(sprite.image, sprite.rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
