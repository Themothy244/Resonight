import pygame
from systems.ping_system import PingSystem
from settings import *

BAT_SIZE = 40

class Bat:
    def __init__(self, x, y, sfx=None):
        self.rect = pygame.Rect(x, y, BAT_SIZE, BAT_SIZE)

        # ================= ANIMATION =================
        self.frames = []
        self.frame_index = 0
        self.animation_speed = 0.15

        try:
            sheet = pygame.image.load(
                "assets/images/entities/bat_spritesheet.png"
            ).convert_alpha()

            frame_w = 16
            frame_h = 16
            scale = BAT_SIZE / frame_w

            for i in range(18):  # 18 frames, single row
                frame = pygame.Surface((frame_w, frame_h), pygame.SRCALPHA)
                frame.blit(
                    sheet,
                    (0, 0),
                    (i * frame_w, 0, frame_w, frame_h)
                )

                frame = pygame.transform.scale(
                    frame,
                    (int(frame_w * scale), int(frame_h * scale))
                )

                self.frames.append(frame)

            self.image = self.frames[0]

        except pygame.error:
            self.frames = []
            self.image = None

        self.alpha = 0
        self.visible_timer = 0

        self.ping = PingSystem((WIDTH, HEIGHT), 200)

        self.triggered = False
        self.cooldown = 0
        self.chain_delay = 0
        self.sfx = sfx

    def reset(self):
        self.ping.reset()
        self.triggered = False
        self.cooldown = 0
        self.chain_delay = 0
        self.alpha = 0
        self.visible_timer = 0
        self.frame_index = 0

    def trigger(self):
        if self.triggered or self.cooldown > 0:
            return

        if self.sfx:
            self.sfx.play()

        self.ping.trigger(self.rect.center)
        self.triggered = True
        self.cooldown = 100
        self.chain_delay = 10

    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1

        if self.chain_delay > 0:
            self.chain_delay -= 1
        
        self.ping.update()

        if not self.ping.active and self.cooldown == 0:
            self.triggered = False

        # ================= ANIMATION UPDATE =================
        if self.frames:
            self.frame_index += self.animation_speed

            if self.frame_index >= len(self.frames):
                self.frame_index = 0

            self.image = self.frames[int(self.frame_index)]

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect.topleft)
        else:
            if self.alpha > 0:
                surf = pygame.Surface(self.rect.size, pygame.SRCALPHA)
                surf.fill((150, 0, 150, int(self.alpha)))
                screen.blit(surf, self.rect.topleft)

        self.ping.draw(screen)