import pygame
import sys

from .characters.player import Player
from .map import Map

class Game:
    def __init__(self):
        """
        initialize the game
        """
        # initialize pygame
        pygame.init()
        # set the framerate of the game
        self.FPS: int = 10
        self.clock = pygame.time.Clock()
        # set the title of the window
        pygame.display.set_caption("Jumpnrun")
        self.width: int = 800
        self.height: int = 400
        # create the window
        self.surface: pygame.Surface = pygame.display.set_mode((self.width, self.height), flags=pygame.RESIZABLE)
        self.map = Map("maps/test.tmx")
        # load player position
        (player_x, player_y) = self.map.get_player_position()
        # create a new player
        self.player = Player("maps/characters2.png", player_x, player_y)
        self.objects = []
        self.running = True

    def run(self):
        """
        gameloop, running the game
        """
        while self.running:
            self.on_events()
            self.apply_physics()
            self.render()
            self.clock.tick(self.FPS)
        self.quit()

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
                self.width, self.height = event.size
        # handle all keypresses
        self.handle_keypresses(pygame.key.get_pressed())

    def render(self):
        """
        render the window and all of its content
        """
        map_width, map_height = self.map.get_dimensions()
        # create temporary surface for transforming
        surface = pygame.Surface((map_width, map_height))
        self.map.render(surface)
        for o in self.objects:
            o.render(surface)
        self.player.render(surface)
        # render the temporary surface to the full screen
        self.surface.blit(pygame.transform.scale(surface, (self.width, self.height)), (0, 0))
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

    def handle_keypresses(self, keys):
        """
        handle the keypresses of the user
        """
        # quit on escape
        if keys[pygame.K_ESCAPE]:
            self.quit()
        if keys[pygame.K_w]:
            self.player.jump(self.map)
        if keys[pygame.K_a]:
            self.player.move_left(self.map)
        if keys[pygame.K_d]:
            self.player.move_right(self.map)
        if keys[pygame.K_s]:
            self.player.move_down(self.map)
