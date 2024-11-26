# strong_enemy.py
import pygame
from enemy import Enemy
from settings import TILE_SIZE, ORANGE, BLACK, DARK_ORANGE
from xp_orb import XPOrb  # Ensure XPOrb is imported

class StrongEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.max_health = 5  # Set base health to 5
        self.health = self.max_health
        self.speed = 50  # Pixels per second
        self.path = []

    def take_damage(self):
        """Handle taking damage by reducing health."""
        self.health -= 1
        print(f"StrongEnemy at ({self.x}, {self.y}) took damage! Remaining health: {self.health}")
        return self.health <= 0  # Return True if the enemy is dead

    def die(self):
        # ...existing death logic...
        xp_orb = XPOrb(self.x, self.y)  # Create an XP orb at enemy's position
        xp_orbs.append(xp_orb)  # Add XP orb to the global list

    def draw(self, screen, camera_x, camera_y):
        """Draw the StrongEnemy with health visualization."""
        enemy_x = self.x - camera_x
        enemy_y = self.y - camera_y

        # Draw the dark orange border
        pygame.draw.rect(screen, DARK_ORANGE, (enemy_x, enemy_y, TILE_SIZE, TILE_SIZE))

        # Draw the orange body
        pygame.draw.rect(screen, ORANGE, (enemy_x + 2, enemy_y + 2, TILE_SIZE - 4, TILE_SIZE - 4))

        # Calculate damage ratio
        damage_ratio = (self.max_health - self.health) / self.max_health

        # Draw black rectangle proportional to damage taken
        pygame.draw.rect(
            screen,
            BLACK,
            (
                enemy_x + 2,
                enemy_y + 2,
                TILE_SIZE - 4,
                (TILE_SIZE - 4) * damage_ratio  # Height increases as damage increases
            )
        )