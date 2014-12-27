import pygame
import sys
from GAME_STATES import *
import GAME_GLOBALS
import Main_Menus

class Start_Screen(GAME_STATES):
    def __init__(self):
        GAME_STATES.__init__(self)
        self.produced_by = "A Game Brought to you by:"
        self.production_team = GAME_GLOBALS.PRODUCTION_TEAM
        self.font = pygame.font.Font(GAME_GLOBALS.DEFAULT_FONT, 50)
        self.back = pygame.image.load(GAME_GLOBALS.START_SCREEN_BACKGROUND).convert()
        self.x = -50
        self.y = 150

    def update(self,event):
        temp = pygame.transform.scale(self.back, GAME_GLOBALS.WINDOW_SIZE)
        self.DRAW_DISP.blit(temp,(0,0))
        self.DRAW_DISP.blit(self.font.render(self.produced_by,1,(0,0,0)),(220,30))
        self.DRAW_DISP.blit(self.font.render(self.production_team,1,(0,0,0)),(self.x,self.y))
        if self.x != 360:
            self.x += 5
        if pygame.key.get_pressed()[pygame.K_SPACE] == 1:
            GAME_GLOBALS.GAME_STATE = Main_Menus.Main_Menu(True)
        if pygame.key.get_pressed()[pygame.K_ESCAPE] == 1:
            pygame.quit()
            sys.exit(0)

