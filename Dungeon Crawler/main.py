import pygame
import random
import math
import sys

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
SPAWN_ENEMY_INTERVAL = 2000

# Room and Corridor Classes
class Room:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def center(self):
        return (self.rect.centerx, self.rect.centery)

class Corridor:
    def __init__(self, start, end):
        self.start = start
        self.end = end

# BSP Algorithm for Dungeon Generation
class BSPNode:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.left = None
        self.right = None
        self.room = None

    def split(self, min_size):
        if self.left or self.right:
            return False

        horizontal = random.choice([True, False])
        if self.rect.width > self.rect.height and self.rect.width / self.rect.height >= 1.25:
            horizontal = False
        elif self.rect.height > self.rect.width and self.rect.height / self.rect.width >= 1.25:
            horizontal = True

        max_size = (self.rect.height if horizontal else self.rect.width) - min_size
        if max_size <= min_size:
            return False

        split = random.randint(min_size, max_size)
        if horizontal:
            self.left = BSPNode(self.rect.x, self.rect.y, self.rect.width, split)
            self.right = BSPNode(self.rect.x, self.rect.y + split, self.rect.width, self.rect.height - split)
        else:
            self.left = BSPNode(self.rect.x, self.rect.y, split, self.rect.height)
            self.right = BSPNode(self.rect.x + split, self.rect.y, self.rect.width - split, self.rect.height)

        return True

def generate_dungeon(width, height, min_room_size, max_room_size):
    root = BSPNode(0, 0, width, height)
    nodes = [root]
    split_nodes = []

    while nodes:
        node = nodes.pop()
        if node.split(min_room_size):
            nodes.append(node.left)
            nodes.append(node.right)
        else:
            split_nodes.append(node)

    rooms = []
    corridors = []

    for node in split_nodes:
        room_width = random.randint(min_room_size, min(max_room_size, node.rect.width))
        room_height = random.randint(min_room_size, min(max_room_size, node.rect.height))
        room_x = random.randint(node.rect.x, node.rect.x + node.rect.width - room_width)
        room_y = random.randint(node.rect.y, node.rect.y + node.rect.height - room_height)
        node.room = Room(room_x, room_y, room_width, room_height)
        rooms.append(node.room)

    for node in split_nodes:
        if node.left and node.right:
            corridors.append(Corridor(node.left.room.center(), node.right.room.center()))

    return rooms, corridors

def draw_dungeon(screen, rooms, corridors):
    for room in rooms:
        pygame.draw.rect(screen, WHITE, room.rect)

    for corridor in corridors:
        pygame.draw.line(screen, WHITE, corridor.start, corridor.end, 2)

# Game Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.xp = 0

    def shoot(self, target_x, target_y):
        bullet = Bullet(self.rect.centerx, self.rect.centery, target_x, target_y)
        return bullet

    def add_xp(self, amount):
        self.xp += amount

    def is_immune(self):
        return False

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10
        angle = math.atan2(target_y - y, target_x - x)
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        pass

class XP(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 255, 0))
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
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
game_over = False
score = 0
start_time = pygame.time.get_ticks()
last_spawn_time = pygame.time.get_ticks()

# Generate dungeon
rooms, corridors = generate_dungeon(SCREEN_WIDTH, SCREEN_HEIGHT, 50, 150)

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

        all_sprites.update()

        for enemy in enemies:
            enemy.update()

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

        screen.fill(BLACK)
        draw_dungeon(screen, rooms, corridors)
        all_sprites.draw(screen)

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        xp_text = font.render(f"XP: {player.xp}", True, WHITE)
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