import random
from settings import TILE_SIZE, MAP_WIDTH, MAP_HEIGHT
from utils import count_white_spaces
from enemy import Enemy

class Room:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def center(self):
        return (self.x + self.width // 2, self.y + self.height // 2)

class Door:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_open = False

    def open(self):
        self.is_open = True

    def close(self):
        self.is_open = False

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

def create_h_tunnel(dungeon_map, x1, x2, y, doors):
    for x in range(min(x1, x2), max(x1, x2) + 1):
        dungeon_map[y][x] = 0
    if count_white_spaces(dungeon_map, x1, y) <= 3:
        doors.append(Door(x1, y))
    if count_white_spaces(dungeon_map, x2, y) <= 3:
        doors.append(Door(x2, y))

def create_v_tunnel(dungeon_map, y1, y2, x, doors):
    for y in range(min(y1, y2), max(y1, y2) + 1):
        dungeon_map[y][x] = 0
    if count_white_spaces(dungeon_map, x, y1) <= 3:
        doors.append(Door(x, y1))
    if count_white_spaces(dungeon_map, x, y2) <= 3:
        doors.append(Door(x, y2))

def generate_room_at(dungeon_map, origin_x, origin_y, doors, enemies):
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
                    create_h_tunnel(dungeon_map, prev_x, new_x, prev_y, doors)
                    create_v_tunnel(dungeon_map, prev_y, new_y, new_x, doors)
                else:
                    create_v_tunnel(dungeon_map, prev_y, new_y, prev_x, doors)
                    create_h_tunnel(dungeon_map, prev_x, new_x, new_y, doors)

            # Spawn an enemy in the room
            spawn_x = new_room.x + new_room.width // 2
            spawn_y = new_room.y + new_room.height // 2
            enemies.append(Enemy(spawn_x * TILE_SIZE, spawn_y * TILE_SIZE))

            rooms.append(new_room)

    return dungeon_map

def load_room_at(player_grid_x, player_grid_y, dungeon_rooms, doors, enemies):
    if (player_grid_x, player_grid_y) not in dungeon_rooms:
        dungeon_map = [[1 for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
        dungeon_map = generate_room_at(dungeon_map, player_grid_x, player_grid_y, doors, enemies)
        dungeon_rooms[(player_grid_x, player_grid_y)] = dungeon_map
    return dungeon_rooms[(player_grid_x, player_grid_y)]

def find_walkable_tile(dungeon_map):
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            if dungeon_map[y][x] == 0:
                return x * TILE_SIZE, y * TILE_SIZE
    raise ValueError("No walkable tiles found in the dungeon map!")

def update_doors(player_x, player_y, doors):
    for door in doors:
        if abs(door.x * TILE_SIZE - player_x) < TILE_SIZE and abs(door.y * TILE_SIZE - player_y) < TILE_SIZE:
            door.open()
        else:
            door.close()