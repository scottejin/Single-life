# main_menu.py
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, RED

class MainMenu:
    def __init__(self):
        self.font = pygame.font.Font(None, 50)
        self.options = ["Start Game", "Options", "Instructions", "Credits", "Exit"]
        self.selected_option = 0

    def draw(self, screen):
        screen.fill(BLACK)
        for i, option in enumerate(self.options):
            color = RED if i == self.selected_option else WHITE
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 60))
            screen.blit(text, rect)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.options[self.selected_option]
        return None