# settings.py
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
TILE_SIZE = 50
PLAYER_SIZE = TILE_SIZE // 2  # Reduced player size to fit through doorways
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)  # Color for doors
MAP_WIDTH, MAP_HEIGHT = 50, 50  # in tiles
WORLD_WIDTH, WORLD_HEIGHT = MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE
TARGET_FPS = 60
player_speed = 200  # Pixels per second