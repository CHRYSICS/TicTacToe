# TicTacToe Game
# Author: Christopher Eckerson
# Date: 12/27/2019


import pygame, sys, time, random
from pygame.locals import *

# Initialize game variables
FPS = 30  # frames per second
WINDOWWIDTH = 300  # size of window's width in pixels
WINDOWHEIGHT = 300  # size of window's height in pixels
BOXSIZE = 50  # size of box width and height in pixels
GAPSIZE = 5  # size of gap between boxes in pixels
BOARDSIZE = 3  # board is a 3 by 3 board
assert (BOARDSIZE * (BOXSIZE + GAPSIZE)) < WINDOWWIDTH, 'Board needs to be smaller than WINDOWWIDTH'
XMARGIN = int((WINDOWWIDTH - (BOARDSIZE * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT -(BOARDSIZE * (BOXSIZE + GAPSIZE))) / 2)

# Colors    R    G    B
WHITE   = (255, 255, 255)
GRAY    = (100, 100, 100)
BLACK   = (  0,   0,   0)
RED     = (255,   0,   0)
BLUE    = (  0,   0, 255)


BGCOLOR = BLACK
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

XPLAYER = 'x'
OPLAYER = 'o'
ALLPLAYERS = [XPLAYER, OPLAYER]


def main():
    global FPSCLOCK, DISPLAYSURF, CURRENT_PLAYER, GAME_STATE, BOARD, ROUND
    pygame.init()
    # pygame.mixer.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('TicTacToe Game')

    random.shuffle(ALLPLAYERS)
    CURRENT_PLAYER = ALLPLAYERS[0]
    GAME_STATE = "UNFINISHED"
    ROUND = 0
    BOARD = [["", "", ""], ["", "", ""], ["", "", ""]]
    # store mouse x and y coordinate of mouse event
    mousex = 0
    mousey = 0
    beginning = True

    # Start game Music
    pygame.mixer.music.load('Maid with the Flaxen Hair.mp3')
    pygame.mixer.music.play(-1, 0.0)

    chosenBoxes = generateChosenBoxesData(False)

    while True:  # main game loop
        if beginning is True:
            beginning = startanimation()
        mouse_clicked = False
        DISPLAYSURF.fill(BGCOLOR)  # drawing the window
        drawBoard()
        for event in pygame.event.get():  # event handling
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                # pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouse_clicked = True

        boxx, boxy = getBoxAtPixel(mousex, mousey)
        if boxx != None and boxy!= None:
            # The mouse is currently over a box
            if not chosenBoxes[boxx][boxy]:
                drawHighlightBox(boxx, boxy)
            if not chosenBoxes[boxx][boxy] and mouse_clicked:
                chosenBoxes[boxx][boxy] = True
                if CURRENT_PLAYER is OPLAYER:
                    BOARD[boxx][boxy] = OPLAYER
                    CURRENT_PLAYER = XPLAYER
                    ROUND += 1
                elif CURRENT_PLAYER is XPLAYER:
                    BOARD[boxx][boxy] = XPLAYER
                    CURRENT_PLAYER = OPLAYER
                    ROUND += 1
        # check if game was won
        gamewon = checkwinstatus(GAME_STATE)
        if gamewon:
            # Reset the Board
            chosenBoxes = generateChosenBoxesData(False)
            pygame.display.update()
            GAME_STATE = "UNFINISHED"
            ROUND = 0
            BOARD = [["", "", ""], ["", "", ""], ["", "", ""]]
        # Redraw the screen and wait a clock tick
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def drawBoard():
    for boxx in range(BOARDSIZE):
        for boxy in range(BOARDSIZE):

            left, top = LeftTopCoordsOfBox(boxx, boxy)
            EMPTY = ""
            # Draw the chosen box
            if BOARD[boxx][boxy] == OPLAYER:
                pygame.draw.rect(DISPLAYSURF, LIGHTBGCOLOR, (left, top, BOXSIZE, BOXSIZE))
                drawPlayerIcon(OPLAYER, boxx, boxy)
            elif BOARD[boxx][boxy] == XPLAYER:
                pygame.draw.rect(DISPLAYSURF, LIGHTBGCOLOR, (left, top, BOXSIZE, BOXSIZE))
                drawPlayerIcon(XPLAYER, boxx, boxy)
            elif BOARD[boxx][boxy] == EMPTY:
                pygame.draw.rect(DISPLAYSURF, WHITE, (left, top, BOXSIZE, BOXSIZE))


def drawHighlightBox(boxx, boxy):
    left, top = LeftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)


def drawPlayerIcon(player, boxx, boxy):
    quarter = int(BOXSIZE * 0.25)
    half = int(BOXSIZE * 0.5)
    left, top = LeftTopCoordsOfBox(boxx, boxy)
    # draw the player
    if player == OPLAYER:
        pygame.draw.circle(DISPLAYSURF, RED, (left + half, top + half), half - 8)
        pygame.draw.circle(DISPLAYSURF, LIGHTBGCOLOR, (left + half, top + half), quarter - 5)
    elif player == XPLAYER:
        pygame.draw.line(DISPLAYSURF, RED, (left + 10, top + 10), (left + BOXSIZE - 10, top + BOXSIZE - 10), 10)
        pygame.draw.line(DISPLAYSURF, RED, (left + BOXSIZE - 10, top + 10), (left + 10, top + BOXSIZE - 10), 10)


def generateChosenBoxesData(val):
    chosenBoxes = []
    for i in range(BOARDSIZE):
        chosenBoxes.append([val] * BOARDSIZE)
    return chosenBoxes


def LeftTopCoordsOfBox(boxx, boxy):
    # convert board coordinates to pixel coordinates
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return left, top


def getBoxAtPixel(x, y):
    for boxx in range(BOARDSIZE):
        for boxy in range(BOARDSIZE):
            left, top = LeftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return boxx, boxy
    return None, None


def checkwinstatus(game_state):
    for player in ALLPLAYERS:
        for row in range(BOARDSIZE):
            if BOARD[0][row] == player and BOARD[1][row] == player and BOARD[2][row] == player:
                game_state = player.upper() + "_WON"
                winanimation(player)
                return True
            elif BOARD[row][0] == player and BOARD[row][1] == player and BOARD[row][2] == player:
                game_state = player.upper() + "_WON"
                winanimation(player)
                return True
            elif BOARD[0][0] == player and BOARD[1][1] == player and BOARD[2][2] == player:
                game_state = player.upper() + "_WON"
                winanimation(player)
                return True
            elif BOARD[2][0] == player and BOARD[1][1] == player and BOARD[0][2] == player:
                game_state = player.upper() + "_WON"
                winanimation(player)
                return True
            elif game_state == "UNFINISHED" and ROUND == 9:
                game_state = "DRAW"
                winanimation(player)
                return True


def startanimation():
    dim = 0
    title = pygame.image.load('TICTACTOE_title.png')
    game_icons = pygame.image.load('Game_icons.png')
    maker_label = pygame.image.load('maker_label.png')
    while dim != 255:
        DISPLAYSURF.fill((dim, dim, dim))
        DISPLAYSURF.blit(game_icons, (-50, 0))
        DISPLAYSURF.blit(title, (80, 0))
        DISPLAYSURF.blit(maker_label, (150, 150))
        pygame.display.update()
        dim += 5
        pygame.time.wait(10)
    while dim != -5:
        DISPLAYSURF.fill((dim, dim, dim))
        DISPLAYSURF.blit(game_icons, (-50, 0))
        DISPLAYSURF.blit(title, (80, 0))
        DISPLAYSURF.blit(maker_label, (150, 150))
        pygame.display.update()
        dim -= 5
        pygame.time.wait(15)
    pygame.time.wait(1000)
    return False


def winanimation(player):
    color1 = [random.randint(0, 200), random.randint(0, 200), random.randint(0, 200)]
    color2 = [(255 - color1[0]) % 0.5, (255 - color1[0]) % 0.5, (255 - color1[0]) % 0.5]
    size = 10
    complete = False
    chosenboxes = generateChosenBoxesData(True)
    while not complete:
        if size == 250:
            complete = True
        else:
            color1, color2 = color2, color1
            DISPLAYSURF.fill(BLACK)
            drawBoard()
            pygame.draw.circle(DISPLAYSURF, color1, (150, 150), size)
            size += 1
        pygame.display.update()
        pygame.time.wait(2)


if __name__ == '__main__':
    main()
