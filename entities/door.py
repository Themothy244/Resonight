import pygame
from settings import WHITE

class Door:
    def __init__(self, x, y, width, height, door_type):
        self.rect = pygame.Rect(x, y, width, height)
        self.alpha = 0
        self.visible_timer = 0
        self.doorType = door_type
        
        if self.doorType == "exit":
            self.bg = pygame.image.load("assets/images/entities/Exit_door.png").convert()
        else:
            self.bg = pygame.image.load("assets/images/entities/Entrance_door.png").convert()

        self.bg.set_colorkey((0, 0, 0))
        self.bg = pygame.transform.scale(self.bg, (width, height))

    def draw(self, screen):
        if self.alpha > 0:
            self.bg.set_alpha(int(self.alpha))
            screen.blit(self.bg, self.rect.topleft)