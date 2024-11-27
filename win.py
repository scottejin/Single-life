import pygame
import sys
import os
import itertools

def draw_victory_screen(screen, elapsed_time, xp_counter, seed):
    screen.fill((0, 0, 0))  # Fill the screen with black

    font = pygame.font.SysFont(None, 48)
    victory_text = font.render("Victory!", True, (255, 255, 255))
    screen.blit(victory_text, (screen.get_width() // 2 - victory_text.get_width() // 2, screen.get_height() // 2 - 100))

    font = pygame.font.SysFont(None, 36)
    time_text = font.render(f"Time Played: {elapsed_time:.2f} seconds", True, (255, 255, 255))
    screen.blit(time_text, (screen.get_width() // 2 - time_text.get_width() // 2, screen.get_height() // 2 - 50))

    xp_text = font.render(f"XP Collected: {xp_counter}", True, (255, 255, 255))
    screen.blit(xp_text, (screen.get_width() // 2 - xp_text.get_width() // 2, screen.get_height() // 2))

    seed_text = font.render(f"Game Seed: {seed}", True, (255, 255, 255))
    screen.blit(seed_text, (screen.get_width() // 2 - seed_text.get_width() // 2, screen.get_height() // 2 + 50))

    pygame.display.flip()

    # Play victory music
    try:
        pygame.mixer.music.load(os.path.join('music', 'victory.wav'))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()
    except pygame.error as e:
        print(f"Error loading or playing victory music: {e}")

    # Rainbow color generator
    def rainbow_colors():
        colors = [(255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (75, 0, 130), (148, 0, 211)]
        for color in itertools.cycle(colors):
            yield color

    color_gen = rainbow_colors()
    waiting_for_input = True
    song_playing = True

    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                    waiting_for_input = False

        if not pygame.mixer.music.get_busy() and song_playing:
            song_playing = False
            message_text = font.render("Out of wins, win again to listen", True, (255, 255, 255))
            screen.blit(message_text, (screen.get_width() // 2 - message_text.get_width() // 2, screen.get_height() // 2 + 100))
            pygame.display.flip()

        if song_playing:
            color = next(color_gen)
            victory_text = font.render("Victory!", True, color)
            screen.blit(victory_text, (screen.get_width() // 2 - victory_text.get_width() // 2, screen.get_height() // 2 - 100))
            pygame.display.flip()
            pygame.time.delay(100)  # Delay to control the speed of color change