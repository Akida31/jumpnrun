import pygame

from jumpnrun.utils import LevelStatus
from jumpnrun.translate import t
from jumpnrun.widgets import Button
from jumpnrun.screens import Screen


class PauseScreen(Screen):
    """
    pause screen in the level
    """

    def __init__(self, surface: pygame.Surface):
        super().__init__(surface, background_image=True)
        self.status = LevelStatus.Paused
        self.add_button(
            Button(
                caption=t("Continue"),
                x=0.4,
                y=0.4,
                width=0.2,
            ),
            self.continue_handler,
        )
        self.add_button(
            Button(
                caption=t("Restart Level"),
                x=0.35,
                y=0.55,
                width=0.3,
            ),
            self.restart_handler,
        )
        self.add_button(
            Button(
                caption=t("Back to Title Screen"),
                x=0.325,
                y=0.85,
                width=0.35,
            ),
            self.quit_handler,
        )

    def set_status(self, status: LevelStatus):
        """
        set the levelstatus
        """
        self.status = status
        self.running = status == LevelStatus.Paused

    def run(self) -> LevelStatus:
        super().run()
        return self.status

    def continue_handler(self):
        self.set_status(LevelStatus.Running)
        # give the player some time to react
        pygame.time.wait(500)

    def restart_handler(self):
        self.set_status(LevelStatus.Restart)

    def quit_handler(self):
        self.set_status(LevelStatus.Quit)
