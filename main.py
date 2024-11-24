import pygame
import sys
import random
import time
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, PLAYER_SIZE, ENEMY_SIZE, WHITE, GREEN, RED, GRAY, BLACK, PURPLE, BLUE, ORANGE, MAP_WIDTH, MAP_HEIGHT, TARGET_FPS, player_speed
from map import load_room_at, find_walkable_tile
from player import Player
from bullet import Bullet
from menu import Menu
from main_menu import MainMenu
from enemy import Enemy
from enemy_spawner import EnemySpawner
from end_game import draw_end_game_screen, handle_end_game_events  # Import from end_game.py

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED | pygame.DOUBLEBUF)
pygame.display.set_caption("Endless Dungeon Explorer")

seed = str(random.randint(0, 1000000))
random.seed(seed)

dungeon_rooms = {}
bullets = []
enemies = []
spawners = []
last_shot_time = 0
bullet_speed = 300  # Pixels per second
menu = Menu(seed)
main_menu = MainMenu()
is_paused = False
in_main_menu = True
in_end_game = False
start_time = time.time()

# Define circle_radius before the game loop
circle_radius = 6 * TILE_SIZE

# Initialize current_room_x and current_room_y
current_room_x, current_room_y = 0, 0

# Load the initial room and find a walkable tile for the player
initial_room = load_room_at(current_room_x, current_room_y, dungeon_rooms, enemies, spawners)
player_x, player_y = find_walkable_tile(initial_room)
player = Player(player_x, player_y, player_speed)

def restart_game(seed):
    global dungeon_rooms, bullets, player, player_x, player_y, current_room_x, current_room_y, enemies, spawners
    random.seed(seed)
    dungeon_rooms = {}
    bullets = []
    enemies = []
    spawners = []
    current_room_x, current_room_y = 0, 0

    while True:
        initial_room = load_room_at(0, 0, dungeon_rooms, enemies, spawners)
        break

    player_x, player_y = find_walkable_tile(initial_room)
    player = Player(player_x, player_y, player_speed)

clock = pygame.time.Clock()
running = True

while running:
    dt = clock.tick(TARGET_FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif in_main_menu:
            action = main_menu.handle_event(event)
            if action == "Start Game":
                in_main_menu = False
                start_time = time.time()
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
        elif in_end_game:
            in_end_game, in_main_menu = handle_end_game_events(event, in_end_game, in_main_menu)
        elif not is_paused:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
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
    elif in_end_game:
        elapsed_time = time.time() - start_time
        draw_end_game_screen(screen, elapsed_time, seed)
    elif not is_paused:
        current_room = load_room_at(current_room_x, current_room_y, dungeon_rooms, enemies, spawners)

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = 1

        player.move(dx, dy, dt, current_room)
        player_x, player_y = player.get_position()

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

        for bullet in bullets[:]:
            if not bullet.is_broken:
                bullet.move(dt)
                if bullet.check_collision(current_room, enemies, spawners):
                    bullet.break_bullet()
            bullet_x, bullet_y = bullet.get_position()
            if bullet.is_broken:
                pygame.draw.circle(screen, (255, 255, 0), (int(bullet_x - camera_x), int(bullet_y - camera_y)), 5)  # Yellow for breaking animation
                bullets.remove(bullet)
            else:
                pygame.draw.circle(screen, RED, (int(bullet_x - camera_x), int(bullet_y - camera_y)), 5)

        # Update and draw enemies
        for spawner in spawners:
            spawner.update(enemies, player_x, player_y, circle_radius)
            spawner.draw(screen, camera_x, camera_y)

        for enemy in enemies[:]:
            if enemy in enemies:  # Check if the enemy is still in the list
                enemy.move_towards_player(player_x, player_y, dt, current_room, player, enemies)
                enemy_x, enemy_y = enemy.get_position()
                if abs(enemy_x - player_x) < TILE_SIZE // 2 and abs(enemy_y - player_y) < TILE_SIZE // 2:
                    if enemy in enemies:  # Double-check before removing
                        enemies.remove(enemy)
                else:
                    # Draw enemy border
                    pygame.draw.rect(screen, ORANGE, (enemy_x - camera_x, enemy_y - camera_y, ENEMY_SIZE, ENEMY_SIZE))

                    # Draw solid orange inside
                    pygame.draw.rect(screen, ORANGE, (enemy_x - camera_x + 2, enemy_y - camera_y + 2, ENEMY_SIZE - 4, ENEMY_SIZE - 4))

                    # Calculate damage ratio
                    damage_ratio = (enemy.max_health - enemy.health) / enemy.max_health

                    # Draw black rectangle proportional to damage taken
                    pygame.draw.rect(
                        screen,
                        BLACK,
                        (
                            enemy_x - camera_x + 2,
                            enemy_y - camera_y + 2,
                            ENEMY_SIZE - 4,
                            (ENEMY_SIZE - 4) * damage_ratio  # Height increases as damage increases
                        )
                    )

        pygame.draw.rect(screen, RED, (SCREEN_WIDTH // 2 - PLAYER_SIZE // 2, SCREEN_HEIGHT // 2 - PLAYER_SIZE // 2, PLAYER_SIZE, PLAYER_SIZE))

        # Drawing the health bar
        health_bar_width = 100
        health_bar_height = 20
        health_ratio = player.health / 5
        pygame.draw.rect(screen, RED, (10, 10, health_bar_width, health_bar_height))  # Background
        pygame.draw.rect(screen, GREEN, (10, 10, health_bar_width * health_ratio, health_bar_height))  # Current health

        # After updating the player and enemies
        if player.health <= 0:
            in_end_game = True  # Enter the end game state

    else:
        menu.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()