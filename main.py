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
from levels.screens import Screens

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Resonight")
        self.clock = pygame.time.Clock()
        self.running = True

        self.dark_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.ground_y = HEIGHT - 40

        self.MENU = "menu"
        self.LEVEL = "level"
        self.GAME_OVER = "game_over"
        self.state = self.MENU
        self.WIN = "win"
        self.timeLeft = 30.0
        self.totalPings = 0
        self.deathReason = ""
        self.win_level = 0
        self.win_time = 0
        self.win_pings = 0

        self.hasNextLevel = True

        # ================= TRANSITION =================
        self.transitioning = False
        self.transition_alpha = 0
        self.transition_duration = 0.5  # seconds
        self.transition_speed = 255 / (FPS * self.transition_duration)
        self.target_state = None
        self.fade_out = False

        self.level_manager = LevelManager()

        # ---------------- LEVEL 1 ----------------
        level1 = Level(
            platforms=[
                Platform(100, 650, 250, 20),
                Platform(100, 580, 200, 20),
                Platform(650, 500, 180, 20),
                
            ],
            spikes=[
                Spike(420, 650, 30, 30),
                Spike(450, 650, 30, 30),
            ],
            doors=[
                Door(50, self.ground_y - 80, 60, 80, "entrance"),
                Door(650, 430, 50, 70, "exit"),
            ],
            player_spawn=(120, 550),
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
                Door(50, self.ground_y - 80, 60, 80, "entrance"),
                Door(650, 430, 50, 70, "exit"),
            ],
            player_spawn=(120, 550),
            bg_path="assets/images/backgrounds/bg_2.png"
        )
        # ---------------- LEVEL 3 ----------------
        level3 = Level(
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
                Door(50, self.ground_y - 80, 60, 80, "entrance"),
                Door(650, 430, 50, 70, "exit"),
            ],
            player_spawn=(120, 550),
            bg_path="assets/images/backgrounds/bg_2.png"
        )
        # ---------------- LEVEL 4 ----------------
        level4 = Level(
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
                Door(50, self.ground_y - 80, 60, 80, "entrance"),
                Door(650, 430, 50, 70, "exit"),
            ],
            player_spawn=(120, 550),
            bg_path="assets/images/backgrounds/bg_2.png"
        )
        # ---------------- LEVEL 5 ----------------
        level5 = Level(
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
                Door(50, self.ground_y - 80, 60, 80, "entrance"),
                Door(800, 160, 60, 80, "exit"),
            ],
            player_spawn=(100, self.ground_y - 70),
            bg_path="assets/images/backgrounds/bg_2.png"
        )
        
        self.level_manager.add_level(1, level1)
        self.level_manager.add_level(2, level2)
        self.level_manager.add_level(3, level3)
        self.level_manager.add_level(4, level4)
        self.level_manager.add_level(5, level5)

        self.current_level_id = 1
        self.current_level = self.level_manager.load(self.current_level_id)

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
        self.mouse_pos = pygame.mouse.get_pos()

        self.nextlevel = Screens(self.screen, self.mouse_pos, self.level_manager.current_level, self.timeLeft, self.totalPings)

    def start_transition(self, new_state):
        if not self.transitioning:
            self.transitioning = True
            self.target_state = new_state
            self.transition_alpha = 0
            self.fade_out = True

    # =========================================================
    #                   LOAD TO NEXT LEVEL
    # =========================================================
    def load_next_level(self):
        next_id = self.current_level_id + 1
        self.timeLeft = 30.0
        self.totalPings = 0

        if self.level_manager.has_level(next_id):
            self.current_level_id = next_id

            self.current_level = self.level_manager.load(next_id)
            self.player = Player(*self.current_level.player_spawn, 40, 40)

            self.ping.reset()
            self.start_transition(self.LEVEL)
        else:
            self.current_level_id = 1
            self.start_transition(self.MENU)

    

    # =========================================================
    #                      EVENTS
    # =========================================================
    def handle_events(self):
        if self.transitioning:
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if self.state == self.MENU:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.start_transition(self.LEVEL)
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.nextlevel.start_btn.collidepoint(event.pos):
                        self.current_level_id = 1
                        self.current_level = self.level_manager.load(1)
                        self.player = Player(*self.current_level.player_spawn, 40, 40)

                        self.ping.reset()
                        self.start_transition(self.LEVEL)

                    if self.nextlevel.quit_btn.collidepoint(event.pos):
                        self.running = False

            elif self.state == self.WIN:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.nextlevel.next_level_btn.collidepoint(event.pos):
                        if self.hasNextLevel:
                            self.load_next_level()
                        else:
                            # FINAL → RESTART GAME
                            self.current_level_id = 1
                            self.current_level = self.level_manager.load(1)
                            self.player = Player(*self.current_level.player_spawn, 40, 40)

                            self.timeLeft = 30.0
                            self.totalPings = 0
                            self.ping.reset()

                            self.start_transition(self.LEVEL)

                    if self.nextlevel.back_btn.collidepoint(event.pos):
                        self.start_transition(self.MENU)

            elif self.state == self.GAME_OVER:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.nextlevel.again_btn.collidepoint(event.pos):
                            self.current_level = self.level_manager.load(self.level_manager.current_level)
                            self.player = Player(*self.current_level.player_spawn, 40, 40)

                            self.timeLeft = 30.0
                            self.totalPings = 0
                            self.deathReason = ""

                            self.ping.reset()

                            self.start_transition(self.LEVEL)

                    if self.nextlevel.back_btn.collidepoint(event.pos):
                        self.start_transition(self.MENU)

            elif self.state == self.LEVEL:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        self.sound.play()
                        self.ping.trigger(self.player.rect.center)

                        self.totalPings += 1

                        self.timeLeft -= 3
                        if self.timeLeft < 0:
                            self.timeLeft = 0

                        self.mask_closing = False
                        self.mask_timer = 0

    # =========================================================
    #                  REVEAL SYSTEM
    # =========================================================
    def update_reveal(self):
        for obj in self.current_level.get_all_objects():
            # if self.ping.active and self.ping.circle_rect_collision(self.ping.origin, self.ping.radius, obj.rect):
            if True:

                obj.visible_timer = 10

            if obj.visible_timer > 0:
                obj.visible_timer -= 1
                obj.alpha = min(255, obj.alpha + self.fade_speed)
            else:
                obj.alpha = max(0, obj.alpha - self.fade_speed)
          
    # =========================================================
    #                    COLLISIONS
    # =========================================================
    def check_collisions(self):
        if self.transitioning:
            return
        
        for s in self.current_level.spikes:
            if self.player.rect.colliderect(s.rect):
                self.ping.reset()
                self.deathReason = "spike"
                self.start_transition(self.GAME_OVER)
        
        for d in self.current_level.doors:
            if d.doorType == "exit" and self.player.rect.colliderect(d.rect):
                self.ping.reset()
                self.win_level = self.current_level_id
                self.win_time = self.timeLeft
                self.win_pings = self.totalPings

                next_id = self.current_level_id + 1
                self.hasNextLevel = self.level_manager.has_level(next_id)
                self.start_transition(self.WIN)

        self.player.rect.x = max(0, min(self.player.rect.x, WIDTH - self.player.rect.width))

    # =========================================================
    #                    MASK SYSTEM
    # =========================================================
    def apply_mask(self):
        if self.ping.radius <= 0:
            self.screen.fill(BLACK)
            return

        self.dark_surface.fill((0, 0, 0, 255))

        size = int(self.ping.radius * 2.3)
        vignette = pygame.transform.smoothscale(self.vignette, (size, size))
        rect = vignette.get_rect(center=self.ping.origin)

        self.dark_surface.blit(vignette, rect, special_flags=pygame.BLEND_RGBA_MULT)
        self.screen.blit(self.dark_surface, (0, 0))

    def update_mask(self):
        if not self.ping.active:
            self.mask_closing = True

        if self.mask_closing:
            self.mask_timer += 1
            if self.mask_timer >= self.MASK_DELAY:
                self.mask_closing = False
                self.ping.radius = 0

    def update_transition(self):
        if self.transitioning:
            if self.fade_out:
                self.transition_alpha += self.transition_speed
                if self.transition_alpha >= 255:
                    self.state = self.target_state
                    self.fade_out = False
            else:
                self.transition_alpha -= self.transition_speed
                if self.transition_alpha <= 0:
                    self.transitioning = False
                    self.transition_alpha = 0

    def draw_ui(self):
        font = pygame.font.SysFont("arial", 24)

        # LEFT: LEVEL
        level_text = font.render(f"Level: {self.current_level_id}", True, (255, 255, 255))
        self.screen.blit(level_text, (10, 10))

        # CENTER: TIMER (0.00 format)
        timer_text = font.render(f"{self.timeLeft:0.2f}", True, (255, 255, 255))
        self.screen.blit(timer_text, (WIDTH//2 - timer_text.get_width()//2, 10))

        # RIGHT: PINGS
        ping_text = font.render(f"Pings: {self.totalPings}", True, (255, 255, 255))
        self.screen.blit(ping_text, (WIDTH - ping_text.get_width() - 10, 10))
    # =========================================================
    #                   LEVEL LOGIC & DRAW
    # =========================================================
    def update(self):
        dt = self.clock.get_time() / 1000  # seconds
        # countdown
        self.timeLeft -= dt

        # if time runs out → GAME OVER
        if self.timeLeft <= 0:
            self.timeLeft = 0
            self.deathReason = "time"
            self.start_transition(self.GAME_OVER)
            return
        
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
        # self.apply_mask()
        self.player.draw(self.screen)
        self.draw_ui() 

    # =========================================================
    #                      MAIN LOOP
    # =========================================================
    def main(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update_transition()

            if self.state == self.MENU:
                self.nextlevel.draw_menu()

            elif self.state == self.LEVEL:
                if not self.transitioning:
                    self.update()
                self.draw()

            elif self.state == self.GAME_OVER:
                self.screen.fill((20, 0, 0))
                self.nextlevel.currentlevel = self.deathReason
                self.nextlevel.draw_game_over()

            elif self.state == self.WIN:
                self.nextlevel.currentlevel = self.win_level
                self.nextlevel.timeLeft = self.win_time
                self.nextlevel.totalPings = self.win_pings
                self.nextlevel.hasNextLevel = self.hasNextLevel
                self.nextlevel.isFinalLevel = not self.hasNextLevel

                self.nextlevel.draw_win()

            if self.transitioning:
                transition_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                transition_surface.fill((0, 0, 0, int(self.transition_alpha)))
                self.screen.blit(transition_surface, (0, 0))

            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    Game().main()