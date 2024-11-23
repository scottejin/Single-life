from settings import TILE_SIZE

class Bullet:
    def __init__(self, x, y, direction, speed):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        self.is_broken = False

    def move(self, dt):
        if not self.is_broken:
            self.x += self.direction[0] * self.speed * dt
            self.y += self.direction[1] * self.speed * dt

    def get_position(self):
        return self.x, self.y

    def check_collision(self, dungeon_map, enemies, spawners):
        map_x, map_y = int(self.x // TILE_SIZE), int(self.y // TILE_SIZE)
        if map_x < 0 or map_x >= len(dungeon_map[0]) or map_y < 0 or map_y >= len(dungeon_map):
            return True
        if dungeon_map[map_y][map_x] == 1:
            return True
        for enemy in enemies:
            enemy_x, enemy_y = enemy.get_position()
            if abs(self.x - enemy_x) < TILE_SIZE // 2 and abs(self.y - enemy_y) < TILE_SIZE // 2:
                if enemy.take_damage():
                    enemies.remove(enemy)
                return True
        for spawner in spawners:
            if spawner.is_active and abs(self.x - spawner.spawn_x) < TILE_SIZE // 2 and abs(self.y - spawner.spawn_y) < TILE_SIZE // 2:
                spawner.take_damage()
                return True
        return False

    def break_bullet(self):
        self.is_broken = True