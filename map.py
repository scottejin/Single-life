import random
from settings import TILE_SIZE, MAP_WIDTH, MAP_HEIGHT
from utils import count_white_spaces
from enemy import Enemy
from enemy_spawner import EnemySpawner

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

    # Ensure a 2x2 space for enemy spawning
    spawn_x = room.x + room.width // 2 - 1
    spawn_y = room.y + room.height // 2 - 1
    for y in range(2):
        for x in range(2):
            dungeon_map[spawn_y + y][spawn_x + x] = 0

def create_h_tunnel(dungeon_map, x1, x2, y):
    max_length = 20
    if abs(x2 - x1) > max_length:
        if x2 > x1:
            x2 = x1 + max_length
        else:
            x2 = x1 - max_length
    for x in range(min(x1, x2), max(x1, x2) + 1):
        dungeon_map[y][x] = 0

def create_v_tunnel(dungeon_map, y1, y2, x):
    max_length = 20
    if abs(y2 - y1) > max_length:
        if y2 > y1:
            y2 = y1 + max_length
        else:
            y2 = y1 - max_length
    for y in range(min(y1, y2), max(y1, y2) + 1):
        dungeon_map[y][x] = 0

def generate_room_at(dungeon_map, origin_x, origin_y, enemies, spawners):
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

            if rooms:
                prev_room = rooms[-1]
                (prev_x, prev_y) = prev_room.center()
                (new_x, new_y) = new_room.center()

                if random.randint(0, 1) == 1:
                    create_h_tunnel(dungeon_map, prev_x, new_x, prev_y)
                    create_v_tunnel(dungeon_map, prev_y, new_y, new_x)
                else:
                    create_v_tunnel(dungeon_map, prev_y, new_y, prev_x)
                    create_h_tunnel(dungeon_map, prev_x, new_x, new_y)

            # Spawn an enemy spawner in the room
            spawn_x = new_room.x + new_room.width // 2
            spawn_y = new_room.y + new_room.height // 2
            spawners.append(EnemySpawner(spawn_x * TILE_SIZE, spawn_y * TILE_SIZE))

            rooms.append(new_room)

    return dungeon_map

def load_room_at(x, y, dungeon_rooms, enemies, spawners):
    if (x, y) not in dungeon_rooms:
        dungeon_map = [[1 for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
        dungeon_map = generate_room_at(dungeon_map, x, y, enemies, spawners)
        dungeon_rooms[(x, y)] = dungeon_map
    return dungeon_rooms[(x, y)]

def find_walkable_tile(dungeon_map):
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            if dungeon_map[y][x] == 0:
                return x * TILE_SIZE, y * TILE_SIZE
    raise ValueError("No walkable tile found")