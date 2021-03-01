from .game import Game


def run():
    game = Game()
    try:
        game.run()
    except KeyboardInterrupt:
        print("KeyboardInterrupt, exiting")
        exit(1)
