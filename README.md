# Endless Dungeon Explorer

## Overview
Endless Dungeon Explorer is a Python-based game built with Pygame, featuring dynamic dungeon generation, enemy spawners, and an XP collection system.

## Features
- **Dynamic Dungeon Generation**: Explore an endless series of dungeon rooms.
- **Enemy Spawners**: Spawn normal and strong enemies with varying behaviors.
- **XP Orbs**: Collect XP orbs to enhance your gameplay.
- **Save and Load System**: Manage multiple save slots with confirmation prompts.
- **Responsive UI**: User interface adapts to various screen resolutions.
- **Accessibility**: Enhanced color contrast and readable fonts for better accessibility.

## New Implementations
### Confirmation Dialog
A dedicated `ConfirmationDialog` class handles all confirmation prompts, ensuring consistency and promoting code reuse. It features dynamic text wrapping and button enhancements for improved user experience.

### Enhanced Buttons
- **Hover Effects**: Buttons change color when hovered over, providing visual feedback.
- **Consistent Styling**: All buttons share the same font, size, and color schemes for a cohesive look.

### Dynamic Text Wrapping
Implemented a utility function to automatically wrap text based on maximum width, ensuring all messages fit within the screen boundaries.

### Accessibility Enhancements
- **Color Contrast**: Selected colors ensure sufficient contrast for readability.
- **Readable Fonts**: Chose clear and appropriately sized fonts, especially for smaller text elements.

### Responsive Design
UI elements dynamically adjust their positions and sizes based on screen resolutions, ensuring that elements remain within visible areas across different devices.

### Robust Error Handling
The `delete_save_slot` function now gracefully handles potential exceptions, such as file permission issues, preventing the game from crashing unexpectedly.

## Installation
1. **Clone the Repository**
    ```bash
    git clone https://github.com/yourusername/endless-dungeon-explorer.git
    ```
2. **Navigate to the Project Directory**
    ```bash
    cd endless-dungeon-explorer
    ```
3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
4. **Run the Game**
    ```bash
    python main.py
    ```

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

