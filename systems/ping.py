import pygame

class PingSystem:
    def __init__(self, screen_size):
        self.radius = 0
        self.max_radius = 350
        self.speed = 30

        self.growing = False
        self.active = False
        self.fading = False

        self.timer = 0
        self.hold_time = 10

        self.alpha = 255
        self.origin = (0, 0)

        self.screen_w, self.screen_h = screen_size

    def circle_rect_collision(self, circle_pos, radius, rect):
        cx, cy = circle_pos
        closest_x = max(rect.left, min(cx, rect.right))
        closest_y = max(rect.top, min(cy, rect.bottom))

        dx = cx - closest_x
        dy = cy - closest_y

        return dx * dx + dy * dy <= radius * radius

    def trigger(self, origin):
        self.radius = 0
        self.growing = True
        self.active = True
        self.timer = 0
        self.origin = origin
        self.alpha = 255
        self.fading = False

    def update(self):
        if not self.active:
            return

        if self.growing:
            progress = self.radius / self.max_radius
            self.radius += max(2, self.speed * (1 - progress))

            if self.radius >= self.max_radius:
                self.growing = False
                self.timer = 0

        else:
            self.timer += 1
            if self.timer >= self.hold_time:
                self.fading = True

        if self.fading:
            self.alpha -= 10
            if self.alpha <= 0:
                self.alpha = 0
                self.active = False

    def draw(self, screen):
        if not self.active:
            return

        temp = pygame.Surface((self.screen_w, self.screen_h), pygame.SRCALPHA)
        pygame.draw.circle(
            temp,
            (255, 255, 255, int(self.alpha)),
            self.origin,
            int(self.radius),
            2
        )
        screen.blit(temp, (0, 0))