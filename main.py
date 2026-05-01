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
        self.game_over_final = False
        self.hasNextLevel = True

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

        # ================= TRANSITIONS & EFFECTS =================
        self.transitioning = False
        self.transition_alpha = 0
        self.transition_duration = 0.5 
        self.transition_speed = 255 / (FPS * self.transition_duration)
        self.fade_speed = 255 / 18
        self.target_state = None
        self.fade_out = False

        # ================= ASSETS =================
        self.vignette = pygame.image.load("assets/images/effects/Vignette.png").convert_alpha()
        self.finger_snap = pygame.mixer.Sound("assets/sounds/Finger_snap.mp3")
        self.bat_sfx = pygame.mixer.Sound("assets/sounds/bat_sfx.wav")
        self.bat_sfx.set_volume(0.5)
        self.clock_tick = pygame.mixer.Sound("assets/sounds/clock_tick.mp3")
        self.game_over_sound = pygame.mixer.Sound("assets/sounds/game_over_sfx.wav")
        self.game_over_sound.set_volume(0.4)
        self.win_sound = pygame.mixer.Sound("assets/sounds/win_sfx.wav")
        self.completed_sound = pygame.mixer.Sound("assets/sounds/completed_sfx.wav")
        self.buff_sound = pygame.mixer.Sound("assets/sounds/pickup_sound.wav")
        pygame.mixer.music.load("assets/sounds/bg_music.ogg")
        pygame.mixer.music.play(-1)
        
        # ================= LEVELS =================
        self.level_manager = LevelManager()

        levels = load_levels(self)
        for level_id, level in levels.items():
            self.level_manager.add_level(level_id, level)

        self.current_level_id = 1
        self.current_level = self.level_manager.load(self.current_level_id)

        # ================= GAME SYSTEMS =================
        self.hud = HUD()
        self.player = Player(*self.current_level.player_spawn)
        self.ping = PingSystem((WIDTH, HEIGHT), 280)
        self.mask = MaskSystem((WIDTH, HEIGHT), self.vignette)
        self.timer = TimerSystem(30.0, self.clock_tick)
        self.nextlevel = Screens(self.screen, self.current_level_id, self.timer.time_left, self.totalPings, self.lives)
        
        ground_rect = pygame.Rect(0, self.ground_y, WIDTH, 40)
        self.buff =  Buff.try_spawn_buff(self.current_level.platforms, ground_rect, self.lives)

    # =========================================================
    #                     STATE CONTROL
    # =========================================================
    def reset_player(self):
        self.player = Player(*self.current_level.player_spawn)
        self.timer.reset()
        self.totalPings = 0
        self.ping.reset()
        for bat in self.current_level.bats:
            bat.reset()

        ground_rect = pygame.Rect(0, self.ground_y, WIDTH, 40)
        self.buff =  Buff.try_spawn_buff(self.current_level.platforms, ground_rect, self.lives)

    def reset_game(self):
        self.lives = 3
        self.current_level_id = 1
        self.current_level = self.level_manager.load(1)

        self.reset_player()

        self.run_total_time = 0
        self.run_total_pings = 0
        self.final_score = 0
        self.final_rank = "C"
        self.game_over_final = False

        ground_rect = pygame.Rect(0, self.ground_y, WIDTH, 40)
        self.buff =  Buff.try_spawn_buff(self.current_level.platforms, ground_rect, self.lives)
        
    def handle_death(self, reason):
        if self.player.forced_state:
            return
    
        self.lives -= 1

        self.timer.stop_tick()
        self.ping.reset()
        for bat in self.current_level.bats:
            bat.reset()
        
        self.player.play_death(reason)

        if self.lives <= 0:
            self.deathReason = "lives"
            self.game_over_final = True
            self.buff = None
        else:
            self.deathReason = reason

    def start_transition(self, new_state):
        if self.transitioning:
            return
        
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
            self.buff = Buff.try_spawn_buff(self.current_level.platforms, ground_rect, self.lives)
            self.start_transition(self.LEVEL)
        else:
            self.current_level_id = 1
            self.start_transition(self.MENU)

    def get_active_pings(self):
        pings = []

        if self.ping.active:
            pings.append(self.ping)

        for bat in self.current_level.bats:
            if bat.ping.active:
                pings.append(bat.ping)

        return pings
    
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

            # ================= KEY INPUT (GLOBAL LOGIC) =================
            if event.type == pygame.KEYDOWN:

                # ---------- MENU ----------
                if self.state == self.MENU:
                    if event.key == pygame.K_RETURN:
                        self.start_transition(self.LEVEL)

                    elif event.key == pygame.K_ESCAPE:
                        self.running = False

                # ---------- GAME OVER ----------
                elif self.state == self.GAME_OVER:
                    if event.key == pygame.K_RETURN:
                        self.current_level = self.level_manager.load(self.current_level_id)
                        self.reset_player()

                        self.player.forced_state = None
                        self.player.animation_finished = False

                        if self.game_over_final:
                            self.reset_game()
                            self.game_over_final = False

                        self.start_transition(self.LEVEL)

                    elif event.key == pygame.K_ESCAPE:
                        self.reset_game()
                        self.start_transition(self.MENU)

                # ---------- WIN ----------
                elif self.state == self.WIN:
                    if event.key == pygame.K_RETURN:
                        if self.hasNextLevel:
                            self.load_next_level()
                        else:
                            self.reset_game()
                            self.start_transition(self.LEVEL)

                    elif event.key == pygame.K_ESCAPE:
                        self.reset_game()
                        self.start_transition(self.MENU)

                # ---------- PING ---------- 
                elif self.state == self.LEVEL:
                    if event.key == pygame.K_e:
                        self.finger_snap.play()
                        self.ping.trigger(self.player.rect.center)
                        self.totalPings += 1
                        self.timer.penalize(2)

            # ================= MOUSE INPUT =================
            elif event.type == pygame.MOUSEBUTTONDOWN:

                if self.state == self.MENU:
                    if self.nextlevel.start_btn.collidepoint(event.pos):
                        self.current_level_id = 1
                        self.current_level = self.level_manager.load(1)
                        self.ping.reset()
                        for bat in self.current_level.bats:
                            bat.reset()
                        self.start_transition(self.LEVEL)

                    elif self.nextlevel.quit_btn.collidepoint(event.pos):
                        self.running = False

                elif self.state == self.GAME_OVER:
                    if self.nextlevel.again_btn.collidepoint(event.pos):
                        self.current_level = self.level_manager.load(self.current_level_id)
                        self.reset_player()

                        self.player.forced_state = None
                        self.player.animation_finished = False

                        if self.game_over_final:
                            self.reset_game()
                            self.game_over_final = False

                        self.start_transition(self.LEVEL)

                    elif self.nextlevel.back_btn.collidepoint(event.pos):
                        self.start_transition(self.MENU)
                        self.reset_game()

                elif self.state == self.WIN:
                    if self.nextlevel.next_level_btn.collidepoint(event.pos):
                        if self.hasNextLevel:
                            self.load_next_level()
                        else:
                            self.reset_game()
                            self.start_transition(self.LEVEL)

                    elif self.nextlevel.back_btn.collidepoint(event.pos):
                        self.reset_game()
                        self.start_transition(self.MENU)

    # =========================================================
    #                  REVEAL SYSTEM
    # =========================================================
    def update_reveal(self):
        pings = self.get_active_pings()

        # Trigger bats
        for bat in self.current_level.bats:
            if bat.triggered or bat.cooldown > 0 or bat.chain_delay > 0:
                continue

            for ping in pings:
                if ping.circle_rect_collision(ping.origin, ping.radius, bat.rect):
                    bat.trigger()
                    break

        # Reveal objects
        for obj in self.current_level.get_all_objects():
            visible = any(
                ping.circle_rect_collision(ping.origin, ping.radius, obj.rect)
                for ping in pings
            )

            if visible:
                obj.visible_timer = 10
                obj.alpha = min(255, obj.alpha + self.fade_speed)
            else:
                obj.alpha = max(0, obj.alpha - self.fade_speed)

    # =========================================================
    #                    COLLISIONS
    # =========================================================
    def check_collisions(self):
        if self.transitioning:
            return
        
        # ================= SPIKES =================
        for s in self.current_level.spikes:
            if self.player.hitbox.colliderect(s.rect):
                self.handle_death("spike")
                break
        
        # ================= EXIT DOOR =================
        for d in self.current_level.doors:
            if d.doorType == "exit" and self.player.hitbox.colliderect(d.rect):
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

        # ================= BUFF =================
        if self.buff and self.player.hitbox.colliderect(self.buff.rect):
            self.buff.apply_effect(self)
            self.buff_sound.play()
            self.buff = None

        # clamp
        self.player.hitbox.x = max(0, min(self.player.hitbox.x, WIDTH - self.player.hitbox.width))

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

                    if self.target_state == self.GAME_OVER:
                        self.game_over_sound.play()

                    elif self.target_state == self.WIN:
                        if self.hasNextLevel:
                            self.win_sound.play()
                        else:
                            self.completed_sound.play()
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
        keys = pygame.key.get_pressed()

        # PLAYER
        self.player.update(keys, self.current_level.platforms, self.ground_y)

        if self.player.forced_state:
            if self.player.animation_finished:
                self.start_transition(self.GAME_OVER)
            return

        # TIMER
        if self.timer.update(dt):
            self.handle_death("time")

        # WORLD
        for platform in self.current_level.platforms:
            platform.update()

        # SYSTEMS
        self.ping.update()
        self.check_collisions()
        self.update_reveal()

        active_pings = self.get_active_pings()
        self.mask.update(active_pings)

        for bat in self.current_level.bats:
            bat.update()

        if self.buff:
            self.buff.update()
    
    def draw(self):
        self.screen.fill(BLACK)
        self.current_level.draw(self.screen)

        if self.buff:
            self.buff.draw(self.screen)

        for bat in self.current_level.bats:
            if not bat.ping.active:
                bat.triggered = False
            bat.ping.draw(self.screen)

        self.ping.draw(self.screen)

        active_pings = self.get_active_pings()
        self.mask.draw(self.screen, active_pings)
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