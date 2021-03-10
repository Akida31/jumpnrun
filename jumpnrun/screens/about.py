import pygame

from jumpnrun.translate import t
from jumpnrun.utils import quit_game
from jumpnrun.widgets import Button, Label, YAlign


def about_screen(surface: pygame.Surface, fps: int, clock: pygame.time.Clock):
    """
    the screen showing additional information about the game
    """
    caption = ["Game by Akida"]
    with open("credits.md") as f:
        for line in f.readlines():
            caption.append(line.strip())
    text = Label(
        caption="",
        x=0.05,
        y=0.1,
        width=0.9,
        height=0.7,
        textsize=0.025,
        yalign=YAlign.TOP
    )
    back_button = Button(
        caption=t("Back to Title Screen"),
        x=0.325,
        y=0.85,
        width=0.35,
        textsize=0.09,
    )
    line = 0
    ticks = 0
    while True:
        for event in pygame.event.get():
            # close the program if the window should be closed
            if event.type == pygame.QUIT:
                quit_game()
            # handle click
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # handle click of back button
                if back_button.check_on(surface):
                    return
        # fill background with complete black
        surface.fill(pygame.Color(0, 0, 0))
        # set the right text
        text.set_caption("\n".join(caption[line:line+9]))
        # render the text
        text.render(surface)
        # render the back button
        back_button.render(surface)
        # update the screen
        pygame.display.flip()
        clock.tick(fps)
        if ticks == fps:
            ticks = 0
            line += 1
        ticks += 1
