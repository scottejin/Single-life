# main.py
import pygame
import sys
from settings import *
from map import load_room_at, find_walkable_tile, update_doors
from player import Player

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED | pygame.DOUBLEBUF)
pygame.display.set_caption("Endless Dungeon Explorer")

dungeon_rooms = {}
doors = []

try:
    initial_room = load_room_at(0, 0, dungeon_rooms, doors)
    player_x, player_y = find_walkable_tile(initial_room)
except ValueError as e:
    print(f"Error during player initialization: {e}")
    pygame.quit()
    sys.exit()

player = Player(player_x, player_y, player_speed)

clock = pygame.time.Clock()
running = True
current_room_x, current_room_y = 0, 0

while running:
    dt = clock.tick(TARGET_FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    current_room = load_room_at(current_room_x, current_room_y, dungeon_rooms, doors)

    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    if keys[pygame.K_LEFT]:
        dx = -1
    if keys[pygame.K_RIGHT]:
        dx = 1
    if keys[pygame.K_UP]:
        dy = -1
    if keys[pygame.K_DOWN]:
        dy = 1

    player.move(dx, dy, dt, current_room, doors)
    player_x, player_y = player.get_position()

    update_doors(player_x, player_y, doors)

    if player_x < 0:
        current_room_x -= 1
        player_x = (MAP_WIDTH - 1) * TILE_SIZE
    elif player_x >= MAP_WIDTH * TILE_SIZE:
        current_room_x += 1
        player_x = 0
    if player_y < 0:
        current_room_y -= 1
        player_y = (MAP_HEIGHT - 1) * TILE_SIZE
    elif player_y >= MAP_HEIGHT * TILE_SIZE:
        current_room_y += 1
        player_y = 0

    camera_x = int(player_x - SCREEN_WIDTH // 2)
    camera_y = int(player_y - SCREEN_HEIGHT // 2)

    screen.fill(BLACK)

    for row in range(MAP_HEIGHT):
        for col in range(MAP_WIDTH):
            tile_x = col * TILE_SIZE - camera_x
            tile_y = row * TILE_SIZE - camera_y

            if current_room[row][col] == 1:
                pygame.draw.rect(screen, GRAY, (tile_x, tile_y, TILE_SIZE, TILE_SIZE))
            elif current_room[row][col] == 0:
                pygame.draw.rect(screen, WHITE, (tile_x, tile_y, TILE_SIZE, TILE_SIZE))

    for door in doors:
        tile_x = door.x * TILE_SIZE - camera_x
        tile_y = door.y * TILE_SIZE - camera_y
        color = GRAY if door.is_open else BLUE
        pygame.draw.rect(screen, color, (tile_x, tile_y, TILE_SIZE, TILE_SIZE))

    pygame.draw.rect(screen, RED, (SCREEN_WIDTH // 2 - PLAYER_SIZE // 2, SCREEN_HEIGHT // 2 - PLAYER_SIZE // 2, PLAYER_SIZE, PLAYER_SIZE))

    pygame.display.flip()

pygame.quit()
sys.exit()