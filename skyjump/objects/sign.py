import pygame

from skyjump.utils import TILESIZE


class Sign(pygame.sprite.Sprite):
    """hint signs in the game"""

    def __init__(
        self, x: int, y: int, description: str, image: pygame.Surface
    ):
        """create a new sign

        :param x: the x-position in tiles
        :param y: the y-position in tiles
        :param description: the description/ content of the sign
        :param image: the sign image
        """
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
        """getter for rect

        is used internally by collision detection from pygame
        """
        return pygame.Rect(self.x, self.y, TILESIZE, TILESIZE)

    def render(self, surface: pygame.Surface):
        """render the sign

        :param surface: surface on which the sign should be rendered
        """
        surface.blit(self.image, self.rect)

    def get_description(self) -> str:
        """get the description of the sign

        :return: description
        """
        return self.description

    def apply_physics(self, *_):
        """signs dont have physics, so do nothing

        :params: take any arguments given so this won't create effort later
        """
        pass
