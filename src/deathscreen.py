__author__ = 'ecarlson'
import pygame
import GAME_GLOBALS
from vec2 import vec2
import random
import time
from button import Button
import Main_Menus

class Deathscreen:
    def __init__(self, score, currentlevel):
        self.backsurf = pygame.Surface((800, 600))
        self.backsurf.fill((0,0,0))
        self.font_obj = pygame.font.Font(GAME_GLOBALS.DEFAULT_FONT, 48)
        self.you = self.font_obj.render("You", 1, (255, 255, 255))
        self.died = self.font_obj.render("Died", 1, (255, 255, 255))
        self.youdied = self.font_obj.render("You Died", 1, (255, 255, 255))
        self.space = self.font_obj.render(" ", 1, (255, 255, 255))
        self.youpos = vec2(GAME_GLOBALS.WINDOW_WIDTH/2 - self.youdied.get_size()[0]/2 - 100, -1*self.you.get_size()[1])
        self.diedpos = vec2(GAME_GLOBALS.WINDOW_WIDTH/2 - self.youdied.get_size()[0]/2 - 100 + self.you.get_size()[0] + self.space.get_size()[0], -1*self.died.get_size()[1])
        self.deadim = pygame.image.load('../images/PLAYER_DEATH.png').convert_alpha()
        self.mainm = Button(text='Main Menu', location=[350, 500], command=self.main)
        self.retry = Button(text='Retry', location=[600, 500], command=self.retry)
        self.buttons= [self.mainm, self.retry]
        self.accel1 = 1
        self.accel2 = 2
        self.accel = 1
        self.vel = 0
        self.stopy = 100
        self.go = False
        self.shake = False
        self.level = currentlevel
        self.shaketimer = 0
        self.final = False
        self.stopshaking = 3
        self.timer = time.time()

    def main(self):
        GAME_GLOBALS.GAME_STATE = Main_Menus.Main_Menu(pygame.display.get_surface())

    def retry(self):
        GAME_GLOBALS.GAME_STATE = GAME_GLOBALS.currentgame.restart()

    def update(self, events):
        if time.time() - self.timer >= self.stopshaking:
            self.shake = False
        if self.shake:
            if time.time() - self.shaketimer >= 0.5:
                self.shake = False
            s = vec2(random.randint(3,10), random.randint(4,10))
            (pygame.display.get_surface()).blit(self.backsurf, (GAME_GLOBALS.WINDOW_WIDTH/2 - self.backsurf.get_size()[0]/2 + s.x, GAME_GLOBALS.WINDOW_HEIGHT/2 - self.backsurf.get_size()[1]/2 + s.y))
        else:
            (pygame.display.get_surface()).blit(self.backsurf, (GAME_GLOBALS.WINDOW_WIDTH/2 - self.backsurf.get_size()[0]/2, GAME_GLOBALS.WINDOW_HEIGHT/2 - self.backsurf.get_size()[1]/2))
        self.backsurf.fill((0, 0, 0))
        for btn in self.buttons:
            btn.draw()
        self.vel += self.accel
        self.youpos.y += self.vel
        if self.youpos.y >= self.stopy and not self.go:
            self.youpos.y = self.stopy
            self.go = True
            self.vel = 0
            self.shaketimer = time.time()
            self.shake = True

        if self.youpos.y >= self.stopy:
            self.youpos.y = self.stopy
        if self.diedpos.y >= self.stopy:
            self.diedpos.y = self.stopy

        if self.go:
            self.vel += self.accel
            self.diedpos.y += self.vel
            if self.diedpos.y >= self.stopy:
                self.diedpos.y = self.stopy
                self.shake = True
                self.shaketimer = time.time()

        self.backsurf.blit(self.you, (self.youpos.x, self.youpos.y))
        self.backsurf.blit(self.died, (self.diedpos.x, self.diedpos.y))
        self.backsurf.blit(self.deadim, (self.backsurf.get_width()/2 - self.deadim.get_size()[0]/2, self.backsurf.get_height()/2 - self.deadim.get_size()[1]/2))
        mouse_events = [x for x in events if x.type == pygame.MOUSEBUTTONDOWN or x.type == pygame.MOUSEBUTTONUP]
        for b in self.buttons:
            b.clickevent(mouse_events)