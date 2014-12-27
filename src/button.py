import pygame
import sys
from GAME_STATES import *
import GAME_GLOBALS
from pygame.locals import *

# Button class for swag points

class Button(object):
    def __init__(self, text='button', size='Font Size',
                 image=[GAME_GLOBALS.DEFAULT_BUTTON_IM, GAME_GLOBALS.DEFAULT_BUTTON_IM_DOWN], command=None,
                 location=[0, 0], font=GAME_GLOBALS.DEFAULT_FONT):

        self.text = text
        #This stuff doesnt have to be a member var
        #but is here currently just so that we can change text and other
        #stuff on the fly
        self.font = pygame.font.Font(font, GAME_GLOBALS.DEFAULT_FONT_SIZE)
        self.textsurf = self.font.render(self.text, 1, (255, 255, 255))
        if size == 'Font Size':
            btn_size = (self.font.size(text)[0] + 20, self.font.size(text)[1] + 20)
        else:
            btn_size = size
        self.upimage = pygame.transform.scale(pygame.image.load(image[0]).convert(), btn_size)
        self.downim = pygame.transform.scale(pygame.image.load(image[1]).convert(), btn_size)
        self.image = self.upimage
        self.location = location
        self.rect = self.image.get_rect(topleft=(location[0], location[1]))
        self.command = command
        self.draw()

    def clickevent(self, event):
        for e in event:
            if e.type == MOUSEBUTTONDOWN:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.image = self.downim

            if e.type == MOUSEBUTTONUP:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.command()
                self.image = self.upimage

    def draw(self):
        #Blit the text to the button. This has to be done in the loop because it gets overwritten
        #everytime the image of the button changes.
        self.image.blit(self.textsurf, (self.rect.width / 2 - self.textsurf.get_rect().width / 2,
                                        self.rect.height / 2 - self.textsurf.get_rect().height / 2))
        (pygame.display.get_surface()).blit(self.image, self.location)
