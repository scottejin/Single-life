import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, RED, BLUE
from save_load import get_available_saves, delete_save_slot
from confirmation_dialog import ConfirmationDialog  # New import
from utils import render_wrapped_text  # New import for text wrapping

class MainMenu:
    def __init__(self):
        self.buttons = [
            Button("New Game", position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 90)),
            Button("Load Game", position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30)),
            Button("Exit", position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        ]
        self.confirmation_dialog = None  # Initialize confirmation dialog

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
            return "Exit"  # Treat Escape as Exit button
        return None

    def select_save_slot(self, screen, title, mode):
        available_saves = get_available_saves()
        running = True
        selected_slot = None
        confirmation = False
        slot_to_overwrite = None  # Renamed variable for clarity

        font = pygame.font.SysFont(None, 36)
        small_font = pygame.font.SysFont(None, 28)
        button_font = pygame.font.SysFont(None, 30)
        while running:
            screen.fill((0, 0, 0))
            title_text = font.render(title, True, WHITE)
            screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, 50))

            slot_rects = []
            for i in range(3):  # Assuming 3 slots
                slot_num = i + 1
                slot_status = "Occupied" if available_saves.get(slot_num, False) else "Empty"
                slot_text = f"Slot {slot_num}: {slot_status}"
                text_color = RED if slot_status == "Occupied" else WHITE
                text_surface = font.render(slot_text, True, text_color)
                slot_rect = text_surface.get_rect(center=(screen.get_width() // 2, 150 + i * 50))
                screen.blit(text_surface, slot_rect)
                slot_rects.append((slot_rect, slot_num, slot_status))

            if confirmation and self.confirmation_dialog:
                self.confirmation_dialog.draw()  # Changed: removed 'screen' argument
            else:
                self.confirmation_dialog = None  # Reset if not in confirmation

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return None
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if confirmation:
                            confirmation = False
                            self.confirmation_dialog = None
                            slot_to_overwrite = None
                        else:
                            running = False
                            return None  # Return to previous menu
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if confirmation and self.confirmation_dialog:
                        result = self.confirmation_dialog.handle_event(event)
                        if result == "Yes":
                            if mode == "save":
                                selected_slot = slot_to_overwrite
                                running = False
                            try:
                                delete_save_slot(slot_to_overwrite)
                                selected_slot = slot_to_overwrite
                                running = False
                            except Exception as e:
                                print(f"Error deleting save slot {slot_to_overwrite}: {e}")
                                # Optionally, display an error message to the user
                        elif result == "No":
                            confirmation = False
                            slot_to_overwrite = None
                    else:
                        for slot_rect, slot_num, slot_status in slot_rects:
                            if slot_rect.collidepoint((mouse_x, mouse_y)):
                                if mode == "load":
                                    if slot_status == "Occupied":
                                        selected_slot = slot_num
                                        running = False
                                elif mode == "save":
                                    if slot_status == "Occupied":
                                        confirm_message = ["Slot is occupied! Do you want to overwrite it?"]
                                        self.confirmation_dialog = ConfirmationDialog(
                                            screen,
                                            confirm_message,
                                            [],
                                            ("Yes", "No"),
                                            position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                                        )
                                        confirmation = True
                                        slot_to_overwrite = slot_num
                                    else:
                                        selected_slot = slot_num
                                        running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and confirmation:
                        confirmation = False
                        self.confirmation_dialog = None
                        slot_to_overwrite = None

            pygame.display.flip()
        return selected_slot

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
            self.rendered_text = self.font.render(self.text, True, self.hover_color)
        else:
            self.rendered_text = self.font.render(self.text, True, self.base_color)
        surface.blit(self.rendered_text, self.rect)