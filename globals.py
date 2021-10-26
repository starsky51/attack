# import libraries
import math
import os
import sys
import pygame
from enum import Enum, auto
from collections import namedtuple

# import locals
from tile import Tile

# global class
class Global:
    # define colours
    class Colour:
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        RED = (192, 0, 0)
        BLUE = (0, 0, 192)

    class TileData(namedtuple('ColorTuple', 'id name src'), Enum):
        WALL = (1, 'Wall', 'images/wall.png')
        TABLE = (2, 'Table', 'images/table.png')

    # main window
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    TILE_WIDTH = TILE_HEIGHT = 24

    # set clock values
    clock = pygame.time.Clock()
    FPS: int = 60

    # initialise
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    pygame.mixer.set_num_channels(24)
    pygame.init()
    pygame.font.init()
    status_font = pygame.font.SysFont('Comic Sans MS', 30)
    item_font = pygame.font.SysFont('Comic Sans MS', 10, bold=True)

    # switch to this scripts folder so that file references work!
    os.chdir(sys.path[0])
