from os import listdir
from typing import Tuple, List

from pygame import Surface
from pytmx.util_pygame import load_pygame

from jumpnrun.objects.sign import Sign
from jumpnrun.objects.star import Star


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

    def get_stars(self) -> List[Star]:
        """
        get all stars
        """
        # load the imgs for the stars
        star_dir: str = "assets/img/star/shine/"
        starfiles: List[str] = list(map(lambda i: f"{star_dir}{i}", listdir(star_dir)))
        # load the star layer
        layer = self.tmx.get_layer_by_name("Stars")
        # create an empty list for all stars
        # every star is just a tuple of x and y position
        stars: List[Star] = []
        # calculate the tileposition of the stars
        for star in layer:
            x = star.x // self.tmx.tilewidth
            y = star.y // self.tmx.tileheight
            stars.append(Star(starfiles, x, y))
        return stars

    def get_signs(self) -> List[Sign]:
        """
        get all signs

        returns a Dictionary in which the description is mapped
        to the position (x,y)
        """
        # load the sign layer
        layer = self.tmx.get_layer_by_name("Signs")
        signs: List[Sign] = []
        for sign in layer:
            x = sign.x // self.tmx.tilewidth
            y = sign.y // self.tmx.tilewidth
            description: str = sign.properties["description"]
            # pytmx fails to load normal \n
            description = description.replace("|n", "\n")
            signs.append(Sign(x, y, description, sign.image))
        return signs

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
