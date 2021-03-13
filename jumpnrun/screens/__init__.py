from typing import Callable, Dict, List, Optional
from os import path
import pygame

from jumpnrun.utils import quit_game
from jumpnrun.widgets import Button, Label
from jumpnrun.config import DATA_DIR

FPS: int = 30


class Screen:
    def __init__(
        self, surface: pygame.Surface, background_image: bool = False
    ):
        self.surface = surface
        self.labels: List[Label] = []
        self.buttons: Dict[Button, Callable] = {}
        self.clock = pygame.time.Clock()
        self.running = True
        self.image: Optional[pygame.Surface] = None
        if background_image:
            self.image = pygame.image.load(
                path.join(DATA_DIR, "img", "screenshot.png")
            )

    def add_label(self, label: Label):
        """
        add a widget to the screen
        """
        self.labels.append(label)

    def add_button(self, button: Button, handler: Callable):
        """
        add a button to the screen

        the handler function will be called if the button is pressed
        """
        self.buttons[button] = handler

    def render(self):
        """
        render all widgets to the surface
        """
        # render the background image
        if self.image:
            width = self.surface.get_width()
            height = self.surface.get_height()
            self.surface.blit(
                pygame.transform.scale(self.image, (width, height)), (0, 0)
            )
        for label in self.labels:
            label.render(self.surface)
        for button in self.buttons:
            button.render(self.surface)
        # update the screen
        pygame.display.flip()

    def run(self):
        """
        run the main loop of the screen
        """
        while self.running:
            for event in pygame.event.get():
                # close the program if the window should be closed
                if event.type == pygame.QUIT:
                    quit_game()
                # handle click
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button, handler in self.buttons.items():
                        if button.check_on(self.surface):
                            handler()
            self.render()
            self.clock.tick(FPS)
