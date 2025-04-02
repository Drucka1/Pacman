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
    
class Alpha_Beta_Leaf():
    def __init__(self, game):
        self.game = game
        
    def get_pacman_leaf(self):
        leafs = []
        for direction in self.game.get_valid_direction(self.game.pacman.position):
            new_leaf = copy.deepcopy(self)
            new_leaf.game.pacman.position += direction.value
            new_leaf.game.pacman.direction = direction
            new_leaf.game.eat(new_leaf.game.pacman.position)
            new_leaf.game.update()
            leafs.append(new_leaf)
        return leafs

    def get_ghosts_leaf(self):
        leafs = []
        for direction_0 in self.game.get_valid_direction(self.game.ghosts[0].position):
            for direction_1 in self.game.get_valid_direction(self.game.ghosts[1].position):
                for direction_2 in self.game.get_valid_direction(self.game.ghosts[2].position):
                    for direction_3 in self.game.get_valid_direction(self.game.ghosts[3].position):
                        new_leaf = copy.deepcopy(self)
                        new_leaf.game.ghosts[0].position += direction_0.value
                        new_leaf.game.ghosts[0].direction = direction_0
                        new_leaf.game.ghosts[1].position += direction_1.value
                        new_leaf.game.ghosts[1].direction = direction_1
                        new_leaf.game.ghosts[2].position += direction_2.value
                        new_leaf.game.ghosts[2].direction = direction_2
                        new_leaf.game.ghosts[3].position += direction_3.value
                        new_leaf.game.ghosts[3].direction = direction_3
                        new_leaf.game.update()
                        leafs.append(new_leaf)
            
        return leafs

def alpha_beta(node, depth, alpha, beta, maximizing_player):
    if depth == 0 or node.game.is_game_over():
        return node.game.evaluate(), Direction.STOP

    if maximizing_player:
        max_eval = float('-inf')
        best_direction = Direction.STOP
        for child in node.get_pacman_leaf():
            eval, _ = alpha_beta(child, depth - 1, alpha, beta, False)
            if eval > max_eval:
                max_eval = eval
                best_direction = child.game.pacman.direction
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_direction
    else:
        min_eval = float('inf')
        for child in node.get_ghosts_leaf():
            eval, _ = alpha_beta(child, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, Direction.STOP
