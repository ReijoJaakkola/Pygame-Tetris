from enum import Enum

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