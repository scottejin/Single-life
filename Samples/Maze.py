import pygame
import random
import sys

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
CELL_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = SCREEN_WIDTH // CELL_SIZE, SCREEN_HEIGHT // CELL_SIZE
WHITE, BLACK = (255, 255, 255), (0, 0, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Generator")
clock = pygame.time.Clock()

# Directions for moving in the grid
DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

def generate_maze(grid, x, y):
    grid[y][x] = True
    directions = DIRECTIONS[:]
    random.shuffle(directions)
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and not grid[ny][nx]:
            # Remove the wall between the current cell and the next cell
            pygame.draw.line(screen, WHITE, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2),
                             (nx * CELL_SIZE + CELL_SIZE // 2, ny * CELL_SIZE + CELL_SIZE // 2), 2)
            pygame.display.flip()
            generate_maze(grid, nx, ny)

def main():
    grid = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    screen.fill(BLACK)
    generate_maze(grid, 0, 0)
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()