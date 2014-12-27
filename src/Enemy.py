import pygame
import sys
import random
import GAME_GLOBALS
import egameobj
import gameobj
from vec2 import *
from projectileobj import *

pygame.init()
pygame.font.init()


class Enemy(egameobj.Gameobj):

    def __init__(self, params, size, location):
        """
        Player constructor.
        :param Default player spritesheet file path:
        """
        self.x = 0
        self.tagged = False
        self.y = 0
        egameobj.Gameobj.__init__(self, params, size, location)
        if params == GAME_GLOBALS.PROJECT_ENEMY:
            self.type = 'projectile'
        elif params == GAME_GLOBALS.MELEE_ENEMY or GAME_GLOBALS.CAPTAIN_ENEMY:
            self.type = 'melee'
        self.lockarrow = pygame.Surface((10,10))
        self.lockarrow.fill(GAME_GLOBALS.RED)
        self.lock = False
        if params == GAME_GLOBALS.CAPTAIN_ENEMY:
            self.health = 200
        else:
            self.health = 100
        self.healthbar = pygame.Surface((50,20))
        self.healthbar.fill(GAME_GLOBALS.BLACK)
        self.healthfont = pygame.font.Font(GAME_GLOBALS.DEFAULT_FONT, 12)
        self.name = 'enemy'
        self.timer = 0
        self.approach = pygame.mixer.Sound('../sounds/ApproachEnemy.ogg')
        if self.type == 'melee':
            if random.randint(0, 1) == 1:
                self.x = 1
            else:
                self.x = -1
            if random.randint(0, 1) == 1:
                self.y = 1
            else:
                self.y = -1
        elif self.type == 'projectile':
            self.x = 0
            self.y = 0
        self.current_bin_pos = 2



    """
    The enemy as of now is set to move randomly throughout the stage.
    We added an element of AI where if we are within the range of a player,
    we start to chase them.
    """
    def update(self, playerlocation, world_objs):
        projectile = None
        self.awareness = self.rect.copy()
        self.awareness = self.awareness.inflate(500, 500)
        dpos = vec2(self.x, self.y)
        dir = 'down'
        direction = self.intelligence(playerlocation)
        if direction[0] > 75:
            dir = 'left'
        elif direction[0] < -75:
            dir = 'right'
        if direction[1] < -75:
            dir = 'down'
        elif direction[1] > 75:
            dir = 'up'

        self.angle = self.angle_lookup.get(dir)
        if self.state != gameobj.ATTACKING:
            if self.type == 'melee':
                self.set_state(gameobj.WALKING)
            elif self.type == 'projectile':
                self.set_state(gameobj.IDLE)

        if self.state == gameobj.ATTACKING and self.type == 'projectile':
            if self.attack_timer == 0:
                projectile = projectileobj((self.rect.centerx, self.rect.centery), (10, 10), direction)


        if not self.modal:
            if self.awareness.collidepoint(playerlocation.center):
                egameobj.Gameobj.update(self, dpos, world_objs, self.type, False)
                direction = self.intelligence(playerlocation)
                if direction[0] < 0:
                    self.x = 1
                elif direction[0] > 0:
                    self.x = -1
                else:
                    self.x = 0
                if direction[1] < 0:
                    self.y = 1
                elif direction[1] > 0:
                    self.y = -1
                else:
                    self.y = 0
            else:
                check = egameobj.Gameobj.update(self, dpos, world_objs, self.type)
                if check == True:
                    if random.randint(0, 1) == 1:
                        self.x = -1 * self.x
                    else:
                        self.x = 1 * self.x
                    if random.randint(0, 1) == 1:
                        self.y = -1 * self.y
                    else:
                        self.y = 1 * self.y

        else:
            egameobj.Gameobj.update(self,dpos,world_objs, self.type)

        if self.lock == True:
            self.image.blit(self.lockarrow, (50, 0))


        return projectile


      #  self.image.blit(self.healthbar, (25, 0))

    """
    checks the location of the player and then makes a new vector
    that points in the player's direction.
    We use this vector to then follow the player around.
    """
    def intelligence(self, playerlocation):
        dx = 0
        dy = 0
        dx = self.rect.centerx - playerlocation.centerx
        dy = self.rect.centery - playerlocation.centery
        return [dx, dy]

    def locked(self):
        self.lock = True

    def unlock(self):
        self.lock = False


