from os import path
from jumpnrun.config import DATA_DIR, MUTED, MUSIC_VOLUME

import pygame

from jumpnrun.translate import t
from jumpnrun.utils import quit_game
from jumpnrun.widgets import Button, Label
from jumpnrun.screens import Screen
from jumpnrun.screens.about import AboutScreen
from jumpnrun.screens.level import LevelScreen


class MainScreen(Screen):
    def __init__(self, surface: pygame.Surface):
        super().__init__(surface, background_image=True)
        self.add_label(
            Label(
                caption="Jumpnrun",
                x=0.3,
                y=0.1,
                width=0.4,
                height=0.2,
                textsize=8,
            )
        )
        self.add_button(
            Button(
                caption=t("Start"),
                x=0.425,
                y=0.35,
            ),
            self.start_handler,
        )
        self.add_button(
            Button(
                caption=t("About Game"),
                x=0.4,
                y=0.5,
                width=0.2,
            ),
            self.about_handler,
        )
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
            pygame.mixer.music.set_volume(MUSIC_VOLUME)
            # play the music in a loop and fade it in
            pygame.mixer.music.play(loops=-1, fade_ms=500)

    def start_handler(self):
        LevelScreen(self.surface).run()

    def about_handler(self):
        AboutScreen(self.surface).run()
