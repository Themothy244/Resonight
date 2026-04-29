import pygame
from settings import WHITE

class Player:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = 5
        self.y_velocity = 0
        self.gravity = 0.5
        self.low_jump_multiplier = 2
        self.jump_strength = 13
        self.is_jumping = False

        self.current_platform = None
        self.on_platform = False

    def on_ground_or_platform(self, platforms, ground_y):
        if self.rect.bottom >= ground_y:
            return True

        for p in platforms:
            if (
                self.rect.bottom >= p.rect.top - 5 and
                self.rect.bottom <= p.rect.top + 5 and
                self.rect.right > p.rect.left and
                self.rect.left < p.rect.right
            ):
                return True
        return False

    def move_and_collide(self, platforms, dx, dy):
        self.rect.x += dx

        for p in platforms:
            if self.rect.colliderect(p.rect):
                if dx > 0:
                    self.rect.right = p.rect.left
                elif dx < 0:
                    self.rect.left = p.rect.right

        self.rect.y += dy

        for p in platforms:
            if self.rect.colliderect(p.rect):
                if dy > 0:
                    self.rect.bottom = p.rect.top
                    dy = 0
                    self.on_platform = True
                    self.current_platform = p
                elif dy < 0:
                    self.rect.top = p.rect.bottom
                    dy = 0

        return dy

    def update(self, keys, platforms, ground_y):
        self.on_platform = False
        self.current_platform = None
        dx = 0

        if keys[pygame.K_LEFT]:
            dx = -self.speed
        if keys[pygame.K_RIGHT]:
            dx = self.speed

        if keys[pygame.K_SPACE] and self.on_ground_or_platform(platforms, ground_y):
                self.y_velocity = -self.jump_strength

        if self.y_velocity < 0:
            if not keys[pygame.K_SPACE]:
                self.y_velocity += self.gravity * self.low_jump_multiplier
            else:
                self.y_velocity += self.gravity
        else:
            self.y_velocity += self.gravity

        self.y_velocity = self.move_and_collide(platforms, dx, self.y_velocity)

        if self.on_platform and self.current_platform:
            if self.current_platform.platformType == "moving":
                platform_dx = self.current_platform.rect.x - self.current_platform.prev_x
                self.rect.x += platform_dx
            self.rect.bottom = self.current_platform.rect.top

        if self.rect.bottom >= ground_y:
            self.rect.bottom = ground_y
            self.y_velocity = 0

        self.prev_x = self.rect.x

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)