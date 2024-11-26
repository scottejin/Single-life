from settings import TILE_SIZE
import pygame
import os

class Bullet:
    def __init__(self, x, y, direction, speed, is_broken=False):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
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
        map_x, map_y = int(self.x // TILE_SIZE), int(self.y // TILE_SIZE)
        if map_x < 0 or map_x >= len(dungeon_map[0]) or map_y < 0 or map_y >= len(dungeon_map):
            return True
        if dungeon_map[map_y][map_x] == 1:
            return True
        for enemy in enemies:
            enemy_x, enemy_y = enemy.get_position()
            collision_radius = enemy.get_collision_radius()  # Get dynamic collision radius
            if abs(self.x - enemy_x) < collision_radius and abs(self.y - enemy_y) < collision_radius:
                if enemy.take_damage():
                    enemy.die(xp_orbs)
                    enemies.remove(enemy)
                    print(f"Enemy at ({enemy_x}, {enemy_y}) killed.")
                return True
        for spawner in spawners:
            if spawner.is_active and abs(self.x - spawner.spawn_x) < TILE_SIZE // 2 and abs(self.y - spawner.spawn_y) < TILE_SIZE // 2:
                spawner.take_damage(xp_orbs)  # Pass xp_orbs as an argument
                return True
        return False

    def break_bullet(self):
        self.is_broken = True

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
            is_broken=data['is_broken']
        )