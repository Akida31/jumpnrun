from time import sleep

import pygame

from jumpnrun.colors import BLACK2
from jumpnrun.utils import LevelStatus
from jumpnrun.translate import t
from jumpnrun.utils import quit_game
from jumpnrun.widgets import Button


def pause_screen(surface: pygame.Surface) -> LevelStatus:
    """
    pause screen in the level
    """
    status = LevelStatus.Paused
    continue_button = Button(
        caption=t("Continue"),
        x=0.4,
        y=0.4,
        width=0.2,
        textsize=0.16,
        hover_color=BLACK2,
    )
    restart_button = Button(
        caption=t("Restart Level"),
        x=0.35,
        y=0.55,
        width=0.3,
        textsize=0.12,
        hover_color=BLACK2,
    )
    quit_button = Button(
        caption=t("Back to Title Screen"),
        x=0.325,
        y=0.7,
        width=0.35,
        textsize=0.09,
        hover_color=BLACK2,
    )
    while status == LevelStatus.Paused:
        for event in pygame.event.get():
            # close the program if the window should be closed
            if event.type == pygame.QUIT:
                quit_game()
            # handle click
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # handle click of continue button
                if continue_button.check_on(surface):
                    status = LevelStatus.Running
                    # give the player some time to react
                    sleep(0.5)
                # handle click of quit button
                elif quit_button.check_on(surface):
                    status = LevelStatus.Quit
                # handle click of restart button
                elif restart_button.check_on(surface):
                    status = LevelStatus.Restart
        # render the continue button
        continue_button.render(surface)
        # render the restart button
        restart_button.render(surface)
        # render the quit button
        quit_button.render(surface)
        # update the screen
        pygame.display.flip()
    return status
