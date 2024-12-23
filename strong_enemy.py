# strong_enemy.py
import pygame
from enemy import Enemy
from settings import TILE_SIZE, ORANGE, BLACK, DARK_ORANGE
from xp_orb import XPOrb  # Ensure XPOrb is imported
from sprites import get_sprite  # Add this import

class StrongEnemy(Enemy):
    """A more powerful enemy variant with increased health and damage."""
    def __init__(self, x, y, sprite, speed=50, health=2, max_health=2, strength=2):
        super().__init__(x, y, speed, sprite)
        self.health = health
        self.max_health = max_health
        self.strength = strength
        self.speed = 50  # Pixels per second
        self.path = []

    @classmethod
    def from_dict(cls, data):
        # Get strong enemy sprite
        strong_enemy_sprite = get_sprite(78, 9)  # Use a different sprite for strong enemy
        return cls(
            x=data['x'],
            y=data['y'],
            sprite=strong_enemy_sprite  # Add sprite parameter
        )

    def take_damage(self):
        """Process damage and return whether enemy was killed."""
        self.health -= 1
        print(f"StrongEnemy at ({self.x}, {self.y}) took damage! Remaining health: {self.health}")
        return self.health <= 0  # Return True if the enemy is dead

    def move_towards_player(self, player_x, player_y, dt, dungeon_map, player, enemies):
        super().move_towards_player(player_x, player_y, dt, dungeon_map, player, enemies)
        # Override collision damage to deal an additional 1 damage (total 2)
        if abs(self.x - player_x) < TILE_SIZE // 2 and abs(self.y - player_y) < TILE_SIZE // 2:
            player.health -= 1  # Deal an additional 1 damage
            # Ensure this is removed to prevent double removal
            print(f"StrongEnemy collided with player! Player health: {player.health}")

    def die(self, xp_orbs):
        """Handle death by spawning multiple XP orbs."""
        # ...existing death logic...
        for _ in range(3):  # Drop 3 XP orbs
            xp_orb = XPOrb(self.x, self.y, size=int(10 * 1.5))  # Set size to match EnemySpawner's orbs
            xp_orbs.append(xp_orb)

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