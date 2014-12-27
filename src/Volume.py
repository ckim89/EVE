import pygame, sys
from button import *
import GAME_GLOBALS
from GAME_STATES import *



class Volume(GAME_STATES):
    def __init__(self):
        self.DRAW_DISP = pygame.display.get_surface()
        self.title = GAME_GLOBALS.DISPLAY_TITLE
        self.up = Button(command=self.loud, location=[40, 250], text="LOUDER")
        self.down = Button(command=self.soft, location=[40, 300], text="SOFTER")
        self.exitb = Button(command=self.exit, location=[40, 350], text="EXIT")
        self.buttons = [self.up, self.down, self.exitb]
        self.DRAW_DISP.fill((15,15,15))
        self.timer = 0
        if GAME_GLOBALS.BALANCE >= 0:
            GAME_GLOBALS.LOFFSET.set_alpha(abs(GAME_GLOBALS.BALANCE) * 20)
            self.DRAW_DISP.blit(GAME_GLOBALS.LOFFSET, (0,0), None, 0)
        else:
            GAME_GLOBALS.DOFFSET.set_alpha(abs(GAME_GLOBALS.BALANCE) * 20)
            self.DRAW_DISP.blit(GAME_GLOBALS.DOFFSET, (0,0), None, 0)

    def update(self, event):
        if self.timer == 150:
            GAME_GLOBALS.POINTS.play(0)
            self.timer += 10
        else:
            self.timer += 10
        if self.timer > 300:
            self.timer -= 10
        for btn in self.buttons:
            btn.draw()
        # Really need a better way of doing this
        mouse_events = [x for x in event if x.type == MOUSEBUTTONDOWN or x.type == MOUSEBUTTONUP]
        for b in self.buttons:
            b.clickevent(mouse_events)

    def loud(self):
        if GAME_GLOBALS.VOLUME > 1:
            return
        else:
            GAME_GLOBALS.VOLUME += .1
        for sounds in GAME_GLOBALS.ALL_SOUNDS:
            sounds.set_volume(GAME_GLOBALS.VOLUME)
        GAME_GLOBALS.POINTS.play(0)

    def soft(self):
        if GAME_GLOBALS.VOLUME < 0:
            return
        else:
            GAME_GLOBALS.VOLUME -= .1
        for sounds in GAME_GLOBALS.ALL_SOUNDS:
            sounds.set_volume(GAME_GLOBALS.VOLUME)
        GAME_GLOBALS.POINTS.play(0)

    def exit(self):
        GAME_GLOBALS.GAME_STATE = GAME_GLOBALS.GAME_MAIN_MENU