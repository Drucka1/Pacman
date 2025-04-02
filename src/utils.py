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
    
class Heuristique():
    def evaluate(self, game): 
        pass
    
class Simple_Heuristique():
    def evaluate(self, game):
        ghost_distances = [
            abs(game.pacman.position.x - ghost.position.x) + abs(game.pacman.position.y - ghost.position.y)
            for ghost in game.ghosts
        ]
        min_distance = min(ghost_distances)

        # Pénalité si un fantôme est trop proche
        danger_penalty = -100 if min_distance <= 1 else 0

        # Bonus pour les grosses boules (boosts)
        boost_positions = [
            (y, x) for y, row in enumerate(game.layout) for x, cell in enumerate(row) if cell == 2
        ]
        boost_distances = [
            abs(game.pacman.position.x - boost[1]) + abs(game.pacman.position.y - boost[0])
            for boost in boost_positions
        ]
        closest_boost_distance = min(boost_distances) if boost_distances else float('inf')
        boost_bonus = 50 if closest_boost_distance < 5 else 0

        # Compter les boules restantes
        remaining_pellets = sum(row.count(1) for row in game.layout)

        scatter_bonus = 1000
        pellet_search_bonus = sum(
            max(0, 20 - (abs(game.pacman.position.x - x) + abs(game.pacman.position.y - y)))
            for y, row in enumerate(game.layout)
            for x, cell in enumerate(row) if cell == 1
        )  # Encourage Pacman to explore for pellets, with higher bonus for closer pellets

        # Calculate the barycenter of remaining pellets if there are less than 30
        remaining_pellet_positions = [
            (y, x) for y, row in enumerate(game.layout) for x, cell in enumerate(row) if cell == 1
        ]
        if len(remaining_pellet_positions) < 30 and remaining_pellet_positions:
            barycenter_x = sum(pos[1] for pos in remaining_pellet_positions) / len(remaining_pellet_positions)
            barycenter_y = sum(pos[0] for pos in remaining_pellet_positions) / len(remaining_pellet_positions)
            barycenter_distance = abs(game.pacman.position.x - barycenter_x) + abs(game.pacman.position.y - barycenter_y)
        else:
            barycenter_distance = 0

        # Bonus pour être loin des fantômes en mode scatter
        if game.scatter_mode:
            return (
            game.score
            + scatter_bonus
            + pellet_search_bonus
            + closest_boost_distance
            - 10 * remaining_pellets
            + danger_penalty
            - 5 * barycenter_distance
            )

        # Heuristique combinée
        return (
            game.score
            + boost_bonus
            + 5 * min_distance
            - 10 * remaining_pellets
            + danger_penalty
        )
    
class Alpha_Beta():
    def __init__(self, heuristique) :
        self.heuristique = heuristique

    def run(self, node, depth, alpha, beta, maximizing_player):
        if depth == 0 or node.game.is_game_over():
            return self.heuristique.evaluate(node.game), Direction.STOP

        if maximizing_player:
            max_eval = float('-inf')
            best_direction = Direction.STOP
            for child in node.get_pacman_leaf():
                eval, _ = self.run(child, depth - 1, alpha, beta, False)
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
                eval, _ = self.run(child, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, Direction.STOP
