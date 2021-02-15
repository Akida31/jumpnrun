import pygame
from jumpnrun.utils import load_spritesheet

TILESIZE = 16


class Player(pygame.sprite.Sprite):
    def __init__(self, sprite_filename: str, x: int, y: int):
        # initialize the Sprite class
        super().__init__()
        # x and y coordinates are from the top left corner of the player
        self.x: int = x
        self.y: int = y
        self.width = self.height = TILESIZE * 2
        self.spritesheet = load_spritesheet(sprite_filename, TILESIZE * 2)
        # for applying gravity we need to save velocity and acceleration of the player

    def render(self, surface: pygame.Surface):
        image = self.spritesheet[0][2]
        image.set_colorkey((255,255,255))
        surface.blit(image, (self.x * TILESIZE, self.y * TILESIZE, self.width, self.height))
    

    def jump(self, map):
        self.y -= 1
        
    def move_left(self, map):
        if not (map.check_collide(self.x-1, self.y) or  map.check_collide(self.x-1, self.y+1)):
            self.x -= 1

    def move_right(self, map):
        if not (map.check_collide(self.x+2, self.y) or  map.check_collide(self.x+2, self.y+1)):
            self.x += 1

    def move_down(self, map):
        self.y += 1
