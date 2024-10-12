import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Pygame Game")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Custom event for spawning enemies
SPAWN_ENEMY_EVENT = pygame.USEREVENT + 1
ENEMY_SPAWN_DELAY = 3000  # milliseconds
pygame.time.set_timer(SPAWN_ENEMY_EVENT, ENEMY_SPAWN_DELAY)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed = 5
        self.spawn_time = pygame.time.get_ticks()  # Track spawn time

    def update(self, *args):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Boundary checks
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def is_immune(self):
        # Check if the player is still within the immunity period
        return pygame.time.get_ticks() - self.spawn_time < 6000

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH)
        self.rect.y = random.randint(0, SCREEN_HEIGHT)
        self.speed = 2

    def update(self, player):
        dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        dist = (dx ** 2 + dy ** 2) ** 0.5
        if dist != 0:
            dx, dy = dx / dist, dy / dist
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5

    def update(self, *args):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

# Tower class
class Tower(pygame.sprite.Sprite):
    def __init__(self, x, y, tower_type="basic"):
        super().__init__()
        self.tower_type = tower_type
        if tower_type == "basic":
            self.image = pygame.Surface((50, 50))
            self.image.fill(RED)
            self.shoot_delay = 500  # milliseconds
        elif tower_type == "rapid":
            self.image = pygame.Surface((50, 50))
            self.image.fill((0, 0, 255))
            self.shoot_delay = 200  # milliseconds
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.last_shot = pygame.time.get_ticks()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            return bullet
        return None

# Create player
player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Create tower
tower = Tower(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, tower_type="basic")
all_sprites.add(tower)

# Create enemies
enemies = pygame.sprite.Group()
for _ in range(5):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Create bullets group
bullets = pygame.sprite.Group()

# Function to spawn a new enemy
def spawn_enemy():
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Function to display game over message
def display_game_over(screen, score):
    font = pygame.font.Font(None, 74)
    game_over_text = font.render("Game Over", True, RED)
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 + game_over_text.get_height() // 2))
    pygame.display.flip()

# Main game loop
clock = pygame.time.Clock()
running = True
game_over = False
score = 0
start_time = pygame.time.get_ticks()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == SPAWN_ENEMY_EVENT:
            spawn_enemy()

    if not game_over:
        # Tower shooting
        bullet = tower.shoot()
        if bullet:
            all_sprites.add(bullet)
            bullets.add(bullet)

        # Update
        all_sprites.update(player)

        # Check for bullet-enemy collisions
        if not player.is_immune():
            hits = pygame.sprite.groupcollide(bullets, enemies, True, False)
            for hit in hits:
                for enemy in hits[hit]:
                    enemy.kill()

        # Update score based on elapsed time
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        score = elapsed_time

        # Check for player-enemy collisions
        if pygame.sprite.spritecollideany(player, enemies):
            game_over = True

        # Draw
        screen.fill(WHITE)
        all_sprites.draw(screen)

        # Display score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

    else:
        display_game_over(screen, score)

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()