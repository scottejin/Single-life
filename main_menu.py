import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, RED, BLUE, enemy_spawn_interval  # Import the spawn interval setting
from save_load import get_available_saves, delete_save_slot
from confirmation_dialog import ConfirmationDialog  # New import
from utils import render_wrapped_text  # New import for text wrapping
import music  # Import the music module

class MainMenu:
    def __init__(self):
        self.buttons = [
            Button("New Game", position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 120)),
            Button("Load Game", position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60)),
            Button("Settings", position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)),
            Button("Exit", position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        ]
        self.confirmation_dialog = None  # Initialize confirmation dialog
        self.settings_menu = None  # Initialize settings menu

    def draw(self, screen):
        screen.fill(BLACK)
        if self.settings_menu:
            self.settings_menu.draw(screen)
        else:
            for button in self.buttons:
                button.draw(screen)
        music.update_track_display(screen, right_side=True)  # Update the music track display

    def handle_event(self, event):
        if self.settings_menu:
            result = self.settings_menu.handle_event(event)
            if result == "Back":
                self.settings_menu = None  # Exit settings menu
            return None  # When in settings menu, do not process other events
        else:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button.rect.collidepoint(mouse_pos):
                        if button.text == "Settings":
                            self.settings_menu = SettingsMenu()  # Open settings menu
                            return None
                        else:
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

            music.update_track_display(screen, right_side=True)  # Update the music track display

            pygame.display.flip()
        return selected_slot  # Add this line to store the selected slot

class SettingsMenu:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 36)
        self.slider_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 20)
        self.slider_handle_rect = pygame.Rect(0, 0, 10, 30)
        self.handle_pos = self.value_to_position(enemy_spawn_interval)
        self.slider_handle_rect.centerx = self.handle_pos
        self.slider_handle_rect.centery = self.slider_rect.centery
        self.dragging = False

    def value_to_position(self, value):
        # Map value (1 to 10) to position on the slider
        min_pos = self.slider_rect.left
        max_pos = self.slider_rect.right
        position = min_pos + (value - 1) / 9 * (max_pos - min_pos)
        return position

    def position_to_value(self, position):
        # Map position on the slider to value (1 to 10)
        min_pos = self.slider_rect.left
        max_pos = self.slider_rect.right
        value = 1 + (position - min_pos) / (max_pos - min_pos) * 9
        return max(1, min(10, value))

    def draw(self, screen):
        # Draw slider background
        pygame.draw.rect(screen, WHITE, self.slider_rect, 2)
        # Draw slider handle
        pygame.draw.rect(screen, RED, self.slider_handle_rect)
        # Draw labels
        min_label = self.font.render("1s", True, WHITE)
        max_label = self.font.render("10s", True, WHITE)
        screen.blit(min_label, (self.slider_rect.left - min_label.get_width() // 2, self.slider_rect.bottom + 5))
        screen.blit(max_label, (self.slider_rect.right - max_label.get_width() // 2, self.slider_rect.bottom + 5))
        # Draw current value
        current_value = round(self.position_to_value(self.handle_pos), 1)
        value_label = self.font.render(f"Spawn Interval: {current_value:.1f}s", True, WHITE)
        screen.blit(value_label, (SCREEN_WIDTH // 2 - value_label.get_width() // 2, self.slider_rect.top - 40))
        # Draw Back button
        back_button = Button("Back", position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50), font_size=36)
        back_button.draw(screen)
        self.back_button = back_button  # Store for event handling

        # Draw difficulty labels
        difficulty_font = pygame.font.SysFont(None, 24)

        # Difficulty levels with their corresponding spawn intervals
        difficulties = [
            ("Easy\n5 sec", 5),
            ("Normal\n3 sec", 3),
            ("Hard\n1.5 sec", 1.5)
        ]

        # Draw each difficulty label at the correct position on the slider
        for label_text, value in difficulties:
            pos_x = self.value_to_position(value)
            label_surface = difficulty_font.render(label_text, True, WHITE)
            label_rect = label_surface.get_rect(center=(pos_x, self.slider_rect.top - 40))
            screen.blit(label_surface, label_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.slider_handle_rect.collidepoint(event.pos):
                self.dragging = True
            elif self.back_button.rect.collidepoint(event.pos):
                return "Back"
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.handle_pos = max(self.slider_rect.left, min(self.slider_rect.right, event.pos[0]))
                self.slider_handle_rect.centerx = self.handle_pos
                # Update the enemy_spawn_interval value
                new_value = self.position_to_value(self.handle_pos)
                from settings import set_spawn_interval
                set_spawn_interval(new_value)
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
            self.rendered_text = self.font.render(self.text, True, self.hover_color)
        else:
            self.rendered_text = self.font.render(self.text, True, self.base_color)
        surface.blit(self.rendered_text, self.rect)