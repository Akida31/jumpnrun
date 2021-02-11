import pygame

RED = (255, 0, 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 10
        self.y = 30
        self.width = 25
        self.height = 25

    def render(self, surface: pygame.Surface):
        pygame.draw.rect(surface, RED, (self.x, self.y, self.width, self.height))

