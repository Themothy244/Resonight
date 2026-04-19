import pygame
import sys

pygame.init()
pygame.mixer.init()

from settings import *
from entities.platform import Platform
from entities.spike import Spike
from entities.door import Door
from entities.player import Player
from systems.ping import PingSystem
from levels.level import Level
from levels.level_manager import LevelManager

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Resonight Prototype")
        self.clock = pygame.time.Clock()
        self.running = True

        self.ground_y = HEIGHT - 40

        self.MENU = "menu"
        self.LEVEL = "level"
        self.GAME_OVER = "game_over"
        self.state = self.MENU

        self.level_manager = LevelManager()

        # ---------------- LEVEL 1 ----------------
        level1 = Level(
            platforms=[
                Platform(160, 240, 800, 20),
                Platform(0, 480, 800, 20),
                Platform(830, 590, 130, 20),
                Platform(0, 360, 130, 20),
            ],
            spikes=[
                Spike(500, self.ground_y - 30, 30, 30),
                Spike(530, self.ground_y - 30, 30, 30),
                Spike(560, self.ground_y - 30, 30, 30),
                Spike(360, 450, 30, 30),
                Spike(390, 450, 30, 30),
                Spike(420, 450, 30, 30),
                Spike(560, 210, 30, 30),
                Spike(590, 210, 30, 30),
                Spike(620, 210, 30, 30),
            ],
            doors=[
                Door(50, self.ground_y - 70, 50, 70, "entrance"),
                Door(800, 170, 50, 70, "exit"),
            ],
            player_spawn=(100, self.ground_y - 70),
            bg_path="assets/images/backgrounds/bg_2.png"
        )

        # ---------------- LEVEL 2 ----------------
        level2 = Level(
            platforms=[
                Platform(100, 650, 250, 20),
                Platform(400, 580, 200, 20),
                Platform(650, 500, 180, 20),
            ],
            spikes=[
                Spike(420, 650, 30, 30),
                Spike(450, 650, 30, 30),
            ],
            doors=[
                Door(650, 430, 50, 70, "exit"),
            ],
            player_spawn=(120, 550),
            bg_path="assets/images/backgrounds/bg_2.png"
        )

        self.level_manager.add_level(1, level1)
        self.level_manager.add_level(2, level2)

        self.current_level = self.level_manager.load(1)

        # ================= PLAYER =================
        self.player = Player(*self.current_level.player_spawn, 40, 40)

        # ================= PING =================
        self.ping = PingSystem((WIDTH, HEIGHT))

        # ================= MASK =================
        self.fade_speed = 255 / 18
        self.mask_closing = False
        self.mask_timer = 0
        self.MASK_DELAY = 30

        # ================= ASSETS =================
        self.vignette = pygame.image.load("assets/images/effects/Vignette.png").convert_alpha()
        self.sound = pygame.mixer.Sound("assets/sounds/Finger_snap.mp3")

        # ================= MENU =================
        self.font_title = pygame.font.SysFont("arial", 60)
        self.font_btn = pygame.font.SysFont("arial", 35)

        self.start_btn = pygame.Rect(WIDTH//2 - 120, HEIGHT//2, 240, 60)
        self.quit_btn = pygame.Rect(WIDTH//2 - 120, HEIGHT//2 + 80, 240, 60)

    # =========================================================
    #                      MENU SCREEN
    # =========================================================
    def draw_menu(self):
        self.screen.fill((10, 10, 20))
        mouse_pos = pygame.mouse.get_pos()

        # Title
        title = self.font_title.render("Resonight", True, (255, 255, 255))
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))

        # START BUTTON
        if self.start_btn.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, (200, 200, 200), self.start_btn)
            text_color = (0, 0, 0)
        else:
            pygame.draw.rect(self.screen, (100, 100, 100), self.start_btn)
            text_color = (255, 255, 255)

        start_text = self.font_btn.render("START", True, text_color)
        self.screen.blit(start_text, (
            self.start_btn.centerx - start_text.get_width() // 2,
            self.start_btn.centery - start_text.get_height() // 2
        ))

        # QUIT BUTTON
        if self.quit_btn.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, (200, 100, 100), self.quit_btn)
            text_color = (0, 0, 0)
        else:
            pygame.draw.rect(self.screen, (120, 50, 50), self.quit_btn)
            text_color = (255, 255, 255)

        quit_text = self.font_btn.render("QUIT", True, text_color)
        self.screen.blit(quit_text, (
            self.quit_btn.centerx - quit_text.get_width() // 2,
            self.quit_btn.centery - quit_text.get_height() // 2
        ))

    # =========================================================
    #                      EVENTS
    # =========================================================
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if self.state == self.MENU:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.state = self.LEVEL
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_btn.collidepoint(event.pos):
                        self.state = self.LEVEL
                    if self.quit_btn.collidepoint(event.pos):
                        self.running = False

            elif self.state == self.LEVEL:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        self.sound.play()
                        self.ping.trigger(self.player.rect.center)
                        self.mask_closing = False
                        self.mask_timer = 0

    # =========================================================
    #                  REVEAL SYSTEM
    # =========================================================
    def update_reveal(self):
        for p in self.current_level.platforms:
            if self.ping.active and self.ping.circle_rect_collision(self.ping.origin, self.ping.radius, p.rect):
                p.visible_timer = 10

            if p.visible_timer > 0:
                p.visible_timer -= 1
                p.alpha = min(255, p.alpha + self.fade_speed)
            else:
                p.alpha = max(0, p.alpha - self.fade_speed)

        for s in self.current_level.spikes:
            if self.ping.active and self.ping.circle_rect_collision(self.ping.origin, self.ping.radius, s.rect):
                s.visible_timer = 10

            if s.visible_timer > 0:
                s.visible_timer -= 1
                s.alpha = min(255, s.alpha + self.fade_speed)
            else:
                s.alpha = max(0, s.alpha - self.fade_speed)
        
        for d in self.current_level.doors:
            if self.ping.active and self.ping.circle_rect_collision(self.ping.origin, self.ping.radius, d.rect):
                d.visible_timer = 10

            if d.visible_timer > 0:
                d.visible_timer -= 1
                d.alpha = min(255, d.alpha + self.fade_speed)
            else:
                d.alpha = max(0, d.alpha - self.fade_speed)

    # =========================================================
    #                    COLLISIONS
    # =========================================================
    def check_collisions(self):
        for s in self.current_level.spikes:
            if self.player.rect.colliderect(s.rect):
                self.state = self.GAME_OVER
        
        for d in self.current_level.doors:
            if d.doorType == "exit" and self.player.rect.colliderect(d.rect):
                next_level = self.level_manager.current_level + 1

                if self.level_manager.get_level(next_level):
                    self.current_level = self.level_manager.load(next_level)
                    self.player = Player(*self.current_level.player_spawn)
                else:
                    self.running = False

        if self.player.rect.x >= WIDTH - self.player.rect.width:
            self.player.rect.x = WIDTH - self.player.rect.width
        
        if self.player.rect.x <= 0:
            self.player.rect.x = 0

    # =========================================================
    #                    MASK SYSTEM
    # =========================================================
    def apply_mask(self):
        if self.ping.radius <= 0:
            self.screen.fill(BLACK)
            return

        dark = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        dark.fill((0, 0, 0, 255))

        size = int(self.ping.radius * 2.3)
        vignette = pygame.transform.smoothscale(self.vignette, (size, size))
        rect = vignette.get_rect(center=self.ping.origin)

        dark.blit(vignette, rect, special_flags=pygame.BLEND_RGBA_MULT)
        self.screen.blit(dark, (0, 0))

    def update_mask(self):
        if not self.ping.active:
            self.mask_closing = True

        if self.mask_closing:
            self.mask_timer += 1
            if self.mask_timer >= self.MASK_DELAY:
                self.mask_closing = False
                self.ping.radius = 0

    # =========================================================
    #                   LEVEL LOGIC & DRAW
    # =========================================================
    def update(self):
        keys = pygame.key.get_pressed()
        self.player.update(keys, self.current_level.platforms, self.ground_y)
        self.ping.update()
        self.check_collisions()
        self.update_reveal()
        self.update_mask()
    
    def draw(self):
        self.screen.fill(BLACK)
        self.current_level.draw(self.screen)
        self.ping.draw(self.screen)
        self.apply_mask()
        self.player.draw(self.screen)

    # =========================================================
    #                      MAIN LOOP
    # =========================================================
    def main(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()

            if self.state == self.MENU:
                self.draw_menu()
            elif self.state == self.LEVEL:
                self.update()
                self.draw()
            elif self.state == self.GAME_OVER:
                self.screen.fill((20, 0, 0))

            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    Game().main()