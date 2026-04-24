import pygame
import sys

pygame.init()
pygame.mixer.init()

from settings import *
from entities.platform import Platform
from entities.spike import Spike
from entities.door import Door
from entities.player import Player
from systems.ping_system import PingSystem
from systems.mask_system import MaskSystem
from systems.timer_system import TimerSystem
from levels.level import Level
from levels.level_manager import LevelManager
from levels.screens import Screens
from levels.hud import HUD

class Game:
    def __init__(self):
        # ================= CORE =================
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Resonight")
        self.clock = pygame.time.Clock()
        self.running = True

        # ================= STATE =================
        self.MENU = "menu"
        self.LEVEL = "level"
        self.GAME_OVER = "game_over"
        self.WIN = "win"
        self.state = self.MENU
        self.lives = 3

        # ================= WORLD =================
        self.ground_y = HEIGHT - 40

        # ================= GAME DATA / STATS =================
        self.totalPings = 0
        self.deathReason = ""
        self.win_level = 0
        self.win_time = 0
        self.win_pings = 0
        self.win_lives = 0

        # ================= INPUT & FLAGS =================
        self.hasNextLevel = True

        # ================= TRANSITIONS & EFFECTS =================
        self.transitioning = False
        self.transition_alpha = 0
        self.transition_duration = 0.5  # seconds
        self.transition_speed = 255 / (FPS * self.transition_duration)
        self.fade_speed = 255 / 18
        self.target_state = None
        self.fade_out = False

        self.level_manager = LevelManager()

        # ---------------- LEVEL 1 ----------------
        level1 = Level(
            platforms=[
                Platform(220, 550, 390, 20),
                Platform(550, 420, 530, 20),
                
            ],
            spikes=[
                Spike(440, 520, 30, 30),
                Spike(470, 520, 30, 30),
                Spike(500, 520, 30, 30),

            ],
            doors=[
                Door(50, self.ground_y - 80, 60, 80, "entrance"),
                Door(830, 350, 54, 70, "exit"),
            ],
            player_spawn=(120, 550),
            bg_path="assets/images/backgrounds/bg_2.png"
        )

        # ---------------- LEVEL 2 ----------------
        level2 = Level(
            platforms=[
                Platform(300, 600, 140, 20),
                Platform(500, 550, 140, 20),
                Platform(700, 480, 140, 20),
                Platform(850, 420, 140, 20),
            ],
            spikes=[
                Spike(240, 650, 30, 30),
                Spike(700, 650, 30, 30),
                Spike(730, 650, 30, 30),
                Spike(700, 450, 30, 30),
            ],
            doors=[
                Door(50, self.ground_y - 80, 60, 80, "entrance"),
                Door(900, 350, 50, 70, "exit"),
            ],
            player_spawn=(120, 550),
            bg_path="assets/images/backgrounds/bg_2.png"
        )
        # ---------------- LEVEL 3 ----------------
        level3 = Level(
            platforms=[
                Platform(220, 540, 180, 20),
                Platform(600, 540, 165, 20),
                Platform(450, 400, 150, 20),
            ],
            spikes=[
                Spike(210, 650, 30, 30),
                Spike(240, 650, 30, 30),
                Spike(270, 650, 30, 30),
                Spike(300, 650, 30, 30),
                Spike(330, 650, 30, 30),
                Spike(360, 650, 30, 30),
                Spike(390, 650, 30, 30),
                Spike(420, 650, 30, 30),
                Spike(450, 650, 30, 30),
                Spike(540, 371, 30, 30),
                Spike(480, 650, 30, 30),
                Spike(510, 650, 30, 30),
                Spike(540, 650, 30, 30),
                Spike(570, 650, 30, 30),
                Spike(600, 650, 30, 30),
                Spike(630, 650, 30, 30),
                Spike(660, 650, 30, 30),
                Spike(690, 650, 30, 30),
                Spike(720, 650, 30, 30),
                Spike(750, 650, 30, 30),
            ],
            doors=[
                Door(50, self.ground_y - 80, 60, 80, "entrance"),
                Door(850, 608, 50, 70, "exit"),
            ],
            player_spawn=(120, 550),
            bg_path="assets/images/backgrounds/bg_2.png"
        )
        # ---------------- LEVEL 4 ----------------
        level4 = Level(
            platforms=[
                Platform(0, 360, 200, 20),
                Platform(250, 480, 350, 20),
                Platform(680, 560, 150, 20),
                Platform(360, 250, 630, 20),
            ],
            spikes=[
                Spike(560, 650, 30, 30),
                Spike(530, 650, 30, 30),
                Spike(500, 650, 30, 30),
                Spike(680, 530, 30, 30),
                Spike(440, 450, 30, 30),
                Spike(410, 450, 30, 30),
                Spike(380, 450, 30, 30),
                Spike(630, 220, 30, 30),
                Spike(600, 220, 30, 30),
                Spike(570, 220, 30, 30),
            ],
            doors=[
                Door(50, self.ground_y - 80, 60, 80, "entrance"),
                Door(800, 180, 50, 70, "exit"),
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
        
        # ================= ASSETS =================
        self.vignette = pygame.image.load("assets/images/effects/Vignette.png").convert_alpha()
        self.finger_snap = pygame.mixer.Sound("assets/sounds/Finger_snap.mp3")
        self.clock_tick = pygame.mixer.Sound("assets/sounds/clock_tick.mp3")

        # ================= GAME SYSTEMS =================
        self.hud = HUD()
        self.player = Player(*self.current_level.player_spawn, 40, 40)
        self.ping = PingSystem((WIDTH, HEIGHT))
        self.mask = MaskSystem((WIDTH, HEIGHT), self.vignette)
        self.timer = TimerSystem(30.0, self.clock_tick)
        self.nextlevel = Screens(self.screen, self.level_manager.current_level, self.timer.time_left, self.totalPings, self.lives)

    # =========================================================
    #                     STATE CONTROL
    # =========================================================
    def reset_player(self):
        self.player = Player(*self.current_level.player_spawn, 40, 40)
        self.timer.reset()
        self.totalPings = 0
        self.ping.reset()

    def start_transition(self, new_state):
        if not self.transitioning:
            self.transitioning = True
            self.target_state = new_state
            self.transition_alpha = 0
            self.fade_out = True

    def load_next_level(self):
        next_id = self.current_level_id + 1
        self.reset_player()

        if self.level_manager.has_level(next_id):
            self.current_level_id = next_id

            self.current_level = self.level_manager.load(next_id)
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
            # ================= MENU / START =================
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
                        self.ping.reset()
                        self.start_transition(self.LEVEL)

                    if self.nextlevel.quit_btn.collidepoint(event.pos):
                        self.running = False

            # ================= WIN =================
            elif self.state == self.WIN:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.nextlevel.next_level_btn.collidepoint(event.pos):
                        if self.hasNextLevel:
                            self.load_next_level()
                        else:
                            # FINAL → RESTART GAME
                            self.current_level_id = 1
                            self.current_level = self.level_manager.load(1)
                            self.reset_player()

                            self.start_transition(self.LEVEL)

                    if self.nextlevel.back_btn.collidepoint(event.pos):
                        self.start_transition(self.MENU)

            # ================= GAME OVER =================
            elif self.state == self.GAME_OVER:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.nextlevel.again_btn.collidepoint(event.pos):
                            self.current_level = self.level_manager.load(self.level_manager.current_level)
                            self.reset_player()
                            self.start_transition(self.LEVEL)

                    if self.nextlevel.back_btn.collidepoint(event.pos):
                            self.reset_player()
                            self.start_transition(self.MENU)

            # ================= LEVEL ================= 
            elif self.state == self.LEVEL:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        self.finger_snap.play()
                        self.ping.trigger(self.player.rect.center)
                        self.totalPings += 1
                        self.timer.penalize(3)
                        self.mask.trigger_open()

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
                self.lives -= 1
                self.timer.stop_tick()
                self.deathReason = "spike"
                self.start_transition(self.GAME_OVER)

                if self.lives <= 0:
                    self.lives = 3
                    self.current_level_id = 1
                    self.current_level = self.level_manager.load(1)
                    self.deathReason = "lives"
                    self.player = Player(*self.current_level.player_spawn, 40, 40)
                break
        
        for d in self.current_level.doors:
            if d.doorType == "exit" and self.player.rect.colliderect(d.rect):
                self.ping.reset()
                self.timer.stop_tick()
                self.win_level = self.current_level_id
                self.win_time = self.timer.time_left
                self.win_pings = self.totalPings
                self.win_lives = self.lives

                next_id = self.current_level_id + 1
                self.hasNextLevel = self.level_manager.has_level(next_id)
                self.start_transition(self.WIN)

        self.player.rect.x = max(0, min(self.player.rect.x, WIDTH - self.player.rect.width))

    # =========================================================
    #                STATE TRANSITION EFFECTS
    # =========================================================
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

    # =========================================================
    #                   LEVEL LOGIC & DRAW
    # =========================================================
    def update(self):
        dt = self.clock.get_time() / 1000

        if self.timer.update(dt):
            self.lives -= 1
            self.deathReason = "time"
            

            if self.lives <= 0:
                self.lives = 3
                self.current_level_id = 1
                self.current_level = self.level_manager.load(1)
                self.deathReason = "lives"
                self.player = Player(*self.current_level.player_spawn, 40, 40)

            self.start_transition(self.GAME_OVER)
        
        keys = pygame.key.get_pressed()
        self.player.update(keys, self.current_level.platforms, self.ground_y)
        self.ping.update()
        self.check_collisions()
        self.update_reveal()
        self.mask.update(self.ping)
    
    def draw(self):
        self.screen.fill(BLACK)
        self.current_level.draw(self.screen)
        self.ping.draw(self.screen)
        # self.mask.draw(self.screen, self.ping)
        self.player.draw(self.screen)
        self.hud.draw(self.screen, self.current_level_id, self.timer.time_left, self.totalPings, self.lives)

    # =========================================================
    #                      MAIN LOOP
    # =========================================================
    def main(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update_transition()
            mouse_pos = pygame.mouse.get_pos()

            if self.state == self.MENU:
                self.nextlevel.draw_menu(mouse_pos)

            elif self.state == self.LEVEL:
                if not self.transitioning:
                    self.update()
                self.draw()

            elif self.state == self.GAME_OVER:
                self.screen.fill((20, 0, 0))
                self.nextlevel.currentlevel = self.deathReason
                self.nextlevel.draw_game_over(mouse_pos)

            elif self.state == self.WIN:
                self.nextlevel.currentlevel = self.win_level
                self.nextlevel.timeLeft = self.win_time
                self.nextlevel.totalPings = self.win_pings
                self.nextlevel.lives = self.win_lives
                self.nextlevel.hasNextLevel = self.hasNextLevel
                self.nextlevel.isFinalLevel = not self.hasNextLevel

                self.nextlevel.draw_win(mouse_pos)

            if self.transitioning:
                transition_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                transition_surface.fill((0, 0, 0, int(self.transition_alpha)))
                self.screen.blit(transition_surface, (0, 0))

            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    Game().main()