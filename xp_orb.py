import pygame

class XPOrb:
    """Experience orb that can be collected by the player for points"""
    def __init__(self, x, y, size=10, collected=False):
        # Initialize orb position and properties
        self.x = x
        self.y = y
        self.size = size
        self.collected = collected
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def update(self, player_rect):
        """Check collision with player and mark as collected if touched"""
        if self.rect.colliderect(player_rect):
            self.collected = True
            return True  # XP collected
        return False

    def draw(self, screen, camera_x, camera_y):
        """Render orb with two-tone gradient effect at camera-adjusted position"""
        # Calculate screen position
        orb_x = self.x - camera_x
        orb_y = self.y - camera_y
        
        # Draw outer yellow glow
        pygame.draw.circle(screen, (255, 255, 0), (orb_x + self.size // 2, orb_y + self.size // 2), self.size // 2)
        
        # Draw inner orange core
        inner_radius = int(self.size * 0.3)
        pygame.draw.circle(screen, (255, 165, 0), (orb_x + self.size // 2, orb_y + self.size // 2), inner_radius)

    def to_dict(self):
        """Serialize orb data for saving"""
        return {
            'x': self.x,
            'y': self.y,
            'collected': self.collected,
            'size': self.size
        }

    @staticmethod
    def from_dict(data):
        """Create orb instance from saved data"""
        return XPOrb(
            x=data['x'],
            y=data['y'],
            size=data['size'],
            collected=data['collected']
        )