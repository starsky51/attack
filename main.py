# import libraries
import pygame
import sys

# import locals
from globals import Global
from game import Game


def main():
    # create window
    pygame.display.set_caption("Ethan Attack!")

    # main loop
    run = True
    game = Game(2, Game.DifficultyLevel.MEDIUM)

    while (run):
        Global.clock.tick(Global.FPS)

        game.update()
        game.draw(Global.screen)

        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

        # update screen
        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
