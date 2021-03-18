import pygame
from skyjump.widgets import Label
from skyjump.colors import BLACK


class Button(Label):
    """a simple button

    small wrapper for a label
    """

    def __init__(self, **kwargs):
        """create a new button

        :param kwargs: all kwargs will be handed over to the label
        :keyword hover_color: the background color on hover
        """
        super().__init__(**kwargs)
        if bg_color := kwargs.get("bg_color"):
            self._bg_color = bg_color
        else:
            self._bg_color = BLACK
        if hover_color := kwargs.get("hover_color"):
            self.hover_color = hover_color
        else:
            # generate a lighter version of the bg_color as hover_color
            self.hover_color = self._bg_color + pygame.Color(30, 30, 30)

    def render(self, out_surface: pygame.Surface):
        """render the button

        :param out_surface: the surface to which the button will be rendered
        """
        # change background color on hover
        if self.check_on(out_surface):
            bg_color = self.hover_color
        else:
            bg_color = self._bg_color
        super().set_bg_color(bg_color)
        # render the label
        super().render(out_surface)

    def check_on(self, surface: pygame.Surface) -> bool:
        """check if the mouse is over the button

        :param surface: the surface is needed to compute
            the absolute position of the button
        :returns: if the mouse is currently over the button
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        x = round(self.x * surface.get_width())
        y = round(self.y * surface.get_height())
        width = round(self.width * surface.get_width())
        height = round(self.height * surface.get_height())
        return (x <= mouse_x <= x + width) and (y <= mouse_y <= y + height)
