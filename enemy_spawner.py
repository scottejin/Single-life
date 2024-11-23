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
        self.width = int(ENEMY_SIZE * 1.5)
        self.height = int(ENEMY_SIZE * 1.5)

    def is_fully_within_blue_circle(self, player_x, player_y, radius):
        """Check if all corners of the spawner are within the blue circle."""
        spawner_corners = [
            (self.spawn_x, self.spawn_y),
            (self.spawn_x + self.width, self.spawn_y),
            (self.spawn_x, self.spawn_y + self.height),
            (self.spawn_x + self.width, self.spawn_y + self.height),
        ]

        for corner_x, corner_y in spawner_corners:
            distance = ((corner_x - player_x) ** 2 + (corner_y - player_y) ** 2) ** 0.5
            if distance > radius:
                return False  # A corner is outside the circle

        return True  # All corners are inside the circle

    def update(self, enemies, player_x, player_y, radius):
        """Update spawner state and spawn enemies if within the blue circle."""
        if self.is_active and self.is_fully_within_blue_circle(player_x, player_y, radius):
            current_time = time.time()
            if current_time - self.last_spawn_time >= self.spawn_interval:
                enemies.append(Enemy(self.spawn_x, self.spawn_y))
                self.last_spawn_time = current_time

    def take_damage(self):
        """Handle spawner taking damage."""
        if self.is_active:
            self.health -= 1
            if self.health <= 0:
                self.is_active = False

    def draw(self, screen, camera_x, camera_y):
        """Draw the spawner and its health bar."""
        spawner_x = self.spawn_x - camera_x
        spawner_y = self.spawn_y - camera_y
        health_ratio = self.health / 10
        inner_color = PURPLE if health_ratio == 1 else (128, 0, 128)  # Darker purple if damaged
        pygame.draw.rect(screen, PURPLE, (spawner_x, spawner_y, self.width, self.height))
        pygame.draw.rect(screen, inner_color, (spawner_x + 2, spawner_y + 2, self.width - 4, self.height - 4))
        pygame.draw.rect(screen, BLACK, (spawner_x + 2, spawner_y + 2, (self.width - 4) * health_ratio, self.height - 4))