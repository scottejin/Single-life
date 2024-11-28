# end_game.py
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, RED
from save_load import delete_save_slot
import music  # Import the music module

def format_time(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

def draw_death_screen(screen, elapsed_time, xp_counter, seed, selected_slot):
    """Draw the death screen with game statistics."""
    screen.fill(BLACK)
    font = pygame.font.SysFont(None, 64)
    stats_font = pygame.font.SysFont(None, 36)
    
    # Calculate center positions
    center_x = SCREEN_WIDTH // 2
    center_y = SCREEN_HEIGHT // 2
    
    # Draw "YOU DIED" text at the center top
    death_text = font.render("YOU DIED", True, RED)
    death_rect = death_text.get_rect(center=(center_x, center_y - 100))
    screen.blit(death_text, death_rect)
    
    # Draw statistics centered vertically
    time_text = stats_font.render(f"Time Survived: {format_time(elapsed_time)}", True, WHITE)
    xp_text = stats_font.render(f"XP Collected: {xp_counter}", True, WHITE)
    seed_text = stats_font.render(f"Map Seed: {seed}", True, WHITE)
    
    spacing = 50
    screen.blit(time_text, (center_x - time_text.get_width() // 2, center_y))
    screen.blit(xp_text, (center_x - xp_text.get_width() // 2, center_y + spacing))
    screen.blit(seed_text, (center_x - seed_text.get_width() // 2, center_y + spacing * 2))
    
    # Draw continue prompt at the center bottom
    prompt_text = stats_font.render("Press SPACE to continue", True, WHITE)
    prompt_rect = prompt_text.get_rect(center=(center_x, center_y + 150))
    screen.blit(prompt_text, prompt_rect)

    # Remove the music track display update
    # music.update_track_display(screen, right_side=True)

    # Remove the pygame.display.flip() call
    # pygame.display.flip()

def handle_death_screen_events(event, selected_slot):
    """Handle events on the death screen."""
    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        if selected_slot is not None:
            delete_save_slot(selected_slot)
        return True  # Return to main menu
    return False