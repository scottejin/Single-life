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
    
    # Calculate right side positions
    right_x = SCREEN_WIDTH * 3 // 4  # Start drawing from 75% of the screen width
    
    # Draw "YOU DIED" text on the right side
    death_text = font.render("YOU DIED", True, RED)
    death_rect = death_text.get_rect(center=(right_x, SCREEN_HEIGHT // 3))
    screen.blit(death_text, death_rect)
    
    # Draw statistics on the right side
    time_text = stats_font.render(f"Time Survived: {format_time(elapsed_time)}", True, WHITE)
    xp_text = stats_font.render(f"XP Collected: {xp_counter}", True, WHITE)
    seed_text = stats_font.render(f"Map Seed: {seed}", True, WHITE)
    
    # Position text on the right
    spacing = 50
    screen.blit(time_text, (right_x - time_text.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(xp_text, (right_x - xp_text.get_width() // 2, SCREEN_HEIGHT // 2 + spacing))
    screen.blit(seed_text, (right_x - seed_text.get_width() // 2, SCREEN_HEIGHT // 2 + spacing * 2))
    
    # Draw continue prompt on the right side
    prompt_text = stats_font.render("Press SPACE to continue", True, WHITE)
    prompt_rect = prompt_text.get_rect(center=(right_x, SCREEN_HEIGHT * 3 // 4))
    screen.blit(prompt_text, prompt_rect)

    # Update the music track display on the right side
    music.update_track_display(screen, right_side=True)

def handle_death_screen_events(event, selected_slot):
    """Handle events on the death screen."""
    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        if selected_slot is not None:
            delete_save_slot(selected_slot)
        return True  # Return to main menu
    return False