from typing import List

import pygame

from jumpnrun.translate import t
from jumpnrun.utils import quit_game
from jumpnrun.widgets import Button, Label

from .about import about_screen
from .level import level_screen

def main_screen(
    surface: pygame.Surface, fps: int, clock: pygame.time.Clock, levels: List[str]
):
    """
    the screen on the beginning of the game
    """
    headline = Label(
        caption="Jumpnrun",
        x=0.35,
        y=0.1,
        width=0.3,
        height=0.2,
    )
    start_btn = Button(
        caption=t("Start"),
        x=0.425,
        y=0.35,
    )
    about_btn = Button(
        caption=t("About Game"),
        x=0.4,
        y=0.5,
        width=0.2,
        textsize=0.16,
    )
    quit_btn = Button(
        caption=t("Quit Game"),
        x=0.4,
        y=0.65,
        width=0.2,
        textsize=0.16,
    )
    # load the music
    pygame.mixer.music.load("assets/music/Lonely_Witch.ogg")
    # play the music in a loop and fade it in
    pygame.mixer.music.play(loops=-1, fade_ms=500)

    image = pygame.image.load("assets/img/screenshot.png")
    while True:
        for event in pygame.event.get():
            # close the program if the window should be closed
            if event.type == pygame.QUIT:
                quit_game()
            # handle click
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn.check_on(surface):
                    level_screen(surface, fps, clock, levels)
                elif about_btn.check_on(surface):
                    about_screen(surface, fps, clock)
                elif quit_btn.check_on(surface):
                    quit_game()
        # render the background image
        width = surface.get_width()
        height = surface.get_height()
        surface.blit(pygame.transform.scale(image, (width, height)), (0, 0))
        # render the headline
        headline.render(surface)
        # render the buttons
        start_btn.render(surface)
        about_btn.render(surface)
        quit_btn.render(surface)
        # update the screen
        pygame.display.flip()
        clock.tick(fps)
