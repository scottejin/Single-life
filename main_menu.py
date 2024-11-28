import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, RED, BLUE, enemy_spawn_interval, set_spawn_interval, get_spawn_interval  # Import the spawn interval setting
from save_load import get_available_saves, delete_save_slot
from confirmation_dialog import ConfirmationDialog  # New import
from utils import render_wrapped_text  # New import for text wrapping
import music  # Import the music module

class MainMenu:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 50)
        self.buttons = [
            Button("New Game", position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60)),
            Button("Load Game", position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)),
            Button("Settings", position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)),
            Button("Exit", position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        ]
        self.settings_buttons = [
            Button("Increase Spawn Rate", position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)),
            Button("Decrease Spawn Rate", position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)),
            Button("Save", position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)),
            Button("Back", position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        ]
        self.in_settings = False
        self.spawn_rate = get_spawn_interval()
        self.confirmation_dialog = None  # Initialize confirmation dialog
        self.settings_menu = None  # Initialize settings menu

    def draw(self, screen):
        screen.fill(BLACK)
        if not self.in_settings:
            for button in self.buttons:
                button.draw(screen)
        else:
            # Draw settings menu
            for button in self.settings_buttons:
                button.draw(screen)
            # Display current spawn rate
            spawn_rate_text = self.font.render(f"Spawn Rate: {self.spawn_rate:.1f}s", True, WHITE)
            spawn_rate_rect = spawn_rate_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
            screen.blit(spawn_rate_text, spawn_rate_rect)
        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if not self.in_settings:
                for button in self.buttons:
                    if button.rect.collidepoint(mouse_pos):
                        if button.text == "Settings":
                            self.in_settings = True
                        else:
                            return button.text
            else:
                for button in self.settings_buttons:
                    if button.rect.collidepoint(mouse_pos):
                        if button.text == "Increase Spawn Rate":
                            self.spawn_rate += 0.5
                            print(f"Spawn rate increased to {self.spawn_rate}s")
                        elif button.text == "Decrease Spawn Rate":
                            self.spawn_rate -= 0.5
                            if self.spawn_rate < 1.0:
                                self.spawn_rate = 1.0  # Minimum spawn rate
                            print(f"Spawn rate decreased to {self.spawn_rate}s")
                        elif button.text == "Save":
                            set_spawn_interval(self.spawn_rate)
                            print("Settings saved!")
                        elif button.text == "Back":
                            self.in_settings = False
        elif event.type == pygame.KEYDOWN:
            if self.in_settings:
                if event.key == pygame.K_UP:
                    self.spawn_rate += 0.5
                    print(f"Spawn rate increased to {self.spawn_rate}s")
                elif event.key == pygame.K_DOWN:
                    self.spawn_rate -= 0.5
                    if self.spawn_rate < 1.0:
                        self.spawn_rate = 1.0  # Minimum spawn rate
                    print(f"Spawn rate decreased to {self.spawn_rate}s")
                elif event.key == pygame.K_s:
                    set_spawn_interval(self.spawn_rate)
                    print("Settings saved!")
                elif event.key == pygame.K_b:
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

            music.update_track_display(screen, right_side=True)  # Update the music track display

            pygame.display.flip()
        return selected_slot  # Add this line to store the selected slot

class SettingsMenu:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 36)
        # Initialize slider with range 1 to 8
        self.slider_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100, 300, 20)  # Increased width for better precision
        self.slider_handle_rect = pygame.Rect(0, 0, 10, 30)
        self.handle_pos = self.value_to_position(enemy_spawn_interval)
        self.slider_handle_rect.centerx = self.handle_pos
        self.slider_handle_rect.centery = self.slider_rect.centery
        self.dragging = False
        
        # Initialize difficulty buttons with adjusted positions
        self.buttons = [
            Button("Easy", position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)),
            Button("Normal", position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10)),
            Button("Hard", position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70)),
            Button("Save", position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 130), font_size=36),
            Button("Back", position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 190), font_size=36)
        ]

    def draw(self, screen):
        screen.fill(BLACK)
        # Draw slider background
        pygame.draw.rect(screen, WHITE, self.slider_rect, 2)
        # Draw slider handle
        pygame.draw.rect(screen, RED, self.slider_handle_rect)
        # Draw current value label
        current_value = round(self.position_to_value(self.handle_pos), 1)
        value_label = self.font.render(f"Spawn Interval: {current_value:.1f}s", True, WHITE)
        screen.blit(value_label, (SCREEN_WIDTH // 2 - value_label.get_width() // 2, self.slider_rect.top - 40))
        
        # Draw buttons
        for button in self.buttons:
            button.draw(screen)

    def handle_event(self, event):
        # Handle slider dragging
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.slider_handle_rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.handle_pos = max(self.slider_rect.left, min(self.slider_rect.right, event.pos[0]))
                self.slider_handle_rect.centerx = self.handle_pos
                # Update spawn interval based on slider
                new_value = self.position_to_value(self.handle_pos)
                from settings import set_spawn_interval
                set_spawn_interval(new_value)
        
        # Handle button clicks
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                if button.rect.collidepoint(mouse_pos):
                    if button.text == "Easy":
                        self.set_spawn_interval(5.0)
                    elif button.text == "Normal":
                        self.set_spawn_interval(3.0)
                    elif button.text == "Hard":
                        self.set_spawn_interval(1.5)
                    elif button.text == "Save":
                        set_spawn_interval(self.position_to_value(self.handle_pos))
                        print("Settings saved!")
                    elif button.text == "Back":
                        return "Back"
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "Back"
        
        return None

    def set_spawn_interval(self, value):
        from settings import set_spawn_interval
        set_spawn_interval(value)
        self.handle_pos = self.value_to_position(value)
        self.slider_handle_rect.centerx = self.handle_pos

    def value_to_position(self, value):
        # Map spawn interval from 1 to 8 seconds to slider position
        min_pos = self.slider_rect.left
        max_pos = self.slider_rect.right
        position = min_pos + (value - 1) / (8 - 1) * (max_pos - min_pos)
        return position

    def position_to_value(self, position):
        # Map slider position back to spawn interval between 1 and 8 seconds
        min_pos = self.slider_rect.left
        max_pos = self.slider_rect.right
        value = 1 + (position - min_pos) / (max_pos - min_pos) * (8 - 1)
        return max(1, min(8, value))

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