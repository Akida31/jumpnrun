from typing import Optional
from os import path
import pygame

from skyjump.widgets import XAlign, YAlign
from skyjump.colors import WHITE
from skyjump.config import DATA_DIR


class Label:
    """
    a simple label
    """

    def __init__(
        self,
        caption: str,
        x: float,
        y: float,
        width: float = 0.15,
        height: float = 0.1,
        textsize: float = 3,
        font_file: str = path.join(DATA_DIR, "fonts", "carobtn.TTF"),
        color: pygame.Color = WHITE,
        bg_color: Optional[pygame.Color] = None,
        xalign: XAlign = XAlign.CENTER,
        yalign: YAlign = YAlign.CENTER,
        line_spacing: float = 1.25,
    ):
        self.caption = caption
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font_file = font_file
        # textsize is given in percent
        self.textsize = textsize / 100
        self.color = color
        self.bg_color = bg_color
        self.xalign = xalign
        self.yalign = yalign
        self.line_spacing = line_spacing
        # font rendering is a bottleneck in pygame
        # so cache the real size and font
        self._font: Optional[pygame.font.Font] = None
        self._fontsize: int = -1

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
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        # fill the background if there is one
        if self.bg_color:
            surface.fill(self.bg_color)
        # calculate the fontsize
        fontsize = round(self.textsize * out_surface.get_width())
        self._render_text(surface, width, height, fontsize)
        # blit the temporary surface
        out_surface.blit(surface, (x, y))

    def _render_text(
        self,
        out_surface: pygame.Surface,
        width: int,
        height: int,
        fontsize: int,
    ):
        """
        render the text to the level surface
        """
        # if the window size changes, the fontsize will be changed aswell
        if self._fontsize != fontsize:
            self._fontsize = fontsize
            self._font = pygame.font.Font(self.font_file, fontsize)
        # get all lines of the text
        lines = self.caption.splitlines()
        # create a temporary surface for the text
        font_height = self._font.size("xX")[1]
        text_height = font_height * ((len(lines) - 1) * self.line_spacing + 1)
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        # render each line to the surface
        for i, line in enumerate(lines):
            # create the text from the font with the given caption and color
            text = self._font.render(line, True, self.color)
            # determine the width of the rendered text
            font_width = self._font.size(line)[0]
            # calculate the xalignment
            if self.xalign == XAlign.LEFT:
                font_x: int = 0
            elif self.xalign == XAlign.CENTER:
                font_x: int = (width - font_width) // 2
            else:
                font_x: int = width - font_width
            font_y = round(i * self.line_spacing * font_height)
            surface.blit(text, (font_x, font_y, font_width, font_height))
        if self.yalign == YAlign.TOP:
            font_y: int = 0
        elif self.yalign == YAlign.CENTER:
            font_y: int = round((height - text_height) / 2)
        else:
            font_y: int = round(height - text_height)
        # blit the font to the temporary surface
        out_surface.blit(surface, (0, font_y, width, text_height))
