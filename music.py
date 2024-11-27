import pygame
import os
import random

pygame.init()

tracks = ['music/Map.wav', 'music/Mars.wav', 'music/Mercury.wav', 'music/Venus.wav']
current_track_index = 0

def play_music():
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(tracks[current_track_index])
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()
        pygame.mixer.music.set_endevent(pygame.USEREVENT)  # Set event for track end
    except pygame.error as e:
        print(f"Error initializing mixer or loading music: {e}")

font = pygame.font.Font(None, 28)  # Make the font a bit smaller

def update_track_display(screen):
    track_name = os.path.basename(tracks[current_track_index])
    text = font.render(f'Now Playing: {track_name}', True, (255, 165, 0))  # Orange color
    screen.blit(text, (screen.get_width() - text.get_width() - 10, screen.get_height() - text.get_height() - 10))
    draw_equalizer(screen, screen.get_width() - text.get_width() - 20, screen.get_height() - text.get_height() - 10)

def draw_equalizer(screen, x, y):
    bar_width = 5
    bar_height = 15  # Reduce the maximum height of the bars
    num_bars = 10
    for i in range(num_bars):
        height = random.randint(5, bar_height)
        pygame.draw.rect(screen, (255, 165, 0), (x + i * (bar_width + 2), y - height, bar_width, height))

def next_track():
    global current_track_index
    pygame.mixer.music.stop()
    current_track_index = (current_track_index + 1) % len(tracks)
    try:
        pygame.mixer.music.load(tracks[current_track_index])
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()
        pygame.mixer.music.set_endevent(pygame.USEREVENT)  # Set event for track end
    except pygame.error as e:
        print(f"Error loading or playing music: {e}")

def handle_music_event(event):
    if event.type == pygame.USEREVENT:
        # Loop the same track
        try:
            pygame.mixer.music.load(tracks[current_track_index])
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play()
            pygame.mixer.music.set_endevent(pygame.USEREVENT)  # Set event for track end
        except pygame.error as e:
            print(f"Error loading or playing music: {e}")