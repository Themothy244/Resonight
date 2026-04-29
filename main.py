import pygame
import sys

pygame.init()
pygame.mixer.init()

from settings import *
from levels.levels_data import load_levels
from entities.player import Player
from systems.ping_system import PingSystem
from systems.mask_system import MaskSystem
from systems.timer_system import TimerSystem
from levels.level_manager import LevelManager
from levels.screens import Screens
from levels.hud import HUD
from entities.buff import Buff

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

        self.run_total_time = 0
        self.run_total_pings = 0

        self.final_time = 0
        self.final_pings = 0
        self.final_score = 0
        self.final_rank = "C"

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

        levels = load_levels(self)

        for level_id, level in levels.items():
            self.level_manager.add_level(level_id, level)

        self.current_level_id = 1
        self.current_level = self.level_manager.load(self.current_level_id)
        ground_rect = pygame.Rect(0, self.ground_y, WIDTH, 40)
        self.buff =  Buff.try_spawn_buff(WIDTH, HEIGHT, self.current_level.platforms, self.current_level.spikes, ground_rect)
        
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
        self.nextlevel = Screens(self.screen, self.current_level_id, self.timer.time_left, self.totalPings, self.lives)

    # =========================================================
    #                     STATE CONTROL
    # =========================================================
    def reset_player(self):
        self.player = Player(*self.current_level.player_spawn, 40, 40)
        self.timer.reset()
        self.totalPings = 0
        self.ping.reset()

    def reset_game(self):
        self.lives = 3
        self.current_level_id = 1
        self.current_level = self.level_manager.load(1)
        self.reset_player()

        self.run_total_time = 0
        self.run_total_pings = 0
        self.final_score = 0
        self.final_rank = "C"
        
    def handle_death(self, reason):
        self.lives -= 1
        self.deathReason = reason

        if self.lives <= 0:
            self.deathReason = "lives"
            self.buff = None

        self.start_transition(self.GAME_OVER)

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
            ground_rect = pygame.Rect(0, self.ground_y, WIDTH, 40)
            self.buff = Buff.try_spawn_buff(WIDTH, HEIGHT, self.current_level.platforms, self.current_level.spikes, ground_rect)
            self.start_transition(self.LEVEL)
        else:
            self.current_level_id = 1
            self.start_transition(self.MENU)

    # =========================================================
    #                      EVENTS
    # =========================================================
    def handle_events(self):
        if self.transitioning:
            pygame.event.clear()
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
                            self.reset_game()
                            self.start_transition(self.LEVEL)

                    if self.nextlevel.back_btn.collidepoint(event.pos):
                        self.reset_game()
                        self.start_transition(self.MENU)

            # ================= GAME OVER =================
            elif self.state == self.GAME_OVER:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.nextlevel.again_btn.collidepoint(event.pos):
                            self.current_level = self.level_manager.load(self.current_level_id)
                            self.reset_player()
                            self.start_transition(self.LEVEL)

                            if self.lives <= 0:
                                self.reset_game()

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
            #if self.ping.active and self.ping.circle_rect_collision(self.ping.origin, self.ping.radius, obj.rect):
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
                self.handle_death("spike")
                self.timer.stop_tick()
                self.start_transition(self.GAME_OVER)

                if self.lives <= 0:
                    self.deathReason = "lives"
                break
        
        for d in self.current_level.doors:
            if d.doorType == "exit" and self.player.rect.colliderect(d.rect):
                self.ping.reset()
                self.timer.stop_tick()
                self.win_level = self.current_level_id
                self.win_time = self.timer.time_left
                self.win_pings = self.totalPings
                self.win_lives = self.lives
                self.run_total_time += self.timer.time_left
                self.run_total_pings += self.totalPings

                next_id = self.current_level_id + 1
                self.hasNextLevel = self.level_manager.has_level(next_id)
                if not self.hasNextLevel:
                    self.final_time = self.run_total_time
                    self.final_pings = self.run_total_pings

                    self.final_score = int((self.final_time * 10) + (self.lives * 100) - (self.final_pings * 5))

                    if self.final_score >= 2000:
                        self.final_rank = "S"
                    elif self.final_score >= 1500:
                        self.final_rank = "A"
                    elif self.final_score >= 1000:
                        self.final_rank = "B"
                    else:
                        self.final_rank = "C"
                self.start_transition(self.WIN)

        if self.buff and self.player.rect.colliderect(self.buff.rect):
            self.buff.apply_effect(self)
            self.buff = None

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
            self.handle_death("time")

            if self.lives <= 0:
                self.reset_game()
                self.deathReason = "lives"

            self.start_transition(self.GAME_OVER)
        
        for platform in self.current_level.platforms:
            platform.update()
        keys = pygame.key.get_pressed()
        self.player.update(keys, self.current_level.platforms, self.ground_y)
        self.ping.update()
        self.check_collisions()
        self.update_reveal()
        self.mask.update(self.ping)
    
    def draw(self):
        self.screen.fill(BLACK)
        self.current_level.draw(self.screen)
        if self.buff:
            self.buff.draw(self.screen)
        self.ping.draw(self.screen)
        #self.mask.draw(self.screen, self.ping)
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
                self.nextlevel.lives = self.lives
                self.nextlevel.draw_game_over(mouse_pos)

            elif self.state == self.WIN:
                self.nextlevel.currentlevel = self.win_level
                self.nextlevel.timeLeft = self.win_time
                self.nextlevel.totalPings = self.win_pings
                self.nextlevel.lives = self.win_lives
                self.nextlevel.hasNextLevel = self.hasNextLevel
                self.nextlevel.isFinalLevel = not self.hasNextLevel

                self.nextlevel.final_time = self.final_time
                self.nextlevel.final_pings = self.final_pings
                self.nextlevel.final_score = self.final_score
                self.nextlevel.final_rank = self.final_rank

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