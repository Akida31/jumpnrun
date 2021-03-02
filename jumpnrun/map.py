from typing import Tuple, List

from pygame import Surface
from pytmx.util_pygame import load_pygame


class Map:
    def __init__(self, path: str):
        """
        create a new map
        :param path: the path of the tmx file to load from
        """
        # load the map from the given TiledMap-File
        self.tmx = load_pygame(path, pixelalpha=True)
        # save the size of the map
        self.size: Tuple[int, int] = (
            self.tmx.width * self.tmx.tilewidth,
            self.tmx.height * self.tmx.tileheight,
        )

    def get_size(self) -> Tuple[int, int]:
        """
        get the size of the map

        returns width, height
        """
        return self.size

    def get_player_position(self) -> Tuple[int, int]:
        """
        get the initial position of the player

        returns (x, y)
        """
        # get the player object from the TiledMapData
        player = self.tmx.get_object_by_name("player")
        # determine the x and y tile position of the player
        x: int = player.x // self.tmx.tilewidth
        y: int = player.y // self.tmx.tileheight
        return x, y

    def get_stars_position(self) -> List[Tuple[int, int]]:
        """
        get the position of all stars

        returns a List of (x, y)
        """
        # load the star layer
        loaded_stars = self.tmx.get_layer_by_name("Stars")
        # create an empty list for all stars
        # every star is just a tuple of x and y position
        stars: List[Tuple[int, int]] = []
        # calculate the tileposition of the stars
        for star in loaded_stars:
            x = star.x // self.tmx.tilewidth
            y = star.y // self.tmx.tileheight
            stars.append((x, y))
        return stars

    def render(self, surface: Surface):
        """
        render the map to the given surface
        """
        # fill background with a eventual background color
        if bg := self.tmx.background_color:
            surface.fill(bg)
        for layer in self.tmx.visible_tile_layers:
            # if not loaded like this, also object layers will be here
            layer = self.tmx.layers[layer]
            for x, y, image in layer.tiles():
                # show each tile of the map with the real position now
                surface.blit(image, (x * self.tmx.tilewidth, y * self.tmx.tileheight))

    def check_collide(self, x: int, y: int) -> bool:
        """
        check if a field has a collision

        there is also collision with the borders of the screen
        """
        # check if the field is outside of the screen
        if x < 0 or y < 0 or x >= self.tmx.width or y >= self.tmx.height:
            return True
        for layer in self.tmx.visible_tile_layers:
            # check each tile of the map if it is a collider
            properties = self.tmx.get_tile_properties(x, y, layer)
            if properties and "colliders" in properties:
                return True
        return False
