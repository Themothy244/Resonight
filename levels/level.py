import pygame
from settings import WIDTH, HEIGHT

class Level:
    def __init__(self, platforms, spikes, doors, player_spawn, bg_path):
        self.platforms = platforms
        self.spikes = spikes
        self.doors = doors
        self.player_spawn = player_spawn

        self.bg = pygame.image.load(bg_path).convert()
        self.bg = pygame.transform.scale(self.bg, (WIDTH, HEIGHT))
        self.ground = pygame.image.load("assets/images/entities/ground.png").convert_alpha()
        self.ground = pygame.transform.scale(self.ground, (WIDTH, 5))

    def draw(self, screen):
        self.bg.set_alpha(20)
        screen.blit(self.bg, (0, 0))
        screen.blit(self.ground, (0, HEIGHT - 40))

        for p in self.platforms:
            p.draw(screen)
        for s in self.spikes:
            s.draw(screen)
        for d in self.doors:
            d.draw(screen)
    
    def get_all_objects(self):
        return self.platforms + self.spikes + self.doors