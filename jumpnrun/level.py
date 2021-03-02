import sys
from os import listdir
from typing import List, Tuple, Optional

import pygame

from jumpnrun.characters.player import Player
from jumpnrun.map import Map
from jumpnrun.objects.star import Star

WHITE = (255, 255, 255)


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

        # load the font and change the size depending on the window size
        self.font_file: str = "assets/fonts/carobtn.TTF"
        self.font = pygame.font.Font(self.font_file, round(0.06 * self.height))
        # set the framerate of the game
        self.FPS: int = 60
        self.clock = pygame.time.Clock()
        # load the map
        self.map = Map(level_file)
        # load player position
        (player_x, player_y) = self.map.get_player_position()
        # create a new player
        self.player = Player("assets/img/characters2.png", player_x, player_y)

        self.objects = []
        # load the position of the stars
        stars: List[Tuple[int, int]] = self.map.get_stars_position()
        # star files
        star_dir: str = "assets/img/star/shine/"
        starfiles: List[str] = list(map(lambda i: f"{star_dir}{i}", listdir(star_dir)))
        for star in stars:
            (x, y) = star
            self.objects.append(Star(starfiles, x, y))

        self.running = True
        # create a timer
        self.timer = 0
        # game is not paused initially
        self.paused = False

    def run(self) -> Optional[int]:
        """
        gameloop, running the game

        returns the time until completion or None if the Level wasn't completed
        """
        while self.running:
            self.on_events()
            if not self.paused:
                # update the timer
                self.timer += 1
                self.apply_physics()
                self.player.interact(self.objects)
                # if the player hit all stars end the level
                if len(self.objects) == 0:
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
        self.font = pygame.font.Font(self.font_file, round(0.06 * self.height))

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
        for o in self.objects:
            o.render(surface)
        # render the player
        self.player.render(surface)
        # render the temporary surface to the full screen
        self.surface.blit(
            pygame.transform.scale(surface, (self.width, self.height)), (0, 0)
        )
        # render the timer
        text = f"Time: {self.timer}"
        timer = self.font.render(text, True, WHITE)
        (text_width, text_height) = self.font.size(text)
        self.surface.blit(timer, (10, 10, text_width, text_height))
        pygame.display.update()

    def apply_physics(self):
        """
        apply physics to all objects
        """
        for o in self.objects:
            o.apply_physics(self.map)
        self.player.apply_physics(self.map)

    def quit(self):
        """
        stop the program and quit the game
        """
        self.running = False
        pygame.quit()
        sys.exit()

    def pause(self):
        """
        pause the game

        the game will only be rendered and some events like closing the game will be handled
        """
        self.paused = True

    def unpause(self):
        """
        unpause the game
        """
        self.paused = False

    def handle_keypresses(self, keys):
        """
        handle the keypresses of the user
        """
        # quit on escape
        if keys[pygame.K_ESCAPE]:
            self.quit()
        if keys[pygame.K_s]:
            if self.paused:
                self.unpause()
            else:
                self.pause()
        if not self.paused:
            if keys[pygame.K_w]:
                self.player.jump(self.map)
            if keys[pygame.K_a]:
                self.player.go_left(self.map)
            if keys[pygame.K_d]:
                self.player.go_right(self.map)
