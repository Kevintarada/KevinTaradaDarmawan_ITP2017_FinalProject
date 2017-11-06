import pygame
from Final_project.settings import Settings
import Final_project.game_functions as gf
from pygame.sprite import Group
from Final_project.nyancat import Nyan
from Final_project.game_stats import GameStats
from Final_project.button import Button
from Final_project.scoreboard import Scoreboard


def play_game():
    # Create screen objects
    pygame.init()
    setting = Settings()
    screen = pygame.display.set_mode((setting.screen_width, setting.screen_height))

    # Clock for FPS
    clock = pygame.time.Clock()

    # Caption
    pygame.display.set_caption("Nyan Adventure")

    # Button
    play_button = Button(setting, screen, "Run Down!")

    # Make Cat to screen
    cat = Nyan(screen, setting, setting.screen_width/2, setting.screen_height)
    cloud = Group()

    # Set up scoreboards
    stats = GameStats(setting)
    sb = Scoreboard(setting, screen, stats)


    while True:
        # Use check event
        gf.check_events(cat, setting, stats, play_button, cloud, screen, sb)

        if stats.game_active:
            # Start counter to generate clouds
            setting.add_counter()

            if setting.counter % setting.cloud_spawn_time == 0 and setting.counter > 0:
                gf.create_fleet(setting, screen, cloud)
                setting.reset_counter()


            # Check if cat/cloud hit top screen
            if gf.hit_top(setting, screen, cat, cloud, stats, sb):
                stats.game_active = False
                pygame.mouse.set_visible(True)
                setting.initialize_dynamic_settings()

            # Check if cat on top of cloud
            gf.check_cat_under(setting, screen, cat, cloud, sb, stats)

            # Update cat and cloud
            cat.update(screen, setting)
            cloud.update()

        # Use function to draw things to screen
        gf.draw_screens(setting, screen, cat, cloud, stats, play_button, sb)

        # Set FPS
        clock.tick(80)

# Call main
play_game()
