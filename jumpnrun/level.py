import sys
from time import sleep
from typing import List, Tuple, Optional, Dict

import pygame

from jumpnrun.characters.player import Player
from jumpnrun.map import Map
from jumpnrun.objects.sign import Sign
from jumpnrun.objects.star import Star
from jumpnrun.utils import quit_game
from jumpnrun.widgets import Label, XAlign, Button, YAlign

WHITE = pygame.Color(255, 255, 255)
BLACK2 = pygame.Color(68, 71, 90)


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
            caption="Time",
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
        self.running = True
        # create a timer
        self.timer = 0

    def run(self) -> Optional[int]:
        """
        gameloop, running the game

        returns the time until completion or None if the Level wasn't completed
        """
        while self.running:
            self.on_events()
            # update the timer
            self.timer += 1
            self.apply_physics()
            self.player.interact(self.objects)
            # if the player hit all stars end the level
            if len(self.objects["stars"]) == 0:
                return self.timer
            self.render()
            self.clock.tick(self.FPS)
        return None

    def on_events(self):
        """
        handle all events of the game
        """
        for event in pygame.event.get():
            # close the program if the window should be closed
            if event.type == pygame.QUIT:
                self.quit()
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
            self.sign_label.set_caption(collision.description)
            self.sign_label.render(self.surface)

        # render the timer
        self.time_label.set_caption(f"Time: {self.timer}")
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

    def quit(self):
        """
        stop the program and quit the game
        """
        self.running = False
        pygame.quit()
        sys.exit()

    def handle_keypresses(self, keys):
        """
        handle the keypresses of the user
        """
        # quit on escape
        if keys[pygame.K_q]:
            self.quit()
        if keys[pygame.K_ESCAPE]:
            if not self.pause_screen():
                self.running = False
                return
            sleep(0.5)
        if keys[pygame.K_w]:
            self.player.jump(self.map)
        if keys[pygame.K_a]:
            self.player.go_left(self.map)
        if keys[pygame.K_d]:
            self.player.go_right(self.map)

    def pause_screen(self) -> bool:
        """
        pause screen in the level
        :return: if the game should be continued
        """
        continue_button = Button(
            caption="Continue",
            x=0.4,
            y=0.45,
            width=0.2,
            textsize=0.2,
            hover_color=BLACK2
        )
        quit_button = Button(
            caption="Quit",
            x=0.45,
            y=0.6,
            hover_color=BLACK2
        )
        while True:
            for event in pygame.event.get():
                # close the program if the window should be closed
                if event.type == pygame.QUIT:
                    quit_game()
                # handle click
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # handle click of continue button
                    if continue_button.check_on(self.surface):
                        return True
                    # handle click of next button
                    if quit_button.check_on(self.surface):
                        return False
            # render the continue button
            continue_button.render(self.surface)
            # render the quit button
            quit_button.render(self.surface)
            # update the screen
            pygame.display.update()

