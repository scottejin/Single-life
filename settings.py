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

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return {"spawn_interval": 3.0, "show_circle": True}
    with open(SETTINGS_FILE, 'r') as f:
        return json.load(f)

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f)

def save_spawn_interval():
    """Save the current spawn interval to a settings file."""
    settings = load_settings()
    settings['spawn_interval'] = current_spawn_interval
    save_settings(settings)

def load_spawn_interval():
    """Load the spawn interval from settings file."""
    global current_spawn_interval
    settings = load_settings()
    current_spawn_interval = settings.get('spawn_interval', DEFAULT_SPAWN_INTERVAL)
    return current_spawn_interval

def set_spawn_interval(value):
    global enemy_spawn_interval
    enemy_spawn_interval = value
    save_spawn_interval()

def get_spawn_interval():
    settings = load_settings()
    return settings.get("spawn_interval", 3.0)

def get_show_circle():
    settings = load_settings()
    return settings.get("show_circle", True)

def set_show_circle(value):
    settings = load_settings()
    settings["show_circle"] = value
    save_settings(settings)

# Load settings when module is imported
load_spawn_interval()