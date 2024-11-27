import pygame
import os

def load_sprite_sheet_image():
    return pygame.image.load(os.path.join('assets', 'sprite_sheet.png')).convert_alpha()