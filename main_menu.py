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
        confirmation = False
        slot_to_delete = None

        font = pygame.font.SysFont(None, 36)
        button_font = pygame.font.SysFont(None, 30)
        while running:
            screen.fill((0, 0, 0))
            title_text = font.render(title, True, (255, 255, 255))
            screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, 50))

            slot_rects = []
            for i in range(3):  # Assuming 3 slots
                slot_num = i + 1
                slot_status = "Occupied" if available_saves.get(slot_num, False) else "Empty"
                slot_text = f"Slot {slot_num}: {slot_status}"
                text_color = (255, 0, 0) if slot_status == "Occupied" else (255, 255, 255)
                text_surface = font.render(slot_text, True, text_color)
                slot_rect = text_surface.get_rect(center=(screen.get_width() // 2, 150 + i * 50))
                screen.blit(text_surface, slot_rect)
                slot_rects.append((slot_rect, slot_num, slot_status))

            if confirmation:
                # Draw confirmation window overlay
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 180))  # Semi-transparent overlay
                screen.blit(overlay, (0, 0))

                # Confirmation message
                confirm_text = font.render(
                    "Slot occupied! Are you sure you want to delete all information inside?",
                    True, (255, 0, 0)
                )
                joke_text = font.render(
                    "Deleting is like forgetting where you hid the remote—irrevocable and slightly tragic!",
                    True, (255, 0, 0)
                )
                screen.blit(
                    confirm_text,
                    (screen.get_width() // 2 - confirm_text.get_width() // 2, SCREEN_HEIGHT // 2 - 60)
                )
                screen.blit(
                    joke_text,
                    (screen.get_width() // 2 - joke_text.get_width() // 2, SCREEN_HEIGHT // 2 - 20)
                )

                # Yes and No buttons
                yes_button = Button("Yes", position=(screen.get_width() // 2 - 100, SCREEN_HEIGHT // 2 + 40))
                no_button = Button("No", position=(screen.get_width() // 2 + 100, SCREEN_HEIGHT // 2 + 40))
                yes_button.draw(screen)
                no_button.draw(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if confirmation:
                        if yes_button.rect.collidepoint((mouse_x, mouse_y)):
                            # Delete the save slot
                            if slot_to_delete:
                                # Implement deletion logic here
                                delete_save_slot(slot_to_delete)  # You need to define this function
                                selected_slot = slot_to_delete
                                running = False
                        elif no_button.rect.collidepoint((mouse_x, mouse_y)):
                            confirmation = False
                            slot_to_delete = None
                    else:
                        for slot_rect, slot_num, slot_status in slot_rects:
                            if slot_rect.collidepoint((mouse_x, mouse_y)):
                                if slot_status == "Occupied":
                                    confirmation = True
                                    slot_to_delete = slot_num
                                else:
                                    selected_slot = slot_num
                                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and confirmation:
                        confirmation = False
                        slot_to_delete = None

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