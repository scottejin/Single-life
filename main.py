import pygame
import sys
import random
from settings import *
from map import load_room_at, find_walkable_tile, update_doors
from player import Player
from bullet import Bullet
from menu import Menu
from main_menu import MainMenu
from enemy import Enemy
import time

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED | pygame.DOUBLEBUF)
pygame.display.set_caption("Endless Dungeon Explorer")

seed = str(random.randint(0, 1000000))
random.seed(seed)

dungeon_rooms = {}
doors = []
bullets = []
enemies = []
last_shot_time = 0
bullet_speed = 300  # Pixels per second
menu = Menu(seed)
main_menu = MainMenu()
is_paused = False
in_main_menu = True

def restart_game(seed):
    global dungeon_rooms, doors, bullets, player, player_x, player_y, current_room_x, current_room_y, enemies
    random.seed(seed)
    dungeon_rooms = {}
    doors = []
    bullets = []
    enemies = []
    current_room_x, current_room_y = 0, 0
    initial_room = load_room_at(0, 0, dungeon_rooms, doors, enemies)
    player_x, player_y = find_walkable_tile(initial_room)
    player = Player(player_x, player_y, player_speed)

try:
    initial_room = load_room_at(0, 0, dungeon_rooms, doors, enemies)
    player_x, player_y = find_walkable_tile(initial_room)
except ValueError as e:
    print(f"Error during player initialization: {e}")
    pygame.quit()
    sys.exit()

player = Player(player_x, player_y, player_speed)

clock = pygame.time.Clock()
running = True
current_room_x, current_room_y = 0, 0

while running:
    dt = clock.tick(TARGET_FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif in_main_menu:
            action = main_menu.handle_event(event)
            if action == "Start Game":
                in_main_menu = False
            elif action == "Options":
                # Handle options menu
                pass
            elif action == "Instructions":
                # Handle instructions screen
                pass
            elif action == "Credits":
                # Handle credits screen
                pass
            elif action == "Exit":
                running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            is_paused = not is_paused
        elif is_paused:
            action = menu.handle_event(event)
            if action == "Restart":
                restart_game(seed)
                is_paused = False
            elif action == "Exit":
                in_main_menu = True
                is_paused = False
            elif action == "Seed":
                seed = menu.seed
                restart_game(seed)
                is_paused = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            current_time = time.time()
            if current_time - last_shot_time >= 0.5:  # Limit to 2 bullets per second
                mouse_x, mouse_y = pygame.mouse.get_pos()
                direction = (mouse_x - SCREEN_WIDTH // 2, mouse_y - SCREEN_HEIGHT // 2)
                direction_length = (direction[0]**2 + direction[1]**2)**0.5
                direction = (direction[0] / direction_length, direction[1] / direction_length)
                bullets.append(Bullet(player_x, player_y, direction, bullet_speed))
                last_shot_time = current_time

    if in_main_menu:
        main_menu.draw(screen)
    elif not is_paused:
        current_room = load_room_at(current_room_x, current_room_y, dungeon_rooms, doors, enemies)

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -1
        if keys[pygame.K_RIGHT]:
            dx = 1
        if keys[pygame.K_UP]:
            dy = -1
        if keys[pygame.K_DOWN]:
            dy = 1

        player.move(dx, dy, dt, current_room, doors)
        player_x, player_y = player.get_position()

        update_doors(player_x, player_y, doors)

        if player_x < 0:
            current_room_x -= 1
            player_x = (MAP_WIDTH - 1) * TILE_SIZE
        elif player_x >= MAP_WIDTH * TILE_SIZE:
            current_room_x += 1
            player_x = 0
        if player_y < 0:
            current_room_y -= 1
            player_y = (MAP_HEIGHT - 1) * TILE_SIZE
        elif player_y >= MAP_HEIGHT * TILE_SIZE:
            current_room_y += 1
            player_y = 0

        camera_x = int(player_x - SCREEN_WIDTH // 2)
        camera_y = int(player_y - SCREEN_HEIGHT // 2)

        screen.fill(BLACK)

        for row in range(MAP_HEIGHT):
            for col in range(MAP_WIDTH):
                tile_x = col * TILE_SIZE - camera_x
                tile_y = row * TILE_SIZE - camera_y

                if current_room[row][col] == 1:
                    pygame.draw.rect(screen, GRAY, (tile_x, tile_y, TILE_SIZE, TILE_SIZE))
                elif current_room[row][col] == 0:
                    pygame.draw.rect(screen, WHITE, (tile_x, tile_y, TILE_SIZE, TILE_SIZE))

        for door in doors:
            tile_x = door.x * TILE_SIZE - camera_x
            tile_y = door.y * TILE_SIZE - camera_y
            color = GRAY if door.is_open else BLUE
            pygame.draw.rect(screen, color, (tile_x, tile_y, TILE_SIZE, TILE_SIZE))

        for bullet in bullets[:]:
            if not bullet.is_broken:
                bullet.move(dt)
                if bullet.check_collision(current_room, enemies):
                    bullet.break_bullet()
            bullet_x, bullet_y = bullet.get_position()
            if bullet.is_broken:
                pygame.draw.circle(screen, (255, 255, 0), (int(bullet_x - camera_x), int(bullet_y - camera_y)), 5)  # Yellow for breaking animation
                bullets.remove(bullet)
            else:
                pygame.draw.circle(screen, RED, (int(bullet_x - camera_x), int(bullet_y - camera_y)), 5)

        for enemy in enemies:
            enemy_x, enemy_y = enemy.get_position()
            health_ratio = enemy.health / 2
            inner_color = ORANGE if health_ratio == 1 else (255, 140, 0)  # Darker orange if damaged
            pygame.draw.rect(screen, ORANGE, (enemy_x - camera_x, enemy_y - camera_y, ENEMY_SIZE, ENEMY_SIZE))
            pygame.draw.rect(screen, inner_color, (enemy_x - camera_x + 2, enemy_y - camera_y + 2, ENEMY_SIZE - 4, ENEMY_SIZE - 4))
            pygame.draw.rect(screen, BLACK, (enemy_x - camera_x + 2, enemy_y - camera_y + 2, (ENEMY_SIZE - 4) * health_ratio, ENEMY_SIZE - 4))

        pygame.draw.rect(screen, RED, (SCREEN_WIDTH // 2 - PLAYER_SIZE // 2, SCREEN_HEIGHT // 2 - PLAYER_SIZE // 2, PLAYER_SIZE, PLAYER_SIZE))

    else:
        menu.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()