import pygame
from systems.ping_system import PingSystem
from settings import *

class Bat:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 30)

        self.alpha = 0
        self.visible_timer = 0

        self.ping = PingSystem((WIDTH, HEIGHT), 200)

        self.triggered = False
        self.cooldown = 0
        self.chain_delay = 0

    def reset(self):
        self.ping.reset()
        self.triggered = False
        self.cooldown = 0
        self.chain_delay = 0
        self.alpha = 0
        self.visible_timer = 0

    def trigger(self):
        if self.triggered or self.cooldown > 0:
            return

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

    def draw(self, screen):
        if self.alpha > 0:
            surf = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            surf.fill((150, 0, 150, int(self.alpha))) 
            screen.blit(surf, self.rect.topleft)

        self.ping.draw(screen)