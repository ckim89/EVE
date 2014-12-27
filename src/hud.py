from __future__ import division
import pygame
import sys
import GAME_GLOBALS

pygame.init()
pygame.font.init()


class Hud(object):
    def __init__(self):
        self.health_bar_length = 180
        self.font = pygame.font.Font(GAME_GLOBALS.DEFAULT_FONT, 12)
        self.status_bar = pygame.Surface((200, 50))
        self.status_bar.fill((255, 255, 255))
        self.heigh = 0
        self.width = 0
        self.mapframe = None
        self.levelmap = None
        self.levelchecker = None
        self.temp = None
        self.status_bar_BCKGD = pygame.image.load('../images/status_bar.png').convert()
        self.current_hp = None
        self.scorefont = pygame.font.Font(GAME_GLOBALS.DEFAULT_FONT, 36)
        fsize = self.scorefont.size("SCORE " + str(0).zfill(10))[0]
        self.score_bar = pygame.Surface((fsize + 14, self.status_bar.get_height()))
        self.score_back = pygame.transform.scale(self.status_bar_BCKGD, (fsize + 14, self.status_bar.get_height()))
        self.score = 0

    def update(self, hp, s, inv, col, row, level, lvlnum):
        self.heigh = 0
        self.width = 0
        dim = row/col
        if dim < 1:
            self.width = 200
            self.heigh = int(200 * (dim))
        else:
            self.heigh = 200
            self.width = int(200 * (dim))
        self.mapframe = pygame.Surface((self.width + 10, self.heigh + 10))
        if self.levelchecker != level:
            self.levelchecker = level
            self.levelmap = pygame.transform.scale(level, (self.width, self.heigh))
        self.mapframe.fill((255,255,255))
        trect = pygame.Rect(self.levelmap.get_rect().left, self.levelmap.get_rect().top, self.width - 10, self.heigh - 10)
        temp = self.levelmap.subsurface(trect)
        self.mapframe.blit(temp, (5, 5))
        self.score = s
        self.current_hp = str(hp[0]) + "/" + str(hp[1])
        self.status_bar.fill((255, 255, 255))
        self.status_bar.blit(self.status_bar_BCKGD, (0, 0))
        x = pygame.draw.rect(self.status_bar, (0, 0, 0), (8, 13, 184, 24))
        if inv:
            g = (220,220,0)
        else:
            g = (0,220,0)
        self.health_bar = pygame.draw.rect(self.status_bar, g,
                                           (10, 15, (hp[0] / hp[1]) * 180, 20))
        self.font_surf = self.font.render(self.current_hp, 1, (255, 255, 255))
        self.status_bar.blit(self.font_surf, (x.centerx - self.font.size(self.current_hp)[0] / 2,
                                              x.centery - self.font.size(self.current_hp)[1] / 2))
        self.score_bar.fill(GAME_GLOBALS.WHITE)
        self.score_bar.blit(self.score_back, (0, 0))
        self.score_bar.blit(self.scorefont.render("SCORE " +
                                                  str(self.score).zfill(10),
                                                  1, (0, 0, 0)),
                            (7, self.score_bar.get_height() / 2 - self.scorefont.size("SCORE " +
                                                                                      str(self.score).zfill(10))[
                                1] / 2))
        self.draw(lvlnum)

    def draw(self, lvlnum):
        if lvlnum != 4:
            (pygame.display.get_surface()).blit(self.mapframe, (0, GAME_GLOBALS.WINDOW_HEIGHT - self.heigh))
        (pygame.display.get_surface()).blit(self.status_bar, (0, 0))
        (pygame.display.get_surface()).blit(self.score_bar, (GAME_GLOBALS.WINDOW_WIDTH - self.score_bar.get_width(), 0))

