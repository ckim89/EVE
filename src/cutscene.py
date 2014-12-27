import pygame
import GAME_STATES
import GAME_GLOBALS
import time
import Game_State
import dialog

class Cutscene(GAME_STATES.GAME_STATES):
    def __init__(self, im, text, exitc, fade=True):
        self.diag = dialog.Dialog(open(text, 'r').read(), GAME_GLOBALS.DIAGBOX_TEXTSPEED)
        self.im = pygame.transform.scale(pygame.image.load(im).convert(), GAME_GLOBALS.WINDOW_SIZE)
        self.display = pygame.display.get_surface()
        self.black_surf = pygame.Surface(GAME_GLOBALS.WINDOW_SIZE)
        self.black_surf.fill(GAME_GLOBALS.BLACK)
        self.black_surf.set_alpha(240)
        self.alpha_add = -10
        self.exitting = False
        self.exit_command = exitc
        self.timer = time.time()
        self.delay = .02

    def update(self, event):
        if self.diag.exitting:
            self.exitting = True
        else:
            self.diag.update(event)
        if not self.exitting:
            self.fade_alpha(0)
        else:
            self.fade_alpha(255, mod=-1)
            if self.black_surf.get_alpha() == 255:
                self.exit_command()

        self.draw()

    def fade_alpha(self, bound, mod=1):
        dt = float(time.time() - self.timer)
        if dt >= self.delay:
            newalpha = self.alpha_add*mod + self.black_surf.get_alpha()
            if newalpha <= 0 or newalpha >= 255:
                newalpha = bound
            self.black_surf.set_alpha(newalpha)
            self.timer+=dt

    def draw(self):
        self.display.blit(self.im, (0, 0))
        self.display.blit(self.black_surf, (0, 0))
        self.diag.draw()
        if GAME_GLOBALS.BALANCE >= 0:
            GAME_GLOBALS.LOFFSET.set_alpha(abs(GAME_GLOBALS.BALANCE) * 20)
            self.display.blit(GAME_GLOBALS.LOFFSET, (0,0), None, 0)
        else:
            GAME_GLOBALS.DOFFSET.set_alpha(abs(GAME_GLOBALS.BALANCE) * 20)
            self.display.blit(GAME_GLOBALS.DOFFSET, (0,0), None, 0)

