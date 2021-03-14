import pygame

from skyjump.translate import t
from skyjump.widgets import Button, Label, YAlign
from skyjump.screens import Screen


class AboutScreen(Screen):
    """
    the screen showing additional information about the game
    """

    def __init__(self, surface: pygame.Surface):
        super().__init__(surface)
        self.caption = ["Game by Akida"]
        with open("credits.md") as f:
            for line in f.readlines():
                # remove the #
                line = line.replace("#", "")
                # strip the newlines
                line = line.strip()
                self.caption.append(line.strip())
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
        self.line = 0
        self.ticks = 0

    def render(self):
        # fill background with complete black
        self.surface.fill(pygame.Color(0, 0, 0))
        # set the right text
        line = self.ticks // 30
        self.text.set_caption("\n".join(self.caption[line : line + 9]))
        super().render()
        self.ticks += 1

    def back_handler(self):
        self.running = False
