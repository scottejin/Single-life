class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 2

    def get_position(self):
        return self.x, self.y

    def take_damage(self):
        self.health -= 1
        return self.health <= 0  # Return True if the enemy is dead