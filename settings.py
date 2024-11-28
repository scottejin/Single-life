import json
import os

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
TILE_SIZE = 50
PLAYER_SIZE = TILE_SIZE // 2  # Reduced player size to fit through doorways
ENEMY_SIZE = PLAYER_SIZE - 5  # Slightly smaller than the player
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)  # Color for the spawner
BLUE = (0, 0, 255)  # Color for doors
ORANGE = (255, 165, 0)  # Color for enemies
GREEN = (0, 255, 0)
DARK_ORANGE = (255, 140, 0)  # Adjust RGB as desired
MAP_WIDTH, MAP_HEIGHT = 50, 50  # in tiles
WORLD_WIDTH, WORLD_HEIGHT = MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE
TARGET_FPS = 60
player_speed = 200  # Pixels per second

ENEMY_SPAWN_INTERVAL_DEFAULT = 5  # Default to 5 seconds
enemy_spawn_interval = ENEMY_SPAWN_INTERVAL_DEFAULT

SETTINGS_FILE = 'settings.json'
DEFAULT_SPAWN_INTERVAL = 5.0
current_spawn_interval = DEFAULT_SPAWN_INTERVAL

def save_spawn_interval():
    """Save the current spawn interval to a settings file."""
    settings = {}
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            settings = json.load(f)
    
    settings['spawn_interval'] = current_spawn_interval
    
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f)

def load_spawn_interval():
    """Load the spawn interval from settings file."""
    global current_spawn_interval
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            settings = json.load(f)
            current_spawn_interval = settings.get('spawn_interval', DEFAULT_SPAWN_INTERVAL)
    return current_spawn_interval

def set_spawn_interval(value):
    global enemy_spawn_interval
    enemy_spawn_interval = value
    save_spawn_interval()

def get_spawn_interval():
    return enemy_spawn_interval

# Load settings when module is imported
load_spawn_interval()