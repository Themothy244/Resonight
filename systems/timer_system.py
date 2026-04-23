class TimerSystem:
    def __init__(self, start_time, tick_sound):
        self.start_time = start_time
        self.time_left = start_time
        self.tick_sound = tick_sound

        self.tick_playing = False
        self.low_time_threshold = 10

    def reset(self):
        self.time_left = self.start_time
        self.stop_tick()

    def penalize(self, amount):
        self.time_left -= amount
        if self.time_left < 0:
            self.time_left = 0

    def update(self, dt):
        self.time_left -= dt

        if self.time_left <= 0:
            self.time_left = 0
            self.stop_tick()
            return True

        if self.time_left <= self.low_time_threshold:
            if not self.tick_playing:
                self.tick_sound.play(-1)
                self.tick_playing = True
        else:
            self.stop_tick()

        return False

    def stop_tick(self):
        if self.tick_playing:
            self.tick_sound.stop()
            self.tick_playing = False