import pygame

from jumpnrun.screens.main import MainScreen
from jumpnrun.translate import t
from os import path, listdir
from jumpnrun.config import DATA_DIR, LANGUAGE

# FPS dont have to be so high for an UI
# higher FPS increased the CPU usage massively
FPS: int = 30


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
        # flags for the window
        # doublebuf and opengl improve the performance massively
        flags = pygame.RESIZABLE | pygame.DOUBLEBUF
        # create the window
        self.surface: pygame.Surface = pygame.display.set_mode(
            (self.width, self.height), flags=flags
        )
        # location of all levels
        map_dir = path.join(DATA_DIR, "maps")
        # load all files from the maps directory
        # which end with the tmx extension
        levels = {}
        self.levels = []
        for f in listdir(map_dir):
            (name, ext) = path.splitext(path.basename(f))
            # the file should only be loaded if the name is right:
            # a number followed by the extension ".tmx"
            if ext != ".tmx" or not name.isnumeric():
                continue
            levels[name] = f

        # sort the levels by their number and save their full path
        for level in sorted(levels, key=int):
            self.levels.append(path.join(map_dir, levels[level]))
        # set language
        t.change_language(LANGUAGE)
        # set the framerate of the game
        self.clock = pygame.time.Clock()

    def run(self):
        """
        run the game
        """
        MainScreen(self.surface, self.levels).run()
