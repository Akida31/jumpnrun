from typing import List, Optional

import pygame

from jumpnrun.translate import t
from jumpnrun.widgets import Button, Label
from jumpnrun.screens import Screen


class EndScreen(Screen):
    def __init__(
        self,
        surface: pygame.Surface,
        level: int,
        time: Optional[float],
        levels: List[str],
    ):
        """
        the screen after a level ended

        level: the number of the completed level
        time: the time in which the level is completed
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
        if level < len(levels) - 1:
            self.add_button(
                Button(
                    caption=t("Next Level"),
                    x=0.375,
                    y=0.45,
                    width=0.25,
                ),
                self.next_handler,
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
