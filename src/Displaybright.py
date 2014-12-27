import pygame, sys
from button import *
import GAME_GLOBALS
from GAME_STATES import *


class Displaybright(GAME_STATES):
    def __init__(self):
        self.DRAW_DISP = pygame.display.get_surface()
        self.title = GAME_GLOBALS.DISPLAY_TITLE
        self.up = Button(command=self.brighten, location=[40, 250], text="BRIGHTER")
        self.down = Button(command=self.dim, location=[40, 300], text="DIMMER")
        self.exitb = Button(command=self.exit, location=[40, 350], text="EXIT")
        self.buttons = [self.up, self.down, self.exitb]
        self.DRAW_DISP.fill((100,100,100))
        if GAME_GLOBALS.BALANCE >= 0:
            GAME_GLOBALS.LOFFSET.set_alpha(abs(GAME_GLOBALS.BALANCE) * 20)
            self.DRAW_DISP.blit(GAME_GLOBALS.LOFFSET, (0,0), None, 0)
        else:
            GAME_GLOBALS.DOFFSET.set_alpha(abs(GAME_GLOBALS.BALANCE) * 20)
            self.DRAW_DISP.blit(GAME_GLOBALS.DOFFSET, (0,0), None, 0)

    def update(self, event):
        for btn in self.buttons:
            btn.draw()
        # Really need a better way of doing this
        mouse_events = [x for x in event if x.type == MOUSEBUTTONDOWN or x.type == MOUSEBUTTONUP]
        for b in self.buttons:
            b.clickevent(mouse_events)

    def brighten(self):
        GAME_GLOBALS.BALANCE += 1
        GAME_GLOBALS.LOFFSET.set_alpha(GAME_GLOBALS.LALPHA * abs(GAME_GLOBALS.BALANCE))
        self.DRAW_DISP.blit(GAME_GLOBALS.LOFFSET, (0,0), None, 0)

    def dim(self):
        GAME_GLOBALS.BALANCE -= 1
        GAME_GLOBALS.DOFFSET.set_alpha(GAME_GLOBALS.DALPHA * abs(GAME_GLOBALS.BALANCE))
        self.DRAW_DISP.blit(GAME_GLOBALS.DOFFSET, (0,0), None, 0)

    def exit(self):
        GAME_GLOBALS.GAME_STATE = GAME_GLOBALS.GAME_MAIN_MENU
