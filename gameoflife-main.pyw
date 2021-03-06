# 1. Any live cell with fewer than two live neighbours dies, as if caused by under-population.
# 2. Any live cell with two or three live neighbours lives on to the next generation.
# 3. Any live cell with more than three live neighbours dies, as if by overcrowding.
# 4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
from typing import Dict, Any

import pygame, sys
import pygame_menu
from pygame.locals import *
from tkinter import *
import random

pygame.init()
FPS = 2
WINDOWW = 900
WINDOWH = 800
CELLSIZE = 10

assert WINDOWW % CELLSIZE == 0, "window width must be a multiple of cell size"
assert WINDOWH % CELLSIZE == 0, "window height must be a multiple of cell size"
CELLW = WINDOWW / CELLSIZE
# width of cells
CELLH = WINDOWH / CELLSIZE
# height of cell

# colors:

BLUE = (108, 154, 139)  # dead
LGREEN = (4, 232, 36)  # alive
YELLOW = (255, 199, 89)
DGREEN = (0, 15, 8)  # grid bg
ORANGE = (176, 46, 12)
WHITE = (255, 255, 255)
GREY = (29, 30, 24)  # grid lines
RED = (255, 105, 105)


# draw grid

def Grid():
    for x in range(0, WINDOWW, CELLSIZE):  # vertical lines
        pygame.draw.line(DISPLAY, GREY, (x, 0), (x, WINDOWH))
    for y in range(0, WINDOWH, CELLSIZE):  # horizontal lines
        pygame.draw.line(DISPLAY, GREY, (0, y), (WINDOWW, y))


# coloring the cells

def colorGrid(item, lifeD):
    x = item[0]  # dead
    y = item[1]  # alive
    y = y * CELLSIZE  # makes it to where it accounts for the cellsize
    x = x * CELLSIZE  # makes it to where it accounts for the cellsize
    if lifeD[item] == 0:
        pygame.draw.rect(DISPLAY, YELLOW, (x, y, CELLSIZE, CELLSIZE))
    if lifeD[item] == 1:
        pygame.draw.rect(DISPLAY, BLUE, (x, y, CELLSIZE, CELLSIZE))
    return None


# creating a dictionary to store data about life, whether dead 0 or alive 1

def blank():
    gridD = {}
    for y in range(int(CELLH)):
        for x in range(int(CELLW)):
            gridD[x, y] = 0
    return gridD


# assigning each item in dict to have a 1 or 0 randomly

def randomizedStartGrid(lifeD):
    for item in lifeD:
        lifeD[item] = random.randint(0, 1)
    return lifeD


# defines the state of neighboring pixels

# potential 8 states for the neighbor:

# x - 1 | x = 0 | x + 1
# y - 1 | y - 1 | y - 1
# ------+-------+------
# x -  1 |   x   | x + 1
# y = 0 |   y   | y = 0
# ------+-------+------
# x -  1 | x = 0 | x + 1
# y + 1 | y + 1 | y + 1

def getNearbyState(item, lifeD):
    nearbyLiving = 0  # the nearby cells that are alive
    for x in range(-1, 2):
        for y in range(-1, 2):
            check = (item[0] + x, item[1] + y)  # |
            # anything that follows these two requirements should be on grid V
            if check[0] < CELLW and check[0] >= 0:
                if check[1] < CELLH and check[1] >= 0:
                    if lifeD[check] == 1:  # there is life if its a 1
                        if x == 0 and y == 0:  # ignore
                            nearbyLiving += 0
                        else:  # only counts 8 surrounding cells doesnt include actual cell of the thing thats doing the check
                            nearbyLiving += 1
    return nearbyLiving


# determine what happens each tick with each gen
def tick(lifeD):
    newTick = {}  # to keep from overwritting data need to create a temp store to tell what is going to happen next gen
    for item in lifeD:
        numberOfNearbyL = getNearbyState(item, lifeD)
        if lifeD[item] == 1:  # if alive
            if numberOfNearbyL < 2:  # underpopulated rule
                newTick[item] = 0
            elif numberOfNearbyL > 3:  # overcrowding rule
                newTick[item] = 0
            else:
                newTick[item] = 1  # keep alive
        elif lifeD[item] == 0:  # if dead
            if numberOfNearbyL == 3:  # it will resurrect if there are three alive nearby
                newTick[item] = 1
            else:
                newTick[item] = 0  # otherwise, if there arent exactly three around it alive it stays dead
    return newTick


# increase pixel grid

def click_inc():
    global CELLSIZE
    CELLSIZE += 1
    cell.config(text=f'cellsize: {CELLSIZE}')


def click_dec():
    global CELLSIZE
    if CELLSIZE <= 10:
        CELLSIZE == 10
    else:
        CELLSIZE -= 1
    cell.config(text=f'cellsize: {CELLSIZE}')


def click_inc_fps():
    global FPS
    FPS += 1
    fps.config(text=f'FPS: {FPS}')


def click_dec_fps():
    global FPS
    if FPS <= 1:
        FPS == 1
    else:
        FPS -= 1
    fps.config(text=f'FPS: {FPS}')


def options_buttons():
    root = Tk()
    global increase_pixels
    global decrease_pixels
    global cell
    global fps
    increase_pixels = Button(root, text="increase pixel size", command=click_inc)
    decrease_pixels = Button(root, text="decrease pixel size", command=click_dec)
    cell = Button(root, text=f'cellsize: {CELLSIZE}', state="disabled")
    increase_fps = Button(root, text="increase FPS", command=click_inc_fps)
    decrease_fps = Button(root, text="decrease FPS", command=click_dec_fps)
    fps = Button(root, text=f'FPS: {FPS}', state="disabled")
    increase_pixels.pack()
    decrease_pixels.pack()
    cell.pack()
    increase_fps.pack()
    decrease_fps.pack()
    fps.pack()
    root.mainloop()


def sidebar():
    global DISPLAY
    sidebar1 = Rect(0, 750, 900, 50)
    pygame.draw.rect(DISPLAY, ORANGE, sidebar1)


def text():
    global FPS
    global DISPLAY
    global CELLSIZE
    global font
    font = pygame.font.SysFont(f'fps: {FPS}', 32)
    fps = font.render(f'fps: {FPS}', True, GREY)
    DISPLAY.blit(fps, (5, 760))
    cell = font.render(f'pixel size: {CELLSIZE}', TRUE, GREY)
    DISPLAY.blit(cell, (80, 760))
    menu_a = font.render("press 'a' for menu", True, GREY)
    DISPLAY.blit(menu_a, (240, 760))


def press_a():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                menu.mainloop(DISPLAY)


def single_pixel():
    global currentx
    global currenty
    global square
    current = pygame.mouse.get_pos()
    currentx = current[0]
    currenty = current[1]
    square = pygame.draw.rect(DISPLAY, BLUE, (currentx // CELLSIZE * 10, currenty // CELLSIZE * 10, CELLSIZE, CELLSIZE))
    # START HERE TOMORROW

#
def l_click():
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if 0 <= currentx <= WINDOWW and 0 <= currenty <= WINDOWH:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 2:
        square



def play_btn():
    global FPS
    global lifeD
    font = pygame.font.SysFont("PLAY", 32)
    play = pygame.draw.rect(DISPLAY, RED, (530, 760, 80, 30))

    play_f = font.render("PLAY", True, WHITE)
    a = DISPLAY.blit(play_f, (530, 760))


    # event = pygame.event.poll()
    # if 453 <= currentx <= 509 and 761 <= currenty <= 787:
    # for event in pygame.event.get():
    #     if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
    #     FPS = 2
    # while True:
    #     for event in pygame.event.get():
    #         if pygame_menu.events.EXIT:
    #             if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
    #                 pos = pygame.mouse.get_pos()
    #                 if a.collidepoint(pos):
    #                     FPS = 2


def pause_btn():
    font = pygame.font.SysFont(f'fps: {FPS}', 24)
    pause = pygame.draw.rect(DISPLAY, RED, (450, 760, 60, 30))
    pause_f = font.render("PAUSE", True, WHITE)
    DISPLAY.blit(pause_f, (450, 760))


def gens():
    font = pygame.font.SysFont(f'fps: {FPS}', 24)
    gens_f = font.render(f'gens: {pygame.time.get_ticks() // 1000}', True, GREY)
    DISPLAY.blit(gens_f, (750, 760))

def play():
    global current
    global currentx
    global currenty
    current = pygame.mouse.get_pos()
    currentx = current[0]
    currenty = current[1]
    paused = True
    while not paused:
        global FPS
        global FPSCLOCK
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if 531 <= currentx <= 715 and 723 <= currenty <= 788:
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:

                    paused = True


def pause():
    global current
    global currentx
    global currenty
    global FPSCLOCK
    current = pygame.mouse.get_pos()
    currentx = current[0]
    currenty = current[1]
    paused = True
    while paused:
        global FPS

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if 453 <= currentx <= 509 and 761 <= currenty <= 787:
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    paused = False

def main():
    global start
    global menu
    global currentx
    global currenty
    global DISPLAY
    pygame.init()
    global FPSCLOCK
    FPSCLOCK = pygame.time.Clock()
    DISPLAY = pygame.display.set_mode((WINDOWW, WINDOWH))
    pygame.display.set_caption('Game of Life')
    DISPLAY.fill(DGREEN)  # fills bg with green
    current = pygame.mouse.get_pos()
    currentx = current[0]
    currenty = current[1]

    def start():
        global FPS
        global lifeD
        global currentx
        global currenty
        global FPSCLOCK

        while True:
            global menu
            global lifeD
            # main part of game
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            # runs a tick
            # creates library and matches it with blank

            # for event in pygame.event.get():
            #     if pygame_menu.events.EXIT:
            #         if event.type == pygame.MOUSEBUTTONDOWN:
            #             if event.button == 1:
            #                 l_click()
            # event = pygame.event.poll()
            lifeD = blank()
            # if FPS >= 2:
            #     lifeD = randomizedStartGrid(lifeD)
            # else:
            #     lifeD = blank()

            # def mouse_check():
            #     global FPS
            #
            #     if FPS == 0:
            #         if 453 <= currentx <= 509 and 761 <= currenty <= 787:
            #             if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            #                 FPS = 2
            #                 count = 1
            #             elif event.type == pygame.MOUSEBUTTONUP and event.button == 2:
            #                 FPS = 0
            for item in lifeD:
                colorGrid(item, lifeD)
            lifeD = tick(lifeD)
            for item in lifeD:
                colorGrid(item, lifeD)

            Grid()
            sidebar()
            text()
            press_a()
            gens()
            play_btn()
            pause_btn()
            if pygame_menu.events.EXIT:
                if 453 <= currentx <= 509 and 761 <= currenty <= 787:
                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        pause()
                if 453 <= currentx <= 509 and 761 <= currenty <= 787:
                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        play()



            # mouse_check()
            single_pixel()
            pygame.display.update()
            FPSCLOCK.tick(FPS)


    menu = pygame_menu.Menu(WINDOWH, WINDOWW, "CONWAYS GAME OF LIFE", theme=pygame_menu.themes.THEME_DARK)
    menu.add_button('Start Simulation', start)
    menu.add_button('Options', options_buttons)
    menu.add_button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(DISPLAY)


if __name__ == '__main__':
    main()
