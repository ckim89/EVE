import pygame
import pygame.event as PGEVENT
import pygame.image as PI
import pygame.display as DISP
import pygame.font
from pygame.locals import *

import sys
import GAME_GLOBALS

from Game_State import *
# from Pause_State import *
from Main_Menus import *
from Start_Screen import *


class core():
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.display = DISP.set_mode(GAME_GLOBALS.WINDOW_SIZE)
        pygame.display.set_caption(GAME_GLOBALS.GAME_TITLE)
        self.fps_clock = pygame.time.Clock()
        self.GAME_STATE = None
        self.can_run = False
        self.exitting = False
        self.cycles_left = 0

    def initialize(self):
        self.can_run = True
        pygame.mixer.init()
        pygame.font.init()
        GAME_GLOBALS.GAME_STATE = Start_Screen()
        GAME_GLOBALS.GAME_MAIN_MENU = Main_Menu(False)
        self.GAME_STATE = GAME_GLOBALS.GAME_STATE  # This might change.


    #TODO: More Initialization stuff

    def run(self):
        while self.can_run:

            self.check_gamestate()
            #want delay for the ideal FPS
            lastframedelay = self.fps_clock.tick(GAME_GLOBALS.MAX_FPS)
            update_count = lastframedelay + self.cycles_left
            if update_count > (GAME_GLOBALS.MAX_FPS * GAME_GLOBALS.UPDATE_INT):
                update_count = GAME_GLOBALS.MAX_FPS * GAME_GLOBALS.UPDATE_INT

            #Do at least 1 update if for some reason
            #the computer is super fast
            event = pygame.event.get()
            self.check_exit(event)
            self.GAME_STATE.update(event)
            update_count -= GAME_GLOBALS.UPDATE_INT
            if update_count > GAME_GLOBALS.UPDATE_INT:
                while update_count > GAME_GLOBALS.UPDATE_INT:
                    update_count -= GAME_GLOBALS.UPDATE_INT
                    #Do update stuff
                    event = pygame.event.get()
                    self.check_exit(event)
                    self.GAME_STATE.update(event)
            self.cycles_left = update_count

            DISP.flip()

        if self.exitting:
            #TODO: save stuff?
            pygame.quit()
            sys.exit(0)
        else:
            #something kicked us out of the event loop but
            #the exitting flag is still false
            self.can_run = True

    #Checks if we are actually trying to exit
    def check_exit(self, event):
        for e in event:
            if e.type == QUIT:
                self.can_run = False
                self.exitting = True

    #Checks if the gamestate was changed by somebody
    #and sets the operating gamestate
    def check_gamestate(self):
        if self.GAME_STATE != GAME_GLOBALS.GAME_STATE:
            self.GAME_STATE = GAME_GLOBALS.GAME_STATE


if __name__ == '__main__':
    program = core()
    program.initialize()
    program.run()
