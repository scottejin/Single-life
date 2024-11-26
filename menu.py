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
        self.buttons = [
            Button("Resume", position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 90)),
            Button("Save and Exit", position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30)),
            Button("Restart", position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30)),
            Button("Exit", position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 90))
        ]

    def draw(self, screen):
        screen.fill(BLACK)
        for button in self.buttons:
            button.draw(screen)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                if button.rect.collidepoint(mouse_pos):
                    return button.text  # Return the text of the clicked button
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

class Button:
    def __init__(self, text, position):
        self.text = text
        self.position = position
        self.font = pygame.font.SysFont(None, 50)
        self.rendered_text = self.font.render(self.text, True, WHITE)
        self.rect = self.rendered_text.get_rect(center=self.position)

    def draw(self, surface):
        surface.blit(self.rendered_text, self.rect)