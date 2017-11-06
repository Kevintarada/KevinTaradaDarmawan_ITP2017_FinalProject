import pygame


class Settings:
    def __init__(self):

        # Screen settings
        self.screen_width = 600
        self.screen_height = 800
        self.background = pygame.transform.scale(pygame.image.load('final proj bg.png'), (self.screen_width, self.screen_height))

        # Cloud destroyed counter
        self.cloud_destroyed = 0

        # Scale of how much score values increase/level
        self.score_scale = 2

        # How quickly the game speeds up
        self.speedup_scale = 2


        # Counter for cloud
        self.counter = 0

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        # Initialize settings that change throughout the game.
        # Cat speed
        self.cat_speed = 3

        # Cloud speed
        self.cloud_speed = 1

        # Cloud spawn time
        self.cloud_spawn_time = 200

        # Cloud points and touch ground points
        self.cloud_points = 5
        self.touch_ground = 10

    def increase_speed(self):
        #Increase speed settings.
        self.cat_speed += self.speedup_scale

        self.cloud_spawn_time /= self.speedup_scale
        self.cloud_speed += self.speedup_scale

        self.cloud_points *= self.score_scale
        self.touch_ground *= self.score_scale

    def add_counter(self):
        self.counter += 1

    def reset_counter(self):
        self.counter = 0
