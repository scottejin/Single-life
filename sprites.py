import pygame
from assets.sprite_sheet import load_sprite_sheet_image  # Import the function
from assets.sprite_sheet import get_sprite

def load_sprite_sheet(sprite_width, sprite_height):
    try:
        sprite_sheet_image = load_sprite_sheet_image()  # Load the image here
        sheet_width, sheet_height = sprite_sheet_image.get_size()
        sprites = []
        for y in range(0, sheet_height, sprite_height):
            for x in range(0, sheet_width, sprite_width):
                rect = pygame.Rect(x, y, sprite_width, sprite_height)
                image = sprite_sheet_image.subsurface(rect)
                sprites.append(image)
        return sprites
    except (FileNotFoundError, pygame.error):
        print(f"Warning: Could not load sprite sheet. Using colored rectangles instead.")
        # Create default colored surfaces for each entity
        sprites = []
        # Player sprite (blue)
        player_sprite = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
        pygame.draw.rect(player_sprite, (0, 0, 255), player_sprite.get_rect())
        sprites.append(player_sprite)
        
        # Enemy sprite (red)
        enemy_sprite = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
        pygame.draw.rect(enemy_sprite, (255, 0, 0), enemy_sprite.get_rect())
        sprites.append(enemy_sprite)
        
        # Bullet sprite (yellow)
        bullet_sprite = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
        pygame.draw.rect(bullet_sprite, (255, 255, 0), bullet_sprite.get_rect())
        sprites.append(bullet_sprite)
        
        return sprites

def get_sprite(row, col, width=32, height=32):
    sprite_sheet = load_sprite_sheet_image()
    return sprite_sheet.subsurface((col * width, row * height, width, height))