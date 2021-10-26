# import libraries
import pygame

#import locals
from globals import Global

# player class


class Player(pygame.sprite.Sprite):
    image : pygame.Surface = None
    game = None
    position : pygame.Vector2 = None
    velocity : pygame.Vector2 = None
    max_speed : float = None
    acceleration : float = None
    angle : float = None
    score : int = None

    # TODO: add angle/direction variable to maintain direction when bouncing off things
    def __init__(self, game, image: pygame.Surface, position: pygame.Vector2, initial_acceleration: float = 0) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image: pygame.Surface = pygame.transform.scale(image, (int(Global.TILE_WIDTH * 1.5), int(Global.TILE_HEIGHT * 1.5)))
        self.game = game
        self.velocity = pygame.Vector2(0, 0)
        self.max_speed = 5
        self.acceleration = 0.5
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
        self.rect.center = position

        return None

    # TODO: fix collision detection! - especially with bounciness
    def move(self) -> None:
        # process key presses
        key: pygame = pygame.key.get_pressed()

        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
            self.max_speed = 12
        else:
            self.max_speed = 8

        overspeed = self.velocity.length() > self.max_speed
        # TODO: add individual controls for each player
        if key[pygame.K_LEFT]:
            if not overspeed:
                self.velocity.x += -self.acceleration
            # self.flip = True
        if key[pygame.K_RIGHT]:
            if not overspeed:
                self.velocity.x += self.acceleration
            # self.flip = False
        if key[pygame.K_UP]:
            if not overspeed:
                self.velocity.y += -self.acceleration
        if key[pygame.K_DOWN]:
            if not overspeed:
                self.velocity.y += self.acceleration

        # hold new player position
        proposed_rect = self.rect.copy()
        proposed_rect.center += self.velocity

        # check for screen edge collision
        # if proposed_rect.left < 0:
        #     self.velocity.x *= -1
        #     proposed_rect.x *= -1
        # if proposed_rect.right > self.game.screen.get_width():
        #     self.velocity.x *= -1
        #     proposed_rect.x -= proposed_rect.right - self.game.screen.get_width()
        # if proposed_rect.top < 0:
        #     self.velocity.y *= -1
        #     proposed_rect.y *= -1
        # if proposed_rect.bottom > self.game.screen.get_height():
        #     self.velocity.y *= -1
        #     proposed_rect.y -= proposed_rect.bottom - self.game.screen.get_height()

        # TODO: cause player collisions to transfer some of a players energy to the other player
        #   fast player should belly bounce the other player further

        # check for player collision
        for player in self.game.players:
            if player is self:
                continue
            # first check collisions on the x-axis, removing the y-axis movement altogether
            proposed_rect_xonly = proposed_rect.copy()
            proposed_rect_xonly.center -= pygame.Vector2(0, self.velocity.y)
            if player.rect.colliderect(proposed_rect_xonly):
                if proposed_rect.left < player.rect.right and self.velocity.x < 0:
                    self.velocity.x *= -1
                    proposed_rect.x += 2 * (player.rect.right - proposed_rect.left)
                elif proposed_rect.right > player.rect.left and self.velocity.x > 0:
                    self.velocity.x *= -1
                    proposed_rect.x -= 2 * (proposed_rect.right - player.rect.left)

            # next, check collisions on the y-axis, including any adjustments made to the x-axis
            #   in the previous step
            if player.rect.colliderect(proposed_rect):
                if proposed_rect.top < player.rect.bottom and self.velocity.y < 0:
                    self.velocity.y *= -1
                    proposed_rect.y += 2 * (player.rect.top - proposed_rect.bottom)
                elif proposed_rect.bottom > player.rect.top and self.velocity.y > 0:
                    self.velocity.y *= -1
                    proposed_rect.y -= 2 * (proposed_rect.top - player.rect.bottom)

        # check for obstacle collision - works similarly to player-player collision
        for obstacle in self.game.obstacles:
            proposed_rect_xonly = proposed_rect.copy()
            proposed_rect_xonly.y = self.rect.y
            # print(self.rect, proposed_rect, proposed_rect_xonly)
            if obstacle.rect.colliderect(proposed_rect_xonly):
                if proposed_rect.left < obstacle.rect.right and self.velocity.x < 0:
                    self.velocity.x *= (-1 * (obstacle.bounciness / 10))
                    proposed_rect.x += 2 * (obstacle.rect.right + 1 - proposed_rect.left)
                elif proposed_rect.right > obstacle.rect.left and self.velocity.x > 0:
                    self.velocity.x *= (-1 * (obstacle.bounciness / 10))
                    proposed_rect.x -= 2 * (proposed_rect.right - obstacle.rect.left)

            if obstacle.rect.colliderect(proposed_rect):
                if proposed_rect.top < obstacle.rect.bottom and self.velocity.y < 0:
                    self.velocity.y *= (-1 * (obstacle.bounciness / 10))
                    proposed_rect.y += 2 * (obstacle.rect.top - proposed_rect.bottom)
                elif proposed_rect.bottom > obstacle.rect.top and self.velocity.y > 0:
                    self.velocity.y *= (-1 * (obstacle.bounciness / 10))
                    proposed_rect.y -= 2 * (proposed_rect.top - obstacle.rect.bottom)

        # add friction 
        if abs(self.velocity.length()) < 0.5:
            self.velocity.update(0, 0)
        else:
            self.velocity.scale_to_length(self.velocity.length() * 0.95)
            # update angle - only when in motion
            self.angle = pygame.Vector2(0, 0).angle_to(self.velocity)

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

    def draw(self, surface: pygame.Surface, camera_pos : pygame.Vector2) -> None:
        # check player angle
        # right = 0deg, left = 180deg, up = -90deg, down = -90deg
        # weird!
         
        flip : bool = (abs(self.angle) > 90) 
        if flip:
            surface.blit(pygame.transform.flip(self.image, flip, False), (self.rect.x -
                         (self.image.get_width() - self.x_limit) - camera_pos[0], self.rect.y - self.y_offset - camera_pos[1]))
        else:
            surface.blit(self.image, (self.rect.x - self.x_offset - camera_pos[0],
                         self.rect.y - self.y_offset - camera_pos[1]))

        return None

        # pygame.draw.rect(surface, WHITE, self.rect, 2)
