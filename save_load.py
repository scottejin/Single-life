import os
import json
import pygame
import random
# import numpy as np  # Remove this import if you're using NumPy arrays
from player import Player
from bullet import Bullet
from enemy import Enemy
from strong_enemy import StrongEnemy
from xp_orb import XPOrb
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, player_speed
from enemy_spawner import EnemySpawner

SAVE_FOLDER = 'saves'

# Ensure the save folder exists
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)

def save_game(player_x, player_y, player, current_room_x, current_room_y, elapsed_time, xp_counter, seed, slot, dungeon_rooms, enemies, spawners, bullets, xp_orbs):
    if not os.path.exists(SAVE_FOLDER):
        os.makedirs(SAVE_FOLDER)
    save_data = {
        'player_x': player_x,
        'player_y': player_y,
        'player_health': player.health,
        'current_room_x': current_room_x,
        'current_room_y': current_room_y,
        'elapsed_time': elapsed_time,
        'xp_counter': xp_counter,
        'seed': seed,
        # Convert room data (2D lists) to serializable format
        'dungeon_rooms': {f"{k[0]},{k[1]}": room.tolist() if hasattr(room, 'tolist') else room 
                         for k, room in dungeon_rooms.items()},
        'enemies': [enemy.to_dict() for enemy in enemies if hasattr(enemy, 'to_dict')],
        'spawners': [spawner.to_dict() for spawner in spawners if hasattr(spawner, 'to_dict')],
        'bullets': [bullet.to_dict() for bullet in bullets if hasattr(bullet, 'to_dict')],
        'xp_orbs': [orb.to_dict() for orb in xp_orbs if hasattr(orb, 'to_dict')],
        # ...other game state data...
    }
    save_file = os.path.join(SAVE_FOLDER, f'save_slot_{slot}.json')
    with open(save_file, 'w') as f:
        json.dump(save_data, f, indent=4)

def load_game(slot):
    save_file = os.path.join(SAVE_FOLDER, f'save_slot_{slot}.json')
    if os.path.exists(save_file):
        with open(save_file, 'r') as f:
            save_data = json.load(f)
        
        # Reconstruct player
        player_x = save_data.get('player_x', 0)
        player_y = save_data.get('player_y', 0)
        player_health = save_data.get('player_health', 5)
        player = Player(player_x, player_y, player_speed)
        player.health = player_health
        
        # Reconstruct other game state
        current_room_x = save_data.get('current_room_x', 0)
        current_room_y = save_data.get('current_room_y', 0)
        elapsed_time = save_data.get('elapsed_time', 0)
        xp_counter = save_data.get('xp_counter', 0)
        seed = save_data.get('seed', str(random.randint(0, 1000000)))
        
        dungeon_rooms = {}
        for key_str, room_data in save_data.get('dungeon_rooms', {}).items():
            key = tuple(map(int, key_str.split(',')))
            # Use room_data directly as a list
            dungeon_rooms[key] = room_data
        
        enemies = [Enemy.from_dict(e) for e in save_data.get('enemies', [])]
        spawners = [EnemySpawner.from_dict(s) for s in save_data.get('spawners', [])]
        bullets = [Bullet.from_dict(b) for b in save_data.get('bullets', [])]
        xp_orbs = [XPOrb.from_dict(o) for o in save_data.get('xp_orbs', [])]
        
        return {
            'player': player,
            'current_room_x': current_room_x,
            'current_room_y': current_room_y,
            'elapsed_time': elapsed_time,
            'xp_counter': xp_counter,
            'seed': seed,
            'dungeon_rooms': dungeon_rooms,
            'enemies': enemies,
            'spawners': spawners,
            'bullets': bullets,
            'xp_orbs': xp_orbs,
        }
    else:
        return None

def get_available_saves():
    available_saves = {}
    for slot in range(1, 4):  # Assuming 3 slots
        save_file = os.path.join(SAVE_FOLDER, f'save_slot_{slot}.json')
        available_saves[slot] = os.path.exists(save_file)
    return available_saves

def show_no_saves_screen(screen):
    no_saves_screen = True
    font = pygame.font.SysFont(None, 50)
    arrow_font = pygame.font.SysFont(None, 36)
    while no_saves_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                # Check if the return arrow is clicked
                if return_arrow_rect.collidepoint(mouse_pos):
                    no_saves_screen = False  # Return to main menu
        screen.fill(BLACK)
        text = font.render("[No saves]", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)
        # Draw return arrow at top-left corner
        arrow_text = arrow_font.render("←", True, WHITE)
        return_arrow_rect = arrow_text.get_rect(topleft=(10, 10))
        screen.blit(arrow_text, return_arrow_rect)
        pygame.display.flip()

def delete_save_slot(slot):
    """Deletes the specified save slot with robust error handling."""
    save_file = os.path.join(SAVE_FOLDER, f'save_slot_{slot}.json')
    try:
        if os.path.exists(save_file):
            os.remove(save_file)
            print(f"Save slot {slot} has been deleted.")
        else:
            print(f"Save slot {slot} does not exist.")
    except PermissionError:
        print(f"Permission denied: Cannot delete save slot {slot}.")
        # Optionally, notify the user through the UI
    except Exception as e:
        print(f"An error occurred while deleting save slot {slot}: {e}")
        # Optionally, notify the user through the UI