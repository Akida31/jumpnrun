from typing import List

import pygame

from jumpnrun.colors import BLACK2
from jumpnrun.translate import t
from jumpnrun.utils import quit_game
from jumpnrun.widgets import Button

from .level import level_screen


def main_screen(
    surface: pygame.Surface, FPS: int, clock: pygame.time.Clock, levels: List[str]
):
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
                if start_btn.check_on(surface):
                    level_screen(surface, FPS, clock, levels)
                elif quit_btn.check_on(surface):
                    quit_game()
        # render the background image
        width = surface.get_width()
        height = surface.get_height()
        surface.blit(pygame.transform.scale(image, (width, height)), (0, 0))
        # render the buttons
        start_btn.render(surface)
        quit_btn.render(surface)
        # update the screen
        pygame.display.flip()
        clock.tick(FPS)
