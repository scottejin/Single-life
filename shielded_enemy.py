# shielded_enemy.py
import pygame
from enemy import Enemy
from settings import TILE_SIZE, ORANGE, BLACK, DARK_ORANGE

class ShieldedEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.total_health = 5
        self.health = self.total_health
        self.shield_health = 3  # 3 shield health
        self.speed = 50  # Pixels per second
        self.path = []

    def take_damage(self):
        """Handle taking damage. Reduce shield first, then health."""
        if self.shield_health > 0:
            self.shield_health -= 1
            print(f"ShieldedEnemy at ({self.x}, {self.y}) shield hit! Remaining shield: {self.shield_health}")
            return False  # Enemy not dead yet
        else:
            self.health -= 1
            print(f"ShieldedEnemy at ({self.x}, {self.y}) took damage! Remaining health: {self.health}")
            return self.health <= 0  # Return True if the enemy is dead

    def draw(self, screen, camera_x, camera_y):
        """Draw the ShieldedEnemy with shield visualization."""
        enemy_x = self.x - camera_x
        enemy_y = self.y - camera_y

        # Draw the dark orange border
        pygame.draw.rect(screen, DARK_ORANGE, (enemy_x, enemy_y, TILE_SIZE, TILE_SIZE))

        if self.shield_health > 0:
            # Draw the white shield
            pygame.draw.rect(screen, ORANGE, (enemy_x + 2, enemy_y + 2, TILE_SIZE - 4, TILE_SIZE - 4))
            
            # Calculate shield damage ratio
            shield_damage_ratio = (3 - self.shield_health) / 3
            # Draw black rectangle proportional to shield damage taken
            pygame.draw.rect(
                screen,
                BLACK,
                (
                    enemy_x + 2,
                    enemy_y + 2,
                    TILE_SIZE - 4,
                    (TILE_SIZE - 4) * shield_damage_ratio  # Height increases as shield damage increases
                )
            )
        else:
            # Draw the normal enemy body without shield
            pygame.draw.rect(screen, ORANGE, (enemy_x, enemy_y, TILE_SIZE, TILE_SIZE))
            
            # Draw solid orange inside
            pygame.draw.rect(screen, ORANGE, (enemy_x + 2, enemy_y + 2, TILE_SIZE - 4, TILE_SIZE - 4))

            # Calculate damage ratio for the remaining health
            damage_ratio = (2 - self.health) / 2  # Since remaining health is 2
            # Draw black rectangle proportional to damage taken
            pygame.draw.rect(
                screen,
                BLACK,
                (
                    enemy_x + 2,
                    enemy_y + 2,
                    TILE_SIZE - 4,
                    (TILE_SIZE - 4) * damage_ratio  # Height increases as health decreases
                )
            )