import pygame
import time
import random  # Ensure this is imported
from enemy import Enemy
from strong_enemy import StrongEnemy  # Updated import
from settings import TILE_SIZE, ENEMY_SIZE, PURPLE, BLACK
from xp_orb import XPOrb  # Ensure XPOrb is imported

class EnemySpawner:
    def __init__(self, spawn_x, spawn_y, spawn_interval=5):
        self.spawn_x = spawn_x
        self.spawn_y = spawn_y
        self.spawn_interval = spawn_interval  # Interval in seconds
        self.last_spawn_time = time.time()
        self.max_health = 10  # Set maximum health
        self.health = self.max_health
        self.is_active = True
        self.width = int(ENEMY_SIZE * 1.5)
        self.height = int(ENEMY_SIZE * 1.5)
        # Removed self.first_seen since it's no longer needed

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
                # 10% chance to spawn StrongEnemy
                if random.random() <= 0.10:
                    new_enemy = StrongEnemy(self.spawn_x, self.spawn_y)
                    print(f"StrongEnemy spawned at ({self.spawn_x}, {self.spawn_y})")
                else:
                    new_enemy = Enemy(self.spawn_x, self.spawn_y)
                    print(f"Normal Enemy spawned at ({self.spawn_x}, {self.spawn_y})")
                
                enemies.append(new_enemy)
                self.last_spawn_time = current_time  # Reset the spawn timer

    def take_damage(self, xp_orbs):
        """Handle spawner taking damage."""
        if self.is_active:
            self.health -= 1
            print(f"EnemySpawner at ({self.spawn_x}, {self.spawn_y}) took damage! Remaining health: {self.health}")
            if self.health <= 0 and self.is_active:
                self.is_active = False
                print(f"EnemySpawner at ({self.spawn_x}, {self.spawn_y}) destroyed!")
                # Drop 5 XP orbs, 1.5 times the normal size
                for _ in range(5):
                    xp_orb = XPOrb(self.spawn_x, self.spawn_y, size=int(10 * 1.5))
                    xp_orbs.append(xp_orb)

    def draw(self, screen, camera_x, camera_y):
        """Draw the spawner and its health bar."""
        spawner_x = self.spawn_x - camera_x
        spawner_y = self.spawn_y - camera_y

        # Draw spawner border
        pygame.draw.rect(screen, PURPLE, (spawner_x, spawner_y, self.width, self.height))

        # Draw solid purple inside
        pygame.draw.rect(screen, PURPLE, (spawner_x + 2, spawner_y + 2, self.width - 4, self.height - 4))

        # Calculate damage ratio
        damage_ratio = (self.max_health - self.health) / self.max_health

        # Draw black rectangle proportional to damage taken
        pygame.draw.rect(
            screen,
            BLACK,
            (
                spawner_x + 2,
                spawner_y + 2,
                self.width - 4,
                (self.height - 4) * damage_ratio  # Height increases as damage increases
            )
        )