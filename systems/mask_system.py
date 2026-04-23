import pygame

class MaskSystem:
    def __init__(self, screen_size, vignette):
        self.width, self.height = screen_size
        self.vignette = vignette

        self.dark_surface = pygame.Surface(screen_size, pygame.SRCALPHA)

        self.mask_closing = False
        self.mask_timer = 0
        self.MASK_DELAY = 30
    
    def trigger_open(self):
        self.mask_closing = False
        self.mask_timer = 0

    def update(self, ping):
        if not ping.active:
            self.mask_closing = True

        if self.mask_closing:
            self.mask_timer += 1
            if self.mask_timer >= self.MASK_DELAY:
                self.mask_closing = False
                ping.radius = 0

    def draw(self, screen, ping):
        if ping.radius <= 0:
            screen.fill((0, 0, 0))
            return

        self.dark_surface.fill((0, 0, 0, 255))

        size = int(ping.radius * 2.3)
        vignette_scaled = pygame.transform.smoothscale(self.vignette, (size, size))
        rect = vignette_scaled.get_rect(center=ping.origin)

        self.dark_surface.blit(vignette_scaled, rect, special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(self.dark_surface, (0, 0))
