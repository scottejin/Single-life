# enemy.py
import pygame
from settings import ENEMY_SIZE, WHITE, BLACK
from sprites import get_sprite  # Add this import
from astar import astar
from settings import TILE_SIZE
from xp_orb import XPOrb  # Ensure XPOrb is imported

class Enemy:
    def __init__(self, x, y, sprite, max_health=2, health=2, speed=50):
        self.x = x
        self.y = y
        self.max_health = max_health
        self.health = health if health is not None else max_health
        self.speed = speed  # Pixels per second
        self.path = []
        self.sprite = sprite

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
            print(f"Enemy collided with player! Player health: {player.health}")

    def die(self, xp_orbs):
        # ...existing death logic...
        xp_orb = XPOrb(self.x, self.y)  # Create an XP orb at enemy's position
        xp_orbs.append(xp_orb)  # Add XP orb to the global list

    def get_collision_radius(self):
        return TILE_SIZE // 2  # Default collision radius for Enemy

    def to_dict(self):
        """Convert enemy to serializable dictionary"""
        return {
            'x': self.x,
            'y': self.y,
            'health': self.health,
            'max_health': self.max_health,
            'speed': self.speed,
            'type': self.__class__.__name__
        }

    @classmethod
    def from_dict(cls, data):
        # Get enemy sprite
        enemy_sprite = get_sprite(78, 8)  # Use the standard enemy sprite
        return cls(
            x=data['x'],
            y=data['y'],
            sprite=enemy_sprite  # Add sprite parameter
        )

    def draw(self, screen, camera_x, camera_y):
        screen.blit(self.sprite, (self.x - camera_x, self.y - camera_y))

class StrongEnemy(Enemy):
    def __init__(self, x, y, max_health=20, health=None, strength=2, speed=50):
        super().__init__(x=x, y=y, max_health=max_health, health=health, speed=speed)
        self.strength = strength
        # ...other attributes...

    def to_dict(self):
        data = super().to_dict()
        data['type'] = 'StrongEnemy'
        data['strength'] = self.strength
        # ...other attributes...
        return data

    @staticmethod
    def from_dict(data):
        return StrongEnemy(
            x=data['x'],
            y=data['y'],
            health=data['health'],
            max_health=data['max_health'],
            strength=data.get('strength', 2),
            speed=data.get('speed', 50),
            # ...other attributes...
        )

# Enemy behavior, combat, and spawning logic
# ...existing code...