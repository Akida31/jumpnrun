import json
from os import listdir, path
from typing import List, Optional

import pygame

from jumpnrun.config import DATA_DIR, LEVEL_FILE, MUSIC_VOLUME, MUTED
from jumpnrun.level import Level, LevelData
from jumpnrun.screens import Screen
from jumpnrun.screens.end import EndScreen
from jumpnrun.translate import t
from jumpnrun.utils import LevelStatus
from jumpnrun.widgets import Button, Label
from jumpnrun.colors import GREY


class LevelScreen(Screen):
    def __init__(self, surface: pygame.Surface):
        super().__init__(surface, background_image=True)
        # load all the levels of the levels file
        self.levels: List[LevelData] = []
        with open(LEVEL_FILE) as f:
            for level in json.load(f):
                self.levels.append(LevelData(level))
        for i, level in enumerate(self.levels):
            # draw label instead of button for unlocked levels
            caption = f"{t('Level')} {level.name}"
            x = (i % 4) * 0.2 + 0.1
            y = (i // 4) * 0.2 + 0.2
            if not level.unlocked:
                self.add_label(Label(caption=caption, x=x, y=y, bg_color=GREY))
            else:
                # because of pythons internal logic two lambdas
                # are the only way to generate the click_handler dynamically
                click_handler = (
                    lambda x: (lambda: self.level_start_handler(x))
                )(i)
                self.add_button(
                    Button(caption=caption, x=x, y=y),
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
                # save the highscore
                highscore: Optional[float] = self.levels[level_nr].highscore
                if highscore == 0.0 or highscore > time:
                    self.levels[level_nr].highscore = time
                    highscore = None
                # unlock the next level
                if level_nr < len(self.levels) - 1:
                    self.levels[level_nr + 1].unlocked = True
                # save the changes
                with open(LEVEL_FILE, "w") as f:
                    json.dump(self.levels, f, default=vars)
                start = EndScreen(
                    self.surface, level_nr, time, self.levels, highscore
                ).run()
                level_nr += 1
            elif status == LevelStatus.Restart:
                pass
            elif status == LevelStatus.Quit:
                start = False
        self.back_handler()
