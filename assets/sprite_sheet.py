import pygame
import os

def load_sprite_sheet_image():
    return pygame.image.load(os.path.join('assets', 'sprite_sheet.png')).convert_alpha()

def get_sprite(row, col, width=32, height=32):
    sprite_sheet = load_sprite_sheet_image()
    return sprite_sheet.subsurface((col * width, row * height, width, height))