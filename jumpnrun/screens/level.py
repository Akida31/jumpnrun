from typing import List
from os import path, listdir
from jumpnrun.config import DATA_DIR, MUTED, MUSIC_VOLUME

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
            # because of pythons internal logic two lambdas
            # are the only way to generate the click_handler dynamically
            click_handler = (lambda x: (lambda: self.level_start_handler(x)))(
                i
            )
            self.add_button(
                Button(
                    caption=f"{t('Level')} {i + 1}",
                    x=(i % 4) * 0.2 + 0.1,
                    y=(i // 4) * 0.2 + 0.2,
                ),
                click_handler,
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
        if not MUTED:
            music_dir = path.join(DATA_DIR, "music")
            # get path of all music files
            musics = list(
                map(lambda x: path.join(music_dir, x), listdir(music_dir))
            )
            # play the first music file
            pygame.mixer.music.load(musics[0])
            # queue all other music files
            for f in musics[1:]:
                pygame.mixer.music.queue(f)
            # play the music in a loop and fade it in
            pygame.mixer.music.set_volume(MUSIC_VOLUME)
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
