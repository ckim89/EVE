import GAME_GLOBALS
import pygame
import random
import pygame.sprite as SPRITE

class projectileobj(SPRITE.Sprite):
    def __init__(self, location, size, direction):
        SPRITE.Sprite.__init__(self)
        self.dx = 0
        self.dy = 0
        self.hitplayer = False
        self.hit = False
        self.hittimer = 0
        self.image = pygame.transform.scale(
            pygame.image.load(GAME_GLOBALS.ENEMY_LASER).convert(), (10,10))
        self.rect = pygame.Rect(location, size)
        dx = direction[0]
        dy = direction[1]
        if dx < -75:
            self.x = 1
        elif dx > -75 and dx < 75:
            self.x = 0
        else:
            self.x = -1
        if dy < -75:
            self.y = 1
        elif dy > -75 and dy < 75:
            self.y = 0
        else:
            self.y = -1


    def update(self, wallgroup, playerlocation, player):
        self.rect.centerx += 5 * self.x
        self.rect.centery += 5 * self.y
        if self.hittimer == 0 and self.hit == True:
            self.hittimer += 5
        if self.hittimer == 100:
            self.hittimer = 0
            self.hit = False
        for walls in wallgroup:
            if self.rect.colliderect(walls.rect):
                self.x = 0
                self.y = 0
                return True
        if self.rect.colliderect(playerlocation):
            self.x = 0
            self.y = 0
            self.hitplayer = True
            player.current_health -= 5
            return True
        return False





