# 1. Any live cell with fewer than two live neighbours dies, as if caused by under-population.
# 2. Any live cell with two or three live neighbours lives on to the next generation.
# 3. Any live cell with more than three live neighbours dies, as if by overcrowding.
# 4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.


import pygame, sys
from pygame.locals import *
import random
FPS = 5
WINDOWW = 900
WINDOWH = 800
CELLSIZE = 10


assert WINDOWW % CELLSIZE == 0, "window width must be a multiple of cell size"
assert WINDOWH % CELLSIZE == 0, "window height must be a multiple of cell size"
CELLW = WINDOWW / CELLSIZE #width of cells
CELLH = WINDOWH / CELLSIZE # height of cell

#colors:

BLUE = (108, 154, 139) #dead
LGREEN = (4, 232, 36) #alive
YELLOW = (255, 199, 89)
DGREEN = (0, 15, 8) #grid bg
ORANGE = (176, 46, 12)
WHITE = (255, 255, 255)
GREY = (29, 30, 24) #grid lines
#draw grid

def Grid():
    for x in range(0, WINDOWW, CELLSIZE): #vertical lines 
        pygame.draw.line(DISPLAY, GREY, (x,0),(x,WINDOWH))
    for y in range(0, WINDOWH, CELLSIZE): #horizontal lines
        pygame.draw.line(DISPLAY, GREY, (0,y), (WINDOWW, y))




#coloring the cells

def colorGrid(item, lifeD):
    x = item[0] #dead
    y = item[1] #alive
    y = y * CELLSIZE #makes it to where it accounts for the cellsize
    x = x * CELLSIZE #makes it to where it accounts for the cellsize
    if lifeD[item] == 0:
        pygame.draw.rect(DISPLAY, YELLOW, (x, y, CELLSIZE, CELLSIZE))
    if lifeD[item] == 1:
        pygame.draw.rect(DISPLAY, BLUE, (x, y, CELLSIZE, CELLSIZE))
    return None

#creating a dictionary to store data about life, whether dead 0 or alive 1

def blank():
    gridD = {}
    for y in range (int(CELLH)):
        for x in range (int(CELLW)):
            gridD[x,y] = 0
    return gridD

#assigning each item in dict to have a 1 or 0 randomly

def randomizedStartGrid(lifeD):
    for item in lifeD:
        lifeD[item] = random.randint(0,1)
    return lifeD

#defines the state of neighboring pixels

#potential 8 states for the neighbor:

# x - 1 | x = 0 | x + 1
# y - 1 | y - 1 | y - 1
# ------+-------+------
# x -  1 |   x   | x + 1
# y = 0 |   y   | y = 0
# ------+-------+------
# x -  1 | x = 0 | x + 1
# y + 1 | y + 1 | y + 1

def getNearbyState(item, lifeD):
    nearbyLiving = 0 #the nearby cells that are alive
    for x in range (-1,2):
        for y in range(-1,2):
            check = (item[0]+x,item[1]+y)                                  # |
            # anything that follows these two requirements should be on grid V
            if check[0] < CELLW and check[0] >=0:
                if check [1] < CELLH and check[1]>= 0:
                       if lifeD[check] == 1: #there is life if its a 1
                           if x == 0 and y == 0: #ignore
                               nearbyLiving += 0
                           else:                   #only counts 8 surrounding cells doesnt include actual cell of the thing thats doing the check
                               nearbyLiving += 1
        return nearbyLiving

#determine what happens each tick with each gen
def tick(lifeD):
    newTick = {}  #to keep from overwritting data need to create a temp store to tell what is going to happen next gen
    for item in lifeD:
        numberOfNearbyL = getNearbyState(item, lifeD)
        if lifeD[item] == 1: #if alive
            if numberOfNearbyL < 2: #underpopulated rule
                newTick[item] = 0
            elif numberOfNearbyL > 3: #overcrowding rule
                newTick[item] = 0
            else:
                newTick[item] = 1 #keep alive
        elif lifeD[item] == 0: #if dead
            if numberOfNearbyL == 3: #it will resurrect if there are three alive nearby
                newTick[item] = 1
            else:
                newTick[item] = 0 #otherwise, if there arent exactly three around it alive it stays dead
    return newTick
def main(): 
    pygame.init()
    global DISPLAY
    FPSCLOCK = pygame.time.Clock()
    DISPLAY = pygame.display.set_mode((WINDOWW, WINDOWH))
    pygame.display.set_caption('Game of Life')
    DISPLAY.fill(DGREEN) #fills bg with green

    lifeD = blank() #creates library and matches it with blank grid
    lifeD = randomizedStartGrid(lifeD)
    for item in lifeD:
        colorGrid(item, lifeD)
    while True: #main part of game
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            #runs a tick
            lifeD = tick(lifeD)
            for item in lifeD:
                colorGrid(item, lifeD)
            Grid()
            pygame.display.update()
            FPSCLOCK.tick(FPS)
if __name__=='__main__':
        main()