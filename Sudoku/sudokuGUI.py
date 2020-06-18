import pygame
from pygame.locals import *
import time
import sys
import os
import easygui
import random

WIDTH = 600
HEIGHT = 660

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

BLUE = (0,17,255)
GREEN = (49, 156, 48)
PINK = (242,42,114)

BACK_COLOR = (17, 17, 17)
TEXT_COLOR = (186, 197, 186)
LINE_COLOR = GREEN

START_PRESSED = 0
FINISH_PRESSED = 0

def pickColor(x,y):
    global LINE_COLOR
    
    if x>=390 and x<=420 and y>=600 and y<=630:
        LINE_COLOR = BLUE
    if x>420 and x<=450 and y>=600 and y<=630:
        LINE_COLOR = GREEN
    if x>450 and x<=480 and y>=600 and y<=630:
        LINE_COLOR = PINK

def drawLines():
    #(0,14,217)
    # The main lines
    for i in (210, 390):
        pygame.draw.line(windowSurface, LINE_COLOR, (i, 30), (i, 570), 2)
        pygame.draw.line(windowSurface, LINE_COLOR, (30, i), (570, i), 2)

    # The secondary lines
    for i in (90, 150, 270, 330, 450, 510):
        for j in (30, 90, 150, 210, 270, 330, 390, 450, 510):
            pygame.draw.line(windowSurface, LINE_COLOR,
                             (i, j+10), (i, j+50), 1)
            pygame.draw.line(windowSurface, LINE_COLOR,
                             (j+10, i), (j+50, i), 1)


def drawButtons():
    #This is the finish button. It will be shown only after the game is started.
    if START_PRESSED == 1:
        pygame.draw.rect(windowSurface, LINE_COLOR, (120, 600, 90, 30), 1)
        finishButton = smallFont.render("Finish",True,TEXT_COLOR)
        windowSurface.blit(finishButton, (120 + (45 - finishButton.get_width()//2),
                                    600 + (15 - finishButton.get_height()//2)))
        
    pygame.draw.rect(windowSurface,BLUE,(390,600,30,30)) 
    pygame.draw.rect(windowSurface,GREEN,(420,600,30,30))    
    pygame.draw.rect(windowSurface,PINK,(450,600,30,30))       
        
    pygame.draw.rect(windowSurface, LINE_COLOR, (210, 600, 90, 30), 1)
    pygame.draw.rect(windowSurface, LINE_COLOR, (300, 600, 90, 30), 1)

    if START_PRESSED == 0:
        startButton = smallFont.render("Start", True, TEXT_COLOR)
    else:
        startButton = smallFont.render("Stop", True, TEXT_COLOR)
    windowSurface.blit(startButton, (210 + (45 - startButton.get_width()//2),
                                     600 + (15 - startButton.get_height()//2)))

    quitButton = smallFont.render("Quit", True, TEXT_COLOR)
    windowSurface.blit(quitButton, (300 + (45 - quitButton.get_width()//2),
                                    600 + (15 - quitButton.get_height()//2)))
    
    


def checkEvent(board):
    global START_PRESSED, FINISH_PRESSED
    count = 0
    while True:
        if not FINISH_PRESSED:
            redraw(board)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if mouse[0] >= 300 and mouse[0] <= 390 and mouse[1] >= 600 and mouse[1] <= 630:
                    pygame.quit()
                    sys.exit()
                if mouse[0] >= 390 and mouse[0] <= 480 and mouse[1] >= 60 and mouse[1] <= 630:
                    pickColor(mouse[0],mouse[1])
                if mouse[0] >= 210 and mouse[0] <= 300 and mouse[1] >= 600 and mouse[1] <= 630:
                    if START_PRESSED == 1:
                        count += 1
                        START_PRESSED = 1 - START_PRESSED
                    else:
                        count += 1
                        START_PRESSED = 1 - START_PRESSED
                if mouse[0] >= 120 and mouse[0] <= 210 and mouse[1] >= 600 and mouse[1] <= 630:
                    if START_PRESSED == 1:
                        FINISH_PRESSED = 1
                        START_PRESSED = 0

        if count != 1:
            break

# Display the interface.
def redraw(board=None):

    windowSurface.fill(BACK_COLOR)
    drawLines()
    drawButtons()
    gap = (WIDTH-60) // 9
    
    if board == None:
        pygame.display.update
        return
    
    for line in range(9):
        for column in range(9):
            x = column * gap + 30
            y = line * gap + 30

            text = basicFont.render(board[line][column], 1, TEXT_COLOR)
            windowSurface.blit(
                text, (x + (gap//2 - text.get_width()//2), y + (gap//2 - text.get_height()//2)))

    pygame.display.update()


def isThereAnyX(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == ' ':
                return i, j
    return False


def freeLine(board, line, value):
    for i in range(9):
        if board[line][i] == value:
            return False
    return True


def freeColumn(board, column, value):
    for i in range(9):
        if board[i][column] == value:
            return False

    return True


def freeSubBoard(board, line, column, value):
    top = line - line % 3
    left = column - column % 3
    for i in range(top, top+3):
        for j in range(left, left+3):
            if board[i][j] == value:
                return False

    return True


def isFree(board, line, column, value):
    return freeLine(board, line, value) and freeColumn(board, column, value) and freeSubBoard(board, line, column, value)


def solve(board):
    position = isThereAnyX(board)
    pygame.event.pump()
    if position == False:
        return True
    for i in range(1, 10):
        if isFree(board, position[0], position[1], str(i)):
            board[position[0]][position[1]] = str(i)
            if not FINISH_PRESSED:
                checkEvent(board)
                pygame.time.delay(50)
                redraw(board)
            if solve(board) == True:
                return True
            board[position[0]][position[1]] = ' '

    return False

def checkFile(file):
    testBoard = file.readlines()
    for i in range(9):
        if len(testBoard[i])>10:
            return False
        for j in range(9):
            if not (testBoard[i][j] in "123456789 "):
                return False
    file.seek(0)
    return True

def getBoard():
    newBoard = []
    for i in range(9):
        newBoard.append([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '])

    return newBoard


def readBoard(test=True):
    while True:
        if test:
            file = open(os.path.join(sys.path[0], "input.txt"), "r")
        else:
            fileName = easygui.fileopenbox(
                "Enter the sudoku board", "Sudoku Board", default='*.txt', filetypes=['*.txt'])
            file = open(os.path.join(sys.path[0], fileName), "r")
        if checkFile(file):
            break
                    
    board = file.readlines()
    tempBoard = getBoard()
    for i in range(9):
        for j in range(9):
            tempBoard[i][j] = board[i][j]
    return tempBoard


def getRandomBoard():
    noOfNumbers = int(random.randint(15,25))
    board = getBoard()
    for i in range(noOfNumbers):
        x,y = random.randint(0,8),random.randint(0,8)
        val = random.randint(1,9)
        board[x][y] = str(val)
    
    return board

def mainProgram():
    board = getBoard()
    board = readBoard(test=False)
    # Draw on the window.
    solvable = solve(board)

    if solvable == True:
        print("The final board is: ")
        redraw(board)
    else:
        print("This Sudoku board is not solvable")
    return board

def main():
    #Initial display.
    global START_PRESSED, FINISH_PRESSED
    testBoard = getRandomBoard()
    redraw(testBoard)
    while True:
        
        START_PRESSED = 0
        FINISH_PRESSED = 0 
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if mouse[0] >= 300 and mouse[0] <= 390 and mouse[1] >= 600 and mouse[1] <= 630:
                    pygame.quit()
                    sys.exit()
                if mouse[0] >= 390 and mouse[0] <= 480 and mouse[1] >= 60 and mouse[1] <= 630:
                    pickColor(mouse[0],mouse[1])
                    redraw(testBoard)
                if mouse[0] >= 210 and mouse[0] <= 300 and mouse[1] >= 600 and mouse[1] <= 630:
                    START_PRESSED = 1 - START_PRESSED
                    testBoard = mainProgram()
                
                    

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
