from typing import List, Optional

import pygame

from jumpnrun.colors import BLACK2
from jumpnrun.translate import t
from jumpnrun.utils import quit_game
from jumpnrun.widgets import Button


def end_screen(
    surface: pygame.Surface,
    level: int,
    time: Optional[int],
    FPS: int,
    clock: pygame.time.Clock,
    levels: List[str],
) -> bool:
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
        hover_color=BLACK2,
    )
    back_button = Button(
        caption=t("Back to Title Screen"),
        x=0.325,
        y=0.6,
        width=0.35,
        textsize=0.09,
        hover_color=BLACK2,
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
        # render the back button
        back_button.render(surface)
        # render the next button it there is a next level
        if level < len(levels) - 1:
            next_button.render(surface)
        # update the screen
        pygame.display.flip()
        clock.tick(FPS)
