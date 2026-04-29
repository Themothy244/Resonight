import pygame
import random 
from settings import WHITE

BUFF_SIZE = 30

class Buff:
    def __init__(self, x, y, width, height, bufftype):
        self.rect = pygame.Rect(x, y, BUFF_SIZE, BUFF_SIZE)
        self.type = bufftype

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

    def try_spawn_buff(width, height, platforms, ground_rect, lives):
        if random.random() < 0.40:
            valid_surfaces =  platforms + [ground_rect]

            if not valid_surfaces:
                return None

            surface = random.choice(valid_surfaces)
            rect = surface.rect if hasattr(surface, "rect") else surface

            x = random.randint(rect.left, rect.right - BUFF_SIZE)
            y = rect.top - BUFF_SIZE - 30

            if lives >= 3:
                bufftype = "timer"
            else:
                bufftype = random.choice(["timer", "lives"])

            return Buff(x, y, width, height, bufftype)
        else:
            return None

