# Import and initialize the pygame library
import pygame
import random

pygame.init()

def resize_image(img, new_height):
    # Calculate the new dimensions to maintain the aspect ratio
    original_height = img.get_height()
    original_width = img.get_width()
    aspect_ratio = original_width / original_height
    new_width = int(new_height * aspect_ratio)
    # Scale the image
    img = pygame.transform.scale(img, (new_width, new_height))
    return img

# Set up the drawing window
screen = pygame.display.set_mode([500, 500])

# Load the background image and scale it
background_image = pygame.image.load('background.png')
background_image = resize_image(background_image, 500)
background_width = background_image.get_width()

# Initialize background positions
background_x1 = 0
background_x2 = background_width

# Load an image and a sound
image = pygame.image.load('mario.png')
jump_sound = pygame.mixer.Sound('jump.wav')
image = resize_image(image, 60)

# Load and resize block image
block_image = pygame.image.load('block.jpg')
block_image = resize_image(block_image, 50)

# Initial position of the block
block_visible = False
block_x = 500  # Start offscreen

# Initial position of the image
x, y = 250, 365  # Centered horizontally and positioned at the bottom

# Set initial velocity for jumping
velocity_y = 0
gravity = 0.5  # Gravity effect
jump_velocity = -10  # Initial velocity of the jump

# Flags to control jumping
is_jumping = False

# Background scrolling speed
scroll_speed = 2

# Run until the user asks to quit
running = True
while running:
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check for key down event
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and not is_jumping:
                velocity_y = jump_velocity
                is_jumping = True
                jump_sound.play()  # Play sound when the up key is pressed

    # Update the background position to continuously scroll to the left
    background_x1 -= scroll_speed
    background_x2 -= scroll_speed
    if background_x1 <= -background_width:
        background_x1 = background_width
    if background_x2 <= -background_width:
        background_x2 = background_width

    # Move the block with the background
    if block_visible:
        block_x -= scroll_speed
        # Reset block position if it moves offscreen
        if block_x < -block_image.get_width():
            block_visible = False  # Make block invisible and reset its position
            block_x = 500  # Reset to start position offscreen

    # Randomly toggle block visibility
    if not block_visible and random.randint(0, 100) > 90:  # ~10% chance per frame to appear
        block_visible = True
        block_x = 500  # Start from the right side of the screen

    # Update the position of the image
    if is_jumping:
        y += velocity_y
        velocity_y += gravity  # Apply gravity

    # Check if the image has landed
    if y >= 365:
        y = 365
        is_jumping = False
        velocity_y = 0

    # Fill the background
    screen.blit(background_image, (background_x1, 0))
    screen.blit(background_image, (background_x2, 0))

    # Blit the block image if visible
    if block_visible:
        screen.blit(block_image, (block_x, 250))

    # Blit the image at the new position
    screen.blit(image, (x, y))

    # Flip the display
    pygame.display.flip()

    # Limit frames per second
    pygame.time.Clock().tick(30)

# Done! Time to quit.
pygame.quit()
