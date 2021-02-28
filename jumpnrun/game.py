import pygame
import sys
from typing import List, Optional

from .level import Level
from .screens.levelchooser import choose_level
from .screens.endscreen import EndScreen

class Game:
    def __init__(self):
        """
        initialize the game
        """
        # initialize pygame
        pygame.init()
        # set the title of the window
        pygame.display.set_caption("Jumpnrun")
        self.width: int = 1200
        self.height: int = 600
        # create the window
        self.surface: pygame.Surface = pygame.display.set_mode((self.width, self.height), flags=pygame.RESIZABLE)
        # location of all levels
        self.levels: List[str] = ["assets/maps/test.tmx"]

    def quit(self):
        """
        quit the game
        """
        pygame.quit()
        sys.exit()

    def run(self):
        """
        run the game
        """
        levelnr = choose_level(self.surface, self.levels)
        level = Level(self.levels[levelnr], self.surface)
        time = level.run()
        EndScreen(self.surface, levelnr, time)

