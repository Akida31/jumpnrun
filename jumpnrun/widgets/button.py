from typing import Optional

import pygame
from jumpnrun.widgets import Label, XAlign, YAlign

WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(40, 42, 54)


class Button:
    """
    a simple button

    a small wrapper for a label
    """

    def __init__(
            self,
            caption: str,
            x: float,
            y: float,
            width: float = 0.15,
            height: float = 0.1,
            textsize: float = 0.24,
            font_file: str = "assets/fonts/carobtn.TTF",
            color: pygame.Color = WHITE,
            bg_color: pygame.Color = BLACK,
            hover_color: Optional[pygame.Color] = None,
            xalign: XAlign = XAlign.CENTER,
            yalign: YAlign = YAlign.CENTER
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bg_color = bg_color
        if hover_color:
            self.hover_color = hover_color
        else:
            # TODO generate hover color manually
            self.hover_color = bg_color
        # create the label of the content
        self.label = Label(
            caption=caption,
            x=self.x,
            y=self.y,
            width=self.width,
            height=self.height,
            font_file=font_file,
            textsize=textsize,
            color=color,
            bg_color=bg_color,
            xalign=xalign,
            yalign=yalign
        )

    def render(self, out_surface: pygame.Surface):
        """
        render the button on the given surface
        """
        # change background color on hover
        if self.check_on(out_surface):
            bg_color = self.hover_color
        else:
            bg_color = self.bg_color
        self.label.set_bg_color(bg_color)
        # render the label
        self.label.render(out_surface)

    def check_on(self, surface: pygame.Surface) -> bool:
        """
        check if the mouse is over the button
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        x = round(self.x * surface.get_width())
        y = round(self.y * surface.get_height())
        width = round(self.width * surface.get_width())
        height = round(self.height * surface.get_height())
        return (x <= mouse_x <= x + width) and (y <= mouse_y <= y + height)
