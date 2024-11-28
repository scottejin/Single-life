import os
import json
import pygame
import random  # Ensure this is imported
from player import Player
from bullet import Bullet
from enemy import Enemy
from strong_enemy import StrongEnemy
from xp_orb import XPOrb
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, player_speed
from enemy_spawner import EnemySpawner
from sprites import get_sprite, load_sprite_sheet_image  # Add this import

SAVE_FOLDER = 'saves'

# Ensure the save folder exists
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)

def convert_dict_keys_to_str(d):
    """Convert tuple keys to string representation for JSON serialization"""
    if isinstance(d, dict):
        return {str(k): v for k, v in d.items()}
    return d

def object_to_dict(obj):
    """Convert an object to a serializable dictionary"""
    if hasattr(obj, 'to_dict'):
        return obj.to_dict()
    elif isinstance(obj, pygame.Surface):
        return None  # Skip pygame surfaces
    elif hasattr(obj, '__dict__'):
        return obj.__dict__
    return obj

def make_serializable(obj):
    """Convert complex objects to serializable format"""
    if isinstance(obj, (pygame.Surface, pygame.sprite.Sprite)):
        return None
    elif isinstance(obj, tuple):
        return list(obj)
    elif hasattr(obj, 'to_dict'):
        return obj.to_dict()
    elif hasattr(obj, '__dict__'):
        return {k: v for k, v in obj.__dict__.items() if not isinstance(v, (pygame.Surface, pygame.sprite.Sprite))}
    return obj

def save_game(slot, game_state):
    save_path = os.path.join(SAVE_FOLDER, f'save_slot_{slot}.json')
    
    # Convert game state to serializable format
    serializable_state = {
        'player_x': game_state['player_x'],
        'player_y': game_state['player_y'],
        'player_health': game_state['player_health'],
        'current_room_x': game_state['current_room_x'],
        'current_room_y': game_state['current_room_y'],
        'elapsed_time': game_state['elapsed_time'],
        'xp_counter': game_state['xp_counter'],
        'seed': game_state['seed'],
        'dungeon_rooms': {str(k): v for k, v in game_state['dungeon_rooms'].items()},
        'enemies': [make_serializable(e) for e in game_state['enemies']],
        'spawners': [spawner.to_dict() for spawner in game_state['spawners']],  # Ensure spawn_interval is included
        'bullets': [make_serializable(b) for b in game_state['bullets']],
        'xp_orbs': [make_serializable(o) for o in game_state['xp_orbs']]
    }
    
    with open(save_path, 'w') as f:
        json.dump(serializable_state, f)

def load_game(slot):
    save_file = os.path.join(SAVE_FOLDER, f'save_slot_{slot}.json')
    if os.path.exists(save_file):
        with open(save_file, 'r') as f:
            try:
                save_data = json.load(f)
            except json.JSONDecodeError:
                print("Error: Save file is corrupted")
                return None

        # Get sprites
        player_sprite = get_sprite(78, 7)
        enemy_sprite = load_sprite_sheet_image().subsurface((8 * 32, 78 * 32, 32, 32))

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

        # Convert string keys back to tuples for dungeon_rooms
        dungeon_rooms = {}
        for key_str, room_data in save_data.get('dungeon_rooms', {}).items():
            try:
                key = tuple(map(int, key_str.strip('()').split(',')))
                dungeon_rooms[key] = room_data
            except ValueError:
                continue

        # Reconstruct player
        player_x = save_data.get('player_x', 0)
        player_y = save_data.get('player_y', 0)
        player_health = save_data.get('player_health', 5)
        player = Player(player_x, player_y, player_speed, player_sprite)
        player.health = player_health
        
        # Reconstruct other game state
        current_room_x = save_data.get('current_room_x', 0)
        current_room_y = save_data.get('current_room_y', 0)
        elapsed_time = save_data.get('elapsed_time', 0)
        xp_counter = save_data.get('xp_counter', 0)
        seed = save_data.get('seed', str(random.randint(0, 1000000)))
        
        # Load enemies with proper sprites based on their type
        enemies = []
        for e in save_data.get('enemies', []):
            if e.get('type') == 'StrongEnemy':
                enemies.append(StrongEnemy.from_dict(e))
            else:
                enemies.append(Enemy.from_dict(e))

        spawners = [EnemySpawner.from_dict(s) for s in save_data.get('spawners', [])]
        bullets = []
        for b in save_data.get('bullets', []):
            bullets.append(Bullet.from_dict(b))  # Let from_dict handle sprite selection
        xp_orbs = [XPOrb.from_dict(o) for o in save_data.get('xp_orbs', [])]
        
        return {
            'player': player,
            'current_room_x': current_room_x,
            'current_room_y': current_room_y,
            'elapsed_time': elapsed_time,
            'xp_counter': xp_counter,
            'seed': seed,
            'dungeon_rooms': dungeon_rooms,  # Use the converted dungeon_rooms
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