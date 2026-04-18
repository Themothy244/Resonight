import pygame
from settings import WHITE

class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.alpha = 0
        self.visible_timer = 0
        self.surface = pygame.Surface((width, height))
        self.surface.fill(WHITE)

    def draw(self, screen):
        if self.alpha > 0:
            self.surface.set_alpha(int(self.alpha))
            screen.blit(self.surface, self.rect.topleft)
