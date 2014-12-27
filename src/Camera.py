import pygame
import GAME_GLOBALS


class Camera():
    def __init__(self):
        self.current_frame = None
        self.r = None

    def update(self, playerect):
        r_left =playerect[0] - GAME_GLOBALS.WINDOW_WIDTH/2
        r_top = playerect[1] - GAME_GLOBALS.WINDOW_HEIGHT/2
        r_bottom = playerect[1] + GAME_GLOBALS.WINDOW_HEIGHT/2
        if r_left < 0:
            r_left = 0
        if r_top < 0:
            r_top = 0

        r = pygame.Rect((r_left,r_top),GAME_GLOBALS.WINDOW_SIZE)
        self.r = r

        self.current_frame = GAME_GLOBALS.CURRENT_LEVEL.subsurface(r)

