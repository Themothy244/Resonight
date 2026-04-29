import pygame
from settings import WHITE

class Player:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = 5
        self.y_velocity = 0
        self.gravity = 0.5
        self.low_jump_multiplier = 2
        self.jump_strength = 13
        self.is_jumping = False

        self.current_platform = None
        self.on_platform = False

        self.sprite_sheet = pygame.image.load("assets\images\entities\white_character.png").convert_alpha()
        self.animations = {
            "idle": [],
            "run": [],
            "jump": []
        }

        self.state = "idle"
        self.frame_index = 0
        self.animation_speed = 0.15
        self.facing_right = True

        def get_image(sheet, x, y, width, height):
            image = pygame.Surface((width, height), pygame.SRCALPHA)
            image.blit(sheet, (0, 0), (x, y, width, height))
            return image

        frame_width = 32
        frame_height = 32
        scale = 1.5

        rows = {
            "idle": 0,
            "run": 1,
            "jump": 2
        }

        for state, row in rows.items():
            for col in range(16):
                x = col * frame_width
                y = row * frame_height

                frame = get_image(self.sprite_sheet, x, y, frame_width, frame_height)
                frame = pygame.transform.scale(frame, (frame_width * scale, frame_height * scale))

                self.animations[state].append(frame)

        self.image = self.animations["idle"][0]
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))

    def on_ground_or_platform(self, platforms, ground_y):
        if self.rect.bottom >= ground_y:
            return True

        for p in platforms:
            if (
                self.rect.bottom >= p.rect.top - 5 and
                self.rect.bottom <= p.rect.top + 5 and
                self.rect.right > p.rect.left and
                self.rect.left < p.rect.right
            ):
                return True
        return False

    def move_and_collide(self, platforms, dx, dy):
        self.rect.x += dx

        for p in platforms:
            if self.rect.colliderect(p.rect):
                if dx > 0:
                    self.rect.right = p.rect.left
                elif dx < 0:
                    self.rect.left = p.rect.right

        self.rect.y += dy

        for p in platforms:
            if self.rect.colliderect(p.rect):
                if dy > 0:
                    self.rect.bottom = p.rect.top
                    dy = 0
                    self.on_platform = True
                    self.current_platform = p
                elif dy < 0:
                    self.rect.top = p.rect.bottom
                    dy = 0

        return dy

    def update(self, keys, platforms, ground_y):
        self.on_platform = False
        self.current_platform = None
        dx = 0

        if keys[pygame.K_LEFT]:
            dx = -self.speed
        if keys[pygame.K_RIGHT]:
            dx = self.speed

        if keys[pygame.K_SPACE] and self.on_ground_or_platform(platforms, ground_y):
                self.y_velocity = -self.jump_strength

        if self.y_velocity < 0:
            if not keys[pygame.K_SPACE]:
                self.y_velocity += self.gravity * self.low_jump_multiplier
            else:
                self.y_velocity += self.gravity
        else:
            self.y_velocity += self.gravity

        self.y_velocity = self.move_and_collide(platforms, dx, self.y_velocity)

        if self.on_platform and self.current_platform:
            if self.current_platform.platformType == "moving":
                platform_dx = self.current_platform.rect.x - self.current_platform.prev_x
                self.rect.x += platform_dx
            self.rect.bottom = self.current_platform.rect.top

        if self.rect.bottom >= ground_y:
            self.rect.bottom = ground_y
            self.y_velocity = 0

        self.prev_x = self.rect.x

        # ================= ANIMATION =================
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

        frames = self.animations[self.state]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(frames):
            self.frame_index = 0

        self.image = frames[int(self.frame_index)]

        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)
        screen.blit(self.image, self.rect)