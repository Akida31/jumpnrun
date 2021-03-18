import pygame

from skyjump.utils import LevelStatus
from skyjump.translate import t
from skyjump.widgets import Button
from skyjump.screens import Screen


class PauseScreen(Screen):
    """pause screen in the level"""

    def __init__(self, surface: pygame.Surface):
        """create a pause screen

        :param surface: the surface to which the screen should be rendered
        """
        super().__init__(surface, background_image=True)
        # status is representing the status of the level, not of the screen
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
        """set the levelstatus

        :param status: the new status of the level
        """
        self.status = status
        # keep running if the level status is paused
        self.running = status == LevelStatus.Paused

    def run(self) -> LevelStatus:
        """run the screen

        wrapper for the superclass
        :returns: the status of the level
        """
        super().run()
        return self.status

    def continue_handler(self):
        """continue the level after a short time"""
        self.set_status(LevelStatus.Running)
        # give the player some time to react
        pygame.time.wait(500)

    def restart_handler(self):
        """restart the current level"""
        self.set_status(LevelStatus.Restart)

    def quit_handler(self):
        """quit the current level and go to the main screen"""
        self.set_status(LevelStatus.Quit)
