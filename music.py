import pygame
import os

pygame.init()

tracks = ['music/Map.wav', 'music/Mars.wav', 'music/Mercury.wav', 'music/Venus.wav']
current_track_index = 0

# Initialize the mixer
try:
    pygame.mixer.init()
    pygame.mixer.music.load(tracks[current_track_index])
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play()
except pygame.error as e:
    print(f"Error initializing mixer or loading music: {e}")

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Game')

font = pygame.font.Font(None, 36)

def update_track_display():
    track_name = os.path.basename(tracks[current_track_index])
    text = font.render(f'Now Playing: {track_name}', True, (255, 255, 255))
    screen.blit(text, (screen.get_width() - text.get_width() - 10, screen.get_height() - text.get_height() - 10))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                pygame.mixer.music.stop()
                current_track_index = (current_track_index + 1) % len(tracks)
                try:
                    pygame.mixer.music.load(tracks[current_track_index])
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play()
                except pygame.error as e:
                    print(f"Error loading or playing music: {e}")

    screen.fill((0, 0, 0))
    update_track_display()
    pygame.display.flip()

pygame.quit()