class GameStats():
    def __init__(self, settings):
        # Initialize statistics.
        self.settings = settings
        self.game_active = False
        self.reset_stats()

        # Initial highscore
        self.high_score = 0


    def reset_stats(self):
        # Initialize statistics that can change during the game.
        self.score = 0
        self.level = 1

        self.cloud_speed = self.settings.cloud_speed
        self.cat_speed = self.settings.cat_speed
