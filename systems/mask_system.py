import pygame

class MaskSystem:
    def __init__(self, screen_size, vignette):
        self.width, self.height = screen_size
        self.vignette = vignette

        self.dark_surface = pygame.Surface(screen_size, pygame.SRCALPHA)

        self.fade_pings = []
        self.FADE_DELAY = 30

    def update(self, active_pings):
        active_set = set(active_pings)

        # Track new pings
        existing = [fp["ping"] for fp in self.fade_pings]
        for ping in active_pings:
            if ping.radius > 0 and ping not in existing:
                self.fade_pings.append({"ping": ping, "timer": 0})

        # Update fade timers
        for fp in self.fade_pings:
            if fp["ping"] not in active_set or fp["ping"].radius <= 0:
                fp["timer"] += 1

        # Remove expired
        self.fade_pings = [
            fp for fp in self.fade_pings
            if fp["timer"] < self.FADE_DELAY
        ]

    def draw(self, screen, active_pings):
        self.dark_surface.fill((0, 0, 0, 255))

        all_pings = list(active_pings) + [dp["ping"] for dp in self.fade_pings]

        if not all_pings:
            screen.fill((0, 0, 0))
            return

        for ping in all_pings:
            size = int(ping.radius * 2.3)
            if size <= 0:
                continue

            vignette_scaled = pygame.transform.smoothscale(self.vignette, (size, size))
            rect = vignette_scaled.get_rect(center=ping.origin)

            self.dark_surface.blit(vignette_scaled, rect, special_flags=pygame.BLEND_RGBA_MULT)

        screen.blit(self.dark_surface, (0, 0))