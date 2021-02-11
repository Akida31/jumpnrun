import pygame
import sys

from .characters.player import Player
from .map import Map

class Game:
    def __init__(self):
        pygame.init()
        width: int = 300
        height: int = 300
        self.surface: pygame.Surface = pygame.display.set_mode((width, height))
        self.objects = [Player()]
        self.map = Map("maps/test.tmx")
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
            self.render()
        self.quit()

    def render(self):
        for o in self.objects:
            o.render(self.surface)
        self.map.render(self.surface)
        pygame.display.update()

    def quit(self):
        self.running = False
        pygame.quit()
        sys.exit()

