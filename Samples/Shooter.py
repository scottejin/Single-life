import pygame
import sys
import heapq
import random
import math

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
SPAWN_ENEMY_INTERVAL = 2000  # Interval in milliseconds

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
        self.spawn_time = pygame.time.get_ticks()
        self.last_shot_time = 0
        self.xp = 0

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

        self.rect.clamp_ip(screen.get_rect())

    def is_immune(self):
        return pygame.time.get_ticks() - self.spawn_time < 6000

    def shoot(self, target_x, target_y):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= 500:
            self.last_shot_time = current_time
            bullet = Bullet(self.rect.centerx, self.rect.centery, target_x, target_y)
            return bullet
        return None

    def add_xp(self, amount):
        self.xp += amount ** 2

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5

        dx, dy = target_x - x, target_y - y
        dist = (dx ** 2 + dy ** 2) ** 0.5
        self.dx, self.dy = (dx / dist, dy / dist) if dist != 0 else (0, 0)

    def update(self, *args):
        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed
        if not screen.get_rect().contains(self.rect):
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

class XP(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((0, 255, 0))  # Green color for XP
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

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
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)

def spawn_enemy(player):
    while True:
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        distance = math.sqrt((x - player.rect.centerx) ** 2 + (y - player.rect.centery) ** 2)
        if distance >= 140:
            break
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
last_spawn_time = pygame.time.get_ticks()

# Sprite groups
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
xp_drops = pygame.sprite.Group()

# Create player instance
player = Player()
all_sprites.add(player)

# Create reset button instance
reset_button = Button(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 50, 100, 50, "Try Again", RED, WHITE)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if game_over and reset_button.is_clicked(event):
                game_over = False
                score = 0
                start_time = pygame.time.get_ticks()
                all_sprites.empty()
                bullets.empty()
                enemies.empty()
                xp_drops.empty()
                player = Player()
                all_sprites.add(player)
            else:
                target_x, target_y = event.pos
                bullet = player.shoot(target_x, target_y)
                if bullet:
                    all_sprites.add(bullet)
                    bullets.add(bullet)

    if not game_over:
        current_time = pygame.time.get_ticks()
        if current_time - last_spawn_time >= SPAWN_ENEMY_INTERVAL:
            spawn_enemy(player)
            last_spawn_time = current_time

        all_sprites.update(player)

        for enemy in enemies:
            enemy.update(player)

        hits = pygame.sprite.groupcollide(bullets, enemies, True, False)
        for hit in hits:
            for enemy in hits[hit]:
                enemy.kill()
                xp_drop = XP(enemy.rect.centerx, enemy.rect.centery)
                all_sprites.add(xp_drop)
                xp_drops.add(xp_drop)

        xp_collected = pygame.sprite.spritecollide(player, xp_drops, True)
        for xp in xp_collected:
            player.add_xp(1)

        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        score = elapsed_time

        if not player.is_immune() and pygame.sprite.spritecollideany(player, enemies):
            game_over = True

        screen.fill(WHITE)
        all_sprites.draw(screen)

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, BLACK)
        xp_text = font.render(f"XP: {player.xp}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(xp_text, (10, 50))

        pygame.display.flip()

    else:
        display_game_over(screen, score)
        reset_button.draw(screen)
        pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()