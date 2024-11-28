from settings import TILE_SIZE
import pygame

def count_white_spaces(dungeon_map, x, y):
    """Count empty cells surrounding a given position in an 8-direction neighbor check."""
    white_spaces = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(dungeon_map[0]) and 0 <= ny < len(dungeon_map) and dungeon_map[ny][nx] == 0:
                white_spaces += 1
    return white_spaces

def is_walkable(x, y, dungeon_map):
    """Check if a given pixel coordinate is within a walkable map tile."""
    map_x, map_y = int(x // TILE_SIZE), int(y // TILE_SIZE)
    if map_x < 0 or map_x >= len(dungeon_map[0]) or map_y < 0 or map_y >= len(dungeon_map):
        return False
    return dungeon_map[map_y][map_x] == 0

def render_wrapped_text(text, font, color, surface, x, y, max_width):
    """Render text with automatic word wrapping to fit within a specified width."""
    """
    Renders text onto a surface with dynamic wrapping based on max_width.

    :param text: The text string to render.
    :param font: Pygame font object.
    :param color: Color of the text.
    :param surface: Pygame surface to render the text on.
    :param x: x-coordinate for text rendering.
    :param y: y-coordinate for text rendering.
    :param max_width: Maximum width in pixels before wrapping text.
    """
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        test_line = f"{current_line} {word}".strip()
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)

    for idx, line in enumerate(lines):
        rendered_text = font.render(line, True, color)
        surface.blit(rendered_text, (x, y + idx * (font.get_height() + 5)))