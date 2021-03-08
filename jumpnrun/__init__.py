from jumpnrun.game import Game


def main():
    """
    create and run the game
    """
    # create a new game
    game = Game()
    try:
        # run the game
        game.run()
    # don't crash the game on keyboard interrupt but end gracefully
    except KeyboardInterrupt:
        print("KeyboardInterrupt, exiting")
        exit(1)
