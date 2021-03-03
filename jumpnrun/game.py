from typing import List

import pygame

from jumpnrun.level import Level
from jumpnrun.utils import Button, quit_game

WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(40, 42, 54)
BLACK2 = pygame.Color(68, 71, 90)


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
        self.levels: List[str] = ["assets/maps/0.tmx", "assets/maps/1.tmx"]

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
            x=0.45,
            y=0.45,
            width=0.1,
            height=0.1,
            textsize=0.35,
            font_file="assets/fonts/carobtn.TTF",
            color=WHITE,
            bg_color=BLACK,
            hover_color=BLACK2,
        )
        quit_btn = Button(
            caption="Quit",
            x=0.45,
            y=0.6,
            width=0.1,
            height=0.1,
            textsize=0.35,
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
                    quit_game()
                # handle click
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if start_btn.check_on(self.surface):
                        self.levelscreen()
                    elif quit_btn.check_on(self.surface):
                        quit_game()
            # render the background image
            width = self.surface.get_width()
            height = self.surface.get_height()
            self.surface.blit(pygame.transform.scale(image, (width, height)), (0, 0))
            # render the buttons
            start_btn.render(self.surface)
            quit_btn.render(self.surface)
            # update the screen
            pygame.display.update()

    def levelscreen(self):
        """
        give the player the ability to choose a level
        """
        level_buttons: List[Button] = []
        for i, level in enumerate(self.levels):
            button = Button(
                caption=f"Level {i+1}",
                x=(i%5) * 0.15 + 0.125,
                y=(i//5) * 0.15 + 0.2,
                width=0.1,
                height=0.1,
                textsize=0.3,
                font_file="assets/fonts/carobtn.TTF",
                color=WHITE,
                bg_color=BLACK,
                hover_color=BLACK2
            )
            level_buttons.append(button)
        back_button = Button(
            caption="Back",
            x=0.45,
            y=0.7,
            width=0.1,
            height=0.1,
            textsize=0.36,
            font_file="assets/fonts/carobtn.TTF",
            color=WHITE,
            bg_color=BLACK,
            hover_color=BLACK2
        )
        image = pygame.image.load("assets/img/screenshot.png")
        while True:
            for event in pygame.event.get():
                # close the program if the window should be closed
                if event.type == pygame.QUIT:
                    quit_game()
                # handle click
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # handle click of the level buttons
                    for i, button in enumerate(level_buttons):
                        # start the clicked level
                        if button.check_on(self.surface):
                            level = i
                            level = Level(self.levels[level], self.surface)
                            _time = level.run()
                    # handle click of back button
                    if back_button.check_on(self.surface):
                        return
            # render the background image
            width = self.surface.get_width()
            height = self.surface.get_height()
            self.surface.blit(pygame.transform.scale(image, (width, height)), (0, 0))
            # render the buttons
            for button in level_buttons:
                button.render(self.surface)
            # render the back button
            back_button.render(self.surface)
            # update the screen
            pygame.display.update()

