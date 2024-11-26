
import os
import json
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK

SAVE_FOLDER = 'saves'

# Ensure the save folder exists
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)

def save_game(player_x, player_y, player, current_room_x, current_room_y, elapsed_time, xp_counter, seed):
    game_state = {
        'player_x': player_x,
        'player_y': player_y,
        'player_health': player.health,
        'current_room_x': current_room_x,
        'current_room_y': current_room_y,
        'elapsed_time': elapsed_time,
        'xp_counter': xp_counter,
        'seed': seed,
        # ...other game state data...
    }
    save_file = os.path.join(SAVE_FOLDER, 'savegame.json')
    with open(save_file, 'w') as f:
        json.dump(game_state, f)

def load_game():
    save_file = os.path.join(SAVE_FOLDER, 'savegame.json')
    if not os.path.exists(save_file):
        return None  # Indicate that there's no save file
    with open(save_file, 'r') as f:
        game_state = json.load(f)
    return game_state

def show_no_saves_screen(screen):
    no_saves_screen = True
    font = pygame.font.SysFont(None, 50)
    arrow_font = pygame.font.SysFont(None, 36)
    while no_saves_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                # Check if the return arrow is clicked
                if return_arrow_rect.collidepoint(mouse_pos):
                    no_saves_screen = False  # Return to main menu
        screen.fill(BLACK)
        text = font.render("[No saves]", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)
        # Draw return arrow at top-left corner
        arrow_text = arrow_font.render("←", True, WHITE)
        return_arrow_rect = arrow_text.get_rect(topleft=(10, 10))
        screen.blit(arrow_text, return_arrow_rect)
        pygame.display.flip()