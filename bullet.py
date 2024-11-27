from settings import TILE_SIZE
import pygame
import os

class Bullet:
    def __init__(self, x, y, direction, speed, sprite, is_broken=False):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        self.sprite = sprite
        self.is_broken = is_broken

    def play_sound(self):
        """This method is kept for compatibility but no longer used"""
        pass

    def move(self, dt):
        if not self.is_broken:
            self.x += self.direction[0] * self.speed * dt
            self.y += self.direction[1] * self.speed * dt

    def get_position(self):
        return self.x, self.y

    def check_collision(self, dungeon_map, enemies, spawners, xp_orbs):
        # Check wall collision
        tile_x = int(self.x // TILE_SIZE)
        tile_y = int(self.y // TILE_SIZE)
        if tile_x < 0 or tile_x >= len(dungeon_map[0]) or tile_y < 0 or tile_y >= len(dungeon_map):
            return True
        if dungeon_map[tile_y][tile_x] == 1:
            return True

        # Check enemy collision
        for enemy in enemies[:]:  # Use slice to avoid modifying list while iterating
            if abs(self.x - enemy.x) < TILE_SIZE // 2 and abs(self.y - enemy.y) < TILE_SIZE // 2:
                if enemy.take_damage():
                    enemy.die(xp_orbs)  # Call die method to drop XP orb
                    enemies.remove(enemy)
                return True

        # Check spawner collision - Updated to use x and y instead of spawn_x and spawn_y
        for spawner in spawners[:]:
            if spawner.is_active and abs(self.x - spawner.x) < TILE_SIZE // 2 and abs(self.y - spawner.y) < TILE_SIZE // 2:
                spawner.take_damage(xp_orbs)
                return True

        return False

    def break_bullet(self):
        self.is_broken = True

    def draw(self, screen, camera_x, camera_y):
        screen.blit(self.sprite, (self.x - camera_x, self.y - camera_y))

    def to_dict(self):
        """Convert bullet to serializable dictionary"""
        return {
            'x': self.x,
            'y': self.y,
            'direction': list(self.direction),  # Convert tuple to list
            'speed': self.speed,
            'is_broken': self.is_broken
        }

    @staticmethod
    def from_dict(data, sprite=None):
        """Create a bullet from dictionary with optional sprite override"""
        if sprite is None:
            from sprites import get_sprite  # Import here to avoid circular import
            direction = data['direction']
            # Determine sprite based on direction
            angle = math.degrees(math.atan2(-direction[1], direction[0])) % 360
            if 22.5 <= angle < 67.5:
                sprite = get_sprite(25, 8)  # northeast
            elif 67.5 <= angle < 112.5:
                sprite = get_sprite(25, 7)  # north
            elif 112.5 <= angle < 157.5:
                sprite = get_sprite(25, 14)  # northwest
            elif 157.5 <= angle < 202.5:
                sprite = get_sprite(25, 13)  # west
            elif 202.5 <= angle < 247.5:
                sprite = get_sprite(25, 12)  # southwest
            elif 247.5 <= angle < 292.5:
                sprite = get_sprite(25, 11)  # south
            elif 292.5 <= angle < 337.5:
                sprite = get_sprite(25, 10)  # southeast
            else:
                sprite = get_sprite(25, 9)  # east

        return Bullet(
            x=data['x'],
            y=data['y'],
            direction=tuple(data['direction']),
            speed=data['speed'],
            sprite=sprite,
            is_broken=data['is_broken']
        )