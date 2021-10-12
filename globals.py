#import libraries
import math
import os
import sys
import pygame

# define colours


class Global:
    class Colour:
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        RED = (192, 0, 0)
        BLUE = (0, 0, 192)

    # main window
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 600

    # set clock values
    clock = pygame.time.Clock()
    FPS: int = 60

    # initialise
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    pygame.init()
    pygame.font.init()
    status_font = pygame.font.SysFont('Comic Sans MS', 30)
    item_font = pygame.font.SysFont('Comic Sans MS', 10, bold=True)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # switch to this scripts folder so that file references work!
    os.chdir(sys.path[0])

    # load images
    bg_img = pygame.image.load('images/bg.png').convert_alpha()
    bg_img_flipy = pygame.transform.flip(bg_img, False, True)
    player_img = pygame.image.load('images/player.png').convert_alpha()
    wall_img = pygame.image.load('images/wall.png').convert_alpha()
    table_img = pygame.image.load('images/table.png').convert_alpha()
    biscuit_img = pygame.image.load('images/cookie.png').convert_alpha()

    # image metrics
    bg_tiles_x = math.ceil(SCREEN_WIDTH / bg_img.get_width())
    bg_tiles_y = math.ceil(SCREEN_HEIGHT / bg_img.get_height())

    # TODO: add more sounds!
    # load sounds
    item_snd = pygame.mixer.Sound('sounds/item.wav')
