# import libraries
import math
import random
import pygame
import logging
from pygame.sprite import Group

# import locals
from globals import Global
from obstacle import Obstacle
from item import Item
from player import Player
from tile import Tile, TileMap

# exception classes
class SpawnObstacleException(Exception):
    pass

class SpawnItemException(Exception):
    pass

# game class
class Game():
    class DifficultyLevel:
        EASY = 0
        MEDIUM = 15
        HARD = 30

    MAX_DIFFICULTY = 50

    # variables
    screen: pygame.Surface
    difficulty : float
    players : Group
    obstacles : Group
    items : Group
    camera_pos : pygame.Vector2
    camera_scale : float

    def __init__(self, num_players : int, difficulty : DifficultyLevel, tiles_x: int = 20, tiles_y: int = 20) -> None:
        self.difficulty = difficulty
        self.players = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.items = pygame.sprite.Group()

        self.tilemap = TileMap('maps/map1.map')
        self.camera_pos = pygame.Vector2(Global.SCREEN_WIDTH // 2, (self.tilemap.height * Global.TILE_HEIGHT) - (Global.SCREEN_HEIGHT // 2))
        self.camera_scale = 1.0
        print(self.camera_pos)

        self.screen = pygame.display.set_mode((Global.SCREEN_WIDTH, Global.SCREEN_HEIGHT))

        # init tileset
        self.tileset = {"WALL": Tile(Global.TileData.WALL.src, Global.TILE_WIDTH, Global.TILE_HEIGHT)
                      , "TABLE": Tile(Global.TileData.TABLE.src, Global.TILE_WIDTH, Global.TILE_HEIGHT)}

        # load images
        self.bg_img = pygame.image.load('images/bg.png').convert_alpha()
        self.bg_img_flipy = pygame.transform.flip(self.bg_img, False, True)
        # load player images        
        self.player_imgs = []
        self.player_imgs.append(pygame.image.load('images/player1.png').convert_alpha())
        self.player_imgs.append(pygame.image.load('images/player2.png').convert_alpha())
        self.player_imgs.append(pygame.image.load('images/player3.png').convert_alpha())
        self.player_imgs.append(pygame.image.load('images/player4.png').convert_alpha())

        # image metrics
        self.bg_tiles_x = math.ceil(self.screen.get_width() / self.bg_img.get_width())
        self.bg_tiles_y = math.ceil(self.screen.get_height() / self.bg_img.get_height())

        # TODO: add more sounds!
        # load sounds
        self.item_snd = pygame.mixer.Sound('sounds/item.wav')
        self.item_snd.set_volume(0.2)

        # for i in range (0, Global.SCREEN_WIDTH // Global.TILE_WIDTH):
        #     self.tilemap.setvalue(i, 0, 1)
        #     self.tilemap.setvalue(i, Global.SCREEN_HEIGHT // Global.TILE_HEIGHT - 1, 1)
        # for j in range (0, Global.SCREEN_HEIGHT // Global.TILE_HEIGHT):
        #     self.tilemap.setvalue(0, j, 1)
        #     self.tilemap.setvalue(Global.SCREEN_WIDTH // Global.TILE_WIDTH - 1, j, 1)

        # create players
        for i in range(0, num_players):
            print(self.tilemap.player_starts[str(i+1)])
            self.players.add(Player(self, self.player_imgs[i], (self.tilemap.player_starts[str(i+1)][0] * Global.TILE_WIDTH, self.tilemap.player_starts[str(i+1)][1] * Global.TILE_HEIGHT)))

        # create obstacles
        # top_wall = Obstacle(self.tileset["WALL"], 0, 0, Global.SCREEN_WIDTH, 20)
        # bottom_wall = Obstacle(self.tileset["WALL"], 0, Global.SCREEN_HEIGHT - 20, Global.SCREEN_WIDTH, 20)
        # left_wall = Obstacle(self.tileset["WALL"], 0, 20, 20, Global.SCREEN_HEIGHT - 20)
        # right_wall = Obstacle(self.tileset["WALL"], Global.SCREEN_WIDTH - 20, 0
        #                         , Global.SCREEN_WIDTH - 20, Global.SCREEN_HEIGHT - 20)
        # self.obstacles.add(top_wall)
        # self.obstacles.add(bottom_wall)
        # self.obstacles.add(left_wall)
        # self.obstacles.add(right_wall)

        for i in range(0, self.tilemap.width):
            for j in range(0, self.tilemap.height):
                tileval = self.tilemap.getvalue(i, j)
                
                if tileval == 0:
                    continue

                if tileval == 1:
                    tile = self.tileset["WALL"]
                elif tileval == 2:
                    tile = self.tileset["TABLE"]
                else:
                    raise(Exception("Tile value not recognised: " + str(i) + ", " + str(j) + " (" + str(tileval) + ")"))

                self.obstacles.add(Obstacle(tile, i * Global.TILE_WIDTH, j * Global.TILE_HEIGHT, Global.TILE_WIDTH, Global.TILE_HEIGHT))
        
        # for i in range(0, 20):
        #     print('Spawning obstacle', i+1, 'of', 24)
        #     try:
        #         self.spawn_table()
        #     except SpawnObstacleException:
        #         print("Unable to create obstacle {}", i)

        for i in range(0, 20):
            print('Spawning item', i+1, 'of', 20)
            self.spawn_biscuit()

        return None

    def update(self) -> None:

        # process key presses
        key: pygame = pygame.key.get_pressed()
        
        if key[pygame.K_EQUALS]:
            self.camera_pos.x += 10
            print(self.camera_pos)
        if key[pygame.K_MINUS]:
            self.camera_pos.x -= 10
            print(self.camera_pos)

        p1_pos = [0, 0]
        # move players
        for idx, player in enumerate(self.players):
            player.move()
            if idx == 0:
                p1_pos = player.rect.center
        
        # update camera
        board_width = self.tilemap.width * Global.TILE_WIDTH
        board_height = self.tilemap.height * Global.TILE_HEIGHT
        self.camera_pos.x, self.camera_pos.y = p1_pos[0], p1_pos[1]
        self.camera_pos.x = min(self.camera_pos.x, board_width - (Global.SCREEN_WIDTH // 2))
        self.camera_pos.x = max(self.camera_pos.x, Global.SCREEN_WIDTH // 2)
        self.camera_pos.y = min(self.camera_pos.y, board_height - (Global.SCREEN_HEIGHT // 2))
        self.camera_pos.y = max(self.camera_pos.y, Global.SCREEN_HEIGHT // 2)

        # update items
        for item in self.items:
            if item.update():
                self.items.remove(item)
                self.spawn_biscuit(wait=0, lifespan=(50 - self.difficulty) / 5)
        
        return None

    def spawn_biscuit(self, wait : int = 0, lifespan : float = 10) -> Item:
        attempt_count = 0
        print("lifespan:", lifespan)
        while True:
            attempt_count += 1
            item = Item(Item.Type.BISCUIT, random.randrange((20 + 15), self.screen.get_width() - (20 + 15))
                        , random.randrange((20 + 15), self.screen.get_height() - (20 + 15)), lifespan)

            collides = False
            # check for collisions with obstacles
            for existing in self.obstacles:
                if existing.rect.colliderect(item.rect):
                    collides = True
            # check for collisions with items
            for existing in self.items:
                if existing.rect.colliderect(item.rect.x - self.players.sprites()[0].width
                                            , item.rect.y - self.players.sprites()[0].height
                                            , item.width + (2*self.players.sprites()[0].width)
                                            , item.height + (2*self.players.sprites()[0].height)):
                    collides = True
            # check for collisions with players
            for existing in self.players:
                if existing.rect.colliderect(item.rect):
                    collides = True
            # if collision is still detected after 20th attempt, raise exception
            if collides:
                if attempt_count > 20:
                    # raise SpawnItemException("Unable to find space to add item!")
                    logging.warning("Unable to find space to add item!")
                    return None
            else:
                #exit loop if no collision is detected
                break

        # add item to the group
        self.items.add(item)

        return item

    def spawn_table(self) -> Obstacle:
        attempt_count = 0
        while True:
            attempt_count += 1
            obstacle = Obstacle(self.tileset['TABLE'], random.randrange((20 + self.players.sprites()[0].width + 30)
                , self.screen.get_width() - (20 + self.players.sprites()[0].width + 30))
                , random.randrange((20 + self.players.sprites()[0].height + 30)
                , self.screen.get_height() - (20 + self.players.sprites()[0].height + 30)))

            collides = False
            # check for collisions with existing obstacles
            for existing in self.obstacles:
                if existing.rect.colliderect(obstacle.rect.x - self.players.sprites()[0].width
                                            , obstacle.rect.y - self.players.sprites()[0].height
                                            , obstacle.width + (2*self.players.sprites()[0].width)
                                            , obstacle.height + (2*self.players.sprites()[0].height)):
                    collides = True
            # check for collisions with players
            for existing in self.players:
                if existing.rect.colliderect(obstacle.rect):
                    collides = True
            # if collision is still found after 20th attempt, raise exception
            if collides:
                if attempt_count > 20:
                    # raise SpawnObstacleException("Unable to find space to add obstacle!")
                    logging.warning("Unable to find space to add obstacle!")
                    return None
            else:
                break

        # add obstacle to the group
        self.obstacles.add(obstacle)

        return obstacle

    def draw(self) -> None:
        # draw background
        for i in range(0, self.bg_tiles_x):
            for j in range(0, self.bg_tiles_y):
                if j % 2 == 0:
                    self.screen.blit(self.bg_img, (i * self.bg_img.get_width()
                        , j * self.bg_img.get_height()))
                else:
                    self.screen.blit(self.bg_img_flipy, (i * self.bg_img.get_width()
                        , j * self.bg_img.get_height()))

        origin = (self.camera_pos[0] - (Global.SCREEN_WIDTH // 2), self.camera_pos[1] - (Global.SCREEN_HEIGHT // 2))
        # draw obstacles
        for obstacle in self.obstacles:
            obstacle.draw(self.screen, origin)

        # draw items
        for item in self.items:
            item.draw(self.screen, origin)

        # draw players and scores
        for index, player in enumerate(self.players):
            player.draw(self.screen, origin)
            score_text = Global.status_font.render(str(player.score), True, Global.Colour.BLACK)
            if index == 0:
                score_x, score_y = 0, 0
            elif index == 1:
                score_x, score_y = self.screen.get_width() - 40, 0
            elif index == 2:
                score_x, score_y = 0, self.screen.get_height() - 40
            elif index == 3:
                score_x, score_y = self.screen.get_width() - 40, self.screen.get_height() - 40
            self.screen.blit(score_text, (score_x, score_y))

        return None