import pygame  # Add this import
from settings import TILE_SIZE, PLAYER_SIZE  # Ensure PLAYER_SIZE is imported
from utils import is_walkable

class Player:
    def __init__(self, x, y, speed, sprite):
        self.x = x
        self.y = y
        self.speed = speed
        self.health = 5  # Add this line
        self.rect = pygame.Rect(self.x, self.y, PLAYER_SIZE, PLAYER_SIZE)  # Initialize player's rect
        self.sprite = sprite

    def move(self, dx, dy, dt, dungeon_map):
        new_x = self.x + dx * self.speed * dt
        new_y = self.y + dy * self.speed * dt

        if is_walkable(new_x, self.y, dungeon_map):
            self.x = new_x
        if is_walkable(self.x, new_y, dungeon_map):
            self.y = new_y

        self.rect.topleft = (self.x, self.y)  # Update the player's rect position

    def get_position(self):
        return self.x, self.y

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen, camera_x, camera_y):
        screen.blit(self.sprite, (self.x - camera_x, self.y - camera_y))