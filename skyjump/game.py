import pygame
from os import path

from skyjump.config import LANGUAGE, DATA_DIR
from skyjump.screens.main import MainScreen
from skyjump.translate import t

# FPS dont have to be so high for an UI
# and higher FPS increased the CPU usage massively
FPS: int = 30


class Game:
    """base class for the skyjump game"""

    def __init__(self):
        """initialize the game"""
        # initialize pygame
        pygame.init()
        # set the title of the window
        pygame.display.set_caption("Skyjump")
        # set the icon of the window
        icon = pygame.image.load(path.join(DATA_DIR, "img", "icon.png"))
        pygame.display.set_icon(icon)
        # the initial size of the window
        self.width: int = 1200
        self.height: int = 600
        # flags for the window
        # doublebuf and opengl improve the performance massively
        flags = pygame.RESIZABLE | pygame.DOUBLEBUF
        # create the window
        self.surface: pygame.Surface = pygame.display.set_mode(
            (self.width, self.height), flags=flags
        )
        # set language
        t.change_language(LANGUAGE)
        # create a clock to slow down the frames to the FPS
        # because it uses less CPU
        self.clock = pygame.time.Clock()

    def run(self):
        """run the game"""
        MainScreen(self.surface).run()
