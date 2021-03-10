from typing import List, Optional

import pygame

from jumpnrun.translate import t
from jumpnrun.utils import quit_game
from jumpnrun.widgets import Button, Label


def end_screen(
    surface: pygame.Surface,
    level: int,
    time: Optional[int],
    fps: int,
    clock: pygame.time.Clock,
    levels: List[str],
) -> bool:
    """
    the screen after a level ended

    level: the number of the completed level
    time: the time in which the level is completed

    returns if the next level should be started
    """
    time_label = Label(
        caption=f"{t('Completed Level #x in #ts')}"
            .replace("#x", str(level + 1))
            .replace("#t", str(time)),
        x=0.25,
        y=0.2,
        width=0.5,
        textsize=0.06,
    )
    next_button = Button(
        caption=t("Next Level"),
        x=0.375,
        y=0.45,
        width=0.25,
        textsize=0.14,
    )
    back_button = Button(
        caption=t("Back to Title Screen"),
        x=0.325,
        y=0.6,
        width=0.35,
        textsize=0.09,
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
                if back_button.check_on(surface):
                    return False
                # handle click of next button
                if next_button.check_on(surface):
                    return True
        # render the background image
        width = surface.get_width()
        height = surface.get_height()
        surface.blit(pygame.transform.scale(image, (width, height)), (0, 0))
        time_label.render(surface)
        back_button.render(surface)
        # render the next button it there is a next level
        if level < len(levels) - 1:
            next_button.render(surface)
        # update the screen
        pygame.display.flip()
        clock.tick(fps)
