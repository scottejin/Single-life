# Generic confirmation dialog for user interactions
import pygame
from settings import WHITE, BLACK

class ConfirmationDialog:
    def __init__(self, screen, confirm_message, joke_message, options, position):
        self.screen = screen
        self.confirm_message = confirm_message
        self.joke_message = joke_message
        self.options = options
        self.position = position
        self.font = pygame.font.SysFont(None, 36)
        self.button_font = pygame.font.SysFont(None, 30)
        self.selected_option = None

    def draw(self):
        dialog_width, dialog_height = 400, 300
        dialog_rect = pygame.Rect(0, 0, dialog_width, dialog_height)
        dialog_rect.center = self.position

        pygame.draw.rect(self.screen, BLACK, dialog_rect)
        pygame.draw.rect(self.screen, WHITE, dialog_rect, 2)

        # Draw confirm message
        y_offset = dialog_rect.top + 20
        for line in self.confirm_message:
            text_surface = self.font.render(line, True, WHITE)
            self.screen.blit(text_surface, (dialog_rect.centerx - text_surface.get_width() // 2, y_offset))
            y_offset += text_surface.get_height() + 5

        # Draw joke message
        y_offset += 20
        for line in self.joke_message:
            text_surface = self.font.render(line, True, WHITE)
            self.screen.blit(text_surface, (dialog_rect.centerx - text_surface.get_width() // 2, y_offset))
            y_offset += text_surface.get_height() + 5

        # Draw options
        button_width, button_height = 100, 40
        button_y = dialog_rect.bottom - 60
        for i, option in enumerate(self.options):
            button_rect = pygame.Rect(0, 0, button_width, button_height)
            button_rect.centerx = dialog_rect.left + (i + 1) * dialog_width // (len(self.options) + 1)
            button_rect.centery = button_y
            pygame.draw.rect(self.screen, WHITE, button_rect, 2)
            text_surface = self.button_font.render(option, True, WHITE)
            self.screen.blit(text_surface, (button_rect.centerx - text_surface.get_width() // 2, button_rect.centery - text_surface.get_height() // 2))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            dialog_width, dialog_height = 400, 300
            dialog_rect = pygame.Rect(0, 0, dialog_width, dialog_height)
            dialog_rect.center = self.position
            button_width, button_height = 100, 40
            button_y = dialog_rect.bottom - 60
            for i, option in enumerate(self.options):
                button_rect = pygame.Rect(0, 0, button_width, button_height)
                button_rect.centerx = dialog_rect.left + (i + 1) * dialog_width // (len(self.options) + 1)
                button_rect.centery = button_y
                if button_rect.collidepoint(mouse_pos):
                    self.selected_option = option
                    return option
        return None