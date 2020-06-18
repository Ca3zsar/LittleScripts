# Sudoku solver

import os
import time

def getBoard():
    newBoard = []
    for i in range(9):
        newBoard.append(['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'])

    return newBoard


def displayBoard(board):
    # os.system("cls")  # Clear the screen
    
    for i in range(9):

        if i % 3 == 0:
            print("-------------")

        for j in range(9):
            if j % 3 == 0:
                print('|', end='')
            print(board[i][j], end='')

        print('|', end='')
        print()

    print("-------------")


def isThereAnyX(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 'X':
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

    if position == False:
        return True
    for i in range(1, 10):
        if isFree(board, position[0], position[1], str(i)):
            board[position[0]][position[1]] = str(i)
            # displayBoard(board)
            if solve(board) == True:
                return True
            board[position[0]][position[1]] = 'X'
            
    return False

def readBoard():
    file = open("input.txt","r")
    board = file.readlines()
    tempBoard = getBoard()
    for i in range(9):
        for j in range(9):
            tempBoard[i][j] = board[i][j]
    return tempBoard
            

def main():

    mainBoard = getBoard()
    mainBoard = readBoard()
    solvable = solve(mainBoard)
    if solvable == True:
        print("The final board is: ")
        displayBoard(mainBoard)
    else:
        print("This Sudoku board is not solvable")

main()