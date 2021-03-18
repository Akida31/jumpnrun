import pygame

from skyjump.translate import t
from skyjump.widgets import Button, Label, YAlign
from skyjump.screens import Screen


class AboutScreen(Screen):
    """the screen showing additional information about the game"""

    def __init__(self, surface: pygame.Surface):
        """create an about screen

        :param surface: the surface to which the screen should be rendered
        """
        super().__init__(surface)
        # creator should be on top of the credits
        self.caption = ["Game by Akida"]
        with open("credits.md") as f:
            for line in f.readlines():
                # remove the #'s
                line = line.replace("#", "")
                # strip the newlines
                line = line.strip()
                self.caption.append(line.strip())
        # the caption will be rendered in the text label
        # this has to be created in an extra variable
        # so we can change the caption later
        self.text = Label(
            caption="",
            x=0.05,
            y=0.1,
            width=0.9,
            height=0.7,
            textsize=2.25,
            yalign=YAlign.TOP,
        )
        self.add_label(self.text)
        self.add_button(
            Button(
                caption=t("Back to Title Screen"),
                x=0.325,
                y=0.85,
                width=0.35,
            ),
            self.back_handler,
        )
        # the current line of the caption
        self.line: int = 0
        # the caption should not switch immediately
        # so we have to create a delay
        self.ticks: int = 0

    def render(self):
        """render the about screen"""
        # fill background with complete black
        self.surface.fill(pygame.Color(0, 0, 0))
        # set the right text
        line = self.ticks // 30
        self.text.set_caption("\n".join(self.caption[line: line + 9]))
        super().render()
        self.ticks += 1

    def back_handler(self):
        """return to the main screen"""
        self.running = False
