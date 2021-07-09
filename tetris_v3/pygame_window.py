import pygame
from pygame.locals import *

class WindowManager:
    def __init__(self,
                 width,
                 height,
                 backgroundColor,
                 gridWidth,
                 gridHeight,
                 gridBackgroundColor,
                 squareSize,
                 previewBoardLeft,
                 previewBoardTop,
                 previewBoardWidth,
                 previewBoardHeight,
                 previewBoardColor):

        self.width = width
        self.height = height

        self.gridWidth = gridWidth
        self.gridHeight = gridHeight
        self.gridBackgroundColor = gridBackgroundColor
        self.squareSize = squareSize

        self.previewBoardLeft = previewBoardLeft
        self.previewBoardTop = previewBoardTop
        self.previewBoardWidth = previewBoardWidth
        self.previewBoardHeight = previewBoardHeight
        self.previewBoardColor = previewBoardColor

        self.window = pygame.display.set_mode((width, height))
        self.window.fill(backgroundColor)

        pygame.draw.rect(self.window, gridBackgroundColor, (0, 0, gridWidth, gridHeight), 0)

        self.redrawPreviewBoardBackground()

    def getGridWidth(self):
        return self.gridWidth

    def getGridHeight(self):
        return self.gridHeight
    
    def getGridBackgroundColor(self):
        return self.gridBackgroundColor

    def getSquareSize(self):
        return self.squareSize

    def update(self):
        pygame.display.update()

    def drawSquareToGrid(self,i,j,color,linewidth = 0):
        pygame.draw.rect(self.window, color, (i*self.squareSize, j*self.squareSize, self.squareSize, self.squareSize), linewidth)

    def redrawPreviewBoardBackground(self):
        pygame.draw.rect(self.window, self.previewBoardColor, (self.previewBoardLeft, self.previewBoardTop, self.previewBoardWidth, self.previewBoardHeight), 0)

    def drawSquareToPreviewBoardBackGround(self,i,j,color,linewidth = 0):
        left = i * self.squareSize + self.previewBoardLeft
        top = j * self.squareSize + self.previewBoardTop
        pygame.draw.rect(self.window, color, (left, top, self.squareSize, self.squareSize), linewidth)