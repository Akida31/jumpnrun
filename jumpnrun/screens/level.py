from typing import List

import pygame

from jumpnrun.level import Level
from jumpnrun.translate import t
from jumpnrun.utils import LevelStatus
from jumpnrun.widgets import Button
from jumpnrun.screens import Screen
from jumpnrun.screens.end import EndScreen


class LevelScreen(Screen):
    def __init__(self, surface: pygame.Surface, levels: List[str]):
        super().__init__(surface, background_image=True)
        for i in range(len(levels)):
            self.add_button(
                Button(
                    caption=f"{t('Level')} {i + 1}",
                    x=(i % 4) * 0.2 + 0.1,
                    y=(i // 4) * 0.2 + 0.2,
                ),
                lambda: self.level_start_handler(i),
            )
        self.add_button(
            Button(
                caption=t("Back to Title Screen"),
                x=0.325,
                y=0.85,
                width=0.35,
            ),
            self.back_handler,
        )
        self.levels = levels

    def back_handler(self):
        self.running = False

    def level_start_handler(self, level_nr: int):
        pygame.mixer.music.load("assets/music/little_town.ogg")
        pygame.mixer.music.queue("assets/music/The_Old_Tower_Inn.ogg")
        pygame.mixer.music.queue("assets/music/the_field_of_dreams.ogg")
        pygame.mixer.music.queue("assets/music/Fantasy_Choir_1.ogg")
        pygame.mixer.music.queue("assets/music/Fantasy_Choir_2.ogg")
        pygame.mixer.music.queue("assets/music/Fantasy_Choir_3.ogg")
        # play the music in a loop and fade it in
        pygame.mixer.music.play(fade_ms=500)
        start = True
        while start:
            level = Level(self.levels[level_nr], self.surface)
            (status, time) = level.run()
            # show endscreen only if the level was completed
            if status == LevelStatus.Finished:
                start = EndScreen(
                    self.surface, level_nr, time, self.levels
                ).run()
                level_nr += 1
            elif status == LevelStatus.Restart:
                pass
            elif status == LevelStatus.Quit:
                start = False
        self.back_handler()
