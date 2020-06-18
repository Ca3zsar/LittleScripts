import pygame
from pygame.locals import *
import time
import sys
import os

WIDTH = 600
HEIGHT = 660

# Colors
BACK_COLOR = (17,17,17)
TEXT_COLOR = (186,197,186)
LINE_COLOR = (49,156,48)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128,128,128)

START_PRESSED = 0

def drawLines():
    # The main lines
    for i in (210, 390):
        pygame.draw.line(windowSurface, LINE_COLOR, (i, 30), (i, 570), 2)
        pygame.draw.line(windowSurface, LINE_COLOR, (30, i), (570, i), 2)

    # The secondary lines
    for i in (90, 150, 270, 330, 450, 510):
        for j in (30,90,150,210,270,330,390,450,510):
            pygame.draw.line(windowSurface, LINE_COLOR, (i, j+10), (i, j+50), 1)
            pygame.draw.line(windowSurface, LINE_COLOR, (j+10, i), (j+50, i), 1)

def drawButtons():
    pygame.draw.rect(windowSurface,LINE_COLOR,(210,600,90,30),1)
    pygame.draw.rect(windowSurface,LINE_COLOR,(300,600,90,30),1)
    
    if START_PRESSED == 0:
        startButton = smallFont.render("Start",True,TEXT_COLOR)
    else:
        startButton = smallFont.render("Stop",True,TEXT_COLOR)
    windowSurface.blit(startButton, (210 + (45 - startButton.get_width()//2), 600 + (15 - startButton.get_height()//2)))
    
    quitButton = smallFont.render("Quit",True,TEXT_COLOR)
    windowSurface.blit(quitButton, (300 + (45 - startButton.get_width()//2), 600 + (15 - startButton.get_height()//2)))
    
    
def stopPressed(board):
    global START_PRESSED
    START_PRESSED = 1 - START_PRESSED
    print(START_PRESSED)
    redraw(board)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if mouse[0] >= 300 and mouse[0] <= 390 and mouse[1] >= 600 and mouse[1] <= 630:
                    pygame.quit()
                    sys.exit()
                if mouse[0] >= 180 and mouse[0] <= 300 and mouse[1] >= 600 and mouse[1] <= 630:
                    START_PRESSED = 1 - START_PRESSED
                    return True

def checkEvent(board):
    global START_PRESSED
    # print(START_PRESSED)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if mouse[0] >= 300 and mouse[0] <= 390 and mouse[1] >= 600 and mouse[1] <= 630:
                pygame.quit()
                sys.exit()
            if mouse[0] >= 180 and mouse[0] <= 300 and mouse[1] >= 600 and mouse[1] <= 630:
                if START_PRESSED == 1:
                    if stopPressed(board):
                        break
                else:
                    START_PRESSED = 1 - START_PRESSED

# Display the interface.
def redraw(board):
    
    if board != None:
        checkEvent(board)
                
    windowSurface.fill(BACK_COLOR)
    drawLines()
    drawButtons()
    gap = (WIDTH-60) // 9
    if board == None:
        pygame.display.update()
        return
    for line in range(9):
        for column in range(9):
            x = column * gap + 30
            y = line * gap + 30

            text = basicFont.render(board[line][column], 1, TEXT_COLOR)
            windowSurface.blit(text, (x + (gap//2 - text.get_width()//2), y + (gap//2 - text.get_height()//2)))
    
    pygame.display.update()

def isThereAnyX(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == ' ':
                return i, j
    return False

def freeLine(board,line,value):
    for i in range(9):
        if board[line][i] == value:
            return False
    return True

def freeColumn(board,column,value):
    for i in range(9):
        if board[i][column] == value:
            return False
        
    return True

def freeSubBoard(board,line,column,value):
    top = line - line % 3
    left = column - column % 3
    for i in range(top,top+3):
        for j in range(left,left+3):
            if board[i][j] == value:
                return False
            
    return True
    

def isFree(board,line,column,value):
    return freeLine(board,line,value) and freeColumn(board,column,value) and freeSubBoard(board,line,column,value)

def solve(board):
    position = isThereAnyX(board)
    pygame.event.pump()
    if position == False:
        return True
    for i in range(1, 10):
        if isFree(board, position[0], position[1], str(i)):
            board[position[0]][position[1]] = str(i)
            pygame.time.delay(50)
            redraw(board)
            if solve(board) == True:
                return True
            board[position[0]][position[1]] = ' '
            
    return False

def getBoard():
    newBoard = []
    for i in range(9):
        newBoard.append([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '])

    return newBoard


def readBoard():
    file = open( os.path.join(sys.path[0], "input.txt"), "r")
    board = file.readlines()
    tempBoard = getBoard()
    for i in range(9):
        for j in range(9):
            tempBoard[i][j] = board[i][j]
    return tempBoard

def mainProgram():
    board = getBoard()
    board = readBoard()
    # Draw on the window.
    solvable = solve(board)
    
    if solvable == True:
        print("The final board is: ")
        redraw(board)
    else:
        print("This Sudoku board is not solvable")


def main():
    global START_PRESSED
    testBoard = getBoard()
    testBoard = readBoard()
    redraw(testBoard)
    while True:
        
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if mouse[0] >= 300 and mouse[0] <= 390 and mouse[1] >= 600 and mouse[1] <= 630:
                    pygame.quit()
                    sys.exit()
                if mouse[0] >= 180 and mouse[0] <= 300 and mouse[1] >= 600 and mouse[1] <= 630:
                    START_PRESSED = 1 - START_PRESSED
                    mainProgram()
    # mainProgram()

 # Initialize the window and font
pygame.init()
windowSurface = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption("Grid")
basicFont = pygame.font.Font(
    os.path.join(sys.path[0], "bebas.ttf"), 24)
smallFont = pygame.font.Font(
    os.path.join(sys.path[0], "bebas.ttf"), 16
)

main()
