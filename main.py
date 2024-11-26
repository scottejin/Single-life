import pygame
import sys
import random
import time
import os
import json
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, PLAYER_SIZE, ENEMY_SIZE, WHITE, GREEN, RED, GRAY, BLACK, PURPLE, BLUE, ORANGE, MAP_WIDTH, MAP_HEIGHT, TARGET_FPS, player_speed, DARK_ORANGE
from map import load_room_at, find_walkable_tile
from player import Player
from bullet import Bullet
from menu import Menu
from main_menu import MainMenu
from enemy import Enemy
from strong_enemy import StrongEnemy  # Updated import
from enemy_spawner import EnemySpawner
from end_game import draw_end_game_screen, handle_end_game_events  # Import from end_game.py
from xp_orb import XPOrb  # Ensure XPOrb is imported
from save_load import save_game, load_game, show_no_saves_screen, get_available_saves  # Updated import

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED | pygame.DOUBLEBUF)
pygame.display.set_caption("Endless Dungeon Explorer")

seed = str(random.randint(0, 1000000))
random.seed(seed)

dungeon_rooms = {}
bullets = []
enemies = []
spawners = []
xp_orbs = []      # List to hold XP orbs
last_shot_time = 0
bullet_speed = 300  # Pixels per second
menu = Menu(seed)
main_menu = MainMenu()
is_paused = False
in_main_menu = True
in_end_game = False
start_time = time.time()
elapsed_time = 0
xp_counter = 0    # XP collected

selected_slot = None  # Holds the slot selected by the player

# Define circle_radius before the game loop
circle_radius = 6 * TILE_SIZE

# Initialize current_room_x and current_room_y
current_room_x, current_room_y = 0, 0

# Load the initial room and find a walkable tile for the player
initial_room = load_room_at(current_room_x, current_room_y, dungeon_rooms, enemies, spawners)
player_x, player_y = find_walkable_tile(initial_room)
player = Player(player_x, player_y, player_speed)

# Define where to save the game files
SAVE_FOLDER = 'saves'

# Ensure the save folder exists and cache available saves
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)
available_saves = get_available_saves()

def restart_game(seed):
    global dungeon_rooms, bullets, player, player_x, player_y, current_room_x, current_room_y, enemies, spawners, start_time, elapsed_time, xp_orbs, xp_counter, selected_slot
    random.seed(seed)
    dungeon_rooms = {}
    bullets = []
    enemies = []
    spawners = []
    xp_orbs = []
    current_room_x, current_room_y = 0, 0

    initial_room = load_room_at(0, 0, dungeon_rooms, enemies, spawners)
    for enemy in enemies:
        enemy.health = 2  # Set enemy health to 2
    player_x, player_y = find_walkable_tile(initial_room)
    player = Player(player_x, player_y, player_speed)
    start_time = time.time()
    elapsed_time = 0
    xp_counter = 0
    selected_slot = None  # Reset selected slot

clock = pygame.time.Clock()
running = True

while running:
    dt = clock.tick(TARGET_FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif in_main_menu:
            action = main_menu.handle_event(event)
            if action == "New Game":
                selected_slot = main_menu.select_save_slot(screen, "Select Slot to Save New Game")
                if selected_slot is not None:
                    restart_game(seed)
                    in_main_menu = False
                    start_time = time.time()
                    elapsed_time = 0
                else:
                    in_main_menu = True  # Return to main menu if no slot selected
            elif action == "Load Game":
                selected_slot = main_menu.select_save_slot(screen, "Select Slot to Load Game")
                if selected_slot is not None:
                    game_state = load_game(selected_slot)
                    if game_state:
                        # Load the game state
                        player = game_state['player']
                        player_x, player_y = player.get_position()
                        current_room_x = game_state['current_room_x']
                        current_room_y = game_state['current_room_y']
                        elapsed_time = game_state['elapsed_time']
                        xp_counter = game_state['xp_counter']
                        seed = game_state['seed']
                        dungeon_rooms = game_state['dungeon_rooms']
                        enemies = game_state['enemies']
                        for enemy in enemies:
                            enemy.health = 2  # Set enemy health to 2
                        spawners = game_state['spawners']
                        bullets = game_state['bullets']
                        xp_orbs = game_state['xp_orbs']
                        # ...load other game state data...
                        in_main_menu = False
                        start_time = time.time() - elapsed_time
                    else:
                        show_no_saves_screen(screen)
                        in_main_menu = True  # Return to main menu after showing the message
                else:
                    in_main_menu = True  # Return to main menu if no slot selected
            elif action == "Exit":
                running = False
        elif in_end_game:
            in_end_game, in_main_menu = handle_end_game_events(event, in_end_game, in_main_menu)
        elif not is_paused:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                is_paused = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                current_time = time.time()
                if current_time - last_shot_time >= 0.5:  # Limit to 2 bullets per second
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    direction = (mouse_x - SCREEN_WIDTH // 2, mouse_y - SCREEN_HEIGHT // 2)
                    direction_length = (direction[0]**2 + direction[1]**2)**0.5
                    if direction_length != 0:
                        direction = (direction[0] / direction_length, direction[1] / direction_length)
                        bullets.append(Bullet(player_x, player_y, direction, bullet_speed))
                        last_shot_time = current_time
        elif is_paused:
            action = menu.handle_event(event)
            if action == "Resume":
                is_paused = False
            elif action == "Save and Exit":
                if selected_slot is None:
                    selected_slot = main_menu.select_save_slot(screen, "Select Slot to Save Game")
                if selected_slot is not None:
                    save_game(
                        player_x, player_y, player,
                        current_room_x, current_room_y,
                        elapsed_time, xp_counter, seed,
                        selected_slot,
                        dungeon_rooms, enemies, spawners,
                        bullets, xp_orbs
                    )
                    in_main_menu = True
                    is_paused = False
                else:
                    is_paused = False  # Return to game if no slot selected

    if in_main_menu:
        main_menu.draw(screen)
    elif in_end_game:
        draw_end_game_screen(screen, elapsed_time, seed)
    elif not is_paused:
        elapsed_time = time.time() - start_time
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
                if bullet.check_collision(current_room, enemies, spawners, xp_orbs):
                    bullet.break_bullet()
            bullet_x, bullet_y = bullet.get_position()
            if bullet.is_broken:
                pygame.draw.circle(screen, (255, 255, 0), (int(bullet_x - camera_x), int(bullet_y - camera_y)), 5)  # Yellow for breaking animation
                bullets.remove(bullet)
            else:
                pygame.draw.circle(screen, RED, (int(bullet_x - camera_x), int(bullet_y - camera_y)), 5)

        for spawner in spawners:
            spawner.update(enemies, player_x, player_y, circle_radius)
            spawner.draw(screen, camera_x, camera_y)

        for enemy in enemies[:]:
            if enemy in enemies:  # Check if the enemy is still in the list
                enemy.move_towards_player(player_x, player_y, dt, current_room, player, enemies)
                enemy_x, enemy_y = enemy.get_position()
                if abs(enemy_x - player_x) < TILE_SIZE // 2 and abs(enemy_y - player_y) < TILE_SIZE // 2:
                    if enemy in enemies:  # Double-check before removing
                        enemies.remove(enemy)  # Remove enemy here
                        print(f"Enemy at ({enemy_x}, {enemy_y}) collided with player.")
                else:
                    # Draw enemy based on its type
                    if isinstance(enemy, StrongEnemy):
                        enemy.draw(screen, camera_x, camera_y)
                    else:
                        # Draw enemy border
                        pygame.draw.rect(screen, DARK_ORANGE, (enemy_x - camera_x, enemy_y - camera_y, ENEMY_SIZE, ENEMY_SIZE))

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

        for xp_orb in xp_orbs[:]:
            if xp_orb.update(player.rect):
                xp_counter += 1  # Increment XP by 1 per orb collected
                xp_orbs.remove(xp_orb)

        pygame.draw.rect(screen, RED, (SCREEN_WIDTH // 2 - PLAYER_SIZE // 2, SCREEN_HEIGHT // 2 - PLAYER_SIZE // 2, PLAYER_SIZE, PLAYER_SIZE))

        # Drawing the health bar
        health_bar_width = 100
        health_bar_height = 20
        health_ratio = player.health / 5
        pygame.draw.rect(screen, RED, (10, 10, health_bar_width, health_bar_height))  # Background
        pygame.draw.rect(screen, GREEN, (10, 10, health_bar_width * health_ratio, health_bar_height))  # Current health

        # Draw the blue circle
        pygame.draw.circle(screen, BLUE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), circle_radius, 1)

        for xp_orb in xp_orbs:
            xp_orb.draw(screen, camera_x, camera_y)

        # Draw XP counter below the health bar
        font = pygame.font.SysFont(None, 24)
        xp_text = font.render(f"XP: {xp_counter}", True, (255, 255, 255))
        screen.blit(xp_text, (10, 10 + health_bar_height + 5))

        # After updating the player and enemies
        if player.health <= 0:
            # Use a specific save slot, e.g., slot 1
            save_game(
                player_x, player_y, player,
                current_room_x, current_room_y,
                elapsed_time, xp_counter, seed,
                slot=1,  # Specify the slot
                dungeon_rooms=dungeon_rooms,
                enemies=enemies,
                spawners=spawners,
                bullets=bullets,
                xp_orbs=xp_orbs
            )
            in_end_game = True  # Enter the end game state
            print("Player has died. Entering end game state.")

    else:
        menu.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()