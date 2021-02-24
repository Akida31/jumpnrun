from typing import List
import pygame
from jumpnrun.utils import load_spritesheet, TILESIZE
import time


class Player(pygame.sprite.Sprite):
    def __init__(self, sprite_filename: str, x: int, y: int):
        # initialize the Sprite class
        super().__init__()
        # x and y are tile position and have to be multiplied with the tilesize
        self.x: int = x * TILESIZE
        self.y: int = y * TILESIZE
        self.width = 16
        self.height = 24
        self.spritesheet = load_spritesheet(sprite_filename, self.width, self.height, 8, 8, 16, 8)
        self.sprite = self.spritesheet[8][2]
        # for applying gravity we need to save velocity and acceleration of the player
        self.acceleration: List[float] = [0,0]
        self.velocity: List[float] = [0,0]
        self.flip = False  # the direction of the sprite image

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def render(self, surface: pygame.Surface):
        image = self.sprite
        if self.flip:
            # flip the image horizontally and not vertically
            image = pygame.transform.flip(image, True, False)
        surface.blit(image, (self.x, self.y, self.width, self.height))

    def interact(self, objects: List, quit_handler):
        if collision := pygame.sprite.spritecollideany(self, objects):
            quit_handler() 

    def apply_physics(self, map):
        # gravity
        if not self._check_down(map):
            self.acceleration[1] += 1
        else:
            # if the player is on ground the velocity will be reset
            self.velocity[1] = 0

        # apply acceleration to velocity
        self.velocity[0] += self.acceleration[0]
        self.velocity[1] += self.acceleration[1]

        # reset acceleration
        self.acceleration = [0, 0]

        # move the player horizontally
        if (v := self.velocity[0]) != 0:
            # change sprite to walking
            self.sprite = self.spritesheet[8][2]
            # determine the direction of the movement
            if v > 0:
                move = self.move_right
                # reset the flip of the sprite
                self.flip = False
            else:
                move = self.move_left
                # flip the sprite
                self.flip = True
            # character can move only half tiles
            for x in range(abs(round(v * 2))):
                move(map, 0.5)

        # move the player vertically
        if (v := self.velocity[1]) != 0:
            # set the right sprite
            self.sprite = self.spritesheet[16][2]
            if v > 0:
                move = self.move_down
            else:
                move = self.move_up
            for y in range(abs(round(v * 2))):
                move(map, 0.5)

        # because of air resistance the velocity in x direction is lowered
        if self.velocity[0] > 0:
            self.velocity[0] -= 2
        elif self.velocity[0] < 0:
            self.velocity[0] += 2

    def jump(self, map):
        if self._check_down(map):
            self.acceleration[1] -= 9

    def go_left(self, map):
        self.acceleration[0] = -2

    def go_right(self, map):
        self.acceleration[0] = 2

    def move_up(self, map, dy):
        if not self._check_up(map):
            self.y -= dy

    def move_down(self, map, dy):
        if not self._check_down(map):
            self.y += dy

    def move_left(self, map, dx):
        if not self._check_left(map):
            self.x -= dx

    def move_right(self, map, dx):
        if not self._check_right(map):
            self.x += dx

    def _check_right(self, map):
        return (map.check_collide(self.x / TILESIZE + 1, self.y / TILESIZE)
                or  map.check_collide(self.x / TILESIZE + 1, self.y / TILESIZE +1))

    def _check_left(self, map):
        return (map.check_collide(self.x / TILESIZE - 0.5, self.y / TILESIZE)
                or  map.check_collide(self.x / TILESIZE - 0.5 , self.y / TILESIZE +1))

    def _check_down(self, map):
        return (map.check_collide(self.x / TILESIZE + 0.5, self.y / TILESIZE + 1.5)
                or map.check_collide(self.x / TILESIZE, self.y / TILESIZE + 1.5))

    def _check_up(self, map):
        return (map.check_collide(self.x / TILESIZE + 0.75, self.y / TILESIZE)
                or map.check_collide(self.x / TILESIZE, self.y / TILESIZE))
