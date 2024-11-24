# end_game.py
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, RED

def draw_end_game_screen(screen, elapsed_time, seed):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 50)
    you_died_text = font.render("You Died", True, RED)
    time_played_text = font.render(f"Time Played: {elapsed_time:.2f} seconds", True, WHITE)
    return_to_menu_text = font.render("Press M to return to Main Menu", True, WHITE)
    seed_text = font.render(f"Seed: {seed}", True, WHITE)

    screen.blit(you_died_text, (SCREEN_WIDTH // 2 - you_died_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(time_played_text, (SCREEN_WIDTH // 2 - time_played_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(return_to_menu_text, (SCREEN_WIDTH // 2 - return_to_menu_text.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(seed_text, (SCREEN_WIDTH // 2 - seed_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

def handle_end_game_events(event, in_end_game, in_main_menu):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_m:
            in_end_game = False
            in_main_menu = True
    return in_end_game, in_main_menu