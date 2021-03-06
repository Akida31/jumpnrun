from typing import List, Optional

import pygame

from jumpnrun.level import Level, LevelStatus
from jumpnrun.translate import Language, t
from jumpnrun.utils import quit_game
from jumpnrun.widgets import Button

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
        self.levels: List[str] = ["assets/maps/0.tmx", "assets/maps/1.tmx", "assets/maps/test.tmx"]
        # set language
        t.change_language(Language.DE)

    def run(self):
        """
        run the game
        """
        self.mainscreen()

    def mainscreen(self):
        """
        the screen on the beginning of the game
        """
        # TODO headline
        start_btn = Button(
            caption=t("Start"),
            x=0.425,
            y=0.45,
            hover_color=BLACK2,
        )
        quit_btn = Button(
            caption=t("Quit Game"),
            x=0.4,
            y=0.6,
            width=0.2,
            textsize=0.16,
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
        # TODO headline
        level_buttons: List[Button] = []
        for i, level in enumerate(self.levels):
            button = Button(
                caption=f"{t('Level')} {i + 1}",
                x=(i % 4) * 0.2 + 0.1,
                y=(i // 4) * 0.2 + 0.2,
                textsize=0.2,
                hover_color=BLACK2
            )
            level_buttons.append(button)
        back_button = Button(
            caption=t("Back to Title Screen"),
            x=0.325,
            y=0.7,
            width=0.35,
            textsize=0.09,
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
                            start = True
                            while start:
                                level = Level(self.levels[i], self.surface)
                                (status, time) = level.run()
                                # show endscreen only if the level was completed
                                if status == LevelStatus.Finished:
                                    start = self.endscreen(i, time)
                                    i += 1
                                elif status == LevelStatus.Restart:
                                    pass
                                elif status == LevelStatus.Quit:
                                    start = False
                            return
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

    def endscreen(self, level: int, time: Optional[int]) -> bool:
        """
        the screen after a level ended

        level: the number of the completed level
        time: the time in which the level is completed

        returns if the next level should be started
        """
        # TODO show time
        print(f"completed Level {level} in {time}")
        next_button = Button(
            caption=t("Next Level"),
            x=0.375,
            y=0.45,
            width=0.25,
            textsize=0.14,
            hover_color=BLACK2
        )
        back_button = Button(
            caption=t("Back to Title Screen"),
            x=0.325,
            y=0.6,
            width=0.35,
            textsize=0.09,
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
                    # handle click of back button
                    if back_button.check_on(self.surface):
                        return False
                    # handle click of next button
                    if next_button.check_on(self.surface):
                        return True
            # render the background image
            width = self.surface.get_width()
            height = self.surface.get_height()
            self.surface.blit(pygame.transform.scale(image, (width, height)), (0, 0))
            # render the back button
            back_button.render(self.surface)
            # render the next button it there is a next level
            if level < len(self.levels) - 1:
                next_button.render(self.surface)
            # update the screen
            pygame.display.update()
