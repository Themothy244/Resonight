import pygame
import sys

pygame.init()

# ================== SCREEN SETUP ==================
WIDTH = 960
HEIGHT = 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Resonight")
clock = pygame.time.Clock()

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

running = True
while running:
    clock.tick(60)
    screen.fill(BLACK)

    # ---------- INPUT / EVENTS ----------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
sys.exit()