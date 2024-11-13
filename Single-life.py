# Single-life.py

import pygame
import sys

# Initialize Pygame
pygame.init()

# Set display resolution
screen_width, screen_height = 700, 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame Window - 1000x1000 Resolution")

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill screen with color (optional)
    screen.fill((255, 255, 255))  # Black background

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
