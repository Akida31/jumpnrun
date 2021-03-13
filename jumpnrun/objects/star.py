from typing import List
from os import path, listdir
from jumpnrun.config import DATA_DIR

import pygame

from jumpnrun.utils import TILESIZE

# the waiting time before the image gets changed
WAITING_TIME: int = 7


class Star(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        # init the Sprite class
        super().__init__()
        # compute the real x and y position
        self.x: int = x * TILESIZE
        self.y: int = y * TILESIZE
        # for the animation we have to save a iteration state
        self.iter_state: int = 0
        # load the different images for the star
        self.images: List[pygame.Surface] = []
        for filename in load_starfiles():
            image = pygame.image.load(filename)
            # scale the image to the tilesize
            image = pygame.transform.scale(image, (TILESIZE, TILESIZE))
            # make the background of the star transparent
            image.set_colorkey(image.get_at((0, 0)))
            self.images.append(image)

    @property
    def rect(self) -> pygame.Rect:
        """
        getter for rect, is used internally by collision detection from pygame
        """
        return pygame.Rect(self.x, self.y, TILESIZE, TILESIZE)

    def render(self, surface: pygame.Surface):
        """
        render the current star image to the given surface
        """
        # get the current image
        image = self.images[self.iter_state // WAITING_TIME]

        # increase the iteration state
        self.iter_state += 1
        if self.iter_state == len(self.images) * WAITING_TIME:
            self.iter_state = 0

        surface.blit(image, self.rect)

    def apply_physics(self, *_):
        """
        stars dont have physics, so do nothing

        take any arguments given so this won't create effort later
        """
        pass


def load_starfiles() -> List[str]:
    """
    load all the files of the star
    """
    # load the imgs for the stars
    star_dir: str = path.join(DATA_DIR, "img", "star", "shine")
    starfiles: List[str] = list(
        map(lambda i: path.join(star_dir, i), listdir(star_dir))
    )
    # sort the files
    starfiles.sort()
    return starfiles
