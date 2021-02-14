from typing import Tuple
from pygame import Surface
from pytmx.util_pygame import load_pygame

class Map:
    def __init__(self, path: str):
        """
        create a new map
        :param path: the path of the tmx file to load from
        """
        self.tmx = load_pygame(path, pixelalpha=True)
        self.size: Tuple[int, int] = self.tmx.width * self.tmx.tilewidth, self.tmx.height * self.tmx.tileheight

    def get_dimensions(self) -> Tuple[int, int]:
        """
        get the dimensions of the map
        
        """
        return self.size

    def render(self, surface: Surface):
        """
        render the map to the given surface
        """
        if bg := self.tmx.background_color:
            surface.fill(bg)
        for layer in self.tmx.visible_tile_layers:
            # if not loaded like this, also object layers will be here
            layer = self.tmx.layers[layer]
            for x, y, image in layer.tiles():
                surface.blit(image, (x * self.tmx.tilewidth, y * self.tmx.tileheight))


    def check_collide(self, x: int, y: int) -> bool:
        """
        check if a field has a collision
        """
        for layer in self.tmx.visible_tile_layers:
            properties = self.tmx.get_tile_properties(x, y, layer)
            if properties and "colliders" in properties:
                return True
        return False
