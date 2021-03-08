from typing import Dict, List, Tuple

import pygame

from jumpnrun.characters.player import Player
from jumpnrun.colors import BLACK
from jumpnrun.map import Map
from jumpnrun.objects import Sign, Spike, Star
from jumpnrun.screens.pause import pause_screen
from jumpnrun.translate import t
from jumpnrun.utils import LevelStatus, quit_game
from jumpnrun.widgets import Label, XAlign, YAlign

# FPS of the game
FPS: int = 60


class Level:
    def __init__(self, level_file: str, surface: pygame.Surface):
        """
        initialize the level

        level_file: the file from which the level should be loaded
        surface: the surface on which should be drawn
        """
        # save the surface
        self.surface = surface
        # save the dimensions of the surface
        (self.width, self.height) = self.surface.get_size()

        # create a label for the timer
        self.time_label = Label(
            caption=t("Time"),
            x=0.01,
            y=0.01,
            width=0.25,
            height=0.1,
            font_file="assets/fonts/carobtn.TTF",
            textsize=0.15,
            color=BLACK,
            xalign=XAlign.LEFT,
        )

        # create a label for the description of signs
        self.sign_label = Label(
            caption="",
            x=0.2,
            y=0.05,
            width=0.6,
            height=0.4,
            font_file="assets/fonts/carobtn.TTF",
            textsize=0.05,
            color=BLACK,
            bg_color=None,
            yalign=YAlign.TOP,
        )

        # create the background image
        self.background = pygame.image.load("assets/img/backgrounds/landscape.png")

        # set the framerate of the game
        self.clock = pygame.time.Clock()
        # load the map
        self.map = Map(level_file)
        # load player position
        (player_x, player_y) = self.map.get_player_position()
        # create a new player
        self.player = Player("assets/img/characters2.png", player_x, player_y)

        self.objects: Dict[str, List] = {}
        # load the position of the stars
        stars: List[Star] = self.map.get_stars()
        self.objects["stars"] = stars
        # load all signs
        signs: List[Sign] = self.map.get_signs()
        self.objects["signs"] = signs
        # load all spikes
        spikes: List[Spike] = self.map.get_spikes()
        self.objects["spikes"] = spikes
        self.status = LevelStatus.Running
        # create a timer
        self.timer = 0

    def run(self) -> Tuple[LevelStatus, int]:
        """
        gameloop, running the game

        returns the status of the end and the time which the game ran
        """
        while self.status == LevelStatus.Running:
            self.on_events()
            # update the timer
            self.timer += 1
            self.apply_physics()
            self.player.interact(self.objects)
            # check if the player is alive
            if not self.player.alive:
                self.status = LevelStatus.Restart
                break
            # if the player hit all stars end the level
            if len(self.objects["stars"]) == 0:
                self.status = LevelStatus.Finished
            self.render()
            self.clock.tick(FPS)
        return self.status, self.timer

    def on_events(self):
        """
        handle all events of the game
        """
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
        """
        resize the window and all content

        size: (width, height)
        """
        self.width, self.height = size

    def render(self):
        """
        render the window and all of its content
        """
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
        # render the background image
        self.surface.blit(
            pygame.transform.scale(self.background, (self.width, self.height)), (0, 0)
        )
        # render the temporary surface to the full screen
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
        self.time_label.set_caption(f"{t('Time')}: {self.timer}")
        self.time_label.render(self.surface)
        pygame.display.flip()

    def apply_physics(self):
        """
        apply physics to all objects
        """
        for group in self.objects:
            for element in self.objects[group]:
                element.apply_physics(self.map)
        self.player.apply_physics(self.map)

    def handle_keypresses(self, keys):
        """
        handle the keypresses of the user
        """
        # quit on escape
        if keys[pygame.K_q]:
            quit_game()
        if keys[pygame.K_ESCAPE]:
            self.status = pause_screen(self.surface)
        if keys[pygame.K_w]:
            self.player.jump(self.map)
        if keys[pygame.K_a]:
            self.player.go_left(self.map)
        if keys[pygame.K_d]:
            self.player.go_right(self.map)
