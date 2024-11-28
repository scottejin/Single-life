# menu.py
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, RED, save_spawn_interval  # Add this import
import music  # Import the music module

class Menu:
    def __init__(self, seed):
        self.font = pygame.font.Font(None, 50)
        self.buttons = [
            Button("Resume", position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)),
            Button("Save and Exit", position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)),
            Button("Save Settings", position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))  # Add new button
        ]

    def draw(self, screen):
        screen.fill(BLACK)
        for button in self.buttons:
            button.draw(screen)
        music.update_track_display(screen, right_side=True)  # Update the music track display

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                if button.rect.collidepoint(mouse_pos):
                    action = button.text
                    if action == "Save Settings":
                        save_spawn_interval()  # Save the current spawn interval
                        print("Settings saved!")  # Optional feedback
                    return action
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "Resume"  # Treat Escape as Resume button
        return None

class Button:
    def __init__(self, text, position, font_size=50, base_color=WHITE, hover_color=BLUE):
        self.text = text
        self.position = position
        self.font = pygame.font.SysFont(None, font_size)
        self.base_color = base_color
        self.hover_color = hover_color
        self.rendered_text = self.font.render(self.text, True, self.base_color)
        self.rect = self.rendered_text.get_rect(center=self.position)

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            # Change color on hover
            rendered = self.font.render(self.text, True, self.hover_color)
        else:
            rendered = self.font.render(self.text, True, self.base_color)
        surface.blit(rendered, self.rect)