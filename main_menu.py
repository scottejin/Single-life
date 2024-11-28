import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, RED, BLUE, enemy_spawn_interval, set_spawn_interval, get_spawn_interval, set_show_circle, get_show_circle  # Import set_show_circle and get_show_circle
from save_load import get_available_saves, delete_save_slot
from confirmation_dialog import ConfirmationDialog  # New import
from utils import render_wrapped_text  # New import for text wrapping
import music  # Import the music module

# Main menu interface with game initialization options and settings management
class MainMenu:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 50)
        self.buttons = [
            Button("New Game", position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60)),
            Button("Load Game", position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)),
            Button("Settings", position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)),
            Button("Exit", position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        ]
        self.in_settings = False
        self.settings_menu = SettingsMenu()

    def draw(self, screen):
        screen.fill(BLACK)
        if not self.in_settings:
            for button in self.buttons:
                button.draw(screen)
        else:
            self.settings_menu.draw(screen)
        # Removed pygame.display.flip() to prevent multiple flips per frame

    def handle_event(self, event):
        if not self.in_settings:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button.rect.collidepoint(mouse_pos):
                        if button.text == "Settings":
                            self.in_settings = True
                        else:
                            return button.text
        else:
            result = self.settings_menu.handle_event(event)
            if result == "Back":
                self.in_settings = False
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
                            selected_slot = slot_to_overwrite
                            running = False
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
            # Add this line to set the previous_slot after selection
            previous_slot = selected_slot

            pygame.display.flip()
        return selected_slot  # Add this line to store the selected slot

class SettingsMenu:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 36)
        self.slider_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50, 300, 20)
        self.slider_handle_rect = pygame.Rect(0, 0, 10, 30)
        self.handle_pos = self.value_to_position(get_spawn_interval())
        self.slider_handle_rect.centerx = self.handle_pos
        self.slider_handle_rect.centery = self.slider_rect.centery
        self.dragging = False
        self.show_circle = get_show_circle()  # Retrieve current setting
        self.circle_toggle_button = Button(
            "Hide Blue Circle" if self.show_circle else "Show Blue Circle",
            position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150),
            font_size=36
        )
        self.buttons = [
            Button("Save Settings", position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50), font_size=36),
            Button("Back", position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 110), font_size=36),
            self.circle_toggle_button
        ]

    def draw(self, screen):
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, self.slider_rect, 2)
        pygame.draw.rect(screen, RED, self.slider_handle_rect)
        current_value = round(self.position_to_value(self.handle_pos), 1)
        value_label = self.font.render(f"Spawn Interval: {current_value:.1f}s", True, WHITE)
        screen.blit(value_label, (SCREEN_WIDTH // 2 - value_label.get_width() // 2, self.slider_rect.top - 40))
        easy_label = self.font.render("Easy (5s)", True, WHITE)
        medium_label = self.font.render("Medium (3s)", True, WHITE)
        hard_label = self.font.render("Hard (1.5s)", True, WHITE)
        screen.blit(easy_label, (self.slider_rect.left, self.slider_rect.top - 60))
        screen.blit(medium_label, (SCREEN_WIDTH // 2 - medium_label.get_width() // 2, self.slider_rect.top - 120))
        screen.blit(hard_label, (self.slider_rect.right - hard_label.get_width(), self.slider_rect.top - 180))
        for button in self.buttons:
            button.draw(screen)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.slider_handle_rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.handle_pos = max(self.slider_rect.left, min(self.slider_rect.right, event.pos[0]))
                self.slider_handle_rect.centerx = self.handle_pos
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                if button.rect.collidepoint(mouse_pos):
                    if button.text == "Save Settings":
                        set_spawn_interval(self.position_to_value(self.handle_pos))
                        set_show_circle(self.show_circle)  # Save the show_circle setting
                        print("Settings saved!")
                    elif button.text == "Back":
                        return "Back"
                    elif button.text == "Show Blue Circle":
                        self.show_circle = True
                        button.text = "Hide Blue Circle"
                    elif button.text == "Hide Blue Circle":
                        self.show_circle = False
                        button.text = "Show Blue Circle"
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "Back"
        return None

    def value_to_position(self, value):
        min_pos = self.slider_rect.left
        max_pos = self.slider_rect.right
        position = min_pos + (value - 1.5) / (5 - 1.5) * (max_pos - min_pos)
        return position

    def position_to_value(self, position):
        min_pos = self.slider_rect.left
        max_pos = self.slider_rect.right
        value = 1.5 + (position - min_pos) / (max_pos - min_pos) * (5 - 1.5)
        return max(1.5, min(5, value))

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
            self.rendered_text = self.font.render(self.text, True, self.hover_color)
        else:
            self.rendered_text = self.font.render(self.text, True, self.base_color)
        surface.blit(self.rendered_text, self.rect)