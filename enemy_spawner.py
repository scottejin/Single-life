import pygame
import time
from enemy import Enemy
from settings import TILE_SIZE, ENEMY_SIZE, PURPLE, BLACK

class EnemySpawner:
    def __init__(self, spawn_x, spawn_y, spawn_interval=5):
        self.spawn_x = spawn_x
        self.spawn_y = spawn_y
        self.spawn_interval = spawn_interval
        self.last_spawn_time = time.time()
        self.health = 10
        self.is_active = True

    def update(self, enemies):
        if self.is_active:
            current_time = time.time()
            if current_time - self.last_spawn_time >= self.spawn_interval:
                enemies.append(Enemy(self.spawn_x, self.spawn_y))
                self.last_spawn_time = current_time

    def take_damage(self):
        if self.is_active:
            self.health -= 1
            if self.health <= 0:
                self.is_active = False

    def draw(self, screen, camera_x, camera_y):
        spawner_x = self.spawn_x - camera_x
        spawner_y = self.spawn_y - camera_y
        health_ratio = self.health / 10
        inner_color = PURPLE if health_ratio == 1 else (128, 0, 128)  # Darker purple if damaged
        pygame.draw.rect(screen, PURPLE, (spawner_x, spawner_y, ENEMY_SIZE, ENEMY_SIZE))
        pygame.draw.rect(screen, inner_color, (spawner_x + 2, spawner_y + 2, ENEMY_SIZE - 4, ENEMY_SIZE - 4))
        pygame.draw.rect(screen, BLACK, (spawner_x + 2, spawner_y + 2, (ENEMY_SIZE - 4) * health_ratio, ENEMY_SIZE - 4))