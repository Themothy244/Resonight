import pygame
import random 
from settings import WHITE
BUFF_SIZE = 32
class Buff:
    def __init__(self, x, y, width, height, bufftype):
        self.rect = pygame.Rect(x, y, BUFF_SIZE, BUFF_SIZE)
        self.type = bufftype

        self.frames = []
        self.frame_index = 0
        self.animation_speed = 0.2

        try:
            if self.type == "timer":
                sheet = pygame.image.load("assets/images/entities/buff.png").convert_alpha()
            else:
                sheet = pygame.image.load("assets/images/entities/buff.png").convert_alpha()

            frame_width = 32
            frame_height = 32
            scale = BUFF_SIZE / 32

            for col in range(13):
                x = col * frame_width
                if self.type == "lives":
                    row = 0
                elif self.type == "timer":
                    row = 1
                else:
                    row = 0

                y = row * frame_height

                frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
                frame.blit(sheet, (0, 0), (x, y, frame_width, frame_height))

                frame = pygame.transform.scale(
                    frame,
                    (int(frame_width * scale), int(frame_height * scale))
                )

                self.frames.append(frame)

            self.image = self.frames[0]

        except pygame.error:
            self.frames = []
            self.image = None
    
    def update(self):
        if self.frames:
            self.frame_index += self.animation_speed

            if self.frame_index >= len(self.frames):
                self.frame_index = 0

            self.image = self.frames[int(self.frame_index)]

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

