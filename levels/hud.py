import pygame
from settings import *

class HUD:
    def __init__(self):
        self.font_timer = pygame.font.SysFont("Inter", 50, bold=True)
        self.font_text = pygame.font.SysFont("arial", 32)

        self.blink_timer = 0
        self.blink_interval = 0.3
        self.heart = pygame.image.load("assets/images/entities/health_icon.png").convert_alpha()
        self.empty = pygame.image.load("assets/images/entities/health_icon_blank.png").convert_alpha()
        
        width, height = 50, 50
        self.heart = pygame.transform.scale(self.heart, (width, height))
        self.empty = pygame.transform.scale(self.empty, (width, height))

    def update(self, dt):
        self.blink_timer += dt

    def draw(self, screen, level, timeLeft, totalPings, lives):
        # LEFT: LEVEL
        level_text = self.font_text.render(f"Level: {level}", True, (255, 255, 255))
        screen.blit(level_text, (10, 10))

        # TIMER
        minutes = int(timeLeft) // 60
        seconds = int(timeLeft) % 60

        # blinking color
        color = (255, 255, 255)
        if timeLeft <= 10:
            if int(self.blink_timer / self.blink_interval) % 2 == 0:
                color = (255, 0, 0)

        timer_text = self.font_timer.render(f"{minutes:02d}:{seconds:02d}", True, color)
        screen.blit(timer_text, (WIDTH//2 - timer_text.get_width()//2, 10))

        # RIGHT: PINGS
        ping_text = self.font_text.render(f"Pings: {totalPings}", True, (255, 255, 255))
        screen.blit(ping_text, (WIDTH - ping_text.get_width() - 10, 10))

        # LIVES 
        for i in range(3):
            if i < lives:
                heart = self.heart
            else:
                heart = self.empty

            screen.blit(heart, (750 + i * 60, 620))