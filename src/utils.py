import copy
from enum import Enum

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
    
class Alpha_Beta_Leaf():
    def __init__(self, maze, pacman, inky, blinky, pinky, clyde):
        self.maze = maze
        self.pacman = pacman
        self.inky = inky
        self.blinky = blinky
        self.pinky = pinky
        self.clyde = clyde
        
    def get_pacman_leaf(self):
        leafs = []
        for direction in self.maze.get_valid_direction(self.pacman.position):
            new_leaf = copy.deepcopy(self)
            new_leaf.pacman.position += direction.value
            new_leaf.maze.eat(new_leaf.pacman.position)
            new_leaf.maze.update()
            leafs.append(new_leaf)
        return leafs

    def get_ghosts_leaf(self):
        leafs = []
        for inky_direction in self.maze.get_valid_direction(self.inky.position):
            for blinky_direction in self.maze.get_valid_direction(self.blinky.position):
                for pinky_direction in self.maze.get_valid_direction(self.pinky.position):
                    for clyde_direction in self.maze.get_valid_direction(self.clyde.position):
                        new_leaf = copy.deepcopy(self)
                        new_leaf.clyde.position += clyde_direction.value
                        new_leaf.pinky.position += pinky_direction.value
                        new_leaf.blinky.position += blinky_direction.value
                        new_leaf.inky.position += inky_direction.value
                        new_leaf.maze.update()
                        leafs.append(new_leaf)
        return leafs

def alpha_beta(node, depth, alpha, beta, maximizing_player):
    if depth == 0 or node.maze.is_game_over():
        return node.maze.evaluate()

    if maximizing_player:
        max_eval = float('-inf')
        for child in node.get_pacman_leaf():
            eval = alpha_beta(child, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for child in node.get_ghosts_leaf():
            eval = alpha_beta(child, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval
