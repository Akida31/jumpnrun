import sys
from enum import Enum
from typing import List, Optional

import pygame

# Tilesize of the map
TILESIZE: int = 16

# FPS of the game
FPS: int = 60


class LevelStatus(Enum):
    Paused = (0,)
    Running = (1,)
    Finished = (2,)
    Quit = (3,)
    Restart = 4


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
