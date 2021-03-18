import pygame


class Spike(pygame.sprite.Sprite):
    """spike traps in the game"""

    def __init__(
        self, x: int, y: int, width: int, height: int, image: pygame.Surface
    ):
        """create a new spike

        :param x: the x-position as real value
        :param y: the y-position as real value
        :param width: the width in px
        :param height: the height in px
        :param image: the image of the spike
        """
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
        """getter for rect

        is used internally by collision detection from pygame
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def render(self, surface: pygame.Surface):
        """render the spike

        :param surface: surface on which the sign should be rendered
        """
        surface.blit(self.image, self.rect)

    def apply_physics(self, *_):
        """spikes dont have physics, so do nothing

        :params: take any arguments given so this won't create effort later
        """
        pass
