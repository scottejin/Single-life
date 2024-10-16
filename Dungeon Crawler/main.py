import pygame
import sys

# Initialize pygame
pygame.init()

# Define constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
CUBE_SIZE = 50
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAY = (128, 128, 128)

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Red and Gray Cube on White Plane")

# Create a large white surface for the plane
plane_width, plane_height = 1600, 1200  # Larger than the screen
plane_surface = pygame.Surface((plane_width, plane_height))
plane_surface.fill(WHITE)

# Red cube's world position (not screen position)
cube_x, cube_y = plane_width // 2, plane_height // 2  # Start at center of plane
cube_speed = 5

# Fixed gray cube position (in world space, not screen space)
gray_cube_x, gray_cube_y = plane_width // 2 + 200, plane_height // 2  # Offset from red cube

# Main game loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get key states for movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        cube_x -= cube_speed
    if keys[pygame.K_RIGHT]:
        cube_x += cube_speed
    if keys[pygame.K_UP]:
        cube_y -= cube_speed
    if keys[pygame.K_DOWN]:
        cube_y += cube_speed

    # Calculate camera offset based on the red cube's position
    camera_x = cube_x - SCREEN_WIDTH // 2
    camera_y = cube_y - SCREEN_HEIGHT // 2

    # Ensure the camera does not go beyond the plane boundaries
    camera_x = max(0, min(camera_x, plane_width - SCREEN_WIDTH))
    camera_y = max(0, min(camera_y, plane_height - SCREEN_HEIGHT))

    # Draw everything
    screen.blit(plane_surface, (-camera_x, -camera_y))

    # Draw the fixed gray cube (stationary in world space)
    pygame.draw.rect(screen, GRAY, (gray_cube_x - camera_x, gray_cube_y - camera_y, CUBE_SIZE, CUBE_SIZE))

    # Draw the movable red cube (always at the center of the screen)
    pygame.draw.rect(screen, RED, ((SCREEN_WIDTH // 2) - (CUBE_SIZE // 2), 
                                   (SCREEN_HEIGHT // 2) - (CUBE_SIZE // 2), 
                                   CUBE_SIZE, CUBE_SIZE))
    
    # Update display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(60)

# Clean up
pygame.quit()
sys.exit()
