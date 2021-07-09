import sys
import pygame

from pygame_window import WindowManager
from pygame_tetris import startGame

WIN_WIDTH = 500
WIN_HEIGHT = 650
BACKGROUND_COLOR = pygame.Color(0,0,102)

GRID_WIDTH = 250
GRID_HEIGHT = 650
GRID_BACKGROUND_COLOR = pygame.Color(0,0,0)
SQUARE_SIZE = GRID_WIDTH // 10

PREVIEW_BOARD_LEFT = 310
PREVIEW_BOARD_TOP = 50
PREVIEW_BOARD_WIDTH = 125
PREVIEW_BOARD_HEIGHT = 150
PREVIEW_BOARD_COLOR = pygame.Color(0,0,0)

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption('Tetris')
    windowManager = WindowManager(WIN_WIDTH,
                                  WIN_HEIGHT,
                                  BACKGROUND_COLOR,
                                  GRID_WIDTH,
                                  GRID_HEIGHT,
                                  GRID_BACKGROUND_COLOR,
                                  SQUARE_SIZE,
                                  PREVIEW_BOARD_LEFT,
                                  PREVIEW_BOARD_TOP,
                                  PREVIEW_BOARD_WIDTH,
                                  PREVIEW_BOARD_HEIGHT,
                                  PREVIEW_BOARD_COLOR)
    startGame(windowManager)
    pygame.quit()
    sys.exit()