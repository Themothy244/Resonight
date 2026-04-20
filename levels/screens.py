import pygame
from settings import *


class Screens:
    def __init__(self, screen, mouse_pos, currentlevel, timeLeft, totalPings):
        self.screen = screen
        self.mouse_pos = mouse_pos
        self.currentlevel = currentlevel
        self.timeLeft = timeLeft
        self.totalPings = totalPings
        self.hasNextLevel = True
        self.isFinalLevel = False

        self.font_title = pygame.font.SysFont("arial", 60)
        self.font_time = pygame.font.SysFont("arial", 30)
        self.font_ping = pygame.font.SysFont("arial", 30)
        self.font_btn = pygame.font.SysFont("arial", 35)

        self.start_btn = pygame.Rect(WIDTH//2 - 120, HEIGHT//2, 240, 60)
        self.quit_btn = pygame.Rect(WIDTH//2 - 120, HEIGHT//2 + 80, 240, 60)

        self.next_level_btn = pygame.Rect(WIDTH//2 - 120, HEIGHT//2, 240, 60)
        self.back_btn = pygame.Rect(WIDTH//2 - 120, HEIGHT//2 + 80, 240, 60)

        self.again_btn = pygame.Rect(WIDTH//2 - 120, HEIGHT//2, 240, 60)


    def draw_menu(self):
        self.screen.fill((10, 10, 20))

        # Title
        title = self.font_title.render("Resonight", True, (255, 255, 255))
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))

        # START BUTTON
        if self.start_btn.collidepoint(self.mouse_pos):
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
        if self.quit_btn.collidepoint(self.mouse_pos):
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
    #                      WIN MENU
    # =========================================================
    def draw_win(self):
        self.screen.fill((10, 10, 20))

        # LEVEL
        if self.isFinalLevel:
            title = self.font_title.render("You Escaped the Darkness", True, (255, 255, 255))
            msg = self.font_time.render("The silence can no longer hold you...", True, (200, 200, 200))
            self.screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 6 + 70))
        else:
            title = self.font_title.render(f"Level {self.currentlevel} Complete", True, (255, 255, 255))
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 6))

        time = self.font_time.render(f"Total Time left: {self.timeLeft:0.2f}", True, (255, 255, 255))
        self.screen.blit(time, (WIDTH // 2 - time.get_width() // 2, HEIGHT // 3 + 10))

        ping = self.font_ping.render(f"Total Ping  Left: {self.totalPings}", True, (255, 255, 255))
        self.screen.blit(ping, (WIDTH // 2 - ping.get_width() // 2, HEIGHT // 3 + 40))

        # ONLY SHOW IF NEXT LEVEL EXISTS
        if self.hasNextLevel:
            # NORMAL NEXT BUTTON
            if self.next_level_btn.collidepoint(self.mouse_pos):
                pygame.draw.rect(self.screen, (200, 200, 200), self.next_level_btn)
                text_color = (0, 0, 0)
            else:
                pygame.draw.rect(self.screen, (100, 100, 100), self.next_level_btn)
                text_color = (255, 255, 255)

            next_text = self.font_btn.render("NEXT LEVEL", True, text_color)
        else:
            # FINAL LEVEL → PLAY AGAIN BUTTON
            if self.next_level_btn.collidepoint(self.mouse_pos):
                pygame.draw.rect(self.screen, (200, 200, 200), self.next_level_btn)
                text_color = (0, 0, 0)
            else:
                pygame.draw.rect(self.screen, (100, 100, 100), self.next_level_btn)
                text_color = (255, 255, 255)

            next_text = self.font_btn.render("PLAY AGAIN", True, text_color)

        self.screen.blit(next_text, (
            self.next_level_btn.centerx - next_text.get_width() // 2,
            self.next_level_btn.centery - next_text.get_height() // 2
        ))

        if self.back_btn.collidepoint(self.mouse_pos):
            pygame.draw.rect(self.screen, (200, 100, 100), self.back_btn)
            text_color = (0, 0, 0)
        else:
            pygame.draw.rect(self.screen, (120, 50, 50), self.back_btn)
            text_color = (255, 255, 255)

        back_text = self.font_btn.render("BACK", True, text_color)
        self.screen.blit(back_text, (
            self.back_btn.centerx - back_text.get_width() // 2,
            self.back_btn.centery - back_text.get_height() // 2
        ))

    # =========================================================
    #                     LOSE MENU
    # =========================================================
    def draw_game_over(self):
        self.screen.fill((10, 10, 20))

        # LEVEL
        if self.currentlevel == "time":
            message = "Your light faded into silence..."
        elif self.currentlevel == "spike":
            message = "The darkness bit back."
        else:
            message = "You Lose"

        title = self.font_title.render(message, True, (255, 255, 255))
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))

        # TRY AGAIN BUTTON
        if self.again_btn.collidepoint(self.mouse_pos):
            pygame.draw.rect(self.screen, (200, 200, 200), self.again_btn)
            text_color = (0, 0, 0)
        else:
            pygame.draw.rect(self.screen, (100, 100, 100), self.again_btn)
            text_color = (255, 255, 255)

        again_text = self.font_btn.render("RESTART", True, text_color)
        self.screen.blit(again_text, (
            self.again_btn.centerx - again_text.get_width() // 2,
            self.again_btn.centery - again_text.get_height() // 2
        ))

        # BACK BUTTON
        if self.back_btn.collidepoint(self.mouse_pos):
            pygame.draw.rect(self.screen, (200, 100, 100), self.back_btn)
            text_color = (0, 0, 0)
        else:
            pygame.draw.rect(self.screen, (120, 50, 50), self.back_btn)
            text_color = (255, 255, 255)

        back_text = self.font_btn.render("BACK", True, text_color)
        self.screen.blit(back_text, (
            self.back_btn.centerx - back_text.get_width() // 2,
            self.back_btn.centery - back_text.get_height() // 2
        ))
