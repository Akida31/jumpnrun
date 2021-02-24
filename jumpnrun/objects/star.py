from typing import List
import pygame
from jumpnrun.utils import TILESIZE

class Star(pygame.sprite.Sprite):
    def __init__(self, sprite_filenames: List[str], x: int, y: int):
        # init the Sprite class
        super().__init__()
        self.x: int = x * TILESIZE
        self.y: int = y * TILESIZE
        # for the animation we have to save a iteration state
        self.iter_state: int = 0
        self.images: List[pygame.Surface] = []
        for filename in sprite_filenames:
            image = pygame.image.load(filename)
            image = pygame.transform.scale(image, (TILESIZE, TILESIZE))
            image.set_colorkey(image.get_at((0,0)))
            self.images.append(image)

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, TILESIZE, TILESIZE)

    def render(self, surface: pygame.Surface):
        # the waiting time before the image gets changed
        WAITING_TIME: int = 10
        image = self.images[self.iter_state // WAITING_TIME]

        self.iter_state += 1
        if self.iter_state == len(self.images) * WAITING_TIME:
            self.iter_state = 0

        surface.blit(image, (self.x, self.y, TILESIZE, TILESIZE))

    def apply_physics(self, *_):
        """
        stars dont have physics, so do nothing
        """
        pass
