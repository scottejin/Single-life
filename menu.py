# menu.py
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, RED

class Menu:
    def __init__(self, seed):
        self.font = pygame.font.Font(None, 74)
        self.options = ["Restart", "Exit"]
        self.selected_option = 0
        self.seed = seed

    def draw(self, screen):
        screen.fill(BLACK)
        for i, option in enumerate(self.options):
            color = RED if i == self.selected_option else WHITE
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 100))
            screen.blit(text, rect)

        seed_text = self.font.render(f"Seed: {self.seed}", True, WHITE)
        seed_rect = seed_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200))
        screen.blit(seed_text, seed_rect)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.options[self.selected_option]
        return None