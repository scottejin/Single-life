import pygame
import sys
import heapq
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
SPAWN_ENEMY_EVENT = pygame.USEREVENT + 1

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shooter Game")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed = 5
        self.spawn_time = pygame.time.get_ticks()  # Track spawn time
        self.last_shot_time = 0  # Track the time of the last shot

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

    def shoot(self, target_x, target_y):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= 500:  # 500 ms = 0.5 seconds
            self.last_shot_time = current_time
            bullet = Bullet(self.rect.centerx, self.rect.centery, target_x, target_y)
            return bullet
        return None

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5

        # Calculate direction
        dx, dy = target_x - x, target_y - y
        dist = (dx ** 2 + dy ** 2) ** 0.5
        if dist != 0:
            self.dx, self.dy = dx / dist, dy / dist
        else:
            self.dx, self.dy = 0, 0

    def update(self, *args):
        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed
        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT or self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 2
        self.path = []

    def update(self, player):
        if not self.path:
            self.path = self.a_star_pathfinding((self.rect.x, self.rect.y), (player.rect.x, player.rect.y))
        if self.path:
            next_move = self.path.pop(0)
            self.rect.x, self.rect.y = next_move

    def a_star_pathfinding(self, start, goal):
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: heuristic(start, goal)}

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (current[0] + dx, current[1] + dy)
                tentative_g_score = g_score[current] + 1

                if 0 <= neighbor[0] < SCREEN_WIDTH and 0 <= neighbor[1] < SCREEN_HEIGHT:
                    if tentative_g_score < g_score.get(neighbor, float('inf')):
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return []

class Button:
    def __init__(self, x, y, width, height, text, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.Font(None, 36)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

def spawn_enemy():
    x = random.randint(0, SCREEN_WIDTH)
    y = random.randint(0, SCREEN_HEIGHT)
    enemy = Enemy(x, y)
    all_sprites.add(enemy)
    enemies.add(enemy)

def display_game_over(screen, score):
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", True, RED)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(3000)

# Main game loop
clock = pygame.time.Clock()
running = True
game_over = False
score = 0
start_time = pygame.time.get_ticks()

# Sprite groups
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Create player instance
player = Player()
all_sprites.add(player)

# Set a timer to spawn enemies
pygame.time.set_timer(SPAWN_ENEMY_EVENT, 2000)  # Spawn an enemy every 2 seconds

# Create reset button instance
reset_button = Button(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 50, 100, 50, "Try Again", RED, WHITE)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == SPAWN_ENEMY_EVENT:
            spawn_enemy()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if game_over and reset_button.is_clicked(event):
                # Reset game state
                game_over = False
                score = 0
                start_time = pygame.time.get_ticks()
                all_sprites.empty()
                bullets.empty()
                enemies.empty()
                player = Player()
                all_sprites.add(player)
            else:
                target_x, target_y = event.pos
                bullet = player.shoot(target_x, target_y)
                if bullet:
                    all_sprites.add(bullet)
                    bullets.add(bullet)

    if not game_over:
        # Update
        all_sprites.update(player)

        # Update enemies with player reference
        for enemy in enemies:
            enemy.update(player)

        # Check for bullet-enemy collisions
        hits = pygame.sprite.groupcollide(bullets, enemies, True, False)
        for hit in hits:
            for enemy in hits[hit]:
                enemy.kill()

        # Update score based on elapsed time
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        score = elapsed_time

        # Check for player-enemy collisions
        if not player.is_immune() and pygame.sprite.spritecollideany(player, enemies):
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
        reset_button.draw(screen)
        pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()