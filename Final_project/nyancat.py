import pygame
from pygame.sprite import Sprite


class Nyan(Sprite):
    def __init__(self, screen, setting, x, y):
        super(Nyan, self).__init__()

        # Put cat's position as screen
        self.screen = screen
        self.settings = setting

        # Load the cat image and get its rect.
        self.image = pygame.transform.scale(pygame.image.load('nyanz.bmp'), (int(setting.screen_width/10), int(setting.screen_height/12)))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start new cat at the bottom center of the screen.
        self.rect.centerx = float(x)
        self.rect.bottom = float(y)

        # Moving state
        self.move_state = True
        self.dash = False
        self.moving_left = False
        self.moving_right = False

        # To determine dash direction
        self.facing = "right"

        # Make x and y into float
        self.rect.y = float(self.rect.y)
        self.rect.x = float(self.rect.x)

    def update(self, screen, setting):
        # Check movement state to move
        if self.dash is True:
            if self.facing == "right":
                self.image = pygame.transform.scale(pygame.image.load('nyannitro.bmp'), (int(setting.screen_width/10), int(setting.screen_height/12)))
                self.rect.centerx += setting.cat_speed*2

                # Dash limit right
                if self.rect.right > setting.screen_width:
                    self.rect.right = setting.screen_width

            elif self.facing == "left":
                self.image = pygame.transform.flip(pygame.transform.scale(pygame.image.load('nyannitro.bmp'), (int(setting.screen_width/10), int(setting.screen_height/12))), True, False)
                self.rect.centerx -= setting.cat_speed*2

                # Dash limit left
                if self.rect.left < 0:
                    self.rect.left = 0

        elif self.moving_left is True and self.rect.left > 0:
            self.image = pygame.transform.flip(pygame.transform.scale(pygame.image.load('nyanrenbo.bmp'), (int(setting.screen_width/10), int(setting.screen_height/12))), True, False)
            self.rect.centerx -= setting.cat_speed

        elif self.moving_right is True and self.rect.right < setting.screen_width:
            self.image = pygame.transform.scale(pygame.image.load('nyanrenbo.bmp'), (int(setting.screen_width/10), int(setting.screen_height/12)))
            self.rect.centerx += setting.cat_speed

    def blitme(self):
        # Draw the cat at its current location.
        self.screen.blit(self.image, self.rect)

    def restart_position(self, setting):
        # Make x to center
        self.rect.centerx = setting.screen_width/2
        self.rect.bottom = setting.screen_height
