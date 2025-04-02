from utils import Direction
import copy

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

    #def get_ghosts_leaf(self):
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
    
    def get_ghosts_leaf(self):
        new_leaf = copy.deepcopy(self)
        new_leaf.game.move_ghost()
        return [new_leaf]

class Alpha_Beta():
    def __init__(self, heuristique) :
        self.heuristique = heuristique

    def run(self, node, depth, alpha, beta, maximizing_player):
        if depth == 0 or node.game.isOver():
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