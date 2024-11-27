import pygame
import os
import random

pygame.init()

tracks = ['music/Map.wav', 'music/Mars.wav', 'music/Mercury.wav', 'music/Venus.wav']
boss_tracks = ['music/BossIntro.wav', 'music/BossMain.wav']
current_track_index = 0
is_boss_mode = False
is_victory_mode = False  # Add victory mode flag

def play_music():
    global current_track_index, is_boss_mode, is_victory_mode
    is_boss_mode = False
    is_victory_mode = False
    current_track_index = 0
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
    if is_victory_mode:
        track_name = "Victory Track"
        color = (255, 215, 0)  # Gold color for victory
    elif is_boss_mode:
        track_name = os.path.basename(boss_tracks[current_track_index])
        color = (139, 0, 0)  # Blood red color
    else:
        track_name = os.path.basename(tracks[current_track_index])
        color = (255, 165, 0)  # Orange color
    text = font.render(f'Now Playing: {track_name}', True, color)
    screen.blit(text, (10, screen.get_height() - text.get_height() - 10))
    draw_equalizer(screen, 10, screen.get_height() - text.get_height() - 30, color)

def draw_equalizer(screen, x, y, color):
    bar_width = 5
    bar_height = 15  # Reduce the maximum height of the bars
    num_bars = 10
    for i in range(num_bars):
        height = random.randint(5, bar_height)
        pygame.draw.rect(screen, color, (x + i * (bar_width + 2), y - height, bar_width, height))

def next_track():
    global current_track_index, is_boss_mode, is_victory_mode
    if is_victory_mode:
        is_victory_mode = False
    else:
        pygame.mixer.music.stop()
        if is_boss_mode:
            is_boss_mode = False
            current_track_index = (current_track_index + 1) % len(tracks)
        else:
            current_track_index = (current_track_index + 1) % len(tracks)
        try:
            pygame.mixer.music.load(tracks[current_track_index])
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play()
            pygame.mixer.music.set_endevent(pygame.USEREVENT)  # Set event for track end
        except pygame.error as e:
            print(f"Error loading or playing music: {e}")

def handle_music_event(event):
    global current_track_index, is_victory_mode
    if event.type == pygame.USEREVENT:
        if is_victory_mode:
            is_victory_mode = False
            play_music()
        else:
            if is_boss_mode and current_track_index == 0:
                current_track_index = 1
            try:
                if is_boss_mode:
                    pygame.mixer.music.load(boss_tracks[current_track_index])
                else:
                    pygame.mixer.music.load(tracks[current_track_index])
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play()
                pygame.mixer.music.set_endevent(pygame.USEREVENT)  # Set event for track end
            except pygame.error as e:
                print(f"Error loading or playing music: {e}")

def play_boss_music():
    global current_track_index, is_boss_mode, is_victory_mode
    if not is_victory_mode:
        is_boss_mode = True
        current_track_index = 0
        try:
            pygame.mixer.music.load(boss_tracks[current_track_index])
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play()
            pygame.mixer.music.set_endevent(pygame.USEREVENT)  # Set event for track end
        except pygame.error as e:
            print(f"Error loading or playing music: {e}")