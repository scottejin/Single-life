import pygame

class XPOrb:
    def __init__(self, x, y, size=10):
        self.x = x
        self.y = y
        self.size = size
        self.collected = False
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def update(self, player_rect):
        if self.rect.colliderect(player_rect):
            self.collected = True
            return True  # XP collected
        return False

    def draw(self, screen, camera_x, camera_y):
        orb_x = self.x - camera_x
        orb_y = self.y - camera_y
        # Draw outer circle (yellow)
        pygame.draw.circle(screen, (255, 255, 0), (orb_x + self.size // 2, orb_y + self.size // 2), self.size // 2)
        # Draw inner circle (orange) for gradient effect
        inner_radius = int(self.size * 0.3)
        pygame.draw.circle(screen, (255, 165, 0), (orb_x + self.size // 2, orb_y + self.size // 2), inner_radius)