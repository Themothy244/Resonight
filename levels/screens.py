import pygame
from settings import *


class Screens:
    def __init__(self, screen, currentlevel, timeLeft, totalPings, lives):
        self.screen = screen
        self.currentlevel = currentlevel
        self.timeLeft = timeLeft
        self.totalPings = totalPings
        self.hasNextLevel = True
        self.isFinalLevel = False
        self.lives = lives

        self.final_time = 0
        self.final_pings = 0
        self.final_score = 0
        self.final_rank = "C"

        self.font_inter = pygame.font.SysFont("Inter", 84, bold=True)
        self.font_inter_medium = pygame.font.SysFont("Inter", 60, bold=True)
        self.font_courier = pygame.font.SysFont("courier", 32)
        self.font_courier_lg = pygame.font.SysFont("courier", 40)
        self.font_courier_sm = pygame.font.SysFont("courier", 24)
        self.font_time = pygame.font.SysFont("arial", 30)
        self.font_ping = pygame.font.SysFont("arial", 30)
        self.font_btn = pygame.font.SysFont("arial", 35)

        self.start_btn = pygame.Rect(600, 440, 300, 60)
        self.quit_btn = pygame.Rect(600, 520, 300, 60)

        self.next_level_btn = pygame.Rect(WIDTH//2 - 150, 400, 300, 60)
        self.back_btn = pygame.Rect(WIDTH//2 - 150, 480, 300, 60)

        self.again_btn = pygame.Rect(WIDTH//2 - 150, 400, 300, 60)
        
        self.heart = pygame.image.load("assets/images/entities/health_icon.png").convert_alpha()
        self.empty = pygame.image.load("assets/images/entities/health_icon_blank.png").convert_alpha()
        self.menu_bg = pygame.image.load("assets/images/backgrounds/menu_bg.png").convert_alpha()
        
        self.heart_width, self.heart_height = 50, 50
        self.heart = pygame.transform.scale(self.heart, (self.heart_width, self.heart_height))
        self.empty = pygame.transform.scale(self.empty, (self.heart_width, self.heart_height))
        self.menu_bg = pygame.transform.scale(self.menu_bg, (WIDTH, HEIGHT))
    
    def draw_lives(self):
        # ================= LIVES =================
        for i in range(3):
            if i < self.lives:
                heart = self.heart
            else:
                heart = self.empty

            self.screen.blit(heart, (400 + i * 60, 320))

    # =========================================================
    #                          MENU 
    # =========================================================
    def draw_menu(self, mouse_pos):
        self.screen.blit(self.menu_bg, (0, 0))

        title = self.font_inter.render("Resonight", True, (255, 255, 255))
        subtitle = self.font_courier.render("Echo your way out.", True, (180, 180, 180))

        self.screen.blit(title, (120, 100))
        self.screen.blit(subtitle, (120, 200))
    
        # ================= START BUTTON =================
        if self.start_btn.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, (150, 150, 150), self.start_btn, border_radius=8)
        else:
            pygame.draw.rect(self.screen, (255, 255, 255), self.start_btn, border_radius=8)

        start_text = self.font_courier.render("START", True, (0, 0, 0))
        self.screen.blit(start_text, (
            self.start_btn.centerx - start_text.get_width() // 2,
            self.start_btn.centery - start_text.get_height() // 2
        ))

        # ================= QUIT BUTTON =================
        if self.quit_btn.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, (150, 150, 150), self.quit_btn, width=2, border_radius=8)
            quit_color = (150, 150, 150)
        else:
            pygame.draw.rect(self.screen, (255, 255, 255), self.quit_btn, width=2, border_radius=8)
            quit_color = (255, 255, 255)

        quit_text = self.font_courier.render("QUIT", True, quit_color)
        self.screen.blit(quit_text, (
            self.quit_btn.centerx - quit_text.get_width() // 2,
            self.quit_btn.centery - quit_text.get_height() // 2
        ))
        
    # =========================================================
    #                          WIN 
    # =========================================================
    def draw_win(self, mouse_pos):
        self.screen.fill((0, 0, 0))

        if self.isFinalLevel:
            title = self.font_inter_medium.render("You Escaped the Darkness", True, (255, 255, 255))

            time_text = self.font_courier_sm.render(f"Time Saved: {self.final_time:.2f}s", True, (255, 255, 255))
            ping_text = self.font_courier_sm.render(f"Pings Used: {self.final_pings}", True, (255, 255, 255))
            lives_text = self.font_courier_sm.render(f"Lives Left: {self.lives}", True, (255, 255, 255))

            score_text = self.font_courier_lg.render(f"Score: {self.final_score}", True, (255, 255, 255))
            rank_text = self.font_courier_lg.render(f"Rank: {self.final_rank}", True, (255, 255, 255))

            self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 120))
            self.screen.blit(time_text, (WIDTH//2 - time_text.get_width()//2, 220))
            self.screen.blit(ping_text, (130, 220))
            self.screen.blit(lives_text, (650, 220))
            self.screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 270))
            self.screen.blit(rank_text, (WIDTH//2 - rank_text.get_width()//2, 320))
        else:
            title = self.font_inter_medium.render(f"Level {self.currentlevel} Complete", True, (255, 255, 255))
            self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 120))

            time = self.font_courier.render(f"Time left: {self.timeLeft:0.2f}", True, (255, 255, 255))
            ping = self.font_courier.render(f"Total Ping: {self.totalPings}", True, (255, 255, 255))

            self.screen.blit(time, (WIDTH // 2 - time.get_width() // 2, 200))
            self.screen.blit(ping, (WIDTH // 2 - ping.get_width() // 2, 260))

            self.draw_lives()
        # ================= NEXT BUTTON =================
        hover = self.next_level_btn.collidepoint(mouse_pos)

        if self.hasNextLevel:
            color = (150, 150, 150) if hover else (255, 255, 255)
            label = "NEXT LEVEL"
        else:
            color = (150, 150, 150) if hover else (255, 255, 255)
            label = "PLAY AGAIN"

        pygame.draw.rect(self.screen, color, self.next_level_btn, border_radius=8)

        text = self.font_courier.render(label, True, (0, 0, 0))
        self.screen.blit(text, (
            self.next_level_btn.centerx - text.get_width() // 2,
            self.next_level_btn.centery - text.get_height() // 2
        ))

        # ================= BACK BUTTON =================
        if self.back_btn.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, (150, 150, 150), self.back_btn, width=2, border_radius=8)
            back_color = (150, 150, 150)
        else:
            pygame.draw.rect(self.screen, (255, 255, 255), self.back_btn, width=2, border_radius=8)
            back_color = (255, 255, 255)

        back_text = self.font_courier.render("BACK", True, back_color)
        self.screen.blit(back_text, (
            self.back_btn.centerx - back_text.get_width() // 2,
            self.back_btn.centery - back_text.get_height() // 2
        ))

    # =========================================================
    #                     LOSE MENU
    # =========================================================
    def draw_game_over(self, mouse_pos):
        self.screen.fill((0, 0, 0))

        if self.currentlevel == "time":
            message = "Faded to silence...."
        elif self.currentlevel == "spike":
            message = "The darkness bit back."
        elif self.currentlevel == "lives":
            message = "Game Over"
        else:
            message = "You Lose"

        title = self.font_inter_medium.render(message, True, (255, 255, 255))
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 220))

        self.draw_lives()
            
        # ================= RESTART BUTTON =================
        if self.again_btn.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, (150, 150, 150), self.again_btn, border_radius=8)
            color = (0, 0, 0)
        else:
            pygame.draw.rect(self.screen, (255, 255, 255), self.again_btn, border_radius=8)
            color = (0, 0, 0)

        text = self.font_courier.render("RESTART", True, color)
        self.screen.blit(text, (
            self.again_btn.centerx - text.get_width() // 2,
            self.again_btn.centery - text.get_height() // 2
        ))

        # ================= BACK BUTTON =================
        if self.back_btn.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, (150, 150, 150), self.back_btn, width=2, border_radius=8)
            back_color = (150, 150, 150)
        else:
            pygame.draw.rect(self.screen, (255, 255, 255), self.back_btn, width=2, border_radius=8)
            back_color = (255, 255, 255)

        back_text = self.font_courier.render("BACK", True, back_color)
        self.screen.blit(back_text, (
            self.back_btn.centerx - back_text.get_width() // 2,
            self.back_btn.centery - back_text.get_height() // 2
        ))