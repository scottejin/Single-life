
import pygame

class TilesetHandler:
    def __init__(self):
        # Load your tilesets
        self.horizontal_tileset = pygame.image.load('path_to_horizontal_tileset.png')
        self.vertical_tileset = pygame.image.load('path_to_vertical_tileset.png')
        self.packed_tileset = pygame.image.load('path_to_packed_tileset.png')
        
        # Set the size of individual tiles (example: 32x32 pixels)
        self.tile_size = 32

    def get_tile_from_horizontal(self, index):
        # Extract tile from horizontal tileset
        x = index * self.tile_size
        return self.horizontal_tileset.subsurface((x, 0, self.tile_size, self.tile_size))

    def get_tile_from_vertical(self, index):
        # Extract tile from vertical tileset
        y = index * self.tile_size
        return self.vertical_tileset.subsurface((0, y, self.tile_size, self.tile_size))

    def get_tile_from_packed(self, row, col):
        # Extract tile from packed tileset
        x = col * self.tile_size
        y = row * self.tile_size
        return self.packed_tileset.subsurface((x, y, self.tile_size, self.tile_size))