import pygame
import sys

from .characters.player import Player
from .map import Map

class Game:
    def __init__(self):
        pygame.init()
        self.width: int = 800
        self.height: int = 400
        self.surface: pygame.Surface = pygame.display.set_mode((self.width, self.height), flags=pygame.RESIZABLE)
        self.player = Player()
        self.objects = []
        self.map = Map("maps/test.tmx")
        self.running = True

    def run(self):
        while self.running:
            self.on_events()
            self.render()
        self.quit()

    def on_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.VIDEORESIZE:
                self.width, self.height = event.size
            elif event.type == pygame.KEYDOWN:
                self.on_key(event.key)

    def render(self):
        map_width, map_height = self.map.get_dimensions()
        # create temporary surface for transforming
        surface = pygame.Surface((map_width, map_height))
        self.map.render(surface)
        for o in self.objects:
            o.render(surface)
        self.player.render(surface)
        # render the temporary surface to the full screen
        self.surface.blit(pygame.transform.scale(surface, (self.width, self.height)), (0, 0))
        pygame.display.update()

    def quit(self):
        self.running = False
        pygame.quit()
        sys.exit()

    def on_key(self, key):
        if key == pygame.KSCAN_ESCAPE:
            self.quit()
        elif key == pygame.K_w:
            self.player.jump()
        elif key == pygame.K_a:
            self.player.move_left()
        elif key == pygame.K_d:
            self.player.move_right()
