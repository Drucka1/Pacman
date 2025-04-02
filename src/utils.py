import copy
from enum import Enum

class Pacman:
    def __init__(self):
        self.position = Coordinate(14,23)  # Starting position
        self.direction = Direction.STOP

class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        if isinstance(other, Coordinate):
            return Coordinate(self.x + other.x, self.y + other.y)
        raise TypeError("Can only add Coordinate to Coordinate")

    def __sub__(self, other):
        if isinstance(other, Coordinate):
            return Coordinate(self.x - other.x, self.y - other.y)
        raise TypeError("Can only subtract Coordinate from Coordinate")
    
    def __eq__(self, other):
        if isinstance(other, Coordinate):
            return self.x == other.x and self.y == other.y
        return False

    def __mul__(self, scalar):
        if isinstance(scalar, (int, float)):
            return Coordinate(self.x * scalar, self.y * scalar)
        raise TypeError("Can only multiply Coordinate by a scalar")

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __repr__(self):
        return f"Coordinate({self.x}, {self.y})"
    
    def distance(self,position):
        return abs(self.x- position.x) + abs(self.y- position.y)

class Direction(Enum):
    UP = Coordinate(0, -1)
    DOWN = Coordinate(0, 1)
    LEFT = Coordinate(-1, 0)
    RIGHT = Coordinate(1, 0)
    STOP = Coordinate(0, 0)

 

    

