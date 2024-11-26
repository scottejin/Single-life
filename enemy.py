# enemy.py
from astar import astar
from settings import TILE_SIZE
from xp_orb import XPOrb  # Ensure XPOrb is imported

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.max_health = 2  # Set maximum health
        self.health = self.max_health
        self.speed = 50  # Pixels per second
        self.path = []

    def get_position(self):
        return self.x, self.y

    def take_damage(self):
        self.health -= 1
        print(f"Enemy at ({self.x}, {self.y}) took damage! Remaining health: {self.health}")
        return self.health <= 0  # Return True if the enemy is dead

    def move_towards_player(self, player_x, player_y, dt, dungeon_map, player, enemies):
        start = (int(self.x // TILE_SIZE), int(self.y // TILE_SIZE))
        goal = (int(player_x // TILE_SIZE), int(player_y // TILE_SIZE))

        if not self.path or self.path[-1] != goal:
            self.path = astar(dungeon_map, start, goal)

        if self.path:
            next_tile = self.path[0]
            direction_x = (next_tile[0] * TILE_SIZE + TILE_SIZE // 2) - self.x
            direction_y = (next_tile[1] * TILE_SIZE + TILE_SIZE // 2) - self.y
            distance = (direction_x ** 2 + direction_y ** 2) ** 0.5
            if distance > 0:
                direction_x /= distance
                direction_y /= distance
                self.x += direction_x * self.speed * dt
                self.y += direction_y * self.speed * dt

            if (int(self.x // TILE_SIZE), int(self.y // TILE_SIZE)) == next_tile:
                self.path.pop(0)

        # Fallback movement if pathfinding fails
        else:
            direction_x = player_x - self.x
            direction_y = player_y - self.y
            distance = (direction_x ** 2 + direction_y ** 2) ** 0.5
            if distance > 0:
                direction_x /= distance
                direction_y /= distance
                self.x += direction_x * self.speed * dt
                self.y += direction_y * self.speed * dt

        # Check for collision with the player
        if abs(self.x - player_x) < TILE_SIZE // 2 and abs(self.y - player_y) < TILE_SIZE // 2:
            player.health -= 1  # Reduce player's health by 1
            enemies.remove(self)  # Remove enemy from the list
            print(f"Enemy collided with player! Player health: {player.health}")

    def die(self):
        # ...existing death logic...
        xp_orb = XPOrb(self.x, self.y)  # Create an XP orb at enemy's position
        xp_orbs.append(xp_orb)  # Add XP orb to the global list