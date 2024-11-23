from astar import astar
from settings import TILE_SIZE

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 2
        self.speed = 50  # Pixels per second
        self.path = []

    def get_position(self):
        return self.x, self.y

    def take_damage(self):
        self.health -= 1
        return self.health <= 0  # Return True if the enemy is dead

    def move_towards_player(self, player_x, player_y, dt, dungeon_map):
        start = (int(self.x // TILE_SIZE), int(self.y // TILE_SIZE))
        goal = (int(player_x // TILE_SIZE), int(player_y // TILE_SIZE))

        if not self.path or self.path[-1] != goal:
            self.path = astar(dungeon_map, start, goal)

        if self.path:
            next_tile = self.path[0]
            direction_x = (next_tile[0] * TILE_SIZE + TILE_SIZE // 2) - self.x
            direction_y = (next_tile[1] * TILE_SIZE + TILE_SIZE // 2) - self.y
            distance = (direction_x**2 + direction_y**2)**0.5
            if distance > 0:
                direction_x /= distance
                direction_y /= distance
                self.x += direction_x * self.speed * dt
                self.y += direction_y * self.speed * dt

            if (int(self.x // TILE_SIZE), int(self.y // TILE_SIZE)) == next_tile:
                self.path.pop(0)