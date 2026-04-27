import pygame
from settings import WHITE

class Platform:
    def __init__(self, x, y, width, height, platformType="normal"):
        self.rect = pygame.Rect(x, y, width, height)
        self.platformType = platformType
        self.alpha = 0
        self.visible_timer = 0
        self.surface = pygame.Surface((width, height))
        self.surface.fill(WHITE)

        self.start_x = x
        self.speed = 2
        self.range = 100
        self.direction = 1
        self.prev_x = x

    def update(self):
        self.prev_x = self.rect.x

        if self.platformType == "moving":
            self.rect.x += self.speed * self.direction

            if self.rect.x > self.start_x + self.range:
                self.direction = -1

            elif self.rect.x < self.start_x - self.range:
                self.direction = 1

    def draw(self, screen):
        if self.alpha > 0:
            self.surface.set_alpha(int(self.alpha))
            screen.blit(self.surface, self.rect.topleft)
