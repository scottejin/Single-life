
import pygame
from settings import WHITE, BLUE

class Button:
    def __init__(self, text, position, font_size=30, base_color=WHITE, hover_color=BLUE):
        """
        Initializes a Button instance.

        :param text: Text to display on the button.
        :param position: Tuple representing the center position of the button.
        :param font_size: Size of the button text.
        :param base_color: Default color of the button text.
        :param hover_color: Color of the button text when hovered.
        """
        self.text = text
        self.position = position
        self.font = pygame.font.SysFont(None, font_size)
        self.base_color = base_color
        self.hover_color = hover_color
        self.rendered_text = self.font.render(self.text, True, self.base_color)
        self.rect = self.rendered_text.get_rect(center=self.position)

    def draw(self, surface):
        """Draws the button on the given surface with hover effects."""
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            # Change color on hover
            self.rendered_text = self.font.render(self.text, True, self.hover_color)
        else:
            self.rendered_text = self.font.render(self.text, True, self.base_color)
        surface.blit(self.rendered_text, self.rect)