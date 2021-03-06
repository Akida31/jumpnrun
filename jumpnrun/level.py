from enum import Enum
from time import sleep
from typing import Dict, List, Tuple

import pygame

from jumpnrun.characters.player import Player
from jumpnrun.map import Map
from jumpnrun.objects.sign import Sign
from jumpnrun.objects.star import Star
from jumpnrun.translate import t
from jumpnrun.utils import quit_game
from jumpnrun.widgets import Button, Label, XAlign, YAlign

WHITE = pygame.Color(255, 255, 255)
BLACK2 = pygame.Color(68, 71, 90)


class LevelStatus(Enum):
    Paused = 0,
    Running = 1,
    Finished = 2,
    Quit = 3,
    Restart = 4


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
            color=WHITE,
            xalign=XAlign.LEFT
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
            color=WHITE,
            bg_color=None,
            yalign=YAlign.TOP
        )

        # set the framerate of the game
        self.FPS: int = 60
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
            # if the player hit all stars end the level
            if len(self.objects["stars"]) == 0:
                self.status = LevelStatus.Finished
            self.render()
            self.clock.tick(self.FPS)
        return (self.status, self.timer)

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
        # create temporary surface for transforming
        surface = pygame.Surface((map_width, map_height))
        # render the map
        self.map.render(surface)
        # render all objects
        for group in self.objects:
            for element in self.objects[group]:
                element.render(surface)
        # render the player
        self.player.render(surface)
        # render the temporary surface to the full screen
        self.surface.blit(
            pygame.transform.scale(surface, (self.width, self.height)), (0, 0)
        )
        # render the description of a sign if a player stands on one
        if collision := pygame.sprite.spritecollideany(self.player, self.objects["signs"]):
            self.sign_label.set_caption(t(collision.description))
            self.sign_label.render(self.surface)

        # render the timer
        self.time_label.set_caption(f"{t('Time')}: {self.timer}")
        self.time_label.render(self.surface)
        pygame.display.update()

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
            self.pause_screen()
        if keys[pygame.K_w]:
            self.player.jump(self.map)
        if keys[pygame.K_a]:
            self.player.go_left(self.map)
        if keys[pygame.K_d]:
            self.player.go_right(self.map)

    def pause_screen(self):
        """
        pause screen in the level
        """
        self.status = LevelStatus.Paused
        continue_button = Button(
            caption=t("Continue"),
            x=0.4,
            y=0.4,
            width=0.2,
            textsize=0.16,
            hover_color=BLACK2
        )
        restart_button = Button(
            caption=t("Restart Level"),
            x=0.35,
            y=0.55,
            width=0.3,
            textsize=0.12,
            hover_color=BLACK2
        )
        quit_button = Button(
            caption=t("Back to Title Screen"),
            x=0.325,
            y=0.7,
            width=0.35,
            textsize=0.09,
            hover_color=BLACK2
        )
        while self.status == LevelStatus.Paused:
            for event in pygame.event.get():
                # close the program if the window should be closed
                if event.type == pygame.QUIT:
                    quit_game()
                # handle click
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # handle click of continue button
                    if continue_button.check_on(self.surface):
                        self.status = LevelStatus.Running
                        # give the player some time to react
                        sleep(0.5)
                    # handle click of quit button
                    elif quit_button.check_on(self.surface):
                        self.status = LevelStatus.Quit
                    # handle click of restart button
                    elif restart_button.check_on(self.surface):
                        self.status = LevelStatus.Restart
            # render the continue button
            continue_button.render(self.surface)
            # render the restart button
            restart_button.render(self.surface)
            # render the quit button
            quit_button.render(self.surface)
            # update the screen
            pygame.display.update()

