# menu.py
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, RED

class Menu:
    def __init__(self, seed):
        self.font = pygame.font.Font(None, 50)
        self.options = ["Restart", "Exit", f"Seed: {seed}"]
        self.selected_option = 0
        self.seed = seed
        self.editing_seed = False

    def draw(self, screen):
        screen.fill(BLACK)
        for i, option in enumerate(self.options):
            color = RED if i == self.selected_option else WHITE
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 60))
            screen.blit(text, rect)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.editing_seed:
                if event.key == pygame.K_RETURN:
                    self.editing_seed = False
                    return "Seed"
                elif event.key == pygame.K_BACKSPACE:
                    self.seed = self.seed[:-1]
                elif event.unicode.isdigit():
                    self.seed += event.unicode
                self.options[2] = f"Seed: {self.seed}"
            else:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    if self.selected_option == 2:
                        self.editing_seed = True
                    else:
                        return self.options[self.selected_option]
        return None