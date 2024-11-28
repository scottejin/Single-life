import pygame
import sys
import random
import time
import os
import json
import math  # Import math module
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, PLAYER_SIZE, ENEMY_SIZE, WHITE, GREEN, RED, GRAY, BLACK, PURPLE, BLUE, ORANGE, MAP_WIDTH, MAP_HEIGHT, TARGET_FPS, player_speed, DARK_ORANGE, get_spawn_interval  # Import the get_spawn_interval function
from map import load_room_at, find_walkable_tile
from player import Player
from bullet import Bullet
from menu import Menu
from main_menu import MainMenu
from enemy import Enemy
from strong_enemy import StrongEnemy  # Updated import
from enemy_spawner import EnemySpawner
from xp_orb import XPOrb  # Ensure XPOrb is imported
from save_load import save_game, load_game, show_no_saves_screen, get_available_saves  # Updated import
from end_game import draw_death_screen, handle_death_screen_events
import music  # Import the music module
from win import draw_victory_screen  # Import the victory screen function

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED | pygame.DOUBLEBUF)
pygame.display.set_caption("Endless Dungeon Explorer")

from sprites import load_sprite_sheet, load_sprite_sheet_image, get_sprite  # Import get_sprite

bullet_sound = None
try:
    sound_file = os.path.join('sounds', 'gun.wav')
    if (os.path.exists(sound_file)):
        bullet_sound = pygame.mixer.Sound(sound_file)
        bullet_sound.set_volume(0.3)
except (pygame.error, FileNotFoundError) as e:
    print(f"Warning: Could not load bullet sound: {e}")

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
previous_slot = None  # Add this line to track the previous save slot

# Define circle_radius before the game loop
circle_radius = 6 * TILE_SIZE

# Initialize current_room_x and current_room_y
current_room_x, current_room_y = 0, 0

# Update the call to load_sprite_sheet and assign sprites before loading the initial room
all_sprites = load_sprite_sheet(32, 32)
player_sprite = get_sprite(78, 7)  # Select sprite at row 78, column 7 for left movement
player_sprite_right = get_sprite(78, 8)  # Select sprite at row 78, column 8 for right movement
enemy_sprite = get_sprite(78, 8)  # Select sprite at row 78, column 8
wall_sprite = pygame.transform.scale(get_sprite(14, 23), (TILE_SIZE, TILE_SIZE))  # Update this line to load wall sprite from row 14, column 23

# Load bullet sprites for all directions
bullet_sprites = {
    'north': get_sprite(25, 7),
    'northeast': get_sprite(25, 8),
    'east': get_sprite(25, 9),
    'southeast': get_sprite(25, 10),
    'south': get_sprite(25, 11),
    'southwest': get_sprite(25, 12),
    'west': get_sprite(25, 13),
    'northwest': get_sprite(25, 14)
}
# Remove the old bullet_sprite assignment
# bullet_sprite = get_sprite(25, 8)

# Preload and cache wall sprites from row 14, columns 23 to 29
wall_sprites = [
    pygame.transform.scale(get_sprite(14, col), (TILE_SIZE, TILE_SIZE))
    for col in range(23, 30)
]

# Load bricks sprite sheet
bricks_sprites = load_sprite_sheet_image('assets/bricks.png', 32, 32)

# Replace walkable_sprites definition
walkable_sprites = [
    get_sprite(bricks_sprites, 1, 1)  # Use bricks.png sprite at (1,1)
]
# ...existing code...

# Load the initial room and find a walkable tile for the player
initial_room = load_room_at(current_room_x, current_room_y, dungeon_rooms, enemies, spawners, enemy_sprite)
player_x, player_y = find_walkable_tile(initial_room)

# Assign a random sprite to each wall and walkable tile
wall_tile_sprites = []
walkable_tile_sprites = []  # New list for walkable tile sprites
for row in range(MAP_HEIGHT):
    row_sprites = []
    walkable_row_sprites = []  # New list for walkable sprites in the row
    for col in range(MAP_WIDTH):
        if (initial_room[row][col] == 1):
            sprite = random.choice(wall_sprites)
            row_sprites.append(sprite)
            walkable_row_sprites.append(None)  # No sprite for wall tiles
        elif (initial_room[row][col] == 0):
            sprite = random.choice(walkable_sprites)
            row_sprites.append(sprite)  # Optional: If you want to keep using row_sprites for walkable tiles
            walkable_row_sprites.append(sprite)  # Assign sprite to walkable tile
        else:
            row_sprites.append(pygame.Surface((TILE_SIZE, TILE_SIZE)))  # Ensure non-wall tiles have a surface
            walkable_row_sprites.append(None)
    wall_tile_sprites.append(row_sprites)
    walkable_tile_sprites.append(walkable_row_sprites)  # Append the walkable row sprites

# Update player initialization
player = Player(player_x, player_y, player_speed, player_sprite)

# Define where to save the game files
SAVE_FOLDER = 'saves'

# Ensure the save folder exists and cache available saves
if (not os.path.exists(SAVE_FOLDER)):
    os.makedirs(SAVE_FOLDER)
available_saves = get_available_saves()

def restart_game(seed):
    global dungeon_rooms, bullets, player, player_x, player_y, current_room_x, current_room_y, enemies, spawners, start_time, elapsed_time, xp_orbs, xp_counter, wall_tile_sprites, walkable_tile_sprites
    random.seed(seed)
    dungeon_rooms = {}
    bullets = []
    enemies = []
    spawners = []
    xp_orbs = []
    current_room_x, current_room_y = 0, 0

    initial_room = load_room_at(0, 0, dungeon_rooms, enemies, spawners, enemy_sprite)
    for enemy in enemies:
        enemy.health = 2  # Set enemy health to 2
    player_x, player_y = find_walkable_tile(initial_room)
    player = Player(player_x, player_y, player_speed, player_sprite)
    start_time = time.time()
    elapsed_time = 0
    xp_counter = 0
    wall_tile_sprites = []
    walkable_tile_sprites = []  # Reset walkable tile sprites
    for row in range(MAP_HEIGHT):
        row_sprites = []
        walkable_row_sprites = []
        for col in range(MAP_WIDTH):
            if (initial_room[row][col] == 1):
                sprite = random.choice(wall_sprites)
                row_sprites.append(sprite)
                walkable_row_sprites.append(None)
            elif (initial_room[row][col] == 0):
                sprite = random.choice(walkable_sprites)
                row_sprites.append(sprite)
                walkable_row_sprites.append(sprite)
            else:
                row_sprites.append(pygame.Surface((TILE_SIZE, TILE_SIZE)))
                walkable_row_sprites.append(None)
        wall_tile_sprites.append(row_sprites)
        walkable_tile_sprites.append(walkable_row_sprites)
    
    for spawner in spawners:
        spawner.spawn_interval = get_spawn_interval()  # Set spawn interval

clock = pygame.time.Clock()
running = True

def create_bullet():
    global last_shot_time
    current_time = time.time()
    if (current_time - last_shot_time < 0.5):  # Limit to one bullet every 500 ms
        return
    last_shot_time = current_time
    mouse_x, mouse_y = pygame.mouse.get_pos()
    direction = (mouse_x - SCREEN_WIDTH // 2, mouse_y - SCREEN_HEIGHT // 2)
    direction_length = (direction[0]**2 + direction[1]**2)**0.5
    if (direction_length != 0):
        direction = (direction[0] / direction_length, direction[1] / direction_length)
        angle = math.degrees(math.atan2(-direction[1], direction[0])) % 360  # Invert y for screen coordinates
        if (22.5 <= angle < 67.5):
            direction_name = 'northeast'
        elif (67.5 <= angle < 112.5):
            direction_name = 'north'
        elif (112.5 <= angle < 157.5):
            direction_name = 'northwest'
        elif (157.5 <= angle < 202.5):
            direction_name = 'west'
        elif (202.5 <= angle < 247.5):
            direction_name = 'southwest'
        elif (247.5 <= angle < 292.5):
            direction_name = 'south'
        elif (292.5 <= angle < 337.5):
            direction_name = 'southeast'
        else:
            direction_name = 'east'
        selected_sprite = bullet_sprites[direction_name]
        new_bullet = Bullet(player_x, player_y, direction, bullet_speed, selected_sprite)
        bullets.append(new_bullet)
        if (bullet_sound):
            bullet_sound.play()

def create_enemy(x, y):
    new_enemy = Enemy(x, y, enemy_sprite)
    enemies.append(new_enemy)

def handle_save_and_exit():
    if (selected_slot is not None):
        save_game(selected_slot, {
            'player_x': player_x,
            'player_y': player_y,
            'player_health': player.health,
            'current_room_x': current_room_x,
            'current_room_y': current_room_y,
            'elapsed_time': elapsed_time,
            'xp_counter': xp_counter,
            'seed': seed,
            'dungeon_rooms': dungeon_rooms,
            'enemies': enemies,
            'spawners': spawners,
            'bullets': bullets,
            'xp_orbs': xp_orbs
        })
        pygame.quit()
        sys.exit()

# Ensure the music starts playing when the game starts
music.play_music()

while running:
    dt = clock.tick(TARGET_FPS) / 1000.0

    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False
        elif (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            if (is_paused):
                is_paused = False  # Return to game
            elif (not in_main_menu and not in_end_game):
                is_paused = True  # Open pause menu
            elif (in_end_game):
                in_end_game = False
                in_main_menu = True  # Return to main menu
        elif (event.type == pygame.KEYDOWN and event.key == pygame.K_m):
            music.next_track()
        elif (event.type == pygame.USEREVENT):
            music.handle_music_event(event)
        elif (in_main_menu):
            action = main_menu.handle_event(event)
            if (action == "New Game"):
                selected_slot = main_menu.select_save_slot(screen, "Select Slot to Save New Game", mode="save")
                if (selected_slot is not None):
                    restart_game(seed)
                    in_main_menu = False
                    start_time = time.time()
                    elapsed_time = 0
                else:
                    in_main_menu = True  # Return to main menu if no slot selected
            elif (action == "Load Game"):
                selected_slot = main_menu.select_save_slot(screen, "Select Slot to Load Game", mode="load")
                if (selected_slot is not None):
                    game_state = load_game(selected_slot)
                    if (game_state):
                        # Load the game state
                        player = game_state['player']
                        player_x, player_y = player.get_position()
                        current_room_x = game_state['current_room_x']
                        current_room_y = game_state['current_room_y']
                        elapsed_time = game_state['elapsed_time']
                        xp_counter = game_state['xp_counter']
                        seed = game_state['seed']
                        random.seed(seed)  # Reset the random seed
                        dungeon_rooms = game_state['dungeon_rooms']
                        enemies = game_state['enemies']
                        spawners = game_state['spawners']
                        bullets = game_state['bullets']
                        xp_orbs = game_state['xp_orbs']
                        # Reconstruct the current room
                        current_room = load_room_at(current_room_x, current_room_y, dungeon_rooms, enemies, spawners, enemy_sprite)
                        # Ensure player is on a walkable tile
                        tile_x = int(player_x // TILE_SIZE)
                        tile_y = int(player_y // TILE_SIZE)
                        if (current_room[tile_y][tile_x] == 1):  # If tile is a wall
                            player_x, player_y = find_walkable_tile(current_room)
                            player.set_position(player_x, player_y)
                        in_main_menu = False
                        start_time = time.time() - elapsed_time
                    else:
                        show_no_saves_screen(screen)
                        in_main_menu = True  # Return to main menu after showing the message
                else:
                    in_main_menu = True  # Return to main menu if no slot selected
            elif (action == "Save and Exit"):
                handle_save_and_exit()
            elif (action == "Exit"):
                running = False
        elif (in_end_game):
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                in_end_game = False
                in_main_menu = True
                restart_game(seed)
        elif (not is_paused):
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                is_paused = True
            elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):  # Left click
                create_bullet()
        elif (is_paused):
            action = menu.handle_event(event)
            if (action == "Save and Exit"):
                handle_save_and_exit()
            elif (action == "Resume"):
                is_paused = False

    if (in_main_menu):
        main_menu.draw(screen)
        music.update_track_display(screen, right_side=True)
        # ...existing code...
    elif (in_end_game):
        draw_death_screen(screen, elapsed_time, xp_counter, seed, selected_slot)
        music.update_track_display(screen, right_side=True)
    elif (not is_paused):
        elapsed_time = time.time() - start_time
        current_room = load_room_at(current_room_x, current_room_y, dungeon_rooms, enemies, spawners, enemy_sprite)

        # Define camera_x and camera_y before using them
        camera_x = int(player_x - SCREEN_WIDTH // 2)
        camera_y = int(player_y - SCREEN_HEIGHT // 2)

        for row in range(MAP_HEIGHT):
            for col in range(MAP_WIDTH):
                tile_x = col * TILE_SIZE - camera_x
                tile_y = row * TILE_SIZE - camera_y

                if (current_room[row][col] == 1):
                    sprite = wall_tile_sprites[row][col]
                    if (sprite):  # Ensure sprite is not None
                        screen.blit(sprite, (tile_x, tile_y))
                elif (current_room[row][col] == 0):
                    sprite = walkable_tile_sprites[row][col]
                    if (sprite):
                        screen.blit(sprite, (tile_x, tile_y))
                    else:
                        pygame.draw.rect(screen, WHITE, (tile_x, tile_y, TILE_SIZE, TILE_SIZE))
                else:
                    pygame.draw.rect(screen, GRAY, (tile_x, tile_y, TILE_SIZE, TILE_SIZE))  # Assign a default color for other tiles

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]):
            dx = -1
            player.sprite = player_sprite  # Change to left-facing sprite
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            dx = 1
            player.sprite = player_sprite_right  # Change to right-facing sprite
        if (keys[pygame.K_UP] or keys[pygame.K_w]):
            dy = -1
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]):
            dy = 1

        player.move(dx, dy, dt, current_room)
        player_x, player_y = player.get_position()

        if (player_x < 0):
            current_room_x -= 1
            player_x = (MAP_WIDTH - 1) * TILE_SIZE
        elif (player_x >= MAP_WIDTH * TILE_SIZE):
            current_room_x += 1
            player_x = 0
        if (player_y < 0):
            current_room_y -= 1
            player_y = (MAP_HEIGHT - 1) * TILE_SIZE
        elif (player_y >= MAP_HEIGHT * TILE_SIZE):
            player_y = 0

        camera_x = int(player_x - SCREEN_WIDTH // 2)
        camera_y = int(player_y - SCREEN_HEIGHT // 2)

        screen.fill(BLACK)

        for row in range(MAP_HEIGHT):
            for col in range(MAP_WIDTH):
                tile_x = col * TILE_SIZE - camera_x
                tile_y = row * TILE_SIZE - camera_y

                if (current_room[row][col] == 1):
                    sprite = wall_tile_sprites[row][col]
                    if (sprite):  # Ensure sprite is not None
                        screen.blit(sprite, (tile_x, tile_y))
                elif (current_room[row][col] == 0):
                    sprite = walkable_tile_sprites[row][col]
                    if (sprite):
                        screen.blit(sprite, (tile_x, tile_y))
                    else:
                        pygame.draw.rect(screen, WHITE, (tile_x, tile_y, TILE_SIZE, TILE_SIZE))
                else:
                    pygame.draw.rect(screen, GRAY, (tile_x, tile_y, TILE_SIZE, TILE_SIZE))  # Assign a default color for other tiles

        for bullet in bullets[:]:
            if (not bullet.is_broken):
                bullet.move(dt)
                if (bullet.check_collision(current_room, enemies, spawners, xp_orbs)):
                    bullet.break_bullet()
            bullet_x, bullet_y = bullet.get_position()
            if (bullet.is_broken):
                pygame.draw.circle(screen, (255, 255, 0), (int(bullet_x - camera_x), int(bullet_y - camera_y)), 5)  # Yellow for breaking animation
                bullets.remove(bullet)
            else:
                bullet.draw(screen, camera_x, camera_y)

        for spawner in spawners:
            spawner.update(enemies, player_x, player_y, circle_radius)
            spawner.draw(screen, camera_x, camera_y)

        for enemy in enemies[:]:
            if (enemy in enemies):  # Check if the enemy is still in the list
                enemy.move_towards_player(player_x, player_y, dt, current_room, player, enemies)
                enemy_x, enemy_y = enemy.get_position()
                if (abs(enemy_x - player_x) < TILE_SIZE // 2 and abs(enemy_y - player_y) < TILE_SIZE // 2):
                    if (enemy in enemies):  # Double-check before removing
                        enemies.remove(enemy)  # Remove enemy here
                        print(f"Enemy at ({enemy_x}, {enemy_y}) collided with player.")
                else:
                    # Draw enemy based on its type
                    if (isinstance(enemy, StrongEnemy)):
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
            if (xp_orb.update(player.rect)):
                xp_counter += 1  # Increment XP by 1 per orb collected
                xp_orbs.remove(xp_orb)

        player.draw(screen, camera_x, camera_y)

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

        # Check if player health is 1 and play boss music
        if player.health == 1 and not music.is_boss_mode:
            music.play_boss_music()

        # Check for victory condition
        if all(spawner.is_defeated for spawner in spawners):
            screen.fill(BLACK)
            draw_victory_screen(screen, elapsed_time, xp_counter, seed)
            pygame.display.flip()
            
            # Handle victory screen events
            waiting_for_input = True
            while waiting_for_input:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        waiting_for_input = False
                        in_main_menu = True
                        restart_game(seed)  # Reset game state

        # After updating the player and enemies
        if (player.health <= 0):
            in_end_game = True
            screen.fill(BLACK)
            draw_death_screen(screen, elapsed_time, xp_counter, seed, selected_slot)
            pygame.display.flip()
            
            # Handle death screen events
            waiting_for_input = True
            while (waiting_for_input):
                for event in pygame.event.get():
                    if (event.type == pygame.QUIT):
                        pygame.quit()
                        sys.exit()
                    if (handle_death_screen_events(event, selected_slot)):
                        waiting_for_input = False
                        in_main_menu = True
                        restart_game(seed)  # Reset game state

        # Update the music track display
        music.update_track_display(screen, right_side=True)

    else:
        menu.draw(screen)
        music.update_track_display(screen, right_side=True)

    pygame.display.flip()

pygame.quit()
sys.exit()