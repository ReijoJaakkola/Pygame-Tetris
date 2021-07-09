import pygame
from pygame.locals import *

from pygame_enums import Color, Shape

class PreviewPieceManager:
    def __init__(self, windowManager):
        self.windowManager = windowManager

    def drawBackground(self):
        self.windowManager.redrawPreviewBoardBackground()

    def drawSquare(self, i, j, color):
        self.windowManager.drawSquareToPreviewBoardBackGround(i,j,color)
        self.windowManager.drawSquareToPreviewBoardBackGround(i,j,pygame.Color(0,0,0),1)

    def drawPiece(self, color, shape):
        self.drawBackground()

        if shape == Shape.SQUARE:
            self.drawSquare(2,2,color)
            self.drawSquare(2,3,color)
            self.drawSquare(3,2,color)
            self.drawSquare(3,3,color)
        elif shape == Shape.PIPE:
            self.drawSquare(2,1,color)
            self.drawSquare(2,2,color)
            self.drawSquare(2,3,color)
            self.drawSquare(2,4,color)
        elif shape == Shape.FIVE:
            self.drawSquare(1,2,color)
            self.drawSquare(2,2,color)
            self.drawSquare(2,3,color)
            self.drawSquare(3,3,color)
        elif shape == Shape.L:
            self.drawSquare(1,3,color)
            self.drawSquare(2,3,color)
            self.drawSquare(3,3,color)
            self.drawSquare(3,2,color)
        elif shape == Shape.MIDDLE:
            self.drawSquare(2,2,color)
            self.drawSquare(1,3,color)
            self.drawSquare(2,3,color)
            self.drawSquare(3,3,color)