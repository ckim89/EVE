import pygame
import sys
import random
import GAME_GLOBALS
import egameobj
import gameobj
from vec2 import *
import High_Score
import time
import deathscreen
import pygame.joystick


def extract_sprites(spritesheet, size):
    """
    Extracts sprites from an inputted spritesheet
    :type self: Gameobj
    :param spritesheet: the path to the spritesheet
    :param size: size of the sprite to scale to in pixels.
    """

    assert isinstance(spritesheet, str)
    assert isinstance(size, tuple)
    anim_images = {}
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
        anim_images.update({args[0]: new_anims[current_pos:current_pos + args[-1]]})
        current_pos += args[-1]

    return anim_images



class Player(gameobj.Gameobj):
    def __init__(self, params, size, location):
        """
        Player constructor.
        :param Default player spritesheet file path:
        """
        gameobj.Gameobj.__init__(self, params, size, location)
        self.max_health = 100
        self.current_health = 100
        self.score = 0
        self.invuln = False
        self.sw = GAME_GLOBALS.SWORDBLOCK
        self.attacksnd= GAME_GLOBALS.PATTACK
        self.dmgmix = GAME_GLOBALS.DAMAGE
        self.distance = 400
        attackanim1 = extract_sprites('../images/attack1.png', (100, 220))
        attackanim2 = extract_sprites('../images/attack2.png', (100, 220))
        self.anim_images.update({gameobj.ATTACKING+"1": attackanim1.get('ATTACK1')})
        self.anim_images.update({gameobj.ATTACKING+"2": attackanim2.get('ATTACK2')})
        a1 = self.anim_images.get('ATTACK1')
        a3 = pygame.image.load('../images/attack3.png').convert_alpha()
        a3 = pygame.transform.scale(a3, (90, 190))
        a1.append(a3)
        for i in range(0, 5):
            a1.append(a1[-1])
        self.anim_images.update({'ATTACK1': a1})
        a2 = self.anim_images.get('ATTACK2')
        for i in range(0, 5):
            a2.append(a2[-1])
        self.anim_images.update({'ATTACK2': a2})
        self.attackdelay = -1

        self.masks = {}
        self.masks['ATTACK1'] =  []
        for i in self.anim_images.get('ATTACK1'):
            self.masks['ATTACK1'].append(pygame.mask.from_surface(i))
        self.masks['ATTACK2'] =  []
        for i in self.anim_images.get('ATTACK2'):
            self.masks['ATTACK2'].append(pygame.mask.from_surface(i))
        self.currentmask = None
        self.current_bin_pos = 2


    def update(self, event, world_objs, enemy_group, cs, proj):
        """
        Override of Gameobj.update() to accept keyboard input
        :param event: events grabbed by the core
        """
        flags = []
        self.score = cs
        if self.current_health <= 0:
            highscorefile = open('hsf.txt', 'r')
            for line in highscorefile:
                data = line.split()
                currhigh = int(data[1])
                if currhigh < cs:
                    updatefile = open('hsf.txt', 'w')
                    updatefile.write('name: ' + str(cs))
                    updatefile.close()
            highscorefile.close()
            return 'died'
        keysdown = pygame.key.get_pressed()
        for events in event:
            if events.type == pygame.JOYBUTTONDOWN:
                GAME_GLOBALS.BUTTONS[events.button] = True
            if events.type == pygame.JOYBUTTONUP:
                GAME_GLOBALS.BUTTONS[events.button] = False
            if GAME_GLOBALS.BUTTONS[13]:
                self.lock_on(enemy_group)
            if events.type == pygame.KEYDOWN:
                if events.key == pygame.K_z:
                    self.lock_on(enemy_group)
        pressed = False
        for i in GAME_GLOBALS.BUTTONS:
            if i == True:
                pressed = True
        dpos = vec2(0, 0)
        if not self.modal:
            if keysdown[pygame.K_UP] or keysdown[pygame.K_RIGHT] or keysdown[pygame.K_DOWN] or keysdown[pygame.K_LEFT] or pressed:
                dir = ''
                if keysdown[pygame.K_UP] or GAME_GLOBALS.BUTTONS[0]:
                    dpos.y = -1
                    dir = 'up'
                elif keysdown[pygame.K_DOWN] or GAME_GLOBALS.BUTTONS[1]:
                    dpos.y = 1
                    dir = 'down'
                if keysdown[pygame.K_LEFT] or GAME_GLOBALS.BUTTONS[2]:
                    dpos.x = -1
                    dir += 'left'
                elif keysdown[pygame.K_RIGHT] or GAME_GLOBALS.BUTTONS[3]:
                    dir += 'right'
                    dpos.x = 1
                if keysdown[pygame.K_SPACE] or GAME_GLOBALS.BUTTONS[8]:
                    self.set_state(gameobj.RUNNING)
                else:
                    self.set_state(gameobj.WALKING)
                self.angle = self.angle_lookup.get(dir)
            else:
                self.set_state(gameobj.IDLE)
        if keysdown[pygame.K_a] or GAME_GLOBALS.BUTTONS[11]:
            if GAME_GLOBALS.BUTTONS[11] == True:
                GAME_GLOBALS.BUTTONS[11] = False
            if self.attackdelay == -1:
                self.attackdelay = time.time()
            if time.time() - self.attackdelay >= 0.2:
                self.attackbuffer+=1
                self.attackdelay = -1
            self.set_state(gameobj.ATTACKING)
            if self.can_sound:
                self.attacksnd.play()
        gameobj.Gameobj.update(self, dpos, world_objs)

        for objects in enemy_group:
            aware = objects.rect.copy()
            aware = aware.inflate(600,600)
            if self.state == gameobj.ATTACKING:
                if self.angle in [0, -45]:
                    r1 = self.image.get_rect(bottomleft=self.rect.bottomleft)
                    r2 = objects.image.get_rect(bottomleft=objects.rect.bottomleft)
                elif self.angle in [180, -135, -90]:
                    r1 = self.image.get_rect(topleft=self.rect.topleft)
                    r2 = objects.image.get_rect(topleft=objects.rect.topleft)
                elif self.angle == 45:
                    r1 = self.image.get_rect(bottomright=self.rect.bottomright)
                    r2 = objects.image.get_rect(bottomright=objects.rect.bottomright)
                else:
                    r1 = self.image.get_rect(topright=self.rect.topright)
                    r2 = objects.image.get_rect(topright=objects.rect.topright)
                off = (r2.left - r1.left, r2.top - r1.top)
                m = self.masks.get(self.currentattack)[int(self.anim_pos)]
                if m.overlap(pygame.mask.from_surface(objects.image), off) != None:
                    objects.health -= 50
                    objects.hit = True
                    self.sw.play()
            if self.rect.collidepoint(objects.rect.center) and self.damagetimer == 0\
                    and objects.state != gameobj.ATTACKING and objects.type == 'melee':
                self.tick += 2
                objects.set_state(gameobj.ATTACKING)
                self.invuln = True
                self.set_state(gameobj.DAMAGED)
                self.dmgmix.play()
                objects.attacked = True
                self.current_health -= 33
                flags.append('player_damage')
                self.rect.center = self.previous_position.center
                break
            if aware.collidepoint(self.rect.centerx, self.rect.centery) and objects.attack_timer == 0\
                    and objects.state != egameobj.ATTACKING and objects.type == 'projectile':
                objects.set_state(egameobj.ATTACKING)
                objects.attacked = True
                break

        if self.current_health/self.max_health <= 0.5:
            self.anim_images['IDLE'] = self.anim_images.get('HIT')

        if self.damagetimer == 500:
            self.damagetimer = 0
            self.tick = 0
            self.invuln = False
        self.damagetimer += self.tick
        return flags


    def lock_on(self, enemies):
        dx = 0
        dy = 0
        rangedenemies = pygame.sprite.Group()
        range = self.rect.inflate(600,600)
        for e in enemies:
            if range.colliderect(e.rect):
                rangedenemies.add(e)
        for ene in rangedenemies:
            if ene == GAME_GLOBALS.LOCKEDENEMY or ene.tagged == True:
                continue
            else:
                if GAME_GLOBALS.LOCKEDENEMY != None:
                    GAME_GLOBALS.LOCKEDENEMY.unlock()
                GAME_GLOBALS.LOCKEDENEMY = ene
                GAME_GLOBALS.LOCKEDENEMY.tagged = True
                GAME_GLOBALS.LOCKEDENEMY.locked()
                return

        for ene in rangedenemies:
            ene.tagged = False



