import pygame
from settings import WHITE

class Player:
    def __init__(self, px, py):
        # ================= SPRITES =================
        self.sprite_sheet = pygame.image.load(
            "assets/images/entities/white_character.png"
        ).convert_alpha()

        self.animations = {
            "idle": [],
            "run": [],
            "jump": [],
            "death_spike": [],
            "death_time": []
        }

        self.state = "idle"
        self.frame_index = 0
        self.animation_speed = 0.15
        self.facing_right = True

        self.forced_state = None
        self.animation_finished = False

        # ================= LOAD ANIMATIONS =================
        frame_width = 32
        frame_height = 32
        scale = 2

        rows = {
            "idle": 0,
            "run": 1,
            "jump": 2,
            "death_spike": 5,
            "death_time": 6  
        }

        frame_counts = {
            "idle": 16,
            "run": 16,
            "jump": 16,
            "death_spike": 4,
            "death_time": 8
        }
        
        def get_image(x, y):
            image = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            image.blit(self.sprite_sheet, (0, 0), (x, y, frame_width, frame_height))
            return pygame.transform.scale(
                image, (frame_width * scale, frame_height * scale)
            )
        
        for state, row in rows.items():
            for col in range(frame_counts[state]):
                x = col * frame_width
                y = row * frame_height
                self.animations[state].append(get_image(x, y))

        self.image = self.animations["idle"][0]
        self.rect = self.image.get_rect(topleft=(px, py))

        # ================= PHYSICS =================
        self.speed = 5
        self.y_velocity = 0
        self.gravity = 0.5
        self.low_jump_multiplier = 2
        self.jump_strength = 13

        # ================= HITBOX =================
        self.hitbox = pygame.Rect(0, 0, self.rect.width * 0.5, self.rect.height * 0.9)
        self.hitbox.midbottom = self.rect.midbottom

        # ================= PLATFORM =================
        self.current_platform = None
        self.on_platform = False

    # ================= GROUND CHECK =================
    def on_ground_or_platform(self, platforms, ground_y):
        if self.hitbox.bottom >= ground_y:
            return True

        for p in platforms:
            if (
                self.hitbox.bottom >= p.rect.top - 5 and
                self.hitbox.bottom <= p.rect.top + 5 and
                self.hitbox.right > p.rect.left and
                self.hitbox.left < p.rect.right
            ):
                return True
        return False

    # ================= COLLISION =================
    def move_and_collide(self, platforms, dx, dy):
        self.hitbox.x += dx

        for p in platforms:
            if self.hitbox.colliderect(p.rect):
                if dx > 0:
                    self.hitbox.right = p.rect.left
                elif dx < 0:
                    self.hitbox.left = p.rect.right

        self.hitbox.y += dy

        self.on_platform = False
        self.current_platform = None

        for p in platforms:
            if self.hitbox.colliderect(p.rect):
                if dy > 0:
                    self.hitbox.bottom = p.rect.top
                    dy = 0
                    self.on_platform = True
                    self.current_platform = p
                elif dy < 0:
                    self.hitbox.top = p.rect.bottom
                    dy = 0

        return dy

    # ================= DEATH =================
    def play_death(self, reason):
        if reason == "spike":
            self.forced_state = "death_spike"
        elif reason == "time":
            self.forced_state = "death_time"

        self.frame_index = 0
        self.animation_finished = False

    # ================= UPDATE =================
    def update(self, keys, platforms, ground_y):
        # ---------- DEATH ANIMATION ----------
        if self.forced_state:
            frames = self.animations[self.forced_state]
            self.frame_index += self.animation_speed

            if self.frame_index >= len(frames):
                self.frame_index = len(frames) - 1
                self.animation_finished = True

            self.image = frames[int(self.frame_index)]
            return 

        # ---------- MOVEMENT ----------
        dx = 0

        if keys[pygame.K_LEFT]:
            dx = -self.speed
        if keys[pygame.K_RIGHT]:
            dx = self.speed

        # jump
        if keys[pygame.K_SPACE] and self.on_ground_or_platform(platforms, ground_y):
            self.y_velocity = -self.jump_strength

        # gravity
        if self.y_velocity < 0:
            if not keys[pygame.K_SPACE]:
                self.y_velocity += self.gravity * self.low_jump_multiplier
            else:
                self.y_velocity += self.gravity
        else:
            self.y_velocity += self.gravity

        # apply movement
        self.y_velocity = self.move_and_collide(platforms, dx, self.y_velocity)

        # moving platform carry
        if self.on_platform and self.current_platform:
            if self.current_platform.platformType == "moving":
                platform_dx = self.current_platform.rect.x - self.current_platform.prev_x
                self.hitbox.x += platform_dx

        # ground clamp
        if self.hitbox.bottom >= ground_y:
            self.hitbox.bottom = ground_y
            self.y_velocity = 0

        # ================= SYNC SPRITE =================
        self.rect.midbottom = self.hitbox.midbottom
        
        previous_state = self.state

        if not self.on_ground_or_platform(platforms, ground_y):
            self.state = "jump"
        elif dx != 0:
            self.state = "run"
        else:
            self.state = "idle"

        if self.state != previous_state:
            self.frame_index = 0

        if dx < 0:
            self.facing_right = False
        elif dx > 0:
            self.facing_right = True

        # ---------- ANIMATION ----------
        frames = self.animations[self.state]
        self.frame_index += self.animation_speed

        if self.frame_index >= len(frames):
            self.frame_index = 0

        self.image = frames[int(self.frame_index)]

        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

    # ================= DRAW =================
    def draw(self, screen):
        # pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)
        # pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)
        screen.blit(self.image, self.rect)