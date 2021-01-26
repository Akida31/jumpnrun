import sys

import pygame

RED = (255, 0, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 10
        self.y = 30
        self.width = 25
        self.height = 25

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, RED, (self.x, self.y, self.width, self.height))


class Game:
    def __init__(self):
        pygame.init()
        width: int = 300
        height: int = 300
        self.surface: pygame.Surface = pygame.display.set_mode((width, height))
        self.objects = [Player()]
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
            self.draw()
        self.quit()

    def draw(self):
        for o in self.objects:
            o.draw(self.surface)
        pygame.display.update()

    def quit(self):
        self.running = False
        pygame.quit()
        sys.exit()



if __name__ == '__main__':
    game = Game()
    game.run()
