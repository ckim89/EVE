

import pygame
import Player
import GAME_GLOBALS
from collections import defaultdict
import math
import random


class Grid:
    def __init__(self, im, position, r):
        self.im = im
        self.position = position
        self.rect = r

def init(filename):

    floor = pygame.image.load('../images/TILE_FLOOR_3.jpg').convert()
    wall = pygame.image.load('../images/TILE_WALL_3.jpg').convert()
    dim = pygame.transform.scale(pygame.image.load('../images/TILE_PORTAL1.jpg').convert(),(50,50))
    ground = pygame.transform.scale(pygame.image.load('../images/BKG_GRASS_TILE.png').convert(), (50,50))
    decor1 = pygame.image.load('../images/LEVEL3/DECOR_1.png').convert_alpha()
    decor2 = pygame.image.load('../images/LEVEL3/DECOR_2.png').convert_alpha()
    decor3 = pygame.image.load('../images/LEVEL3/DECOR_3.png').convert_alpha()
    decor5 = pygame.image.load('../images/LEVEL3/DECOR_5.png').convert_alpha()
    adecor = [decor1, decor2, decor3, decor5]
    floor_tag = 'o'
    floor_wall = 'x'



    floors = []
    walls = []
    nullspace = []
    door = []
    enemy = []
    penemy = []
    cenemy = []
    decor = []

    f = open(filename, 'r')
    row = 0
    col = 0

    finish_trigger = []


    maxcol = 0
    for line in f:
        col = 0
        for char in line:
            newrect = pygame.Rect((col*50, row*50), (50, 50))
            onerect = pygame.Rect((col*50, row*50), (150,150))
            tworect = pygame.Rect((col*50, row*50), (200,400))
            threerect = pygame.Rect((col*50, row*50), (300, 100))
            if char == 'o':
                floors.append(Grid(floor, (row, col), newrect))
            elif char == 'x':
                walls.append(Grid(wall, (row, col), newrect))
            elif char == 'D':
                door.append(Grid(dim,(row,col), newrect))
            elif char == 'E':
                enemy.append((row, col))
                floors.append(Grid(floor, (row, col), newrect))
            elif char == 'Z':
                penemy.append((row, col))
                floors.append(Grid(floor, (row, col), newrect))
            elif char == 'C':
                cenemy.append((row, col))
                floors.append(Grid(floor, (row, col), newrect))
            elif char == 'F':
                floors.append(Grid(floor, (row, col), newrect))
                finish_trigger.append((row,col))
            elif char == 'P':
                floors.append(Grid(floor, (row, col), newrect))
                playerpos = (col*50, row*50)
            elif char == '1':
                floors.append(Grid(floor, (row, col), newrect))
                decor.append(Grid(adecor[0], (row, col), onerect))
            elif char == '2':
                floors.append(Grid(floor, (row, col), newrect))
                decor.append(Grid(adecor[1], (row, col), tworect))
            elif char == '3':
                floors.append(Grid(floor, (row, col), newrect))
                decor.append(Grid(adecor[2], (row, col), threerect))
            elif char == '5':
                floors.append(Grid(floor, (row, col), newrect))
                decor.append(Grid(adecor[3], (row, col), newrect))
            else:
                  nullspace.append(Grid(ground, (row, col), newrect))

            col += 1
        if col > maxcol:
            maxcol = col
        row += 1

    f.close()

    gridsize = 500
    size = (maxcol*50, row*50)
    grid = defaultdict(list)
    x = range(0, size[0], gridsize)
    y = range(0, size[1], gridsize)
    #Initialize grid
    for c in x:
        for r in y:
            grid[(c,r)] = []

    for w in walls:
        pos = (math.floor(w.rect.topleft[0]/gridsize)*gridsize, math.floor(w.rect.topleft[1]/gridsize)*gridsize)
        grid[pos].append(w)

    return [decor, floors,walls,door, nullspace, enemy,row,maxcol,finish_trigger, playerpos, penemy, cenemy, grid]



