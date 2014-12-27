import pygame
import pygame.sprite as SPRITE
from vec2 import *
from collections import namedtuple
import GAME_GLOBALS
from collections import defaultdict
import time
# Enumerate types for states
ACCELERATING = 'ACCEL'
INVULNERABLE = 'INVULN'
IDLE = 'IDLE'
WALKING = 'WALK'
RUNNING = 'RUN'
ATTACKING = 'ATTACK'
DAMAGED = 'DAMAGED'
STUNNED = 'STUNNED'
DECELERATING = 0x10


Animation = namedtuple('animation', ['im', 'speed', 'count'], verbose=False)


class animation():
    def __init__(self, im, speed, frame_length):
        self.im = im
        self.speed = speed
        self.framecount = frame_length


class Gameobj(SPRITE.Sprite):
    def __init__(self, spritesheet, size, location):
        """
        Parent class for all game objects. Inherits from pygame's Sprite
        Class and the States class.
        :type self: pygame.sprite.Sprite
        :param spritesheet: path to the spritesheet for the gameobj
        :param size: size of the object
        :param spritesheet_dim: size of each sprite on the spritesheet
               (in pixels)
        :param location: where to place the object
        """
        # Parent constructor call
        SPRITE.Sprite.__init__(self)

        assert isinstance(spritesheet, str)
        assert isinstance(size, tuple)

        # Animation controls:
        # anim_delay: controls animation speed
        #anim_pos: controls which image in the animation string to display
        #anim_images: dictionary containing all animations
        #anim_delay: Controls how fast the current animation plays
        #angle: angle to rotate the current image so things make sense
        #current_anim: list of the frames for the current animation
        #image: the image that is currently being drawn
        self.anim_images = defaultdict(list)
        self.extract_sprites(spritesheet, size)
        self.anim_delay = .1
        self.type = None
        self.anim_pos = 0
        self.angle = 0
        self.angle_lookup = {}
        self.image = None
        directions = ['', 'up', 'right', 'left', 'down', 'upleft', 'upright', 'downleft', 'downright']
        angle = [0, 0, -90, 90, 180, 45, -45, 135, -135]
        for i in range(0, len(directions)):
            self.angle_lookup.update({directions[i]: angle[i]})
        self.current_anim = self.anim_images.get('IDLE')

        #External game control:
        #rect: bounding rectangle for detection
        #state: current state of the object can take on:
        #   IDLE: Default
        #   RUNNING
        #   ATTACKING
        #   DAMAGED
        #   STUNNED
        #pending_IDLE: used for movement control (maybe deleted?)
        #state_change: a boolean that allows the update loop to know
        #              if the state was changed and do appropriate updates
        #vel: a vec2 that determines how fast the object moves
        #accel: how fast the vel is accelerating
        #decel: how fast the vel decelerating
        #walk_speed: how fast the object can move when state = WALKING
        #run_speed: how fast the object can move when state = RUNNING
        #max_speed: a generic variable that is set to walk_speed or run_speed
        self.rect = pygame.Rect(location, size)
        self.previous_position = (self.rect.centerx, self.rect.centery)
        self.attack_timer = 0
        self.swordflag = False
        self.state = IDLE
        self.state_mod = None
        self.pending_IDLE = False
        self.state_change = False
        self.speed = 0
        self.vel = vec2(0.0, 0.0)
        self.accel = .5
        self.decel = .2
        self.walk_speed = 3
        self.run_speed = 7
        self.max_speed = 0
        self.modal = False
        self.damagetimer = 0
        self.tick = 0
        self.attacked = False
        self.bump = GAME_GLOBALS.BUMP
        self.bump.set_volume(0.2)
        self.can_sound = True
        self.attackbuffer = 0
        self.attackpos = 1
        self.freeze = False
        self.currentattack =''

    def rotate_center(self, im, theta):
        """
        Rotates an image about its center without rectangle distortion
        :type im: pygame.Surface
        :param im: image to rotate
        :param theta: how much to rotated
        Code Credit: www.pygame.org/wiki/RotateCenter?parent=CookBook
        """
        orig_rect = im.get_rect()
        rotated = pygame.transform.rotate(im, theta)
        rotated_rect = orig_rect.copy()
        rotated_rect.center = rotated.get_rect().center
        rotated = rotated.subsurface(rotated_rect).copy().convert_alpha()
        rotated.set_alpha(255)
        return rotated

    def extract_sprites(self, spritesheet, size):
        """
        Extracts sprites from an inputted spritesheet
        :type self: Gameobj
        :param spritesheet: the path to the spritesheet
        :param size: size of the sprite to scale to in pixels.
        """

        assert isinstance(spritesheet, str)
        assert isinstance(size, tuple)

        # Pull in spritesheet specs from associated file
        fpath = spritesheet.split('/')
        fpath[-1] = fpath[-1].split('.')[0] + ".dat"
        fpath = '/'.join(fpath)
        spritesheet_config = open(fpath)
        anim_args = []
        sprite_dimensions = 0
        exec spritesheet_config
        spritesheet_config.close()
        # temp fix
        a_images = pygame.image.load(spritesheet).convert()
        assert isinstance(a_images, pygame.Surface)
        rect = a_images.get_rect()
        row_count = rect.size[1] / sprite_dimensions[1]
        col_count = rect.size[0] / sprite_dimensions[0]

        a_images = pygame.transform.scale(a_images,
                                          (col_count * size[0],
                                           row_count * size[1]))

        key = a_images.get_at((0, 0))
        new_anims = []
        for j in range(0, row_count):
            for i in range(0, col_count):
                new_im = pygame.Surface(size)
                new_im.fill((255, 255, 255, 0),None, pygame.BLEND_RGBA_MULT)
                new_im.set_colorkey(key)
                new_im.blit(a_images, (0, 0), (i * size[0], j * size[1], size[0], size[1]))
                new_anims.append(new_im)

        current_pos = 0
        for args in anim_args:
            self.anim_images.update({args[0]: new_anims[current_pos:current_pos + args[-1]]})
            current_pos += args[-1]

        self.anim_images.update({'IDLE': [(self.anim_images.get('WALK')[0]).convert()]})
        #self.anim_images.update({'RUN': self.anim_images.get('WALK')})

    def set_state(self,state):
        if state == DAMAGED:
            self.modal = True
        if self.state != state:
            self.state = state
            self.anim_pos = 0
            self.current_anim = self.anim_images.get(state)
            self.state_change = True


    def update(self, dpos, world_objects, skip = False):
        """
        Parent update function. Keeps track of current speed and states
        :rtype : None
        :param dpos: a vec2 that says which direction to go
        """
        #assert isinstance(dpos, vec2)
        #angle = [0, 0, -90, 90, 180, 45, -45, 135, -135]

        check = False
        self.anim_delay = 0.1
        if self.attackbuffer > 2:
            self.attackbuffer = 2
        if self.state_change:
            if self.state == RUNNING:
                self.max_speed = self.run_speed
            elif self.state == WALKING:
                self.max_speed = self.walk_speed
            elif self.state == IDLE:
                self.max_speed = 0
            elif self.state == ATTACKING:
                self.modal = True
            self.state_change = False


        if self.state == DAMAGED:
            self.modal = True
            if self.anim_pos >= len(self.current_anim) - 1:
                self.attack_timer = 0
                self.set_state(IDLE)
                self.can_sound = True
                self.modal = False

        if self.state == ATTACKING:
            self.anim_delay = 0.2
            h = self.state+str(self.attackpos)
            self.currentattack = h
            self.current_anim = self.anim_images.get(self.state+str(self.attackpos))

            if self.anim_pos >= len(self.current_anim) - 1:
                self.attackbuffer -= 1
                if self.attackbuffer > 0:
                    if self.attackpos + 1 > 2:
                        self.attackpos = 0
                    self.attackpos += 1
                else:
                    self.attack_timer = 0
                    self.set_state(IDLE)
                    self.can_sound = True
                    self.modal = False


        if not self.modal:
            if self.speed < self.max_speed:
                self.speed += self.accel
            if self.speed >= self.max_speed and self.state != IDLE:
                self.speed -= self.accel

            dx = self.speed*dpos.x
            dy = self.speed*dpos.y
            self.previous_position = self.rect.copy()
            self.previous_position.centerx += dx
            self.previous_position.centery += dy

            if not skip:
                for walls in world_objects:
                    if self.previous_position.colliderect(walls.rect):
                        self.set_state(IDLE)
                        check = True
                        dx = 0
                        dy = 0
                        break

            self.rect.centerx += dx
            self.rect.centery += dy
        self.draw()

        return check

    def draw(self):
        self.image = pygame.transform.rotate(self.current_anim[int(self.anim_pos)], self.angle)
        if self.anim_pos <= len(self.current_anim) - 1:
            self.anim_pos = self.anim_pos + self.anim_delay
        else:
            if not self.freeze:
                self.anim_pos = 0
        #(pygame.display.get_surface()).blit(self.image, self.rect.topleft)
