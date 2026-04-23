import pygame
from settings import *


class Screens:
    def __init__(self, screen, currentlevel, timeLeft, totalPings, lives,):
        self.screen = screen
        self.currentlevel = currentlevel
        self.timeLeft = timeLeft
        self.totalPings = totalPings
        self.hasNextLevel = True
        self.isFinalLevel = False
        self.lives = lives

        self.font_inter = pygame.font.SysFont("Inter", 84, bold=True)
        self.font_inter_medium = pygame.font.SysFont("Inter", 60, bold=True)
        self.font_courier = pygame.font.SysFont("courier", 32)
        self.font_time = pygame.font.SysFont("arial", 30)
        self.font_ping = pygame.font.SysFont("arial", 30)
        self.font_lives = pygame.font.SysFont("arial", 30)
        self.font_btn = pygame.font.SysFont("arial", 35)

        self.start_btn = pygame.Rect(WIDTH//2 - 150, 360, 300, 60)
        self.quit_btn = pygame.Rect(WIDTH//2 - 150, 440, 300, 60)

        self.next_level_btn = pygame.Rect(WIDTH//2 - 150, 360, 300, 60)
        self.back_btn = pygame.Rect(WIDTH//2 - 150, 440, 300, 60)

        self.again_btn = pygame.Rect(WIDTH//2 - 150, 360, 300, 60)

    # =========================================================
    #                          MENU 
    # =========================================================
    def draw_menu(self, mouse_pos):
        self.screen.fill((0, 0, 0))

        title = self.font_inter.render("Resonight", True, (255, 255, 255))
        subtitle = self.font_courier.render("Echo your way out.", True, (180, 180, 180))

        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 200))
        self.screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 300))

        # START BUTTON (clean hover brightness)
        if self.start_btn.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, (245, 245, 245), self.start_btn, border_radius=8)
        else:
            pygame.draw.rect(self.screen, (255, 255, 255), self.start_btn, border_radius=8)

        start_text = self.font_courier.render("START", True, (0, 0, 0))
        self.screen.blit(start_text, (
            self.start_btn.centerx - start_text.get_width() // 2,
            self.start_btn.centery - start_text.get_height() // 2
        ))

        # QUIT BUTTON (more contrast hover)
        if self.quit_btn.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, (220, 80, 80), self.quit_btn, border_radius=8)
            quit_color = (0, 0, 0)
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
        else:
            title = self.font_inter_medium.render(f"Level {self.currentlevel} Complete", True, (255, 255, 255))
            self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 140))

        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 120))

        time = self.font_courier.render(f"Time left: {self.timeLeft:0.2f}", True, (255, 255, 255))
        self.screen.blit(time, (WIDTH // 2 - time.get_width() // 2, 190))

        ping = self.font_courier.render(f"Total Ping: {self.totalPings}", True, (255, 255, 255))
        self.screen.blit(ping, (WIDTH // 2 - ping.get_width() // 2, 230))

        lives = self.font_courier.render(f"Total Lives Remain: {self.lives}", True, (255, 255, 255))
        self.screen.blit(lives, (WIDTH // 2 - lives.get_width() // 2, 280))

        hover = self.next_level_btn.collidepoint(mouse_pos)

        if self.hasNextLevel:
            color = (230, 230, 230) if hover else (255, 255, 255)
            label = "NEXT LEVEL"
        else:
            color = (200, 200, 200) if hover else (120, 120, 120)
            label = "PLAY AGAIN"

        pygame.draw.rect(self.screen, color, self.next_level_btn)

        text = self.font_courier.render(label, True, (0, 0, 0))
        self.screen.blit(text, (
            self.next_level_btn.centerx - text.get_width() // 2,
            self.next_level_btn.centery - text.get_height() // 2
        ))

        # BACK
        back_hover = self.back_btn.collidepoint(mouse_pos)

        if back_hover:
            pygame.draw.rect(self.screen, (220, 120, 120), self.back_btn)
            back_color = (0, 0, 0)
        else:
            pygame.draw.rect(self.screen, (255, 255, 255), self.back_btn, 2)
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

        # LEVEL
        if self.currentlevel == "lives":
            message = "game over"
        elif self.currentlevel == "spike":
            message = "The darkness bit back."
        elif self.currentlevel == "time":
            message = "Your light faded into silence..."
        else:
            message = "You Lose"

        title = self.font_inter_medium.render(message, True, (255, 255, 255))
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))

        hover = self.again_btn.collidepoint(mouse_pos)

        if hover:
            pygame.draw.rect(self.screen, (230, 230, 230), self.again_btn)
            color = (0, 0, 0)
        else:
            pygame.draw.rect(self.screen, (255, 255, 255), self.again_btn)

            color = (0, 0, 0)

        text = self.font_courier.render("RESTART", True, color)
        self.screen.blit(text, (
            self.again_btn.centerx - text.get_width() // 2,
            self.again_btn.centery - text.get_height() // 2
        ))

        back_hover = self.back_btn.collidepoint(mouse_pos)

        if back_hover:
            pygame.draw.rect(self.screen, (220, 120, 120), self.back_btn)
            back_color = (0, 0, 0)
        else:
            pygame.draw.rect(self.screen, (255, 255, 255), self.back_btn, 2)
            back_color = (255, 255, 255)

        back_text = self.font_courier.render("BACK", True, back_color)
        self.screen.blit(back_text, (
            self.back_btn.centerx - back_text.get_width() // 2,
            self.back_btn.centery - back_text.get_height() // 2
        ))