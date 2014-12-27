import pygame
import sys
import core
from Displaybright import *
from High_Score import *
from GAME_STATES import *
import GAME_GLOBALS
from button import *
import Game_State
import cutscene
from Volume import *
import level3
import level0
import level1
import level2
import level4

# TODO: This is really messy. Need to restructure to
#fit the new GAME_STATES structure



class Main_Menu(GAME_STATES):
    def __init__(self, disp):
        GAME_STATES.__init__(self)
        self.new = Button(command=self.newgame , location=[40, 150], text="New Game")
        self.video = Button(command=self.videomenu, location=[40, 200], text="Video Settings")
        self.audio = Button(command=self.audiomenu, location=[40, 250], text="Audio Settings")
        self.highscore = Button(command=self.highscoremenu, location=[40, 300], text="High Scores")
        self.exitb = Button(command=self.exit, location=[40, 350], text="Exit")
        self.buttons = [self.video, self.audio, self.highscore, self.new, self.exitb]
        self.background = pygame.transform.scale(pygame.image.load(GAME_GLOBALS.MAIN_MENU_BACKGROUND).convert(), GAME_GLOBALS.WINDOW_SIZE)
        if disp:
            GAME_GLOBALS.MAIN_MENU_TRACK.play(-1)

    def exit(self):
        pygame.quit()
        sys.exit(0)

    def startcutscene(self):
        #TODO: Cleaner more efficient Game_State calls
        GAME_GLOBALS.MAIN_MENU_TRACK.stop()
        GAME_GLOBALS.GAME_STATE = cutscene.Cutscene('../images/cutscene1.jpg', '../resource/cutscene1_text.txt', self.startlvl1)

    def startcutscene2(self):
        #TODO: Cleaner more efficient Game_State calls
        GAME_GLOBALS.MAIN_MENU_TRACK.stop()
        GAME_GLOBALS.GAME_STATE = cutscene.Cutscene('../images/Eve awake.png','../resource/EVEawkeningcinematic', self.startlvl2)


    def startcutscene3(self):
        #TODO: Cleaner more efficient Game_State calls
        GAME_GLOBALS.MAIN_MENU_TRACK.stop()
        GAME_GLOBALS.GAME_STATE = cutscene.Cutscene('../images/darkalley.jpg','../resource/EVEknows', self.startlvl3)

    def startcutscene4(self):
        #TODO: Cleaner more efficient Game_State calls
        GAME_GLOBALS.MAIN_MENU_TRACK.stop()
        GAME_GLOBALS.GAME_STATE = cutscene.Cutscene('../images/darkmaze.jpg','../resource/EVEmaze', self.startlvl4)

    def startcutscene5(self):
        #TODO: Cleaner more efficient Game_State calls
        GAME_GLOBALS.MAIN_MENU_TRACK.stop()
        GAME_GLOBALS.GAME_STATE = cutscene.Cutscene('../images/flare.png','../resource/EVEplots', self.startlvl5)

    def newgame(self):
        lvl1 = Button(command=self.startcutscene, location=[250, 250], text="Level 0")
        lvl2 = Button(command=self.startcutscene2, location=[250, 300], text="Level 1")
        lvl3 = Button(command=self.startcutscene3, location=[250, 350], text="Level 2")
        lvl4 = Button(command=self.startcutscene4, location=[250, 400], text="Level 3")
        lvl5 = Button(command=self.startcutscene5, location=[250, 450], text="Level 4")
        self.buttons.append(lvl1)
        self.buttons.append(lvl2)
        self.buttons.append(lvl3)
        self.buttons.append(lvl4)
        self.buttons.append(lvl5)
    def startlvl1(self):
        GAME_GLOBALS.MAIN_MENU_TRACK.stop()
        GAME_GLOBALS.GAME_STATE = Game_State.Game_State()
    def startlvl2(self):
        GAME_GLOBALS.MAIN_MENU_TRACK.stop()
        GAME_GLOBALS.GAME_STATE = Game_State.Game_State(levelname='../images/ASCIILEVEL1.txt', level=level1.init, name=1, final= False, text="KILL ALL ENEMIES")
    def startlvl3(self):
        GAME_GLOBALS.MAIN_MENU_TRACK.stop()
        GAME_GLOBALS.GAME_STATE = Game_State.Game_State(levelname='../images/bigelevatorthing.txt', level=level2.init, name=2, final= True, text="SURVIVE")
    def startlvl4(self):
        GAME_GLOBALS.MAIN_MENU_TRACK.stop()
        GAME_GLOBALS.GAME_STATE = Game_State.Game_State(levelname='../images/ASCIILEVEL3.txt', level=level3.init, name=3, final= False, text="ESCAPE")
    def startlvl5(self):
        GAME_GLOBALS.MAIN_MENU_TRACK.stop()
        GAME_GLOBALS.GAME_STATE = Game_State.Game_State(levelname='../images/ASCIILEVEL4.txt', level=level4.init, name=4, final= False, text="FREEDOM")

    def playmusic(self):
        GAME_GLOBALS.MAIN_MENU_TRACK.play(-1)
        pass

    def videomenu(self):
        GAME_GLOBALS.GAME_STATE = Displaybright()

    def audiomenu(self):
        GAME_GLOBALS.MAIN_MENU_TRACK.stop()
        GAME_GLOBALS.GAME_STATE = Volume()

    def highscoremenu(self):
        currhigh = 0
        currname = ''
        highscorefile = open('hsf.txt', 'r')
        for line in highscorefile:
            data = line.split()
            currhigh = int(data[1])
            currname = data[0]
        highscorefile.close()
        GAME_GLOBALS.GAME_STATE = High_Score(currhigh, currname)

    def update(self, event):

        self.DRAW_DISP.blit(self.background, (0, 0))
        for btn in self.buttons:
            btn.draw()
        if GAME_GLOBALS.BALANCE >= 0:
            GAME_GLOBALS.LOFFSET.set_alpha(abs(GAME_GLOBALS.BALANCE) * 20)
            self.DRAW_DISP.blit(GAME_GLOBALS.LOFFSET, (0,0), None, 0)
        else:
            GAME_GLOBALS.DOFFSET.set_alpha(abs(GAME_GLOBALS.BALANCE) * 20)
            self.DRAW_DISP.blit(GAME_GLOBALS.DOFFSET, (0,0), None, 0)
        #Really need a better way of doing this
        mouse_events = [x for x in event if x.type == MOUSEBUTTONDOWN or x.type == MOUSEBUTTONUP]
        for b in self.buttons:
            b.clickevent(mouse_events)
