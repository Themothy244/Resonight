class LevelManager:
    def __init__(self):
        self.levels = {}

    def add_level(self, level_id, level):
        self.levels[level_id] = level

    def get_level(self, level_id):
        return self.levels.get(level_id)

    def load(self, level_id):
        self.current_level = level_id
        return self.levels[level_id]