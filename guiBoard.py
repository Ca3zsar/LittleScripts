import pygame
from pygame.locals import *
import time
import sys
import os

WIDTH = 540
HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GRAY = (128,128,128)


def drawLines():
    # The main lines
    for i in (180, 360):
        pygame.draw.line(windowSurface, BLUE, (i, 0), (i, 540), 2)
        pygame.draw.line(windowSurface, BLUE, (0, i), (540, i), 2)

    # The secondary lines
    for i in (60, 120, 240, 300, 420, 480):
        pygame.draw.line(windowSurface, BLUE, (i, 0), (i, 540), 1)
        pygame.draw.line(windowSurface, BLUE, (0, i), (540, i), 1)

def drawButtons():
    pygame.draw.rect(windowSurface,GRAY,(180,550,90,30),1)
    pygame.draw.rect(windowSurface,GRAY,(270,550,90,30),1)
    
    startButton = smallFont.render("Start",True,BLACK)
    windowSurface.blit(startButton, (180 + (45 - startButton.get_width()//2), 550 + (15 - startButton.get_height()//2)))
    
    quitButton = smallFont.render("Quit",True,BLACK)
    windowSurface.blit(quitButton, (270 + (45 - startButton.get_width()//2), 550 + (15 - startButton.get_height()//2)))
    
    

# Display the text.
def redraw(board):
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if mouse[0] >= 270 and mouse[0] <= 360 and mouse[1] >= 550 and mouse[1] <= 580:
                pygame.quit()
                sys.exit()
    windowSurface.fill(WHITE)
    drawLines()
    drawButtons()
    gap = WIDTH // 9
    if board == None:
        pygame.display.update()
        return
    for line in range(9):
        for column in range(9):
            x = column * gap
            y = line * gap

            text = basicFont.render(board[line][column], 1, BLACK)
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
    while True:
        testBoard = getBoard()
        testBoard = readBoard()
        redraw(testBoard)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if mouse[0] >= 270 and mouse[0] <= 360 and mouse[1] >= 550 and mouse[1] <= 590:
                    pygame.quit()
                    sys.exit()
                if mouse[0] >= 180 and mouse[0] <= 270 and mouse[1] >= 550 and mouse[1] <= 590:
                    mainProgram()
                    pygame.quit()
                    sys.exit()
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
