import sys
import pygame
from Final_project.cloud import Cloud
import random
from Final_project.nyancat import Nyan


def check_events(cat, setting, stats, play_button, cloud, screen, sb):
    # Respond to key-presses and mouse events.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Check if quit button is clicked and stop game
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if mouse click button
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x, mouse_y, cloud, cat, setting, screen, sb)

        # Determine between key-down and up
        elif event.type == pygame.KEYDOWN:

            # If move state is True then move, else only cat facing change
            if cat.move_state == True:
                if event.key == pygame.K_RIGHT:
                    # Move right
                    cat.facing = "right"
                    cat.moving_right = True

                if event.key == pygame.K_LEFT:
                    # Move left
                    cat.facing = "left"
                    cat.moving_left = True

                if event.key == pygame.K_SPACE:
                    # Dash
                    cat.dash = True

            else:
                if event.key == pygame.K_RIGHT:
                    # Face right
                    cat.facing = "right"

                if event.key == pygame.K_LEFT:
                    # Face left
                    cat.facing = "left"

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                # Change pic and stop move right
                cat.image = pygame.transform.scale(pygame.image.load('nyanz.bmp'), (int(setting.screen_width/10), int(setting.screen_height/12)))
                cat.moving_right = False

            if event.key == pygame.K_LEFT:
                # Change pic and stop move left
                cat.image = pygame.transform.flip(pygame.transform.scale(pygame.image.load('nyanz.bmp'), (int(setting.screen_width/10), int(setting.screen_height/12))), True, False)
                cat.moving_left = False

            if event.key == pygame.K_SPACE:
                cat.dash = False
                # Return pic
                if cat.facing == "left":
                    cat.image = pygame.transform.flip(pygame.transform.scale(pygame.image.load('nyanz.bmp'), (int(setting.screen_width/10), int(setting.screen_height/12))), True, False)

                elif cat.facing == "right":
                    cat.image = pygame.transform.scale(pygame.image.load('nyanz.bmp'), (int(setting.screen_width/10), int(setting.screen_height/12)))

def check_play_button(stats, play_button, mouse_x, mouse_y, cloud, cat, setting, screen, sb):

    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Restart speed settings of all things
        setting.initialize_dynamic_settings()

        # Hide the mouse cursor
        pygame.mouse.set_visible(False)

        # Start a new game when the player clicks Run Down!.
        if play_button.rect.collidepoint(mouse_x, mouse_y):

            # Reset the game statistics.
            stats.reset_stats()
            stats.game_active = True

            # Reset the scoreboard images.
            sb.prep_score()
            sb.prep_highscore()
            sb.prep_level()

            # Reset counter
            setting.reset_counter()

            # Empty the list of clouds.
            cloud.empty()

            # Create a new cat and center it.
            cat.restart_position(setting)

            # Music
            pygame.mixer.music.load('Nyancat.mp3')
            pygame.mixer.music.play(-1)

def draw_screens(setting, screen, cat, cloud, stats, play_button, sb):

    # Blit/Draw things to screen
    screen.blit(setting.background, (0, 0))

    # Blit cats
    cat.blitme()

    # Blit clouds
    for clouds in cloud:
        clouds.blitme()

    # Draw the score information.
    sb.show_score()

    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()

    # Make the most recently drawn screen visible.
    pygame.display.flip()

def create_fleet(setting, screen, cloud):
    # If counter reached spawn time for cloud
        # Randomise no-cloud position
        positions = [0, 1, 1, 1, 1, 1, 1, 1]

        # if counter % setting.cloud_spawn_time == 0:
        x = random.randint(0, 7)
        positions[0], positions[x] = positions[x], positions[0]

        for i in range(len(positions)):
            # Make a cloud to add
            clouds = Cloud(screen, setting)
            cloud_width = clouds.rect.width

            # If value is 1, add cloud with position of x = width * order
            if positions[i] == 1:
                clouds.x = cloud_width * i
                clouds.rect.x = clouds.x
                cloud.add(clouds)

            else:
                # Add nothing
                continue

def check_cat_under(setting, screen, cat, cloud, sb, stat):

    # Check cat on top of cloud
    if pygame.sprite.spritecollideany(cat, cloud):
        # Push cat up and let move
        cat.move_state = True
        cat.rect.y -= setting.cloud_speed

    else:
        if cat.rect.bottom == setting.screen_height:
            # Add more points if hit ground
            stat.score += setting.touch_ground

        elif cat.rect.bottom > setting.screen_height:
            # If cat fall below screen move its bottom to base of screen
            cat.rect.bottom = setting.screen_height

        elif cat.rect.bottom < setting.screen_height:
            # Push cat down while cat's bottom above screen's height
            cat.rect.y += setting.cloud_speed
            stat.score += setting.cloud_points

            # Make cat unable to move to prevent colliding with cloud's side
            cat.move_state = False
            cat.moving_right, cat.moving_left, cat.dash = False, False, False

        # Change the score after adding
        sb.prep_score()
        check_high_score(stat, sb)

def hit_top(setting, screen, cat, cloud, stats, sb):
    # Destroy cloud in the group after hitting top screen
    cloud_destroy = 0
    for clouds in cloud.copy():
        if clouds.rect.bottom < 0:
            cloud_destroy += 1
            cloud.remove(clouds)
            if cloud_destroy == 7:
                setting.cloud_destroyed += 1

    if setting.cloud_destroyed / 10 == 1:

        # Max level is 3
        if stats.level == "MAX":
            pass
        elif int(stats.level) < 3:
            # Increase level
            stats.level = str(int(stats.level) + 1)

            # Increase speed
            setting.increase_speed()

        elif stats.level == "3":
            stats.level = "MAX"
        setting.cloud_destroyed = 0
        sb.prep_level()

    # If cat hit top return True which will stop (not exit) game in Run_Down.py
    if cat.rect.top <= 0:
        # Music stop
        pygame.mixer.music.fadeout(1000)

        return True


def check_high_score(stats, sb):
    # Check to see if there's a new high score.
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_highscore()
