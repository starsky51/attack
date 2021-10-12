# import libraries
import pygame

#import locals
from globals import Global

# player class


class Player(pygame.sprite.Sprite):
    image : pygame.Surface = None
    game = None
    max_speed : float = None
    acceleration : float = None
    velocity : pygame.Vector2 = None
    angle : float = None
    score : int = None

    def __init__(self, game, image: pygame.Surface, x: int, y: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image: pygame.Surface = pygame.transform.scale(image, (40, 50))
        self.game = game
        self.max_speed = 5
        self.acceleration = 0.5
        self.velocity = pygame.Vector2(0, 0)
        self.angle = 0
        self.score = 0

        # calculate visible pixel boundaries
        self.x_offset: int = self.image.get_width()
        self.x_limit: int = 0
        self.y_offset: int = self.image.get_height()
        self.y_limit: int = 0
        pixelarray = pygame.PixelArray(self.image)
        for i in range(0, self.image.get_width()-1):
            for j in range(0, self.image.get_height()-1):
                if pixelarray[i, j] > 0 and i < self.x_offset:
                    self.x_offset = i
                if pixelarray[i, j] > 0 and i > self.x_limit:
                    self.x_limit = i
                if pixelarray[i, j] > 0 and j < self.y_offset:
                    self.y_offset = j
                if pixelarray[i, j] > 0 and j > self.y_limit:
                    self.y_limit = j

        self.width: int = self.x_limit - self.x_offset
        self.height: int = self.y_limit - self.y_offset
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)

        return None

    def move(self) -> None:
        # process key presses
        key: pygame = pygame.key.get_pressed()

        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
            self.max_speed = 12
        else:
            self.max_speed = 8

        # TODO: add individual controls for each player
        if key[pygame.K_LEFT]:
            self.velocity.x += -self.acceleration
            # self.flip = True
        if key[pygame.K_RIGHT]:
            self.velocity.x += self.acceleration
            # self.flip = False
        if key[pygame.K_UP]:
            self.velocity.y += -self.acceleration
        if key[pygame.K_DOWN]:
            self.velocity.y += self.acceleration

        # check for screen edge collision
        if self.rect.left + self.velocity.x < 0:
            self.velocity.x = -self.rect.left
        if self.rect.right + self.velocity.x > Global.SCREEN_WIDTH:
            self.velocity.x = Global.SCREEN_WIDTH - self.rect.right
        if self.rect.top + self.velocity.y < 0:
            self.velocity.y = -self.rect.top
        if self.rect.bottom + self.velocity.y > Global.SCREEN_HEIGHT:
            self.velocity.y = Global.SCREEN_HEIGHT - self.rect.bottom

        # TODO: cause player collisions to transfer some of a players energy to the other player
        #   fast player should belly bounce the other player further
        
        # check for player collision
        for player in self.game.players:
            if player is self:
                continue
            if player.rect.colliderect(self.rect.left + self.velocity.x, self.rect.top, self.width, self.height):
                if (self.rect.left + self.velocity.x) < player.rect.right and self.velocity.x < 0:
                    # self.velocity.x = player.rect.right - self.rect.left
                    self.velocity.x *= -1
                elif (self.rect.right + self.velocity.x) > player.rect.left and self.velocity.x > 0:
                    # self.velocity.x = player.rect.left - self.rect.right
                    self.velocity.x *= -1

            if player.rect.colliderect(self.rect.left + self.velocity.x, self.rect.top + self.velocity.y, self.width, self.height):
                if (self.rect.top + self.velocity.y) < player.rect.bottom and self.velocity.y < 0:
                    # self.velocity.y = player.rect.bottom - self.rect.top
                    self.velocity.y *= -1
                elif (self.rect.bottom + self.velocity.y) > player.rect.top and self.velocity.y > 0:
                    # self.velocity.y = player.rect.top - self.rect.bottom
                    self.velocity.y *= -1

        # check for obstacle collision
        for obstacle in self.game.obstacles:
            if obstacle.rect.colliderect(self.rect.left + self.velocity.x, self.rect.top, self.width, self.height):
                if (self.rect.left + self.velocity.x) < obstacle.rect.right and self.velocity.x < 0:
                    # self.velocity.x = obstacle.rect.right - self.rect.left
                    self.velocity.x *= (-1 * (obstacle.bounciness / 10))
                elif (self.rect.right + self.velocity.x) > obstacle.rect.left and self.velocity.x > 0:
                    # self.velocity.x = obstacle.rect.left - self.rect.right
                    self.velocity.x *= (-1 * (obstacle.bounciness / 10))

            if obstacle.rect.colliderect(self.rect.left + self.velocity.x, self.rect.top + self.velocity.y, self.width, self.height):
                if (self.rect.top + self.velocity.y) < obstacle.rect.bottom and self.velocity.y < 0:
                    # self.velocity.y = obstacle.rect.bottom - self.rect.top
                    self.velocity.y *= (-1 * (obstacle.bounciness / 10))
                elif (self.rect.bottom + self.velocity.y) > obstacle.rect.top and self.velocity.y > 0:
                    # self.velocity.y = obstacle.rect.top - self.rect.bottom
                    self.velocity.y *= (-1 * (obstacle.bounciness / 10))

        # manage top speed
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        # add friction 
        if abs(self.velocity.length()) < 0.5:
            self.velocity.update(0, 0)
        else:
            self.velocity.scale_to_length(self.velocity.length() * 0.95)
            # update angle - only when in motion
            self.angle = pygame.Vector2(0, 0).angle_to(self.velocity)
            print (self.angle)
        print(self.velocity.x, self.velocity.y)

        # update rect position
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        # check for item collision
        for item in self.game.items:
            if item.collectable and item.rect.colliderect(self.rect):
                item.collect(self)
                # increase difficulty if appropriate
                total_score = sum(p.score for p in self.game.players)
                if total_score % 10 == 0:
                    self.game.difficulty += 1
                    print("Difficulty:", self.game.difficulty)

        return None

    def draw(self, surface: pygame.Surface) -> None:
        # check player angle
        # right = 0deg, left = 180deg, up = -90deg, down = -90deg
        # weird!
         
        flip : bool = (abs(self.angle) > 90) 
        if flip:
            surface.blit(pygame.transform.flip(self.image, flip, False), (self.rect.x -
                         (self.image.get_width() - self.x_limit), self.rect.y - self.y_offset))
        else:
            surface.blit(self.image, (self.rect.x - self.x_offset,
                         self.rect.y - self.y_offset))

        return None

        # pygame.draw.rect(surface, WHITE, self.rect, 2)
