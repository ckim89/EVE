import pygame
import sys
import GAME_GLOBALS
from GAME_STATES import *


class win(GAME_STATES):
    def __init__(self):
        self.text = GAME_GLOBALS.WINNING
        self.font = pygame.font.Font(GAME_GLOBALS.DEFAULT_FONT, 50)
        self.back = pygame.image.load(GAME_GLOBALS.WIN).convert()
        self.back = pygame.transform.scale(self.back, GAME_GLOBALS.WINDOW_SIZE)
        self.back.blit(self.font.render(self.text, 1, (255, 255, 255)), (10,240))



    def update(self, event):

        (pygame.display.get_surface()).blit(self.back, (0, 0))
        self.check_esc()

    def check_esc(self):
        if pygame.key.get_pressed()[pygame.K_ESCAPE] == 1:
            GAME_GLOBALS.GAME_STATE = GAME_GLOBALS.GAME_MAIN_MENU
            GAME_GLOBALS.GAME_STATE.playmusic()