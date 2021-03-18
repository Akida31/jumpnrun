from os import path
from skyjump.config import DATA_DIR, MUTED, MUSIC_VOLUME

import pygame

from skyjump.translate import t
from skyjump.utils import quit_game
from skyjump.widgets import Button, Label
from skyjump.screens import Screen
from skyjump.screens.about import AboutScreen
from skyjump.screens.level import LevelScreen


class MainScreen(Screen):
    """the main (or title) screen of the game"""

    def __init__(self, surface: pygame.Surface):
        """create the main screen with all of its widgets

        :param surface: the surface to which the screen will be rendered
        """
        # initialize the super class
        super().__init__(surface, background_image=True)
        # add the title label
        self.add_label(
            Label(
                caption="Skyjump",
                x=0.3,
                y=0.1,
                width=0.4,
                height=0.2,
                textsize=8,
            )
        )
        # add the button to go to the level choosing screen
        self.add_button(
            Button(
                caption=t("Start"),
                x=0.425,
                y=0.35,
            ),
            self.start_handler,
        )
        # add the button to go to the about screen
        self.add_button(
            Button(
                caption=t("About Game"),
                x=0.4,
                y=0.5,
                width=0.2,
            ),
            self.about_handler,
        )
        # add a button to quit the game
        self.add_button(
            Button(
                caption=t("Quit Game"),
                x=0.4,
                y=0.65,
                width=0.2,
            ),
            quit_game,
        )
        if not MUTED:
            # load the music
            pygame.mixer.music.load(
                path.join(DATA_DIR, "music", "Lonely_Witch.ogg")
            )
            # set the volume according to the music volume setting
            pygame.mixer.music.set_volume(MUSIC_VOLUME)
            # play the music in a loop and fade it in
            pygame.mixer.music.play(loops=-1, fade_ms=500)

    def start_handler(self):
        """start the game by going to the level screen"""
        LevelScreen(self.surface).run()

    def about_handler(self):
        """go to the about screen"""
        AboutScreen(self.surface).run()
