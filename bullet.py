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
        return {
            'x': self.x,
            'y': self.y,
            'direction': self.direction,
            'speed': self.speed,
            'is_broken': self.is_broken,
        }

    @staticmethod
    def from_dict(data):
        return Bullet(
            x=data['x'],
            y=data['y'],
            direction=tuple(data['direction']),
            speed=data['speed'],
            sprite=None,  # Placeholder for sprite, should be set appropriately
            is_broken=data['is_broken']
        )