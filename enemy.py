class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 2
        self.speed = 50  # Pixels per second

    def get_position(self):
        return self.x, self.y

    def take_damage(self):
        self.health -= 1
        return self.health <= 0  # Return True if the enemy is dead

    def move_towards_player(self, player_x, player_y, dt):
        direction_x = player_x - self.x
        direction_y = player_y - self.y
        distance = (direction_x**2 + direction_y**2)**0.5
        if distance > 0:
            direction_x /= distance
            direction_y /= distance
            self.x += direction_x * self.speed * dt
            self.y += direction_y * self.speed * dt