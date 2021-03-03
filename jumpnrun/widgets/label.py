from typing import Optional

import pygame

from jumpnrun.widgets import XAlign, YAlign


class Label:
    """
    a simple label
    """

    def __init__(self, caption: str, x: float, y: float,
                 width: float, height: float,
                 font_file: str,
                 textsize: float,
                 color: pygame.Color,
                 bg_color: Optional[pygame.Color] = None,
                 xalign: XAlign = XAlign.CENTER,
                 yalign: YAlign = YAlign.CENTER):
        self.caption = caption
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font_file = font_file
        self.textsize = textsize
        self.color = color
        self.bg_color = bg_color
        self.xalign = xalign
        self.yalign = yalign

    def set_caption(self, caption: str):
        """
        set a new caption
        """
        self.caption = caption

    def set_bg_color(self, bg_color: Optional[pygame.Color]):
        """
        set a new background color
        """
        self.bg_color = bg_color

    def render(self, out_surface: pygame.Surface):
        """
        render the label on the given surface
        """
        # create absolute position values
        x = round(self.x * out_surface.get_width())
        y = round(self.y * out_surface.get_height())
        width = round(self.width * out_surface.get_width())
        height = round(self.height * out_surface.get_height())
        # create a temporary surface
        surface = pygame.Surface((width, height))
        # fill the background if there is one
        if self.bg_color:
            surface.fill(self.bg_color)
        # load the font and change it size with the window size
        font = pygame.font.Font(self.font_file, int(self.textsize * width))
        # create the text from the font with the given caption and color
        text = font.render(self.caption, True, self.color)
        # determine the size of the rendered text
        (font_width, font_height) = font.size(self.caption)
        # render the font with the right alignment
        if self.xalign == XAlign.LEFT:
            font_x: int = 0
        elif self.xalign == XAlign.CENTER:
            font_x: int = (width - font_width) // 2
        else:
            font_x: int = width - font_width
        if self.yalign == YAlign.TOP:
            font_y: int = 0
        elif self.yalign == YAlign.CENTER:
            font_y: int = (height - font_height) // 2
        else:
            font_y: int = height - font_height
        # blit the font to the temporary surface
        surface.blit(text, (font_x, font_y, font_width, font_height))
        # blit the temporary surface
        out_surface.blit(surface, (x, y))
