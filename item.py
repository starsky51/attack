# import libraries
import pygame

# import locals
from globals import Global
from enum import Enum, auto

from player import Player

# item class


class Item(pygame.sprite.Sprite):

    # type constants
    class Type(Enum):
        BISCUIT = auto()

    # state constants
    class State(Enum):
        IDLE = auto()
        COLLECT = auto()
        COLLECTED = auto()
        EXPIRING = auto()
        EXPIRED = auto()
        DESTROY = auto()

    def __init__(self, type: Type, x: int, y: int, lifespan: float = 10.0) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.x: int = x
        self.y: int = y
        self.lifespan : int = lifespan

        # handle item type
        if type == Item.Type.BISCUIT:
            self.width: int = 15
            self.height: int = 15
            self.value: int = 1
            self.collectable: bool = True
            self.collector: Player = None
            self.state: Item.State = Item.State.IDLE
            self.timer: int = 0
            self.image: pygame.Surface = pygame.transform.scale(
                Global.biscuit_img, (self.width, self.height))
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        return None

    def update(self) -> bool:
        self.timer += 1
        if self.state == Item.State.COLLECT:
            self.collector.score += self.value
            self.collectable = False
            self.state = Item.State.COLLECTED
            self.timer = 0
        elif self.state == Item.State.COLLECTED and self.timer >= (Global.FPS * (self.lifespan / 5)):
            self.state = Item.State.DESTROY
            self.timer = 0
        elif self.state == Item.State.IDLE and self.timer >= (Global.FPS * (self.lifespan / 1.5)):
            self.state = Item.State.EXPIRING
            self.timer = 0
        elif self.state == Item.State.EXPIRING and self.timer >= (Global.FPS * (self.lifespan / 2.5)):
            self.state = Item.State.EXPIRED
            self.collectable = False
            self.value = 0
            self.timer = 0
        elif self.state == Item.State.EXPIRED and self.timer >= (Global.FPS * (self.lifespan / 5)):
            self.state = Item.State.DESTROY
            self.collectable = False
            self.timer = 0
        elif self.state == Item.State.DESTROY:
            return True

        return False

    def collect(self, player: Player) -> None:
        Global.item_snd.play()
        self.state = Item.State.COLLECT
        self.collector = player
        return None

    def draw(self, surface: pygame.Surface) -> None:
        if self.state == Item.State.EXPIRED:
            item_value = Global.item_font.render(
                str(self.value), True, Global.Colour.RED)
            surface.blit(item_value, (self.x + (self.width // 2),
                         self.y - (self.timer // 2)))
        elif self.state == Item.State.COLLECTED:
            item_value = Global.item_font.render(
                str(self.value), True, Global.Colour.BLUE)
            surface.blit(item_value, (self.x + (self.width // 2),
                         self.y - (self.timer // 2)))
        elif self.state != Item.State.DESTROY:
            if self.state == Item.State.EXPIRING:
                if (self.timer // 10) % 2 == 0:
                    surface.blit(self.image, self.rect)
            else:
                surface.blit(self.image, self.rect)

        return None
