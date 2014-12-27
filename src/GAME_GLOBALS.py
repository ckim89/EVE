import pygame
pygame.init()
from pygame.locals import *
#global variables
#Useful for debug purposes and changing stuff easily

CURRENT_LEVEL = None

GAME_TITLE = "EVE: The Millennium Project"
HIGH_SCORE_TITLE = "HIGH SCORES: "
DISPLAY_TITLE = "ADJUST THE BRIGHTNESS: "
PRODUCTION_TEAM = "NoName Corp"
WINNING = "Congratulations... You have escaped."

#Window Size Vars
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
WINDOW_SIZE  = (WINDOW_WIDTH,WINDOW_HEIGHT)

#Update controls
GAME_STATE = None
GAME_MAIN_MENU = None
MAX_FPS = 60
MIN_FPS = 15
UPDATE_INT = (1/MAX_FPS)
MAX_UPDATECOUNT_PER_FRAME = (MAX_FPS/MIN_FPS)

currentgame = None

#Color macros for what ever reason
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

#Default controls Fonts, button things, etc.
DEFAULT_FONT = '../images/fonts/Futured.TTF'
DEFAULT_BUTTON_IM = '../images/button.png'
DEFAULT_BUTTON_IM_DOWN = '../images/button_down.png'
DEFAULT_FONT_SIZE = 18
DEFAULT_PLAYER = '../images/PLAYER_ALL_SPRITESHEET.png'
MELEE_ENEMY = '../images/ENEMY2_SPRITESHEET.png'
PROJECT_ENEMY = '../images/ENEMY1_SPRITESHEET.png'
CAPTAIN_ENEMY = '../images/ENEMY3_SPRITESHEET.png'
ENEMY_LASER = '../images/LASERBEAM.png'
HIGH_SCORE_BACK = '../images/HIGHSCORES_SCREEN.jpg'
MAIN_MENU_BACKGROUND = '../images/MENU_SCREEN.jpg'
START_SCREEN_BACKGROUND = '../images/TITLE_SCREEN.jpg'
DEFAULT_DIAG = '../images/DIALOG_BOX.png'
WIN = '../images/WIN_SCREEN.png'
DIAGBOX_TEXTSPEED = 45

#Sounds
pygame.mixer.init()
VOLUME = .5
MAIN_MENU_TRACK = pygame.mixer.Sound('../sounds/OpeningMain.ogg')
BUMP = pygame.mixer.Sound('../sounds/blip.wav')
POINTS = pygame.mixer.Sound('../sounds/point.ogg')
APPROACH = pygame.mixer.Sound('../sounds/ApproachEnemy.ogg')
LVL_1_TRACK = pygame.mixer.Sound('../sounds/level1.ogg')
LVL_2_TRACK = pygame.mixer.Sound('../sounds/level2.ogg')
LVL_3_TRACK = pygame.mixer.Sound('../sounds/level3.ogg')
LVL_4_TRACK = pygame.mixer.Sound('../sounds/level4.ogg')
LVL_5_TRACK = pygame.mixer.Sound('../sounds/finallevel.ogg')
FOOTSTEPS = pygame.mixer.Sound('../sounds/footsteps.ogg')
PATTACK = pygame.mixer.Sound('../sounds/swoosh1.ogg')
P1ATTACK = pygame.mixer.Sound('../sounds/swoosh2.ogg')
SWORDBLOCK = pygame.mixer.Sound('../sounds/swordblock.ogg')
ZAP = pygame.mixer.Sound('../sounds/zap.ogg')
DAMAGE = pygame.mixer.Sound('../sounds/DamageMix.ogg')
ALL_SOUNDS = {MAIN_MENU_TRACK, BUMP, SWORDBLOCK, DAMAGE, POINTS, APPROACH, LVL_1_TRACK, LVL_2_TRACK, LVL_3_TRACK, LVL_4_TRACK, FOOTSTEPS, PATTACK, P1ATTACK, ZAP}
for sounds in ALL_SOUNDS:
    sounds.set_volume(VOLUME)

#joystick controls
pygame.joystick.init()
joysticks = []
for i in range(0, pygame.joystick.get_count()):
    joysticks.append(pygame.joystick.Joystick(i))
    joysticks[-1].init()
BUTTONS = [False, False, False, False, False, False, False, False, False, False, False, False, False, False]
if pygame.joystick.get_count() != 0:
    x = joysticks[0].get_numbuttons()
    BUTTONS = [False for i in range(joysticks[0].get_numbuttons())]
COUNT = pygame.joystick.get_count()
#Other
LOCKEDENEMY = None
LA = 255
DA = 0
BALANCE = 0
LIGHT = 0
LALPHA = 10
DALPHA = 10
DOFFSET = pygame.Surface(WINDOW_SIZE)
DOFFSET.set_alpha(20)
DOFFSET.fill((DA,DA,DA))
LOFFSET = pygame.Surface(WINDOW_SIZE)
LOFFSET.set_alpha(20)
LOFFSET.fill((LA,LA,LA))







