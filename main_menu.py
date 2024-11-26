import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, RED
from save_load import get_available_saves

class MainMenu:
    def __init__(self):
        self.buttons = [
            Button("New Game", position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 90)),
            Button("Load Game", position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30)),
            Button("Exit", position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
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
        return None

    def select_save_slot(self, screen, title):
        available_saves = get_available_saves()
        running = True
        selected_slot = None

        font = pygame.font.SysFont(None, 36)
        while running:
            screen.fill((0, 0, 0))
            title_text = font.render(title, True, (255, 255, 255))
            screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, 50))

            slot_rects = []
            for i in range(3):  # Assuming 3 slots
                slot_num = i + 1
                slot_status = "Occupied" if available_saves[slot_num] else "Empty"
                slot_text = f"Slot {slot_num}: {slot_status}"
                text_surface = font.render(slot_text, True, (255, 255, 255))
                slot_rect = text_surface.get_rect(center=(screen.get_width() // 2, 150 + i * 50))
                screen.blit(text_surface, slot_rect)
                slot_rects.append((slot_rect, slot_num))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    for slot_rect, slot_num in slot_rects:
                        if slot_rect.collidepoint(mouse_x, mouse_y):
                            selected_slot = slot_num
                            running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        return None

            pygame.display.flip()
        return selected_slot

class Button:
    def __init__(self, text, position):
        self.text = text
        self.position = position
        self.font = pygame.font.SysFont(None, 50)
        self.rendered_text = self.font.render(self.text, True, WHITE)
        self.rect = self.rendered_text.get_rect(center=self.position)

    def draw(self, surface):
        surface.blit(self.rendered_text, self.rect)