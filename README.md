# Endless Dungeon Explorer

## Overview
Endless Dungeon Explorer is a Python-based game built with Pygame, featuring dynamic dungeon generation, enemy spawners, and an XP collection system.

## Features
- **Dynamic Dungeon Generation**: Explore an endless series of procedurally generated dungeon rooms.
- **Enemy Spawners**: Spawn normal and strong enemies with varying behaviors and health systems.
- **XP Orbs**: Collect XP orbs to enhance your gameplay and upgrade abilities.
- **Save and Load System**: Manage multiple save slots with confirmation prompts.
- **Responsive UI**: User interface adapts to various screen resolutions.
- **Accessibility**: Enhanced color contrast and readable fonts for better accessibility.
- **Shop System**: Upgrade shooting speed using collected XP orbs.
- **Dynamic Music System**: Multiple background tracks with seamless transitions.
- **Visual Feedback**: 
  - Enemy health indicators
  - Player health bar
  - XP counter
  - Range indicator circle (toggleable)
- **Directional Shooting**: Eight-way bullet system with unique sprites for each direction.
- **Boss Mode**: Special music triggers when player health is critical.

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

## Controls
- **WASD/Arrow Keys**: Move player
- **Mouse**: Aim
- **Left Click**: Shoot
- **E**: Open shop
- **M**: Change music track
- **ESC**: Pause game/Exit menus

## Installation
1. **Clone the Repository**
    ```bash
    git clone https://github.com/scottejin/Single-life
    ```
2. **Navigate to the Project Directory**
    ```bash
    cd Single-life
    ```
3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
4. **Run the Game**
    ```bash
    python main.py
    ```

## Asset Credits
All assets used in this game are public domain:

- **Dungeon Bricks Textures**: 16x16 4-color dungeon bricks by Arachne
  - Source: [OpenGameArt](https://opengameart.org/content/4-color-dungeon-bricks-16x16)
  - License: Public Domain

- **Background Music**: NES-Style Shooter Music (5 tracks, 3 jingles) by SketchyLogic
  - Source: [OpenGameArt](https://opengameart.org/content/nes-shooter-music-5-tracks-3-jingles)
  - License: Public Domain

- **Player and Wall Textures**: Dungeon Crawl 32x32 tiles
  - Source: [OpenGameArt](https://opengameart.org/content/dungeon-crawl-32x32-tiles)
  - License: Public Domain


