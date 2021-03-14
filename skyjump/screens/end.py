from typing import List, Optional

import pygame

from skyjump.translate import t
from skyjump.widgets import Button, Label
from skyjump.screens import Screen
from skyjump.level import LevelData


class EndScreen(Screen):
    def __init__(
        self,
        surface: pygame.Surface,
        level: int,
        time: float,
        levels: List[LevelData],
        highscore: Optional[float],
    ):
        """
        the screen after a level ended

        level: number of the completed level
        time: time in which the level is completed
        highscore: time of the highscore if the current time is higher or None
        """
        super().__init__(surface, background_image=True)
        self.add_label(
            Label(
                caption=f"{t('Completed Level #x in #ts')}".replace(
                    "#x", str(level + 1)
                ).replace("#t", str(time)),
                x=0.25,
                y=0.2,
                width=0.5,
            )
        )
        if highscore:
            highscore_text = f"Highscore: {highscore}s"
        else:
            highscore_text = t("New Highscore")
        self.add_label(
            Label(caption=highscore_text, x=0.25, y=0.35, width=0.5)
        )
        if level < len(levels) - 1:
            self.add_button(
                Button(
                    caption=t("Next Level"),
                    x=0.375,
                    y=0.6,
                    width=0.25,
                ),
                self.next_handler,
            )
        else:
            self.add_label(
                Label(
                    caption=t(
                        "Congratulations!\nYou completed all Levels.\n"
                        + "Now you can hunt for new highscores"
                    ),
                    x=0.2,
                    y=0.45,
                    width=0.6,
                    height=0.4,
                )
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
        self.status: bool = False

    def run(self):
        """
        run the screen

        returns if the next level should be started
        """
        super().run()
        return self.status

    def next_handler(self):
        self.status = True
        self.running = False

    def back_handler(self):
        self.running = False
