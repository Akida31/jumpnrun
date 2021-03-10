from typing import List

import pygame

from jumpnrun.colors import BLACK2
from jumpnrun.level import Level
from jumpnrun.translate import t
from jumpnrun.utils import LevelStatus, quit_game
from jumpnrun.widgets import Button

from .end import end_screen


def level_screen(
    surface: pygame.Surface, fps: int, clock: pygame.time.Clock, levels: List[str]
):
    """
    give the player the ability to choose a level
    """
    # TODO headline
    level_buttons: List[Button] = []
    for i, level in enumerate(levels):
        button = Button(
            caption=f"{t('Level')} {i + 1}",
            x=(i % 4) * 0.2 + 0.1,
            y=(i // 4) * 0.2 + 0.2,
            textsize=0.2,
            hover_color=BLACK2,
        )
        level_buttons.append(button)
    back_button = Button(
        caption=t("Back to Title Screen"),
        x=0.325,
        y=0.7,
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
                # handle click of the level buttons
                for i, button in enumerate(level_buttons):
                    # start the clicked level
                    if button.check_on(surface):
                        start = True
                        # load the level music
                        pygame.mixer.music.load("assets/music/little_town.ogg")
                        pygame.mixer.music.queue("assets/music/The_Old_Tower_Inn.ogg")
                        pygame.mixer.music.queue("assets/music/the_field_of_dreams.ogg")
                        pygame.mixer.music.queue("assets/music/Fantasy_Choir_1.ogg")
                        pygame.mixer.music.queue("assets/music/Fantasy_Choir_2.ogg")
                        pygame.mixer.music.queue("assets/music/Fantasy_Choir_3.ogg")
                        # play the music in a loop and fade it in
                        pygame.mixer.music.play(loops=-1, fade_ms=500)
                        while start:
                            level = Level(levels[i], surface)
                            (status, time) = level.run()
                            # show endscreen only if the level was completed
                            if status == LevelStatus.Finished:
                                start = end_screen(surface, i, time, fps, clock, levels)
                                i += 1
                            elif status == LevelStatus.Restart:
                                pass
                            elif status == LevelStatus.Quit:
                                start = False
                        return
                # handle click of back button
                if back_button.check_on(surface):
                    return
        # render the background image
        width = surface.get_width()
        height = surface.get_height()
        surface.blit(pygame.transform.scale(image, (width, height)), (0, 0))
        # render the buttons
        for button in level_buttons:
            button.render(surface)
        # render the back button
        back_button.render(surface)
        # update the screen
        pygame.display.flip()
        clock.tick(fps)
