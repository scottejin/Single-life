import pygame
import sys
import os
import itertools
import music
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

def draw_victory_screen(screen, elapsed_time, xp_counter, seed):
    """
    Display the victory screen with game statistics and rainbow animation.
    Shows play time, XP collected, and game seed while playing victory music.
    """
    # Initialize screen
    screen.fill((0, 0, 0))
    
    # Setup fonts and positioning
    font = pygame.font.SysFont(None, 48)
    stats_font = pygame.font.SysFont(None, 36)
    center_x = SCREEN_WIDTH // 2
    center_y = SCREEN_HEIGHT // 2

    # Draw victory message and stats
    # Draw "Victory!" text at the center top
    victory_text = font.render("Victory!", True, (255, 255, 255))
    victory_rect = victory_text.get_rect(center=(center_x, center_y - 100))
    screen.blit(victory_text, victory_rect)

    # Draw statistics centered vertically
    time_text = stats_font.render(f"Time Played: {elapsed_time:.2f} seconds", True, (255, 255, 255))
    xp_text = stats_font.render(f"XP Collected: {xp_counter}", True, (255, 255, 255))
    seed_text = stats_font.render(f"Game Seed: {seed}", True, (255, 255, 255))

    spacing = 50
    screen.blit(time_text, (center_x - time_text.get_width() // 2, center_y - 50))
    screen.blit(xp_text, (center_x - xp_text.get_width() // 2, center_y))
    screen.blit(seed_text, (center_x - seed_text.get_width() // 2, center_y + 50))

    # Draw continue prompt at the center bottom
    prompt_text = stats_font.render("Press SPACE to continue", True, (255, 255, 255))
    prompt_rect = prompt_text.get_rect(center=(center_x, center_y + 150))
    screen.blit(prompt_text, prompt_rect)

    # Initialize victory music
    try:
        pygame.mixer.music.load(os.path.join('music', 'victory.wav'))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()
        pygame.mixer.music.set_endevent(pygame.USEREVENT)  # Set event for track end
        music.is_victory_mode = True  # Set victory mode flag
    except pygame.error as e:
        print(f"Error loading or playing victory music: {e}")

    def rainbow_colors():
        """Generate an infinite cycle of rainbow colors"""
        colors = [(255, 0, 0), (255, 127, 0), (255, 255, 0),
                 (0, 255, 0), (0, 0, 255), (75, 0, 130), (148, 0, 211)]
        for color in itertools.cycle(colors):
            yield color

    color_gen = rainbow_colors()
    waiting_for_input = True
    song_playing = True

    # Main victory screen loop
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_SPACE, pygame.K_ESCAPE]:
                    waiting_for_input = False
                elif event.key == pygame.K_m:
                    music.next_track()
                    waiting_for_input = False

        if not pygame.mixer.music.get_busy() and song_playing:
            song_playing = False
            message_text = stats_font.render("Out of wins, win again to listen", True, (255, 255, 255))
            screen.blit(message_text, (center_x - message_text.get_width() // 2, center_y + 100))
            pygame.display.flip()

        if song_playing:
            color = next(color_gen)
            victory_text = font.render("Victory!", True, color)
            screen.blit(victory_text, victory_rect)
            pygame.display.flip()
            pygame.time.delay(100)  # Delay to control the speed of color change