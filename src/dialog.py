import pygame
import sys
import GAME_GLOBALS
import numpy
import time


GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)


class Dialog(object):
    def __init__(self, text, speed=45, text_font=GAME_GLOBALS.DEFAULT_FONT, font_size=14,
                 size=(GAME_GLOBALS.WINDOW_WIDTH, 200), position=(0, GAME_GLOBALS.WINDOW_HEIGHT - 200)):
        self.speed = speed
        self.fast = self.speed + 30
        self.norm = self.speed
        self.position = position
        self.exitting = False
        self.font_obj = pygame.font.Font(GAME_GLOBALS.DEFAULT_FONT, font_size)
        self.diagbox_im = pygame.image.load(GAME_GLOBALS.DEFAULT_DIAG).convert()
        self.diagbox_im = pygame.transform.scale(self.diagbox_im, size)
        self.maxcharcount = size[0] / (
            (self.font_obj.size("A")[0] + self.font_obj.size("b")[0] + self.font_obj.size("c")[0]) / 3.0)
        self.text_start_pos = (20, 20)
        helpsize = self.font_obj.size("Press Space to Continue...")
        self.next_hint = pygame.Surface((helpsize[0] + 40, helpsize[1] + 40))
        self.next_hint.fill((0,0,0))
        self.next_hint.blit(self.font_obj.render("Press Space to Continue...", 1, (255, 255, 255)), (20, 20))
        self.next_hint_location = pygame.Rect((0, 0), self.next_hint.get_size())
        self.next_hint_location.center = (GAME_GLOBALS.WINDOW_WIDTH/2, GAME_GLOBALS.WINDOW_HEIGHT/4)
        self.line_height = self.font_obj.size("Q")[1]
        self.pending_next = False
        self.current_line = 0
        self.current_char = 0
        self.line_in_progress = ""
        self.timer = time.time()
        self.text_surf = pygame.Surface(
            (self.diagbox_im.get_rect().width - 2 * self.text_start_pos[0],
             self.diagbox_im.get_rect().height - 2 * self.text_start_pos[1]))
        self.done = False
        self.lines = self.get_fontobject_from_text(text)
        self.flashon = False
        self.flash_delay = 1
        self.flash_timer = 0

    def get_fontobject_from_text(self, text):
        txt = text.split('\n')
        result = []
        for line in range(0, len(txt)):
            current = " "
            for char in range(0, len(txt[line])):
                if char + 1 < self.maxcharcount:
                    current += txt[line][char]
                else:
                    txt.insert(line + 1, txt[line][char:])
                    break
            result.append(current)
        return result

    def flash_next(self, dt):
        if dt >= self.flash_delay:
            if self.flashon:
                self.flashon = False
            else:
                self.flashon = True
            self.timer += dt

    def update(self, event):
        keys = pygame.key.get_pressed()
        self.check_space(event)
        dt = time.time() - self.timer
        if not (self.pending_next or self.done):
            self.flashon = False
            if dt >= 1.0 / self.speed:
                self.timer += dt
                if self.current_char >= len(self.lines[self.current_line]):
                    self.current_char = 0
                    self.line_in_progress = ""
                    if self.current_line + 1 >= len(self.lines):
                        self.done = True
                    elif self.line_height * self.current_line + self.line_height >= self.text_surf.get_rect().height:
                        self.pending_next = True
                    else:
                        self.current_line += 1
                self.line_in_progress += self.lines[self.current_line][self.current_char]
                f = self.font_obj.render(self.line_in_progress, 1, (255, 255, 255))
                self.text_surf.blit(f, (0, self.line_height * self.current_line))
                self.diagbox_im.blit(self.text_surf, self.text_start_pos)
                self.current_char += 1
        else:
            self.flash_next(dt)


    def check_space(self, event):
        for e in event:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    self.speed = self.fast
                    if self.pending_next:
                        self.pending_next = False
                        self.lines = self.lines[self.current_line + 1:]
                        self.text_surf.fill((0, 0, 0))
                        self.current_line = 0
                        self.current_char = 0
                        self.line_in_progress = ""
                    if self.done:
                        self.exitting = True
                if e.key == pygame.K_ESCAPE:
                    self.exitting = True
            else:
                self.speed = self.norm

    def draw(self):
        if self.flashon:
            pygame.display.get_surface().blit(self.next_hint, self.next_hint_location.topleft)
        pygame.display.get_surface().blit(self.diagbox_im, self.position)


if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    d = pygame.display.set_mode((800, 600))
    diag = Dialog('../resource/cutscene1_text.txt', 45)
    while True:
        diag.update(pygame.event.get())
        pygame.display.flip()
