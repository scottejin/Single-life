# menu.py
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, RED

class Menu:
    def __init__(self, seed):
        self.font = pygame.font.Font(None, 50)
        self.buttons = [
            Button("Resume", position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)),
            Button("Save and Exit", position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
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
                    return button.text
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "Resume"  # Treat Escape as Resume button
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