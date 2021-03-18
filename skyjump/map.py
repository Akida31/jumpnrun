from typing import Tuple, List

import pygame
import pytmx
from skyjump.objects import Sign, Spike, Star


class Tile(pygame.sprite.Sprite):
    """basic class for all collidable Tiles
    """

    def __init__(self, x: int, y: int, width: int, height: int):
        """create a new tile

        :param x, y: the position of the tile
        :param width, height: the dimensions of the tile
        """
        # initialize the sprite class
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @property
    def rect(self) -> pygame.Rect:
        """ needed for collision
        :returns: the rect of the tile
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)


class Map:
    """the map of each level
    """
    def __init__(self, path: str):
        """create a new map

        :param path: the path of the tmx file to load from
        """
        # load the map from the given TiledMap-File
        self.tmx: pytmx.TiledMap = pytmx.load_pygame(path, pixelalpha=True)
        # save the size of the map
        self.size: Tuple[int, int] = (
            self.tmx.width * self.tmx.tilewidth,
            self.tmx.height * self.tmx.tileheight,
        )
        # create a group for map colliders
        self.colliders: pygame.sprite.Group = pygame.sprite.Group()
        # add only the content of the visible layers
        for layer_nr in self.tmx.visible_tile_layers:
            # if not loaded like this, also object layers will be here
            layer = self.tmx.layers[layer_nr]
            # ignore the image of the tile
            for x, y, _ in layer.tiles():
                # check each tile of the map if it is a collider
                properties = self.tmx.get_tile_properties(x, y, layer_nr)
                if properties and "colliders" in properties:
                    sprite = Tile(
                        x * self.tmx.tilewidth,
                        y * self.tmx.tileheight,
                        self.tmx.tilewidth,
                        self.tmx.tileheight,
                    )
                    self.colliders.add(sprite)

    def get_size(self) -> Tuple[int, int]:
        """get the size of the map

        :returns: width, height
        """
        return self.size

    def get_player_position(self) -> Tuple[int, int]:
        """get the initial position of the player

        :returns: x, y
        """
        # get the player object from the TiledMapData
        player = self.tmx.get_object_by_name("player")
        # determine the x and y tile position of the player
        x: int = player.x // self.tmx.tilewidth
        y: int = player.y // self.tmx.tileheight
        return x, y

    def get_stars(self) -> List[Star]:
        """get all stars

        :returns: the stars in the level
        """
        # load the star layer
        layer = self.tmx.get_layer_by_name("Stars")
        # create an empty list for all stars
        # every star is just a tuple of x and y position
        stars: List[Star] = []
        # calculate the tileposition of the stars
        for star in layer:
            x = star.x // self.tmx.tilewidth
            y = star.y // self.tmx.tileheight
            stars.append(Star(x, y))
        return stars

    def get_signs(self) -> List[Sign]:
        """get all signs

        similar to `get_stars`
        """
        # load the sign layer
        layer = self.tmx.get_layer_by_name("Signs")
        signs: List[Sign] = []
        for sign in layer:
            x = sign.x // self.tmx.tilewidth
            y = sign.y // self.tmx.tileheight
            description: str = sign.properties["description"]
            signs.append(Sign(x, y, description, sign.image))
        return signs

    def get_spikes(self) -> List[Spike]:
        """get all spikes

        similar to `get_stars`
        """
        # load the spike layer
        layer = self.tmx.get_layer_by_name("Spikes")
        spikes: List[Spike] = []
        for spike in layer:
            x = spike.x
            y = spike.y
            width = int(spike.width)
            height = int(spike.height)
            spikes.append(Spike(x, y, width, height, spike.image))
        return spikes

    def render(self, surface: pygame.Surface):
        """render the map to the given surface

        :param surface: the surface to which the map should be rendered
        """
        # fill background with a eventual background color
        if bg := self.tmx.background_color:
            surface.fill(bg)
        for layer in self.tmx.visible_tile_layers:
            # if not loaded like this, also object layers will be here
            layer = self.tmx.layers[layer]
            for x, y, image in layer.tiles():
                # show each tile of the map with the real position now
                surface.blit(
                    image, (x * self.tmx.tilewidth, y * self.tmx.tileheight)
                )
