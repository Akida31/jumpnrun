import pygame

from skyjump.utils import TILESIZE


class Sign(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, description: str, image: pygame.Surface):
        # init the Sprite class
        super().__init__()
        # compute the real x and y position
        self.x: int = x * TILESIZE
        self.y: int = y * TILESIZE
        # save the image for the rendering
        self.image = image
        self.description = description

    @property
    def rect(self) -> pygame.Rect:
        """
        getter for rect, is used internally by collision detection from pygame
        """
        return pygame.Rect(self.x, self.y, TILESIZE, TILESIZE)

    def render(self, surface: pygame.Surface):
        """
        render the sign to the given surface
        """
        surface.blit(self.image, self.rect)

    def get_description(self):
        return self.description

    def apply_physics(self, *_):
        """
        signs dont have physics, so do nothing

        take any arguments given so this won't create effort later
        """
        pass
