# player.py
from settings import TILE_SIZE
from utils import is_walkable

class Player:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

    def move(self, dx, dy, dt, dungeon_map, doors):
        new_x = self.x + dx * self.speed * dt
        new_y = self.y + dy * self.speed * dt

        if is_walkable(new_x, self.y, dungeon_map, doors):
            self.x = new_x
        if is_walkable(self.x, new_y, dungeon_map, doors):
            self.y = new_y

    def get_position(self):
        return self.x, self.y