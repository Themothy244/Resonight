import pygame

class Spike:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.alpha = 0
        self.visible_timer = 0

    def draw(self, screen):
        if self.alpha <= 0:
            return

        temp = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        points = [
            (0, self.rect.height),
            (self.rect.width, self.rect.height),
            (self.rect.width // 2, 0)
        ]
        pygame.draw.polygon(temp, (255, 255, 255, int(self.alpha)), points)
        screen.blit(temp, self.rect.topleft)