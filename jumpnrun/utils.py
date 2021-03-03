from typing import List, Optional, Tuple
import pygame
import sys

# Tilesize of the map
TILESIZE: int = 16


def quit_game():
    """
    quit the game
    """
    pygame.quit()
    sys.exit()


def load_spritesheet(
    filename: str,
    tile_width: int,
    tile_height: Optional[int] = None,
    offset_x: int = 0,
    offset_y: int = 0,
    spacing_x: int = 0,
    spacing_y: int = 0,
    alphacolor: Optional[Tuple[int, int, int]] = None,
) -> List[List[pygame.Surface]]:
    """
    load a spritesheet from a given file

    filename: the file from which the spritesheet should be loaded
    tile_width: the width of a single tile in the sheet
    tile_height: the height of a single tile in the sheet,
                 if not given the tile_width will be used
    offset_x/ offset_y: the offset of the sprite in the top left corner in px
    spacing_x/ spacing_y: the spacing between the sprites
    alphacolor: the background alpha color
    """
    if tile_height is None:
        tile_height = tile_width
    image = pygame.image.load(filename).convert()
    # TODO is this still necessary?
    # if alphacolor is None:
    # determine the alphacolor from the pixel in the top left corner
    # alphacolor = image.get_at((0, 0))
    # image.set_colorkey(alphacolor)
    width, height = image.get_size()
    tiles_x = (width - offset_x + spacing_x) // (tile_width + spacing_x)
    tiles_y = (height - offset_y + spacing_y) // (tile_height + spacing_y)
    sheet = []
    for x in range(tiles_x):
        line = []
        for y in range(tiles_y):
            # x1, y1 -> upper left corner
            x1 = offset_x + x * (tile_width + spacing_x)
            y1 = offset_y + y * (tile_height + spacing_y)
            rect = (x1, y1, tile_width, tile_height)
            line.append(image.subsurface(rect))
        sheet.append(line)
    return sheet


class Button:
    """
    a simple button
    """

    def __init__(
        self,
        caption: str,
        x: float,
        y: float,
        width: float,
        height: float,
        textsize: float,
        font_file: str,
        color: pygame.Color,
        bg_color: pygame.Color,
        hover_color: Optional[pygame.Color] = None,
    ):
        self.caption = caption
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.textsize = textsize
        self.font_file = font_file
        self.color = color
        self.bg_color = bg_color
        if hover_color:
            self.hover_color = hover_color
        else:
            # TODO generate hover color manually
            self.hover_color = bg_color

    def rect(self, surface: pygame.Surface) -> Tuple[int, int, int, int]:
        """
        determine the position and size of the button

        returns (x, y, width, height)
        """
        x = round(self.x * surface.get_width())
        y = round(self.y * surface.get_height())
        width = round(self.width * surface.get_width())
        height = round(self.height * surface.get_height())
        return x, y, width, height


    def render(self, out_surface: pygame.Surface):
        """
        render the button on the given surface
        """
        x, y, width, height = self.rect(out_surface)
        # create a temporary surface
        surface = pygame.Surface((width, height))
        # change background color on hover
        if self.check_on(out_surface):
            surface.fill(self.hover_color)
        else:
            surface.fill(self.bg_color)
        # load the font and change it size with the window size
        font = pygame.font.Font(self.font_file, int(self.textsize * width))
        # create the text from the font with the given caption and color
        text = font.render(self.caption, True, self.color)
        # determine the size of the rendered text
        (font_width, font_height) = font.size(self.caption)
        # render the font in the center of the surface
        font_x: int = (width - font_width) // 2
        font_y: int = (height - font_height) // 2
        surface.blit(text, (font_x, font_y, font_width, font_height))
        # blit the temporary surface
        out_surface.blit(surface, (x, y))

    def check_on(self, surface: pygame.Surface) -> bool:
        """
        check if the mouse is over the button
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        x, y, width, height = self.rect(surface)
        return (x <= mouse_x <= x + width) and (y <= mouse_y <= y + height)
