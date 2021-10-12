# import libraries
import pygame

# import locals
from globals import Global
from enum import Enum, auto

# obstacle class


class Obstacle(pygame.sprite.Sprite):

    # type constants
    class Type(Enum):
        WALL = auto()
        TABLE = auto()

    # variables    
    x: int = None
    y: int = None
    type: Type = None
    bounciness: int = None # 0 to 10
    width: int = None
    height: int = None
    rect: pygame.Rect = None

    def __init__(self, type: Type, x: int, y: int, width: int, height: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.type = type
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)

        # handle obstacle types
        if type == Obstacle.Type.WALL:
            # TODO: improve wall obstacle to look modular rather than a single stretched image
            self.image = pygame.transform.scale(
                Global.wall_img, (width, height))
            self.bounciness = 7
        elif type == Obstacle.Type.TABLE:
            self.image = pygame.transform.scale(
                Global.table_img, (width, height))
            self.bounciness = 2
        else:
            raise ValueError('Obstacle type not recognised: ' + type)

        return None
