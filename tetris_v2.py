import pygame
import sys
import time
import os
import random
import queue
from enum import Enum
from pygame.locals import *

pygame.init()

# WIDTH should be an even number.
WIN_WIDTH = 250
WIN_HEIGHT = 650
# Every square is of size SQUARE_SIZE^2. The code
# assumes that SQUARE_SIZE * 10 = WIN_WIDTH.
SQUARE_SIZE = 25
# Background color for the window
BACKGROUND_COLOR = pygame.Color(0,0,0)

# How many milliseconds one tick is.
TICK = 25
# How many ticks does the game wait until it moves the current piece down.
TICKS = 10

# Window where the game takes place.
WINDOW = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

# Mp3 file containing the music.
SONG = 'OmaKappale18.mp3'

# Grid contains the information of which squares are currently
# being used and what is the color of every square. Grid is also
# responsible for actually drawing the pictures, although
# GameManager will make the requests mostly.
# 
# For every square in the board grid contains value 0 or 1.
# If the value of square is 0, then the square is free. If it is
# 1, then it is occupied, which means that it contains part of some
# earlier peace which has already landed.
class Grid:
	def __init__(self):
		self.width = WIN_WIDTH // SQUARE_SIZE
		self.height = WIN_HEIGHT // SQUARE_SIZE
		self.board = []
		
		for i in range(self.width):
			row = []
			for j in range(self.height):
				row.append([0,BACKGROUND_COLOR])
			self.board.append(row)

	def paint(self,i,j,color,linewidth = 0):
		pygame.draw.rect(WINDOW, color, (i*SQUARE_SIZE, j*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), linewidth)

	def paintSquare(self,i,j,color):
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
			self.board[i][j] = [0,BACKGROUND_COLOR]
			self.paint(i,j,BACKGROUND_COLOR)

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
			if not self.board[i][j][1] == BACKGROUND_COLOR:
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
					self.board[i][self.height - j - 1] = [0,BACKGROUND_COLOR]
					# Paint it black.
					self.paint(i, self.height - j - 1, BACKGROUND_COLOR)
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

GRID = Grid()

# Enum for the possible directions for the current piece.
class Direction(Enum):
	RIGHT = 0
	LEFT = 1
	DOWN = 2

# Enum for the possible colors.
class Color(Enum):
	GREEN = 0
	RED = 1
	BLUE = 2 
	YELLOW = 3
	VIOLET = 4

# Enum for the possible shapes for the current piece.
class Shape(Enum):
	SQUARE = 0
	PIPE = 1
	FIVE = 2
	L = 3
	MIDDLE = 4

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
	# Current shape of the piece.
	SHAPE = Shape.SQUARE
	# List of squares which constitute the piece.
	PIECE = []
	# List for the possible rotations of the piece.
	PIECES = []
	# List of squares which constitute a preview image of piece,
	# which is used to demonstrate where the piece will be landing.
	PREVIEW_PIECE = []
	# Index for the next rotation.
	NEXT_PIECE = 1
	# Current score.
	SCORE = 0

	def __init__(self):
		self.GAME_OVER = False

		# Start playing the song.
		pygame.mixer.music.load('OmaKappale18.mp3')
		pygame.mixer.music.play(-1)
		
	def musicOnOff(self):
		if self.SONG:
			self.SONG = False
			pygame.mixer.music.pause()
		else:
			self.SONG = True
			pygame.mixer.music.unpause()

	def updatePreviewPiece(self):
		for square in self.PREVIEW_PIECE:
			if not GRID.isColored(square.i,square.j):
				GRID.paintSquare(square.i,square.j,BACKGROUND_COLOR)

		self.PREVIEW_PIECE = []
		for square in self.PIECE:
			self.PREVIEW_PIECE.append(Square(square.i,square.j,square.color))

		down = 0
		done = False
		while not done:
			moveAllowed = True
			for square in self.PREVIEW_PIECE:
				if GRID.isReserved(square.i, square.j + down + 1) or (square.j + down + 1) >= GRID.height:
					moveAllowed = False
			if not moveAllowed:
				done = True
			else:
				down += 1

		for square in self.PREVIEW_PIECE:
			square.j = square.j + down
			if not GRID.isColored(square.i,square.j):
				GRID.paintPreviewSquare(square.i,square.j,square.color)		

	def newPiece(self):
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
			self.NEW = True
			self.X_COORD_DIFF = 0
			self.Y_COORD_DIFF = 0
			self.NEXT_PIECE = 1
			self.PIECE = [Square(4,0,color),Square(5,0,color),Square(4,-1,color),Square(5,-1,color)]
			self.PIECES = []
			for i in range(4):
				self.PIECES.append([Square(4,0,color),Square(5,0,color),Square(4,-1,color),Square(5,-1,color)])

		elif shape == Shape.PIPE:
			self.NEW = True
			self.X_COORD_DIFF = 0
			self.Y_COORD_DIFF = 0
			self.NEXT_PIECE = 1
			self.PIECE = [Square(5,0,color),Square(5,-1,color),Square(5,-2,color),Square(5,-3,color)]
			self.PIECES = []
			self.PIECES.append([Square(5,0,color),Square(5,-1,color),Square(5,-2,color),Square(5,-3,color)])
			self.PIECES.append([Square(4,-2,color),Square(5,-2,color),Square(6,-2,color),Square(7,-2,color)])
			self.PIECES.append([Square(4,0,color),Square(4,-1,color),Square(4,-2,color),Square(4,-3,color)])
			self.PIECES.append([Square(3,-2,color),Square(4,-2,color),Square(5,-2,color),Square(6,-2,color)])

		elif shape == Shape.FIVE:
			self.NEW = True
			self.X_COORD_DIFF = 0
			self.Y_COORD_DIFF = 0
			self.NEXT_PIECE = 1
			self.PIECE = [Square(4,0,color),Square(4,-1,color),Square(5,-1,color),Square(5,-2,color)]
			self.PIECES = []
			self.PIECES.append([Square(4,0,color),Square(4,-1,color),Square(5,-1,color),Square(5,-2,color)])
			self.PIECES.append([Square(6,0,color), Square(7,0,color), Square(5,-1,color), Square(6,-1,color)])
			self.PIECES.append([Square(5,2,color), Square(5,1,color), Square(6,1,color), Square(6,0,color)])
			self.PIECES.append([Square(4,1,color), Square(5,1,color), Square(3,0,color), Square(4,0,color)])

		elif shape == Shape.L:
			self.NEW = True
			self.X_COORD_DIFF = 0
			self.Y_COORD_DIFF = 0
			self.NEXT_PIECE = 1
			self.PIECE = [Square(4,0,color), Square(5,0,color), Square(5,-1,color), Square(5,-2,color)]
			self.PIECES = []
			self.PIECES.append([Square(4,0,color), Square(5,0,color), Square(5,-1,color), Square(5,-2,color)])
			self.PIECES.append([Square(5,0,color), Square(6,0,color), Square(7,0,color), Square(5,-1,color)])
			self.PIECES.append([Square(5,2,color), Square(5,1,color), Square(5,0,color), Square(6,0,color)])
			self.PIECES.append([Square(5,1,color), Square(5,0,color), Square(4,0,color), Square(3,0,color)])

		elif shape == Shape.MIDDLE:
			self.NEW = True
			self.X_COORD_DIFF = 0
			self.Y_COORD_DIFF = 0
			self.NEXT_PIECE = 1
			self.PIECE = [Square(4,0,color),Square(5,0,color),Square(6,0,color),Square(5,-1,color)]
			self.PIECES = []
			self.PIECES.append([Square(4,0,color),Square(5,0,color),Square(6,0,color),Square(5,-1,color)])
			self.PIECES.append([Square(5,1,color),Square(5,0,color),Square(6,0,color),Square(5,-1,color)])
			self.PIECES.append([Square(5,1,color),Square(4,0,color),Square(5,0,color),Square(6,0,color)])
			self.PIECES.append([Square(5,1,color),Square(4,0,color),Square(5,0,color),Square(5,-1,color)])

		self.updatePreviewPiece()
	
	def updateScore(self, rows):
		# Player will gain 100 points for each row removed.
		self.SCORE += rows * 100

	def movePiece(self,direction):
		for square in self.PIECE:
			GRID.paintSquare(square.i,square.j,BACKGROUND_COLOR)

		if direction == Direction.RIGHT:
			for square in self.PIECE:
				square.i += 1
				GRID.paintSquare(square.i,square.j,square.color)
		elif direction == Direction.LEFT:
			for square in self.PIECE:
				square.i -= 1
				GRID.paintSquare(square.i,square.j,square.color)
		elif direction == Direction.DOWN:
			for square in self.PIECE:
				square.j += 1
				GRID.paintSquare(square.i,square.j,square.color)

	def movePieceRight(self):
		okToMove = True
		for square in self.PIECE:
			if GRID.isReserved(square.i + 1, square.j) == True:
				okToMove = False
			elif square.i + 1 >= GRID.width:
				okToMove = False
		if okToMove == True:
			self.movePiece(Direction.RIGHT)
			self.updatePreviewPiece()
			self.X_COORD_DIFF += 1

	def movePieceLeft(self):
		okToMove = True
		for square in self.PIECE:
			if GRID.isReserved(square.i - 1,square.j) == True:
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
			if GRID.isReserved(square.i, square.j + 1) == True:
				okToMove = False
			elif square.j + 1 >= GRID.height:
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
					GRID.reserve(square.i, square.j, square.color)
				# Remove all of the full rows...
				numRowsRemoved = GRID.check()
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
		for square in self.PIECES[self.NEXT_PIECE]:
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
			if GRID.isReserved(square.i, square.j) == True:
				okToRotate = False
			elif square.j >= GRID.height:
				okToRotate = False
			elif square.i >= GRID.width:
				okToRotate = False
			elif square.i < 0:
				okToRotate = False

		# Green light.
		if okToRotate == True:
			for square in self.PIECE:
				GRID.paintSquare(square.i,square.j,BACKGROUND_COLOR)
			for square in ROTATION:
				GRID.paintSquare(square.i,square.j,square.color)
			self.PIECE = ROTATION
			self.updatePreviewPiece()
			self.NEXT_PIECE = (self.NEXT_PIECE  + 1) % 4

GAME_MANAGER = GameManager()

def main():
	pygame.display.set_caption('Tetris')
	WINDOW.fill(BACKGROUND_COLOR)
	
	ticks = 0
	pygame.time.wait(TICK)

	GAME_MANAGER.newPiece()
	while GAME_MANAGER.GAME_OVER == False:
		ticks += 1
		pygame.time.wait(TICK)

		# Go through the events
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN:
				# User pressed key button. Move the current piece according
				# to the key pressed.
				if event.key == K_LEFT:
					GAME_MANAGER.movePieceLeft()
				elif event.key == K_RIGHT:
					GAME_MANAGER.movePieceRight()
				# User pressed down key --> move the current peace to bottom.
				elif event.key == K_DOWN:
					GAME_MANAGER.pushDown()
				# Rotate the piece clockwise if user pressed spacebar.
				elif event.key == K_SPACE:
					GAME_MANAGER.rotate()
				# Pause or unpause the song.
				elif event.key == K_m:
					GAME_MANAGER.musicOnOff()

		if ticks == TICKS:
			ticks = 0
			GAME_MANAGER.movePieceDown()

		# Update the window
		pygame.display.update()

	# Game has ended, close the window.	
	pygame.quit()
	sys.exit()

# Start the game.
main()