from settings import TILE_SIZE

def count_white_spaces(dungeon_map, x, y):
    white_spaces = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(dungeon_map[0]) and 0 <= ny < len(dungeon_map) and dungeon_map[ny][nx] == 0:
                white_spaces += 1
    return white_spaces

def is_walkable(x, y, dungeon_map):
    map_x, map_y = int(x // TILE_SIZE), int(y // TILE_SIZE)
    if map_x < 0 or map_x >= len(dungeon_map[0]) or map_y < 0 or map_y >= len(dungeon_map):
        return False
    return dungeon_map[map_y][map_x] == 0