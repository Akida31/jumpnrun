import pygame


class Spike(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int, image):
        # init the Sprite class
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        # save the image for the rendering
        self.image = pygame.transform.scale(image, (width, height))

    @property
    def rect(self) -> pygame.Rect:
        """
        getter for rect, is used internally by collision detection from pygame
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def render(self, surface: pygame.Surface):
        """
        render the sign to the given surface
        """
        surface.blit(self.image, self.rect)

    def apply_physics(self, *_):
        """
        spikes dont have physics, so do nothing

        take any arguments given so this won't create effort later
        """
        pass
