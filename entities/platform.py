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

        self.bg_image = pygame.image.load("assets\images\entities\platform_transparent.png").convert_alpha()

        img_w, img_h = self.bg_image.get_size()
        scale = height / img_h
        new_width = int(img_w * scale)

        self.bg_scaled = pygame.transform.smoothscale(self.bg_image, (new_width, height))

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
            previous_clip = screen.get_clip()
            screen.set_clip(self.rect)

            self.bg_scaled.set_alpha(int(self.alpha))
            screen.blit(self.bg_scaled, self.rect.topleft)
            self.bg_scaled.set_alpha(None)  

            screen.set_clip(previous_clip)
