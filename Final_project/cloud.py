import pygame
from pygame.sprite import Sprite


class Cloud(Sprite):
    # Make cloud
    def __init__(self, screen, setting):
        super(Cloud, self).__init__()
        self.screen = screen
        self.settings = setting

        # Load the cloud image and set its rect attribute
        self.image = pygame.transform.scale(pygame.image.load('cloud.png'), (int(setting.screen_width/8), int(setting.screen_height/12)))
        self.rect = self.image.get_rect()

        # Start each new cloud near the bottom left of the screen.
        self.rect.x = 0
        self.rect.y = setting.screen_height + self.rect.height

        # Store the cloud's exact position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def blitme(self):
        # Draw the cloud
        self.screen.blit(self.image, self.rect)

    def update(self):
        # Make move
        self.y -= self.settings.cloud_speed
        self.rect.y = self.y
