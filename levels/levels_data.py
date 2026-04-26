from entities.platform import Platform
from entities.spike import Spike
from entities.door import Door
from levels.level import Level

def load_levels(self):
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
    # ---------------- LEVEL 6 ----------------
    level6 = Level(
        platforms=[
            Platform(165, 640, 150, 20),
            Platform(380, 520, 180, 20),
            Platform(599, 380, 400, 20),
        ],
        spikes=[
            Spike(320, 670, 30, 30),
            Spike(350, 670, 30, 30),
            Spike(550, 540, 30, 30),
            Spike(580, 540, 30, 30),
            Spike(610, 540, 30, 30),
            Spike(800, 350, 30, 30),
            Spike(830, 350, 30, 30),
            Spike(860, 350, 30, 30),
        ],
        doors=[
            Door(50, self.ground_y - 80, 60, 80, "entrance"),
            Door(888, 305, 60, 80, "exit"),
        ],
        player_spawn=(120, 550),
        bg_path="assets/images/backgrounds/bg_2.png"
    )
    # ---------------- LEVEL 7 ----------------
    level7 = Level(
        platforms=[
            Platform(0, 530, 250, 20),
            Platform(350, 550, 200, 20),
            Platform(650, 550, 150, 20),
            Platform(100, 440, 140, 20),
            Platform(300, 400, 140, 20),
            Platform(500, 360, 140, 20),
            Platform(50, 300, 90, 20),
            Platform(180, 270, 90, 20),
            Platform(300, 240, 90, 20),
            Platform(420, 210, 130, 20),
            Platform(20, 140, 110, 20),
        ],
        spikes=[
            Spike(130, 410, 30, 30),
            Spike(330, 370, 30, 30),
            Spike(530, 330, 30, 30),
            Spike(210, 240, 30, 30),
            Spike(240, 210, 30, 30),
            Spike(340, 170, 30, 30),
            Spike(370, 170, 30, 30),
        ],
        doors=[
            Door(20, 60, 60, 80, "exit"), #TOP LEFT DOOR CORNER
            Door(20, self.ground_y - 80, 60, 80, "entrance")
        ],
        player_spawn=(30, self.ground_y - 70),
        bg_path="assets/images/backgrounds/bg_2.png"
    )

    # ---------------- LEVEL 8 ----------------
    level8 = Level(
        platforms=[
            Platform(400, 560, 130, 20),
            Platform(260, 430, 240, 20),
            Platform(470, 330, 160, 20),
            Platform(560, 500, 190, 20),
            Platform(640, 240, 150, 20),
            Platform(820, 160, 200, 20),
        ],
        spikes=[ 
            Spike(600, 300, 30, 30),
            Spike(570, 300, 30, 30),
            Spike(540, 300, 30, 30),
            Spike(720, 470, 30, 30),
            Spike(690, 470, 30, 30),
            Spike(660, 470, 30, 30),
            Spike(630, 470, 30, 30),
            Spike(700, 210, 30, 30),
            Spike(730, 210, 30, 30),
            Spike(760, 210, 30, 30),
        ],
        doors=[
            Door(50, self.ground_y - 80, 60, 80, "entrance"),
            Door(860, 80, 60, 80, "exit"),
        ],
        player_spawn=(120, self.ground_y - 70),
        bg_path="assets/images/backgrounds/bg_2.png"
    )

    # ---------------- LEVEL 9 ----------------
    level9 = Level(
        platforms=[
            Platform(200, 550, 150, 20),
            Platform(400, 450, 150, 20),
            Platform(100, 350, 150, 20),
            Platform(860, 350, 150, 20),
            Platform(400, 250, 250, 20),
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
            Spike(780, 650, 30, 30),
            Spike(810, 650, 30, 30),
            Spike(840, 650, 30, 30),
            Spike(870, 650, 30, 30),
            Spike(900, 650, 30, 30),
            Spike(930, 650, 30, 30),
            Spike(460, 420, 30, 30),
            Spike(100, 320, 30, 30),
            Spike(130, 320, 30, 30),
            Spike(470, 220, 30, 30),
            Spike(500, 220, 30, 30),
            Spike(530, 220, 30, 30),
            Spike(560, 220, 30, 30),
        ],
        doors=[
            Door(50, self.ground_y - 80, 60, 80, "entrance"),
            Door(860, 270, 60, 80, "exit"),
        ],
        player_spawn=(120, self.ground_y - 70),
        bg_path="assets/images/backgrounds/bg_2.png"
    )

    # ---------------- LEVEL 10 ----------------
    level10 = Level(
        platforms=[
            Platform(400, 550, 400, 20),
            Platform(520, 458, 150, 15),
            Platform(250, 450, 150, 15),
            Platform(400, 320, 150, 15),
            Platform(700, 380, 150, 15),
            Platform(600, 130, 250, 15),
            Platform(250, 230, 180, 15),
        ],
        spikes=[
            Spike(770, 520, 30, 30),
            Spike(740, 520, 30, 30),
            Spike(710, 520, 30, 30),
            Spike(680, 520, 30, 30),
            Spike(820, 350, 30, 30),
            Spike(790, 350, 30, 30),
            Spike(760, 350, 30, 30),
            Spike(400, 290, 30, 30),
            Spike(430, 290, 30, 30),
            Spike(460, 290, 30, 30),
            Spike(710, 100, 30, 30),
        ],
        doors=[
            Door(50, self.ground_y - 80, 60, 80, "entrance"),
            Door(790, 50, 60, 80, "exit"),
        ],
        player_spawn=(120, self.ground_y - 70),
        bg_path="assets/images/backgrounds/bg_2.png"
    )

    return {
        1: level1,
        2: level2,
        3: level3,
        4: level4,
        5: level5,
        6: level6,
        7: level7,
        8: level8,
        9: level9,
        10: level10,
    }