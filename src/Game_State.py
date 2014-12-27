import pygame
import sys
import random
from Enemy import *
from Player import *
from GAME_STATES import *
from Wall import *
import GAME_GLOBALS
import level3
import level0
import level1
import level2
import level4
from Camera import *
import Door
import High_Score
import win
import hud
import dialog
import time
import cutscene
import Ball
import time
from deathscreen import Deathscreen

class Game_State(GAME_STATES):
    def __init__(self, levelname = '../images/ASCIILEVEL0.txt', level = level0.init, prev = None, health = 100,name=0, score = 0, final = False, text='BEGIN TEST'):
        GAME_STATES.__init__(self)

        GAME_GLOBALS.currentgame = self

        self.introte = text
        self.inname = name

        decor, floor, walls, doors, nulls, ene, row, col, finish,player_location, pene, cene, grid = level(levelname)
        self.hashgrid = grid
        self.gridsize = 500
        self.search_padding = 15
        self.font_obj = pygame.font.Font(GAME_GLOBALS.DEFAULT_FONT, 28)
        self.text = self.font_obj.render("- Level " + str(name) + " - " + text, 1, (255, 255, 255))
        self.intro_text = pygame.Surface(self.text.get_size())
        self.intro_text.fill(GAME_GLOBALS.BLACK)
        self.intro_text.set_alpha(255)
        self.intro_text.blit(self.text, (0, 0))
        self.timer = time.time()
        self.row = row
        self.col = col
        self.fade = pygame.Surface(GAME_GLOBALS.WINDOW_SIZE)
        self.shade = pygame.image.load('../images/shade.png').convert()
        self.fade.fill(GAME_GLOBALS.BLACK)
        self.fade.set_alpha(255)
        self.fade_rate = 1
        newmap = pygame.Surface((50 * (col + 5), 50 * (row + 5)))
        self.currhealth = health
        self.shaketimer = 0
        self.shakecooldown = 1000
        self.leveltimer = 2000
        self.Player = Player(GAME_GLOBALS.DEFAULT_PLAYER, (100, 100), player_location)
        self.music = GAME_GLOBALS.LVL_1_TRACK
        self.levelhandle = level
        if prev != None:
            del prev
        self.currlevel = 0
        if level == level1.init:
            self.music = GAME_GLOBALS.LVL_2_TRACK
            self.currlevel = 1
            self.Player.current_health = self.currhealth
        if level == level2.init:
            self.music = GAME_GLOBALS.LVL_3_TRACK
            self.currlevel = 2
            self.Player.current_health = self.currhealth
        if level == level3.init:
            self.music = GAME_GLOBALS.LVL_4_TRACK
            self.currlevel = 3
            self.Player.current_health = self.currhealth
        if level == level4.init:
            self.music = GAME_GLOBALS.LVL_5_TRACK
            self.currlevel = 4
            self.Player.current_health = self.currhealth
        self.music.play(-1)
        self.points = GAME_GLOBALS.POINTS
        self.Doorgroup = pygame.sprite.Group()
        self.Enemygroup = pygame.sprite.Group()
        self.Wallgroup = pygame.sprite.Group()
        self.Projectiles = pygame.sprite.Group()
        for i in walls:
            self.Wallgroup.add(Wall((i.position[1] * 50 + 25, i.position[0] * 50 + 25)))
            newmap.blit(i.im, ((i.position[1]) * 50, i.position[0] * 50))
        for f in floor:
            newmap.blit(f.im, (f.position[1] * 50, f.position[0] * 50))
        for d in doors:
            newmap.blit(d.im, (d.position[1] * 50, d.position[0] * 50))
            self.Doorgroup.add(Door.Door((d.position[1] * 50 + 25, d.position[0] * 50 + 25)))
        for n in nulls:
            newmap.blit(n.im, (n.position[1] * 50, n.position[0] * 50))
        for d in decor:
            newmap.blit(d.im, (d.position[1] * 50, d.position[0] * 50))
            bins = self.getbinpos(d, skip=True)
            for b in bins:
                self.hashgrid[b].append(d)

        for e in ene:
            self.Enemygroup.add(Enemy(GAME_GLOBALS.MELEE_ENEMY, (100, 100),
                                      (e[1] * 50, e[0] * 50)))
        for e in pene:
            self.Enemygroup.add(Enemy(GAME_GLOBALS.PROJECT_ENEMY, (100, 100),
                                      (e[1] * 50, e[0] * 50)))
        for e in cene:
            self.Enemygroup.add(Enemy(GAME_GLOBALS.CAPTAIN_ENEMY, (100, 100),
                                      (e[1] * 50, e[0] * 50)))
        self.font = pygame.font.Font(GAME_GLOBALS.DEFAULT_FONT, GAME_GLOBALS.DEFAULT_FONT_SIZE)
        self.search_padding = 15
        self.playerbin = 0
        self.hashgrid = grid


        self.levelname = levelname
        self.finish = [(x[1] * 50, x[0] * 50) for x in finish]
        self.newmap = newmap
        GAME_GLOBALS.CURRENT_LEVEL = self.newmap
        self.camera = Camera()
        self.bump = GAME_GLOBALS.BUMP
        self.HUD = hud.Hud()
        self.current_score = score
        self.current_score_rate = 100
        self.time_flag = time.time()
        self.approach = GAME_GLOBALS.APPROACH
        self.splatter = False
        self.currentsplatter = None
        self.dirtydraws = pygame.sprite.LayeredDirty
        self.modal = False
        self.final = False
        self.ds = None
        self.extras = []

    def restart(self):
        return Game_State(self.levelname, self.levelhandle, text=self.introte, name=self.inname,final=self.final)

    def getbinpos(self, spriteobj, skip=False):
        obj = spriteobj.rect
        top = obj.top - self.search_padding
        left = obj.left - self.search_padding
        right = obj.right + self.search_padding
        bottom = obj.bottom + self.search_padding
        pos = [(left, top), (right, top), (left, bottom), (right, bottom)]
        for i in range(0, 4):
            pos[i] = (math.floor(pos[i][0]/self.gridsize)*self.gridsize, math.floor(pos[i][1]/self.gridsize)*self.gridsize)
        newbins = list(set(pos))
        if not skip:
            spriteobj.current_bin_pos = newbins
        else:
            return newbins

    def get_binobjs(self, obj):
        positions = obj.current_bin_pos
        hashset = []
        for p in positions:
            h = self.hashgrid.get(p)
            if h != None:
                hashset += h
        return hashset

    def check_active_dialog(self):
        pass

    def update_score(self, dt):
        if dt >= 5:
                if self.current_score_rate > 0:
                    self.current_score_rate -= 5
                self.current_score += self.current_score_rate
                self.time_flag += dt

    def nextl(self):
        if self.levelname == '../images/ASCIILEVEL1.txt':
            self.music.stop()
            GAME_GLOBALS.GAME_STATE = Game_State(levelname='../images/bigelevatorthing.txt', level = level2.init, prev = self, health = self.Player.current_health, name=2, score = self.current_score, final= True, text = "Kill the enemies")
        elif self.levelname == '../images/ASCIILEVEL0.txt':
            self.music.stop()
            GAME_GLOBALS.GAME_STATE = Game_State(levelname='../images/ASCIILEVEL1.txt', level = level1.init, prev = self, health = self.Player.current_health, name=1, score = self.current_score, final= False, text = "Survive")
        elif self.levelname == '../images/bigelevatorthing.txt':
            self.music.stop()
            GAME_GLOBALS.GAME_STATE = Game_State(levelname='../images/ASCIILEVEL3.txt', level = level3.init, prev = self, health = self.Player.current_health, name=3, score = self.current_score, final= False, text = "Escape")
        elif self.levelname == '../images/ASCIILEVEL3.txt':
            self.music.stop()
            GAME_GLOBALS.GAME_STATE = Game_State(levelname='../images/ASCIILEVEL4.txt', level = level4.init, prev = self, health = self.Player.current_health, name=4, score = self.current_score, final= False, text = "Freedom")

    def update(self, event):

        self.getbinpos(self.Player)
        worldob = self.get_binobjs(self.Player)

        dt = float(time.time() - self.timer)
        if dt >= 1:
            pass
        if dt >=  3:
            self.intro_text.set_alpha(self.intro_text.get_alpha() - (self.fade_rate + 2))
        if self.intro_text.get_alpha() <= 0:
            pass
        if self.fade.get_alpha() - self.fade_rate <= 0:
             self.fade.set_alpha(0)
        else:
            curr_a = self.fade.get_alpha()
            curr_a -= self.fade_rate
            self.fade.set_alpha(curr_a)
            x = self.fade.get_alpha()
        self.check_esc()
        self.DRAW_DISP.fill(GAME_GLOBALS.BLACK)
        self.check_active_dialog()
        self.update_score(time.time() - self.time_flag)

        if self.currlevel == 2:
            self.leveltimer -= 2
        if self.leveltimer == 0:
            GAME_GLOBALS.GAME_STATE = cutscene.Cutscene('../images/darkmaze.jpg','../resource/EVEmaze', self.nextl)

        for f in self.finish:
            if self.currlevel == 4:
                self.final = True
                self.music.stop()
            if self.Player.rect.collidepoint(f):
                if self.final:
                    GAME_GLOBALS.GAME_STATE = win.win()
                elif self.currlevel == 0:
                    GAME_GLOBALS.GAME_STATE = cutscene.Cutscene('../images/Eve awake.png','../resource/EVEawkeningcinematic', self.nextl)
                elif self.currlevel == 1:
                    GAME_GLOBALS.GAME_STATE = cutscene.Cutscene('../images/darkalley.jpg','../resource/EVEknows', self.nextl)
                elif self.currlevel == 3:
                    GAME_GLOBALS.GAME_STATE = cutscene.Cutscene('../images/flare.png','../resource/EVEplots', self.nextl)

        for e in self.Enemygroup:
            self.getbinpos(e)
            proj = e.update(self.Player.rect, self.get_binobjs(e))
            if proj != None:
                self.Projectiles.add(proj)
        for p in self.Projectiles:
            test = p.update(self.Wallgroup, self.Player.rect, self.Player)
            if test == True and p.hitplayer == True:
                bloodsplatter = pygame.sprite.Group()
                self.splatter = True
                for j in range(20):
                    bloodsplatter.add(Ball.Ball((0,0,0),100,self.Player.rect.center))
                self.currentsplatter = bloodsplatter
                self.Projectiles.remove(p)
                p = None
            elif test == True:
                self.Projectiles.remove(p)

        flags = self.Player.update(event, worldob, self.Enemygroup, self.current_score, self.Projectiles)
        if flags == 'died':
            GAME_GLOBALS.GAME_STATE = deathscreen.Deathscreen(self.current_score, self.levelname)
        if 'player_dmg' in flags:
            bloodsplatter = pygame.sprite.Group()
            self.splatter = True
            for j in range(20):
                bloodsplatter.add(Ball.Ball((0,1,0),100,self.Player.rect.center))
            self.currentsplatter = bloodsplatter

        for d in self.Doorgroup:
            dpos = d.teleport_hax(self.Player.rect)
            self.Player.rect.centerx += dpos[0]

        self.camera.update(self.Player.rect.center)
        for i in self.Enemygroup:
            if i.health <= 0:

                bloodsplatter = pygame.sprite.Group()
                self.splatter = True
                for j in range(20):
                    bloodsplatter.add(Ball.Ball((0,0,0),100,i.rect.center))
                self.currentsplatter = bloodsplatter
                self.current_score += 500
                scoretext = pygame.Surface((100,100))
                scoretext.fill(GAME_GLOBALS.BLACK)
                scoretext.set_colorkey(GAME_GLOBALS.BLACK)
                scoretext.blit(self.font_obj.render("+500", 1,
                                             (random.randint(1,255),
                                              random.randint(1,255),
                                              random.randint(1,255))), (0,0))
                scoretext.set_alpha(255)
                newball = Ball.Ball((0, 0, 0), 2, i.rect.topleft, im=scoretext)

                self.extras.append(newball)

                self.points.play()
                self.Enemygroup.remove(i)


        self.DRAW_DISP.blit(self.camera.current_frame, (0, 0))
        for e in self.Enemygroup:
            p = (e.rect.left - self.camera.r.left, e.rect.top - self.camera.r.top)
            self.DRAW_DISP.blit(e.image, p)
        for p in self.Projectiles:
            f = (p.rect.left - self.camera.r.left, p.rect.top - self.camera.r.top)
            self.DRAW_DISP.blit(p.image, f)
        if self.splatter:
            if len(self.currentsplatter) != 0:
                for b in self.currentsplatter:
                    if b.update() == 1:
                        self.currentsplatter.remove(b)
                    else:
                        c = (b.rect.left - self.camera.r.left, b.rect.top - self.camera.r.top)
                        self.DRAW_DISP.blit(b.image,c)
            else:
                self.splatter = False
        self.HUD.update((self.Player.current_health, self.Player.max_health), self.current_score, self.Player.invuln, self.col, self.row, self.newmap, self.currlevel)
        if self.Player.state == gameobj.ATTACKING:
            if self.Player.angle in [0, -45, -90]:
                self.DRAW_DISP.blit(self.Player.image, (462, 434 - self.Player.image.get_size()[1]))
            elif self.Player.angle in [180, -135]:
                self.DRAW_DISP.blit(self.Player.image, (462, 334))
            elif self.Player.angle == 45:
                self.DRAW_DISP.blit(self.Player.image, (562- self.Player.image.get_size()[0], 434- self.Player.image.get_size()[1]))
            else:
                self.DRAW_DISP.blit(self.Player.image, (562 - self.Player.image.get_size()[0], 334))
        else:
            self.DRAW_DISP.blit(self.Player.image, (462, 334))

        if self.currlevel == 2 or self.currlevel == 4:
            if self.shaketimer == 500:
                self.shakecooldown = 0
            if self.shaketimer != 500 and self.shakecooldown == 1000:
                x = self.shake()
                temp = pygame.Surface(GAME_GLOBALS.WINDOW_SIZE)
                temp.blit(self.DRAW_DISP, (0,0))
                self.DRAW_DISP.blit(temp, x)
                self.shaketimer += 2
            else:
                self.shakecooldown += 5
                self.shaketimer = 0

        for e in self.extras:

            if e.update() == 1:
                self.extras.remove(e)
            else:
                c = (e.rect.left - self.camera.r.left, e.rect.top - self.camera.r.top)
                self.DRAW_DISP.blit(e.image, c)



        self.DRAW_DISP.blit(self.fade, (0, 0))
        self.DRAW_DISP.blit(self.intro_text, (GAME_GLOBALS.WINDOW_WIDTH/2 - self.intro_text.get_size()[0]/2,
                                              GAME_GLOBALS.WINDOW_HEIGHT/3))

        if GAME_GLOBALS.BALANCE >= 0:
            GAME_GLOBALS.LOFFSET.set_alpha(abs(GAME_GLOBALS.BALANCE) * 20)
            self.DRAW_DISP.blit(GAME_GLOBALS.LOFFSET, (0,0), None, 0)
        else:
            GAME_GLOBALS.DOFFSET.set_alpha(abs(GAME_GLOBALS.BALANCE) * 20)
            self.DRAW_DISP.blit(GAME_GLOBALS.DOFFSET, (0,0), None, 0)

        if self.levelname == '../images/ASCIILEVEL3.txt':
            self.DRAW_DISP.blit(self.shade, (0, 0), special_flags=pygame.BLEND_MULT)
            self.HUD.update((self.Player.current_health, self.Player.max_health), self.current_score, self.Player.invuln, self.col, self.row, self.newmap, self.currlevel)

        if self.ds != None:
            self.ds.update()
            self.DRAW_DISP.blit(self.ds.backsurf, (GAME_GLOBALS.WINDOW_WIDTH/2 - self.ds.backsurf.get_size()[0]/2, GAME_GLOBALS.WINDOW_HEIGHT/2 - self.ds.backsurf.get_size()[1]/2))
        self.check_esc()


    def check_esc(self):
        if pygame.key.get_pressed()[pygame.K_ESCAPE] == 1:
            self.music.stop()
            GAME_GLOBALS.GAME_STATE = GAME_GLOBALS.GAME_MAIN_MENU
            GAME_GLOBALS.GAME_STATE.playmusic()

    def shake(self):
        dx = 0
        dy = 0
        temp = [0, 3, -3]
        randx = temp[random.randint(0, 2)]
        randy = temp[random.randint(0, 2)]
        return (randx, randy)

