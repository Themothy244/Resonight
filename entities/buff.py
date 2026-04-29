import pygame
import random 
from settings import WHITE

BUFF_SIZE = 30

class Buff:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, BUFF_SIZE, BUFF_SIZE)

        self.type = random.choice(["timer", "lives"])

        try:
            if self.type == "timer":
                self.image = pygame.image.load("assets/images/entities/timer_icon.png").convert_alpha()
            
            else:
                self.image = pygame.image.load("assets/images/entities/health_icon.png").convert_alpha()

            self.image =  pygame.transform.smoothscale(self.image, (BUFF_SIZE, BUFF_SIZE))
        
        except pygame.error:
            self.image = None
    
    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect)
        else:
            color = (255, 215, 0) if self.type == "timer" else (255, 50, 50)
            pygame.draw.rect(screen, color, self.rect)

    def apply_effect(self, game):
        if self.type == "lives":
            game.lives += 1
        elif self.type == "timer":
            game.timer.time_left += 5

    def try_spawn_buff(width, height, platforms, spikes, ground_rect):
        if random.random() < 0.40:
            valid_surfaces =  platforms + spikes + [ground_rect]

            if not valid_surfaces:
                return None

            surface = random.choice(valid_surfaces)

            x = random.randint(surface.rect.left, surface.rect.right - BUFF_SIZE)
            y = surface.rect.top - BUFF_SIZE - 30

            return Buff(x, y, width, height)
        else:
            return None

