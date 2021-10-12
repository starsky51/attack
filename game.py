# import libraries
import random
import pygame
import logging
from pygame.sprite import Group

# import locals
from globals import Global
from obstacle import Obstacle
from item import Item
from player import Player

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

    def __init__(self, num_players : int, difficulty : DifficultyLevel) -> None:
        self.difficulty : float = difficulty

        self.players : Group = pygame.sprite.Group()
        self.obstacles : Group = pygame.sprite.Group()
        self.items : Group = pygame.sprite.Group()

        # TODO: give each player a different sprite
        # create players
        for i in range(0, num_players):
            self.players.add(Player(self, Global.player_img, 70 + (i * 70), Global.SCREEN_HEIGHT - 100))

        # create obstacles
        top_wall = Obstacle(Obstacle.Type.WALL, 0, 0, Global.SCREEN_WIDTH, 20)
        bottom_wall = Obstacle(Obstacle.Type.WALL, 0, Global.SCREEN_HEIGHT - 20, Global.SCREEN_WIDTH, 20)
        left_wall = Obstacle(Obstacle.Type.WALL, 0, 20, 20, Global.SCREEN_HEIGHT - 20)
        right_wall = Obstacle(Obstacle.Type.WALL, Global.SCREEN_WIDTH - 20, 0
                                , Global.SCREEN_WIDTH - 20, Global.SCREEN_HEIGHT - 20)
        self.obstacles.add(top_wall)
        self.obstacles.add(bottom_wall)
        self.obstacles.add(left_wall)
        self.obstacles.add(right_wall)

        for i in range(0, 10):
            print('Spawning obstacle', i+1, 'of', 24)
            try:
                self.spawn_table()
            except SpawnObstacleException:
                print("Unable to create obstacle {}", i)

        for i in range(0, 20):
            print('Spawning item', i+1, 'of', 20)
            self.spawn_biscuit()

        return None

    def update(self) -> None:
        # move players
        for player in self.players:
            player.move()

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
            item = Item(Item.Type.BISCUIT, random.randrange((20 + 15), Global.SCREEN_WIDTH - (20 + 15))
                        , random.randrange((20 + 15), Global.SCREEN_HEIGHT - (20 + 15)), lifespan)

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
            obstacle = Obstacle(Obstacle.Type.TABLE, random.randrange((20 + self.players.sprites()[0].width + 30)
                , Global.SCREEN_WIDTH - (20 + self.players.sprites()[0].width + 30))
                , random.randrange((20 + self.players.sprites()[0].height + 30)
                , Global.SCREEN_HEIGHT - (20 + self.players.sprites()[0].height + 30))
                , 30, 30)

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

    def draw(self, surface : pygame.Surface) -> None:
        # draw background
        for i in range(0, Global.bg_tiles_x):
            for j in range(0, Global.bg_tiles_y):
                if j % 2 == 0:
                    surface.blit(Global.bg_img, (i * Global.bg_img.get_width()
                        , j * Global.bg_img.get_height()))
                else:
                    surface.blit(Global.bg_img_flipy, (i * Global.bg_img.get_width()
                        , j * Global.bg_img.get_height()))

        # draw obstacles
        self.obstacles.draw(surface)

        # draw items
        for item in self.items:
            item.draw(surface)

        # draw players and scores
        for index, player in enumerate(self.players):
            player.draw(surface)
            score_text = Global.status_font.render(str(player.score), True, Global.Colour.BLACK)
            if index == 0:
                score_x, score_y = 0, 0
            elif index == 1:
                score_x, score_y = Global.SCREEN_WIDTH - 40, 0
            elif index == 2:
                score_x, score_y = 0, Global.SCREEN_HEIGHT - 40
            elif index == 3:
                score_x, score_y = Global.SCREEN_WIDTH - 40, Global.SCREEN_HEIGHT - 40
            surface.blit(score_text, (score_x, score_y))

        return None