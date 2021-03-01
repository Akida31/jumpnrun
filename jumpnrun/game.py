import pygame
import sys
from typing import List, Optional

from .level import Level
from .utils import Button


WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)
BLACK2 = pygame.Color(15, 15, 15)


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
        self.surface: pygame.Surface = pygame.display.set_mode(
            (self.width, self.height), flags=pygame.RESIZABLE
        )
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
        self.mainscreen()

    def mainscreen(self):
        """
        the screen on the beginning of the game
        """
        start_btn = Button(
            caption="Start",
            x=0.4,
            y=0.45,
            width=0.2,
            height=0.1,
            textsize=36,
            font_file="assets/fonts/carobtn.TTF",
            color=WHITE,
            bg_color=BLACK,
            hover_color=BLACK2,
        )
        image = pygame.image.load("assets/img/screenshot.png")
        # TODO settings screen
        while True:
            for event in pygame.event.get():
                # close the program if the window should be closed
                if event.type == pygame.QUIT:
                    self.quit()
                # handle click
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if start_btn.check_on(self.surface):
                        self.levelscreen()
            # render
            width = self.surface.get_width()
            height = self.surface.get_height()
            self.surface.blit(pygame.transform.scale(image, (width, height)), (0, 0))
            start_btn.render(self.surface)
            pygame.display.update()

    def levelscreen(self):
        # TODO give the player an option to choose the level
        level = 0
        level = Level(self.levels[level], self.surface)
        time = level.run()
