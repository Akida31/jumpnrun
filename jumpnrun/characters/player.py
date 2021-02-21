from typing import List
import pygame
from jumpnrun.utils import load_spritesheet
import time

TILESIZE = 16


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

    def render(self, surface: pygame.Surface):
        image = self.sprite
        image.set_colorkey((255,255,255))
        surface.blit(image, (self.x, self.y, self.width, self.height))
    

    def apply_physics(self, map):
        # gravity
        if not self._check_down(map):
            self.acceleration[1] += 6
        # apply acceleration to velocity
        # move player
        x_acc = round(self.acceleration[0])
        y_acc = round(self.acceleration[1])
        # let the player look like he moves
        self.sprite = self.spritesheet[8][2]
        if y_acc != 0:
            self.sprite = self.spritesheet[16][2]

        if x_acc > 0:
            acc = self.move_right
        else:
            acc = self.move_left
        for x in range(abs(x_acc)):
            acc(map, 1)
        if y_acc > 0:
            acc = self.move_down
        else:
            acc = self.move_up
        for y in range(abs(y_acc)):
            acc(map, 1)
        # reset acceleration
        self.acceleration = [0, 0]

    def jump(self, map):
        if self._check_down(map):
            self.acceleration[1] -= 42

    def move_up(self, map, dy):
        if not self._check_up(map):
            self.y -= dy
        
    def move_left(self, map, dx=8):
        if not (map.check_collide(self.x / TILESIZE - 0.5, self.y / TILESIZE) 
                or  map.check_collide(self.x / TILESIZE - 0.5 , self.y / TILESIZE +1)):
            self.x -= dx

    def move_right(self, map, dx=8):
        if not (map.check_collide(self.x / TILESIZE + 1, self.y / TILESIZE) 
                or  map.check_collide(self.x / TILESIZE + 1, self.y / TILESIZE +1)):
            self.x += dx

    def move_down(self, map, dy=8):
        if not self._check_down(map):
            self.y += dy

    def _check_down(self, map):
        return (map.check_collide(self.x / TILESIZE + 0.5, self.y / TILESIZE + 1.5) 
                or map.check_collide(self.x / TILESIZE, self.y / TILESIZE + 1.5))

    def _check_up(self, map):
        return (map.check_collide(self.x / TILESIZE + 0.5, self.y / TILESIZE) 
                or map.check_collide(self.x / TILESIZE, self.y / TILESIZE))
