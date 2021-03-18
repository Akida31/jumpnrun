from typing import Callable, Dict, List, Optional
from os import path
import pygame

from skyjump.utils import quit_game
from skyjump.widgets import Button, Label
from skyjump.config import DATA_DIR

FPS: int = 30


class Screen:
    """base class for all screens.
    keeps track of the content of the screen and also renders it
    You must call `super().__init__` in your __init__ method first
        in all your inherited classes
    """

    def __init__(
        self, surface: pygame.Surface, background_image: bool = False
    ):
        """create a screen and initialize it

        :param surface: the surface to which the screen should be rendered
        :param background_image: if there should be a background image
            or transparent background
        """
        self.surface = surface
        self.labels: List[Label] = []
        self.buttons: Dict[Button, Callable] = {}
        self.clock = pygame.time.Clock()
        self.running = True
        # initially there is no background image
        self.image: Optional[pygame.Surface] = None
        if background_image:
            self.image = pygame.image.load(
                path.join(DATA_DIR, "img", "screenshot.png")
            )

    def add_label(self, label: Label):
        """add a widget to the screen

        :param label: the label which should be added
        """
        self.labels.append(label)

    def add_button(self, button: Button, handler: Callable):
        """add a button to the screen

        :param button: the button which should be added
        :param handler: function which will be called if the button is pressed
        """
        self.buttons[button] = handler

    def render(self):
        """render all widgets to the surface"""
        # render the background image
        if self.image:
            width = self.surface.get_width()
            height = self.surface.get_height()
            # scale the background image to full screen
            self.surface.blit(
                pygame.transform.scale(self.image, (width, height)), (0, 0)
            )
        # render all child widgets
        for label in self.labels:
            label.render(self.surface)
        for button in self.buttons:
            button.render(self.surface)
        # update the screen
        pygame.display.flip()

    def run(self):
        """run the main loop of the screen"""
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
            # delay the event loop to save CPU
            self.clock.tick(FPS)
