import sys
import random

import pygame
from pygame.locals import *

from pygame_enums import Direction, Color, Shape
from pygame_gameboard import GameBoard
from pygame_preview import PreviewPieceManager

# How many milliseconds one tick is.
TICK = 25
# How many ticks does the game wait until it moves the current piece down.
TICKS = 10

# Mp3 file containing the music.
SONG = 'OmaKappale18.mp3'

# Square class just for storing the location
# of a square in the game board and its color.
class Square:
    def __init__(self,i,j,color):
        self.i = i
        self.j = j
        self.color = color

# GameManager class contains information of whether
# the game has ended and what squares contain part of the piece that the player is moving.
# GameManager is also responsible for generating new pieces
# for the player to move and actually moving them.
class GameManager:
    # Whether the game manager is playing the background song or not.
    SONG = True
    # Whether the current piece is new i.e. it has not been moved previously.
    NEW = True

    # Difference in x-coordinate with respect to the original one.
    X_COORD_DIFF = 0
    # Difference in y-coordinate with respect to the original one.
    Y_COORD_DIFF = 0

    # List of squares which constitute the piece.
    PIECE = []
    # List for the possible rotations of the piece.
    PIECES = []
    
    # Color of the next piece
    NEXT_COLOR = Color.GREEN
    # Shape of the next piece
    NEXT_SHAPE = Shape.SQUARE
    # List of squares which constitute the next piece.
    NEXT_PIECE = []
    # List for the possible rotations of the next piece.
    NEXT_PIECES = []
    
    # List of squares which constitute a preview image of piece,
    # which is used to demonstrate where the piece will be landing.
    PREVIEW_PIECE = []
    # Index for the next rotation.
    NEXT_ROTATION = 1
    # Current score.
    SCORE = 0

    def __init__(self, gameBoard, gamePreview):
        self.gameBoard = gameBoard
        self.gamePreview = gamePreview
        self.GAME_OVER = False

        # Start playing the song.
        pygame.mixer.music.load(SONG)
        pygame.mixer.music.play(-1)

        self.NEXT_PIECE, self.NEXT_PIECES = self.generatePiece()
        self.newPiece()
        
    def musicOnOff(self):
        if self.SONG:
            self.SONG = False
            pygame.mixer.music.pause()
        else:
            self.SONG = True
            pygame.mixer.music.unpause()

    def updatePreviewPiece(self):
        for square in self.PREVIEW_PIECE:
            if not self.gameBoard.isColored(square.i,square.j):
                self.gameBoard.paintSquare(square.i,square.j)

        self.PREVIEW_PIECE = []
        for square in self.PIECE:
            self.PREVIEW_PIECE.append(Square(square.i,square.j,square.color))

        down = 0
        done = False
        while not done:
            moveAllowed = True
            for square in self.PREVIEW_PIECE:
                if self.gameBoard.isReserved(square.i, square.j + down + 1) or (square.j + down + 1) >= self.gameBoard.height:
                    moveAllowed = False
            if not moveAllowed:
                done = True
            else:
                down += 1

        for square in self.PREVIEW_PIECE:
            square.j = square.j + down
            if not self.gameBoard.isColored(square.i,square.j):
                self.gameBoard.paintPreviewSquare(square.i,square.j,square.color)		

    def generatePiece(self):
        # Pick a random color
        color = pygame.Color(0,0,0)
        colorIndex = random.choice(list(Color))
        if colorIndex == Color.GREEN:
            color = pygame.Color(0,255,0)
        elif colorIndex == Color.RED:
            color = pygame.Color(255,0,0)
        elif colorIndex == Color.BLUE:
            color = pygame.Color(0,0,255)
        elif colorIndex == Color.YELLOW:
            color = pygame.Color(255,255,0)
        elif colorIndex == Color.VIOLET:
            color = pygame.Color(75,0,130)

        # Pick a random shape
        shape = random.choice(list(Shape))
        if shape == Shape.SQUARE:
            piece = [Square(4,0,color),Square(5,0,color),Square(4,-1,color),Square(5,-1,color)]
            pieces = []
            for i in range(4):
                pieces.append([Square(4,0,color),Square(5,0,color),Square(4,-1,color),Square(5,-1,color)])

        elif shape == Shape.PIPE:
            piece = [Square(5,0,color),Square(5,-1,color),Square(5,-2,color),Square(5,-3,color)]
            pieces = []
            pieces.append([Square(5,0,color),Square(5,-1,color),Square(5,-2,color),Square(5,-3,color)])
            pieces.append([Square(4,-2,color),Square(5,-2,color),Square(6,-2,color),Square(7,-2,color)])
            pieces.append([Square(4,0,color),Square(4,-1,color),Square(4,-2,color),Square(4,-3,color)])
            pieces.append([Square(3,-2,color),Square(4,-2,color),Square(5,-2,color),Square(6,-2,color)])

        elif shape == Shape.FIVE:
            piece = [Square(4,0,color),Square(4,-1,color),Square(5,-1,color),Square(5,-2,color)]
            pieces = []
            pieces.append([Square(4,0,color),Square(4,-1,color),Square(5,-1,color),Square(5,-2,color)])
            pieces.append([Square(6,0,color), Square(7,0,color), Square(5,-1,color), Square(6,-1,color)])
            pieces.append([Square(5,2,color), Square(5,1,color), Square(6,1,color), Square(6,0,color)])
            pieces.append([Square(4,1,color), Square(5,1,color), Square(3,0,color), Square(4,0,color)])

        elif shape == Shape.L:
            piece = [Square(4,0,color), Square(5,0,color), Square(5,-1,color), Square(5,-2,color)]
            pieces = []
            pieces.append([Square(4,0,color), Square(5,0,color), Square(5,-1,color), Square(5,-2,color)])
            pieces.append([Square(5,0,color), Square(6,0,color), Square(7,0,color), Square(5,-1,color)])
            pieces.append([Square(5,2,color), Square(5,1,color), Square(5,0,color), Square(6,0,color)])
            pieces.append([Square(5,1,color), Square(5,0,color), Square(4,0,color), Square(3,0,color)])

        elif shape == Shape.MIDDLE:
            piece = [Square(4,0,color),Square(5,0,color),Square(6,0,color),Square(5,-1,color)]
            pieces = []
            pieces.append([Square(4,0,color),Square(5,0,color),Square(6,0,color),Square(5,-1,color)])
            pieces.append([Square(5,1,color),Square(5,0,color),Square(6,0,color),Square(5,-1,color)])
            pieces.append([Square(5,1,color),Square(4,0,color),Square(5,0,color),Square(6,0,color)])
            pieces.append([Square(5,1,color),Square(4,0,color),Square(5,0,color),Square(5,-1,color)])

        # TODO: This side-effect should be somewhere else...
        self.NEXT_COLOR = color
        self.NEXT_SHAPE = shape
        return piece, pieces

    def newPiece(self):
        self.NEW = True
        self.X_COORD_DIFF = 0
        self.Y_COORD_DIFF = 0
        self.NEXT_ROTATION = 1

        self.PIECE, self.PIECES = self.NEXT_PIECE, self.NEXT_PIECES
        self.NEXT_PIECE, self.NEXT_PIECES = self.generatePiece()

        self.updatePreviewPiece()
        self.gamePreview.drawPiece(self.NEXT_COLOR, self.NEXT_SHAPE)
    
    def updateScore(self, rows):
        # Player will gain 100 points for each row removed.
        self.SCORE += rows * 100

    def movePiece(self,direction):
        for square in self.PIECE:
            self.gameBoard.paintSquare(square.i,square.j)

        if direction == Direction.RIGHT:
            for square in self.PIECE:
                square.i += 1
                self.gameBoard.paintSquare(square.i,square.j,square.color)
        elif direction == Direction.LEFT:
            for square in self.PIECE:
                square.i -= 1
                self.gameBoard.paintSquare(square.i,square.j,square.color)
        elif direction == Direction.DOWN:
            for square in self.PIECE:
                square.j += 1
                self.gameBoard.paintSquare(square.i,square.j,square.color)

    def movePieceRight(self):
        okToMove = True
        for square in self.PIECE:
            if self.gameBoard.isReserved(square.i + 1, square.j) == True:
                okToMove = False
            elif square.i + 1 >= self.gameBoard.width:
                okToMove = False
        if okToMove == True:
            self.movePiece(Direction.RIGHT)
            self.updatePreviewPiece()
            self.X_COORD_DIFF += 1

    def movePieceLeft(self):
        okToMove = True
        for square in self.PIECE:
            if self.gameBoard.isReserved(square.i - 1,square.j) == True:
                okToMove = False
            elif square.i - 1 < 0:
                okToMove = False
        if okToMove == True:
            self.movePiece(Direction.LEFT)
            self.updatePreviewPiece()
            self.X_COORD_DIFF -= 1

    def movePieceDown(self):
        okToMove = True
        for square in self.PIECE:
            if self.gameBoard.isReserved(square.i, square.j + 1) == True:
                okToMove = False
            elif square.j + 1 >= self.gameBoard.height:
                okToMove = False
        if okToMove == True:
            self.movePiece(Direction.DOWN)
            self.NEW = False
            self.Y_COORD_DIFF += 1
        else:
            if self.NEW == True:
                self.GAME_OVER = True
            else:
                for square in self.PIECE:
                    self.gameBoard.reserve(square.i, square.j, square.color)
                # Remove all of the full rows...
                numRowsRemoved = self.gameBoard.check()
                # ... and update the current score based on how many rows were removed.
                self.updateScore(numRowsRemoved)
                self.newPiece()
                return True
        return False

    def pushDown(self):
            done = False
            while done == False:
                done = self.movePieceDown()
                pygame.time.wait(TICK)
                pygame.display.update()

    def rotate(self):
        # Pic the next piece in the cycle.
        ROTATION = []
        for square in self.PIECES[self.NEXT_ROTATION]:
            ROTATION.append(Square(square.i,square.j,square.color))

        # The pieces are stored in their original
        # coordinates, so we have to first move them
        # according to how the active piece has moved.
        for square in ROTATION:
            square.i += self.X_COORD_DIFF
            square.j += self.Y_COORD_DIFF

        # Check would we hit boundaries or other pieces.
        okToRotate = True
        for square in ROTATION:
            if self.gameBoard.isReserved(square.i, square.j) == True:
                okToRotate = False
            elif square.j >= self.gameBoard.height:
                okToRotate = False
            elif square.i >= self.gameBoard.width:
                okToRotate = False
            elif square.i < 0:
                okToRotate = False

        # Green light.
        if okToRotate == True:
            for square in self.PIECE:
                self.gameBoard.paintSquare(square.i,square.j)
            for square in ROTATION:
                self.gameBoard.paintSquare(square.i,square.j,square.color)
            self.PIECE = ROTATION
            self.updatePreviewPiece()
            self.NEXT_ROTATION = (self.NEXT_ROTATION  + 1) % 4

    def handleNextEvent(self):
        events = pygame.event.get()
        if len(events) == 0:
            return
        event = events[0]
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                self.movePieceLeft()
            elif event.key == K_RIGHT:
                self.movePieceRight()
            elif event.key == K_DOWN:
                self.pushDown()
            elif event.key == K_SPACE:
                self.rotate()
            elif event.key == K_m:
                self.musicOnOff()

def startGame(windowManager):
    ticks = 0
    pygame.time.wait(TICK)

    gameBoard = GameBoard(windowManager)
    gamePreview = PreviewPieceManager(windowManager)
    gameManager = GameManager(gameBoard, gamePreview)

    while gameManager.GAME_OVER == False:
        ticks += 1
        pygame.time.wait(TICK)

        gameManager.handleNextEvent()

        if ticks == TICKS:
            ticks = 0
            gameManager.movePieceDown()

        # Update the window
        windowManager.update()