import pygame
import sys
import time
import os
import random
import queue
from enum import Enum
from pygame.locals import *

# WIDTH should be an even number.
WIN_WIDTH = 250
WIN_HEIGHT = 700
# Every square is of size SQUARE_SIZE^2. The code
# assumes that SQUARE_SIZE * 10 = WIN_WIDTH.
SQUARE_SIZE = 25
# Background color for the window
BACKGROUND_COLOR = pygame.Color(0,0,0)

# Window where the game takes place.
WINDOW = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

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

	# For testing
	# TODO: DELETE
	def print(self):
		for j in range(self.height):
			for i in range(self.width):
				print(self.board[i][j][0], end = "")
			print()
		print()

	def paint(self,i,j,color,linewidth = 0):
		pygame.draw.rect(WINDOW, color, (i*SQUARE_SIZE, j*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), linewidth)

	def paintSquare(self,i,j,color):
		if i >= 0 and j >= 0 and self.width > i and self.height > j:
			self.board[i][j][1] = color
			self.paint(i,j,color)
			self.paint(i,j,pygame.Color(0,0,0),1)

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
	# Whether the current piece is new i.e. it has not been moved previously.
	NEW = True
	# Difference in x-coordinate with respect to the original one.
	X_COORD_DIFF = 0
	# Difference in y-coordinate with respect to the original one.
	Y_COORD_DIFF = 0
	# Current shape of the piece.
	SHAPE = Shape.SQUARE
	# List for the possible rotations of the piece.
	PIECES = []
	# Index for the next rotation.
	NEXT_PIECE = 1
	# List of squares which constitute the piece.
	PIECE = []

	def __init__(self):
		self.GAME_OVER = False
		
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

	
	def moveSquare(self,square,direction):
		if direction == Direction.RIGHT:
			GRID.paintSquare(square.i,square.j,BACKGROUND_COLOR)
			square.i += 1
			GRID.paintSquare(square.i,square.j,square.color)
		elif direction == Direction.LEFT:
			GRID.paintSquare(square.i,square.j,BACKGROUND_COLOR)
			square.i -= 1
			GRID.paintSquare(square.i,square.j,square.color)
		elif direction == Direction.DOWN:
			GRID.paintSquare(square.i,square.j,BACKGROUND_COLOR)
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
			for square in self.PIECE:
				self.moveSquare(square, Direction.RIGHT)
			self.X_COORD_DIFF += 1

	
	def movePieceLeft(self):
		okToMove = True
		for square in self.PIECE:
			if GRID.isReserved(square.i - 1,square.j) == True:
				okToMove = False
			elif square.i - 1 < 0:
				okToMove = False
		if okToMove == True:
			for square in self.PIECE:
				self.moveSquare(square, Direction.LEFT)
			self.X_COORD_DIFF -= 1

	
	def movePieceDown(self):
		okToMove = True
		for square in self.PIECE:
			if GRID.isReserved(square.i, square.j + 1) == True:
				okToMove = False
			elif square.j + 1 >= GRID.height:
				okToMove = False
		if okToMove == True:
			for square in self.PIECE:
				self.moveSquare(square, Direction.DOWN)
			self.NEW = False
			self.Y_COORD_DIFF += 1
		else:
			if self.NEW == True:
				self.GAME_OVER = True
			else:
				for square in self.PIECE:
					GRID.reserve(square.i, square.j, square.color)
				GRID.check()
				self.newPiece()
				return True
		return False

	
	def move(self,direction):
		if direction == Direction.RIGHT:
			self.movePieceRight()
		elif direction == Direction.LEFT:
			self.movePieceLeft()
		elif direction == Direction.DOWN:
			self.movePieceDown()

	def pushDown(self):
			done = False
			while done == False:
				done = self.movePieceDown()


	def rotate(self):
		# Pic the next piece in the cycle.
		ROTATION = self.PIECES[self.NEXT_PIECE]
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
			self.NEXT_PIECE = (self.NEXT_PIECE  + 1) % 4


GAME_MANAGER = GameManager()


def main():
	WINDOW.fill(BACKGROUND_COLOR)
	clock = pygame.time.Clock()
	piece = GAME_MANAGER.newPiece()

	while GAME_MANAGER.GAME_OVER == False:
		clock.tick(7)

		# Go through the events
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN:
				# User pressed key button. Move the current piece according
				# to the key pressed.
				if event.key == K_LEFT:
					GAME_MANAGER.move(Direction.LEFT)
				elif event.key == K_RIGHT:
					GAME_MANAGER.move(Direction.RIGHT)
				# User pressed down key --> move the current peace to bottom.
				elif event.key == K_DOWN:
					GAME_MANAGER.pushDown()
				# Rotate the piece clockwise if user pressed spacebar.
				elif event.key == K_SPACE:
					GAME_MANAGER.rotate()

		# Move always the piece down.
		GAME_MANAGER.move(Direction.DOWN)

		# Update the window
		pygame.display.update()

	# Game has ended, close the window.	
	pygame.quit()
	sys.exit()

# Start the game.
main()