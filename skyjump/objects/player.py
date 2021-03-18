from typing import Dict, List

import pygame

from skyjump.map import Map
from skyjump.utils import TILESIZE, load_spritesheet
from skyjump.sound import play_sound

# the movement speed of the player in x-direction
MOVESPEED: float = 2


class Player(pygame.sprite.Sprite):
    """the player of the game"""

    def __init__(self, sprite_filename: str, x: int, y: int):
        """create the player

        :param: sprite_filename: the file from which the sprite shown
            on the screen should be loaded
        :param x: the initial x position of the player in tiles
        :param y: the initial y position of the player in tiles
        """
        # initialize the Sprite class
        super().__init__()
        # x and y are tile position and have to be multiplied with the tilesize
        # to get the real position
        self.x: float = x * TILESIZE
        self.y: float = y * TILESIZE
        # size of the player is manually inserted
        # because the character file was adjusted for that
        self.width = 16
        self.height = 24
        # load all sprites from the file
        self.spritesheet = load_spritesheet(
            sprite_filename, self.width, self.height, 8, 8, 16, 8
        )
        # the initial sprite
        self.sprite = self.spritesheet[8][2]
        self.velocity: List[float] = [0, 0]
        self.flip = False  # the direction of the sprite image
        self.alive = True

    @property
    def rect(self) -> pygame.Rect:
        """getter for rect

        this is used internally by collision detection from pygame
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def render(self, surface: pygame.Surface):
        """render the player

        :param surface: the surface on which the player should be rendered
        """
        # copy the sprite so we don't flip the original
        image = self.sprite
        if self.flip:
            # flip the image horizontally and not vertically
            image = pygame.transform.flip(image, True, False)
        surface.blit(image, self.rect)

    def interact(self, objects: Dict[str, pygame.sprite.Group]):
        """interact with objects in the world

        :param objects: the objects with which the player can interact
        """
        # check collision with stars
        if collision := pygame.sprite.spritecollideany(self, objects["stars"]):
            objects["stars"].remove(collision)
            play_sound("coin.ogg")
        # check collision with spikes
        if pygame.sprite.spritecollideany(self, objects["spikes"]):
            self.alive = False

    def apply_physics(self, map: Map):
        """apply physics to the player

        currently this includes gravity and collision
        :param map: the map used for colliders
        """
        # gravity
        if not self._check_down(map):
            self.velocity[1] += 1
        else:
            # if the player is on ground the velocity
            # in y-direction will be reset
            self.velocity[1] = min(0.0, self.velocity[1])

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
            # moves will be done partly so that collision is detected correctly
            for _ in range(abs(round(v * 2))):
                move(map, 0.5)

        # move the player vertically
        if (v := self.velocity[1]) != 0:
            # set the right sprite
            self.sprite = self.spritesheet[16][2]
            if v > 0:
                move = self.move_down
            else:
                move = self.move_up
            for _ in range(abs(round(v * 2))):
                move(map, 0.5)

        # because of resistance the velocity in x direction is lowered
        # so that it is a constant velocity and not an acceleration
        if self.velocity[0] > 0:
            self.velocity[0] -= max(self.velocity[0], MOVESPEED)
        elif self.velocity[0] < 0:
            self.velocity[0] -= min(self.velocity[0], -MOVESPEED)

        # the player shouldn't be alive if he falls off the screen
        if self.y >= map.get_size()[1]:
            self.alive = False

    def jump(self, map: Map):
        """the player jumps if nothing is above him"""
        if self._check_down(map):
            self.velocity[1] -= 11

    def go_left(self, _: Map):
        """the player goes left"""
        self.velocity[0] = -MOVESPEED

    def go_right(self, _: Map):
        """the player goes right"""
        self.velocity[0] = MOVESPEED

    def move_up(self, map: Map, dy: float):
        """move the player directly up if nothing is in his way

        :param map: the map on which the player moves
        :param dy: the distance to move
        """
        if not self._check_up(map):
            self.y -= dy

    def move_down(self, map: Map, dy: float):
        """move the player directly down if nothing is in his way

        :param map: the map on which the player moves
        :param dy: the distance to move
        """
        if not self._check_down(map):
            self.y += dy

    def move_left(self, map: Map, dx: float):
        """move the player directly left if nothing is in his way

        :param map: the map on which the player moves
        :param dx: the distance to move
        """
        if not self._check_left(map):
            self.x -= dx

    def move_right(self, map: Map, dx: float):
        """move the player directly right if nothing is in his way

        :param map: the map on which the player moves
        :param dx: the distance to move
        """
        if not self._check_right(map):
            self.x += dx

    def _check_up(self, map: Map) -> bool:
        """check for collision on the upper side of the player"""
        self.y -= 0.5
        collision = pygame.sprite.spritecollideany(self, map.colliders)
        self.y += 0.5
        return collision is not None

    def _check_down(self, map: Map) -> bool:
        """check for collision on the bottom side of the player"""
        self.y += 0.5
        collision = pygame.sprite.spritecollideany(self, map.colliders)
        self.y -= 0.5
        return collision is not None

    def _check_left(self, map: Map) -> bool:
        """check for collision on the left side of the player"""
        if self.x <= 0:
            return True
        self.x -= 0.5
        collision = pygame.sprite.spritecollideany(self, map.colliders)
        self.x += 0.5
        return collision is not None

    def _check_right(self, map: Map) -> bool:
        """check for collision on the right side of the player"""
        if self.x >= map.size[0] - self.width:
            return True
        self.x += 0.5
        collision = pygame.sprite.spritecollideany(self, map.colliders)
        self.x -= 0.5
        return collision is not None
