import pygame
import sys
import GAME_GLOBALS
from GAME_STATES import *


class High_Score(GAME_STATES):
    def __init__(self, scores, name):
        self.hi_title = GAME_GLOBALS.HIGH_SCORE_TITLE
        self.font = pygame.font.Font(GAME_GLOBALS.DEFAULT_FONT, 50)
        self.back = pygame.image.load(GAME_GLOBALS.HIGH_SCORE_BACK).convert()
        self.back = pygame.transform.scale(self.back, GAME_GLOBALS.WINDOW_SIZE)
        self.scoretext = str(scores).zfill(10)
        self.name = name
        self.back.blit(self.font.render(self.name, 1, (255,255,255)), (130, 240))
        self.back.blit(self.font.render(self.scoretext, 1, (255, 255, 255)), (GAME_GLOBALS.WINDOW_WIDTH-self.font.size(self.scoretext)[0],240))


    def update(self, event):

        (pygame.display.get_surface()).blit(self.back, (0, 0))
        self.check_esc()

    def check_esc(self):
        if pygame.key.get_pressed()[pygame.K_ESCAPE] == 1:
            GAME_GLOBALS.GAME_STATE = GAME_GLOBALS.GAME_MAIN_MENU
            GAME_GLOBALS.GAME_STATE.playmusic()
		
