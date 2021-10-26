# import libraries
import math
import pygame
from enum import Enum, auto

# import locals
from globals import Global
from tile import Tile

# obstacle class
class Obstacle(pygame.sprite.Sprite):

    # type constants
    class Type(Enum):
        WALL = auto()
        TABLE = auto()

    # variables    
    x: int
    y: int
    bounciness: int # 0 to 10
    width: int
    height: int
    rect: pygame.Rect
    tile: Tile
    image: pygame.Surface

    def __init__(self, tile: Tile, x: int, y: int, width: int = Global.TILE_WIDTH
               , height: int = Global.TILE_HEIGHT, bounciness: int = 0) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.tile = tile
        self.bounciness = bounciness
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)

        # create image from tiles
        self.image = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        for i in range(0, width, self.tile.width):
            for j in range(0, height, self.tile.height):
                self.image.blit(self.tile.get_image(), (i, j))

        return None

    def draw(self, surface: pygame.Surface, camera_pos : pygame.Vector2) -> None:
        surface.blit(self.image, (self.rect.x - camera_pos[0], self.rect.y - camera_pos[1]))
        return None
