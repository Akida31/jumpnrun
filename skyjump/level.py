from os import path
import json
from typing import Dict, List, Tuple

import pygame

from skyjump.colors import BLACK
from skyjump.config import DATA_DIR
from skyjump.map import Map
from skyjump.objects import Star
from skyjump.objects.player import Player
from skyjump.screens.pause import PauseScreen
from skyjump.sound import play_sound
from skyjump.translate import t
from skyjump.utils import FPS, LevelStatus, quit_game
from skyjump.widgets import Label, XAlign, YAlign


class LevelData:
    """a deserializer for the levels saved in the level file"""

    name: str  # the name of the level
    filename: str  # the file from which the level should be loaded
    highscore: float  # the current highscore of the level
    # if the level is currently unlocked (the level before was completed)
    unlocked: bool

    def __init__(self, data: Dict):
        """create leveldata from the given json"""
        self.name = data["name"]
        self.filename = data["filename"]
        self.highscore = data["highscore"]
        self.unlocked = data["unlocked"]

    def to_json(self) -> str:
        """create the json string from the leveldata"""
        # self.__dict__ is a dictionary of all attributes of the class
        return json.dumps(self.__dict__)


class Level:
    def __init__(self, level_data: LevelData, surface: pygame.Surface):
        """initialize the level

        :param level_data: the data of the level containing
            the necessary information like highscore
        :param surface: the surface to which the level should be rendered
        """
        # if the level is not unlocked there is probably some cheating going on
        if not level_data.unlocked:
            print(
                f"ERROR, Level {level_data.name} was not unlocked but started"
            )
            quit_game()
        # save the surface
        self.surface = surface
        # save the level_data
        self.level_data = level_data
        # save the dimensions of the surface
        (self.width, self.height) = self.surface.get_size()

        # create a label for the timer
        self.time_label = Label(
            caption=t("Time"),
            x=0.01,
            y=0.01,
            width=0.25,
            height=0.1,
            color=BLACK,
            xalign=XAlign.LEFT,
        )

        # create a label for the description of signs
        # on the start it has no caption but it will be set if necessary
        self.sign_label = Label(
            caption="",
            x=0.15,
            y=0.05,
            width=0.75,
            height=0.5,
            textsize=2.5,
            color=BLACK,
            bg_color=None,
            yalign=YAlign.TOP,
        )

        # load the background image
        self.background = pygame.image.load(
            path.join(DATA_DIR, "img", "backgrounds", "landscape.png")
        )

        # create a clock for the level
        # the clock will delay the time between the frames
        # so that the CPU usage is limited
        self.clock = pygame.time.Clock()
        # load the map
        self.map = Map(path.join(DATA_DIR, "maps", self.level_data.filename))
        # load player position
        (player_x, player_y) = self.map.get_player_position()
        # create a new player
        self.player = Player(
            path.join(DATA_DIR, "img", "characters2.png"), player_x, player_y
        )

        self.objects: Dict[str, pygame.sprite.Group] = {}
        # load the position of the stars
        stars: pygame.sprite.Group = self.map.get_stars()
        self.objects["stars"] = stars
        # load the star hints
        self.star_hints: List[Star] = []
        for i in range(len(self.objects["stars"])):
            self.star_hints.append(Star(1 + i, 2))
        # load all signs
        signs: pygame.sprite.Group = self.map.get_signs()
        self.objects["signs"] = signs
        # load all spikes
        spikes: pygame.sprite.Group = self.map.get_spikes()
        self.objects["spikes"] = spikes
        # the level is initially running
        self.status: LevelStatus = LevelStatus.Running
        # the timer to show the playing time and determining the highscore
        self.timer: int = 0

    def run(self) -> Tuple[LevelStatus, float]:
        """gameloop, running the game

        :returns: status of the end and the time which the game ran
        """
        # the time between frames is not everytime the same
        # so use the difference
        dt: int = 0
        while self.status == LevelStatus.Running:
            # update the timer
            self.timer += dt
            # if the dt is higher, apply everything multiple times
            # the rendering is the cost intensive action
            # so this will render only every 20 times
            for _ in range(max(1, dt // 20)):
                self.on_events()
                self.apply_physics()
                self.player.interact(self.objects)
                # restart the level if the player is not alive anymore
                if not self.player.alive:
                    self.status = LevelStatus.Restart
                    play_sound("jingle_lose.ogg", pause=True)
                    break
                # if the player hit all stars end the level
                if len(self.objects["stars"]) == 0:
                    self.status = LevelStatus.Finished
            self.render()
            # get the time difference since the last frame
            dt = self.clock.tick(FPS)
        if self.status == LevelStatus.Finished:
            play_sound("jingle_win.ogg", pause=True)
        return self.status, self.get_time()

    def get_time(self) -> float:
        """get the time in seconds"""
        return round(self.timer / 1000, 2)

    def on_events(self):
        """handle all events of the game"""
        for event in pygame.event.get():
            # close the program if the window should be closed
            if event.type == pygame.QUIT:
                quit_game()
            # handle the resizing of the window
            elif event.type == pygame.VIDEORESIZE:
                self.resize(event.size)
        # handle all keypresses
        self.handle_keypresses(pygame.key.get_pressed())

    def resize(self, size: Tuple[int, int]):
        """resize the window and all content on next render

        :param size: (width, height)
        """
        self.width, self.height = size

    def render(self):
        """render the window and all of its content"""
        map_width, map_height = self.map.get_size()
        # create temporary surface for transforming with transparent background
        surface = pygame.Surface((map_width, map_height), pygame.SRCALPHA)
        # render the map
        self.map.render(surface)
        # render all objects
        for group in self.objects:
            for element in self.objects[group]:
                element.render(surface)
        # render the player
        self.player.render(surface)
        # render the background image to the full window
        self.surface.blit(
            pygame.transform.scale(self.background, (self.width, self.height)),
            (0, 0),
        )
        # render the hint stars
        for i in range(len(self.objects["stars"])):
            self.star_hints[i].render(surface)
        # render the temporary surface scaled up to the full screen
        self.surface.blit(
            pygame.transform.scale(surface, (self.width, self.height)), (0, 0)
        )
        # render the description of a sign if a player stands on one
        if collision := pygame.sprite.spritecollideany(
            self.player, self.objects["signs"]
        ):
            self.sign_label.set_caption(t(collision.description))
            self.sign_label.render(self.surface)

        # render the timer
        self.time_label.set_caption(f"{t('Time')}: {self.get_time()}")
        self.time_label.render(self.surface)
        # update the display
        pygame.display.flip()

    def apply_physics(self):
        """apply physics to all objects"""
        for group in self.objects:
            for element in self.objects[group]:
                element.apply_physics(self.map)
        self.player.apply_physics(self.map)

    def handle_keypresses(self, keys: List[bool]):
        """handle the keypresses of the user

        :param keys: the list of keypresses determined by
            `pygame.key.get_pressed()`
        """
        if keys[pygame.K_ESCAPE]:
            self.status = PauseScreen(self.surface).run()
        if keys[pygame.K_w]:
            self.player.jump(self.map)
        if keys[pygame.K_a]:
            self.player.go_left(self.map)
        if keys[pygame.K_d]:
            self.player.go_right(self.map)
