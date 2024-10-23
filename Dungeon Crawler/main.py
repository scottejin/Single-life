import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Define constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
TILE_SIZE = 50
PLAYER_SIZE = TILE_SIZE // 2  # Reduced player size to fit through doorways
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Endless Dungeon Explorer")

# Map settings
MAP_WIDTH, MAP_HEIGHT = 32, 24  # in tiles
WORLD_WIDTH, WORLD_HEIGHT = MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE

# Dictionary to store dungeon rooms (for endless generation)
dungeon_rooms = {}

# Binary Space Partitioning (BSP) room generation
class Room:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def center(self):
        return (self.x + self.width // 2, self.y + self.height // 2)

def create_room(dungeon_map, room):
    for y in range(room.height):
        for x in range(room.width):
            dungeon_map[room.y + y][room.x + x] = 0  # Carve out space

def create_h_tunnel(dungeon_map, x1, x2, y):
    for x in range(min(x1, x2), max(x1, x2) + 1):
        dungeon_map[y][x] = 0

def create_v_tunnel(dungeon_map, y1, y2, x):
    for y in range(min(y1, y2), max(y1, y2) + 1):
        dungeon_map[y][x] = 0

def generate_room_at(dungeon_map, origin_x, origin_y):
    """Generates a new room at the specified grid location."""
    max_rooms = 10
    min_room_size = 4
    max_room_size = 8
    rooms = []

    for _ in range(max_rooms):
        room_width = random.randint(min_room_size, max_room_size)
        room_height = random.randint(min_room_size, max_room_size)
        room_x = random.randint(1, MAP_WIDTH - room_width - 1)
        room_y = random.randint(1, MAP_HEIGHT - room_height - 1)
        new_room = Room(room_x, room_y, room_width, room_height)

        # Check if the new room intersects with any existing rooms
        failed = False
        for other_room in rooms:
            if (new_room.x < other_room.x + other_room.width and
                new_room.x + new_room.width > other_room.x and
                new_room.y < other_room.y + other_room.height and
                new_room.y + new_room.height > other_room.y):
                failed = True
                break

        if not failed:
            create_room(dungeon_map, new_room)

            if len(rooms) > 0:
                # Connect the new room to the previous room with a tunnel
                prev_room = rooms[-1]
                (prev_x, prev_y) = prev_room.center()
                (new_x, new_y) = new_room.center()

                if random.randint(0, 1) == 1:
                    # First move horizontally, then vertically
                    create_h_tunnel(dungeon_map, prev_x, new_x, prev_y)
                    create_v_tunnel(dungeon_map, prev_y, new_y, new_x)
                else:
                    # First move vertically, then horizontally
                    create_v_tunnel(dungeon_map, prev_y, new_y, prev_x)
                    create_h_tunnel(dungeon_map, prev_x, new_x, new_y)

            rooms.append(new_room)

    return dungeon_map

def load_room_at(player_grid_x, player_grid_y):
    """Load or generate a new room based on the player's grid position."""
    if (player_grid_x, player_grid_y) not in dungeon_rooms:
        dungeon_map = [[1 for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
        dungeon_map = generate_room_at(dungeon_map, player_grid_x, player_grid_y)
        dungeon_rooms[(player_grid_x, player_grid_y)] = dungeon_map
    return dungeon_rooms[(player_grid_x, player_grid_y)]

# Player starting position
player_x, player_y = MAP_WIDTH // 2 * TILE_SIZE, MAP_HEIGHT // 2 * TILE_SIZE
player_speed = 5

# Collision detection function
def is_walkable(x, y, dungeon_map):
    """Check if a position on the map is walkable (not a wall)."""
    map_x, map_y = x // TILE_SIZE, y // TILE_SIZE
    if map_x < 0 or map_x >= MAP_WIDTH or map_y < 0 or map_y >= MAP_HEIGHT:
        return False
    return dungeon_map[map_y][map_x] == 0

# Main game loop
clock = pygame.time.Clock()
running = True
current_room_x, current_room_y = 0, 0  # Start in the first room

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Load the current room based on player's grid position
    current_room = load_room_at(current_room_x, current_room_y)

    # Get key states for movement
    keys = pygame.key.get_pressed()
    new_player_x, new_player_y = player_x, player_y

    if keys[pygame.K_LEFT]:
        new_player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        new_player_x += player_speed
    if keys[pygame.K_UP]:
        new_player_y -= player_speed
    if keys[pygame.K_DOWN]:
        new_player_y += player_speed

    # Collision detection
    if is_walkable(new_player_x, player_y, current_room):
        player_x = new_player_x
    if is_walkable(player_x, new_player_y, current_room):
        player_y = new_player_y

    # Check if the player has moved to a new room (off the edge of the current room)
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

    # Calculate camera offset based on the player's position
    camera_x = player_x - SCREEN_WIDTH // 2
    camera_y = player_y - SCREEN_HEIGHT // 2

    # Fill the screen
    screen.fill(BLACK)

    # Draw the current dungeon room (only visible tiles)
    for row in range(MAP_HEIGHT):
        for col in range(MAP_WIDTH):
            tile_x = col * TILE_SIZE - camera_x
            tile_y = row * TILE_SIZE - camera_y

            if current_room[row][col] == 1:  # Wall
                pygame.draw.rect(screen, GRAY, (tile_x, tile_y, TILE_SIZE, TILE_SIZE))
            elif current_room[row][col] == 0:  # Path
                pygame.draw.rect(screen, WHITE, (tile_x, tile_y, TILE_SIZE, TILE_SIZE))

    # Draw the player (red cube)
    pygame.draw.rect(screen, RED, (SCREEN_WIDTH // 2 - PLAYER_SIZE // 2, SCREEN_HEIGHT // 2 - PLAYER_SIZE // 2, PLAYER_SIZE, PLAYER_SIZE))

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Clean up
pygame.quit()
sys.exit()
