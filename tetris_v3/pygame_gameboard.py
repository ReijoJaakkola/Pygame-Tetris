import pygame
from pygame.locals import *

# GameBoard contains the information of which squares are currently
# being used and what is the color of every square. For every square
# in the board grid contains value 0 or 1. If the value of square is 0,
# then the square is free. If it is 1, then it is occupied, which means
# that it contains part of some earlier peace which has already landed.
class GameBoard:
    def __init__(self, windowManager):
        self.windowManager = windowManager
        self.width =  windowManager.getGridWidth() // windowManager.getSquareSize()
        self.height = windowManager.getGridHeight() // windowManager.getSquareSize()
        self.board = []
        
        for i in range(self.width):
            row = []
            for j in range(self.height):
                row.append([0,windowManager.getGridBackgroundColor()])
            self.board.append(row)

    def paint(self,i,j,color,linewidth = 0):
        self.windowManager.drawSquareToGrid(i,j,color,linewidth)

    def paintSquare(self,i,j,color = None):
        if color is None:
            color = self.windowManager.getGridBackgroundColor()

        if i >= 0 and j >= 0 and self.width > i and self.height > j:
            self.board[i][j] = [0,color]
            self.paint(i,j,color)
            self.paint(i,j,pygame.Color(0,0,0),1)

    def paintPreviewSquare(self,i,j,color):
        if i >= 0 and j >= 0 and self.width > i and self.height > j:
            self.paint(i,j,color,1)

    def reserve(self,i,j,color):
        if i >= 0 and j >= 0 and self.width > i and self.height > j:
            self.board[i][j] = [1,color]
            self.paint(i,j,color)
            self.paint(i,j,pygame.Color(0,0,0),1)

    def free(self,i,j):
        if i >= 0 and j >= 0 and self.width > i and self.height > j:
            self.board[i][j] = [0,self.windowManager.getGridBackgroundColor()]
            self.paint(i,j,self.windowManager.getGridBackgroundColor())

    def isReserved(self,i,j):
        if i >= 0 and j >= 0 and self.width > i and self.height > j:
            if self.board[i][j][0] == 1:
                return True
            else:
                return False
        else:
            return False

    def isColored(self,i,j):
        if i >= 0 and j >= 0 and self.width > i and self.height > j:
            if not self.board[i][j][1] == self.windowManager.getGridBackgroundColor():
                return True
            else:
                return False
        else:
            return False
    
    def check(self):
        # Count how many rows should be removed.
        counter = 0
        # Index of first row which should be removed.
        index = -1
        for j in range(self.height):
            # Flag to check whether the row is full.
            full = True
            for	i in range(self.width):
                if self.board[i][self.height - j - 1][0] == 0:
                    full = False
            # If the row is full, remove it.
            if full == True:
                if index < 0:
                    index = j
                for i in range(self.width):
                    # Free the square and change it color to be black.
                    self.board[i][self.height - j - 1] = [0,self.windowManager.getGridBackgroundColor()]
                    # Paint it black.
                    self.paint(i, self.height - j - 1, self.windowManager.getGridBackgroundColor())
                # Increase the counter for the number of removed rows.
                counter += 1

        # Move the squares down for every row removed.
        for c in range(0, counter):
            for j in range(index, self.height - 1):
                for i in range(self.width):
                    square = self.board[i][self.height - j - 2]
                    # Move the square down
                    self.board[i][self.height - j - 1] = square
                    # Paint the square
                    self.paint(i, self.height - j - 1, square[1])
                    self.paint(i, self.height - j - 1, pygame.Color(0,0,0),1)

        # Inform the game manager as to how many rows were removed.
        return counter