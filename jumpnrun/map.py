from pygame import Surface
from pytmx.util_pygame import load_pygame

class Map:
    def __init__(self, path: str):
        """
        create a new map
        :param path: the path of the tmx file to load from
        """
        self.tmx = load_pygame(path, pixelalpha=True)
        self.size = self.tmx.width * self.tmx.tilewidth, self.tmx.height * self.tmx.tileheight

    def render(self, surface: Surface):
        """
        render the map to the given surface
        """
        if bg := self.tmx.background_color:
            surface.fill(bg)
        for layer in self.tmx.visible_layers:
            for x, y, image in layer.tiles():
                surface.blit(image, (x * self.tmx.tilewidth, y * self.tmx.tileheight))
