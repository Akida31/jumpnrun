from typing import List, Optional
import pygame

def load_spritesheet(filename: str, tile_width: int, 
        tile_height: Optional[int] = None) -> List[List[pygame.Surface]]:
    """
    load a spritesheet from a given file

    filename: the file from which the spritesheet should be loaded
    tile_width: the width of a single tile in the sheet
    tile_height: the height of a single tile in the sheet,
                 if not given the tile_width will be used
    """
    if tile_height is None:
        tile_height = tile_width
    image = pygame.image.load(filename).convert()
    width, height = image.get_size()
    sheet = []
    for x in range(width//tile_width):
        line = []
        for y in range(height//tile_height):
            rect = (x*tile_width, y* tile_height, tile_width, tile_height)
            line.append(image.subsurface(rect))
        sheet.append(line)
    return sheet
