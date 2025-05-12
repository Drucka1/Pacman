from collections import deque
import heapq
from bitarray import bitarray
from enum import Enum

class Direction(Enum):
    LEFT = (-1,0)
    RIGHT = (1,0)
    UP = (0,-1)
    DOWN = (0,1)
    
    def get_opposite_direction(self):
        if self == Direction.UP: return Direction.DOWN
        if self == Direction.DOWN: return Direction.UP
        if self == Direction.LEFT: return Direction.RIGHT
        if self == Direction.RIGHT: return Direction.LEFT
        return None
    
    @staticmethod
    def toDirection(direction: str):
        try:
            return Direction[direction.upper()]
        except KeyError:
            return None

class Tree():
    initial_pos = {
        'pacman' : (11, 23),
        'inky' : (12, 15),
        'pinky' : (13, 15),
        'blinky' : (14, 15),
        'clyde' : (15, 15)
    }
    board = [   
        bitarray([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
        bitarray([0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]),
        bitarray([0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0]),
        bitarray([0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0]),
        bitarray([0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0]),
        bitarray([0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]),
        bitarray([0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0]),
        bitarray([0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0]),
        bitarray([0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0]),
        bitarray([0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0]),
        bitarray([0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0]),
        bitarray([0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0]),
        bitarray([0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0]),
        bitarray([0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0]),
        bitarray([0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0]),
        bitarray([0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0]),
        bitarray([0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0]),
        bitarray([0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0]),
        bitarray([0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0]),
        bitarray([0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0]),
        bitarray([0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]),
        bitarray([0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0]),
        bitarray([0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0]),
        bitarray([0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0]),
        bitarray([0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0]),
        bitarray([0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0]),
        bitarray([0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0]),
        bitarray([0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]),
        bitarray([0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]),
        bitarray([0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]),
        bitarray([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    ]
    heuristique = None
    initial_depth = None

    def __init__(self,initial_depth, heuristique, pacman_score, pacman_lives_number, pacman_direction, scatter_mode,
                       scatter_chrono, inky_movement_turns, inky_last_choice, pos, pellets, boosts):
        Tree.initial_depth = initial_depth
        Tree.heuristique = heuristique
        self.value = None
        self.pacman_score = pacman_score
        self.pacman_lives_number = pacman_lives_number
        self.pacman_direction = pacman_direction
        self.scatter_mode = scatter_mode
        self.scatter_chrono = scatter_chrono
        self.inky_movement_turns = inky_movement_turns
        self.inky_last_choice = inky_last_choice
        self.pos = pos
        self.pellets = pellets
        self.boosts = boosts
           
    def clone(self):
        return Tree(Tree.initial_depth, Tree.heuristique, self.pacman_score, self.pacman_lives_number, 
                    self.pacman_direction, self.scatter_mode, self.scatter_chrono, self.inky_movement_turns, 
                    self.inky_last_choice, self.pos.copy(), self.pellets.copy(), self.boosts.copy())
    
    @staticmethod
    def _manhattan_distance(pos1, pos2):
        """Computes the Manhattan distance between two points."""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    @staticmethod
    def a_star_function(start, endpoint):
        """
        A* pathfinding algorithm.
        Returns the path as a list of (x, y) tuples, or None if no path is found.
        """
        if start == endpoint:
            return [start]

        open_set = []  # Priority queue: (f_score, g_score, position, path_list)
        # g_score is used as a tie-breaker for f_score to prefer longer paths if f_scores are equal,
        # which can sometimes lead to more 'natural' looking paths, though not strictly necessary for correctness.
        # A simpler (f_score, position, path_list) would also work.
        heapq.heappush(open_set, (Tree._manhattan_distance(start, endpoint), 0, start, [start]))

        # g_scores: cost from start to a node
        g_scores = {start: 0}
        
        # came_from is implicitly handled by storing the full path in the priority queue items

        while open_set:
            f_s, g_s, current_pos, path = heapq.heappop(open_set)

            if current_pos == endpoint:
                return path

            # Explore neighbors
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]: # Down, Up, Right, Left
                neighbor_pos = (current_pos[0] + dx, current_pos[1] + dy)
                
                # Check bounds and walls
                if not (0 <= neighbor_pos[0] < len(Tree.board[0]) and \
                        0 <= neighbor_pos[1] < len(Tree.board) and \
                        Tree.board[neighbor_pos[1]][neighbor_pos[0]] == 1):
                    continue

                tentative_g_score = g_s + 1 # Cost to move to a neighbor is 1

                if tentative_g_score < g_scores.get(neighbor_pos, float('inf')):
                    g_scores[neighbor_pos] = tentative_g_score
                    h_score = Tree._manhattan_distance(neighbor_pos, endpoint)
                    f_score = tentative_g_score + h_score
                    new_path = path + [neighbor_pos]
                    heapq.heappush(open_set, (f_score, tentative_g_score, neighbor_pos, new_path))
        
        return None
    
    @staticmethod
    def get_first_direction_a_star(start, endpoint):
        """
        Gets the first direction of the shortest path from start to endpoint using A*.
        """
        path = Tree.a_star_function(start, endpoint)
        if not path or len(path) < 2:
            return None  # No path or already at the destination

        x0, y0 = path[0]
        x1, y1 = path[1]

        if x1 == x0 + 1 and y1 == y0:
            return Direction.RIGHT
        elif x1 == x0 - 1 and y1 == y0:
            return Direction.LEFT
        elif x1 == x0 and y1 == y0 + 1: # Board y-axis increases downwards
            return Direction.DOWN
        elif x1 == x0 and y1 == y0 - 1: # Board y-axis decreases upwards
            return Direction.UP
        else:
            # Should not happen if path is valid
            return None
       
    def direction_valide(self, pacman_pos, direction):
        x, y = pacman_pos
        dx, dy = direction.value
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(self.board[0]) and 0 <= ny < len(self.board):
            return self.board[ny][nx] == 1
        return False
    
    def update_pacman_move(self, direction):
        x, y = self.pos['pacman']
        dx, dy = direction.value
        nx, ny = x + dx, y + dy

        if 0 <= nx < len(self.board[0]) and 0 <= ny < len(self.board):
            if self.board[ny][nx] != 0:
                self.pos['pacman'] = (nx, ny)
                if (nx, ny) in self.pellets:
                    self.pacman_score += 10
                    self.pellets.remove((nx, ny))
                if (nx, ny) in self.boosts:
                    self.pacman_score += 500
                    self.scatter_chrono = 50
                    self.scatter_mode = True
                    self.boosts.remove((nx, ny))
                if len(self.boosts) == 0 and len(self.pellets) == 0:
                    self.value = float('inf')
                

    def update_ghosts_move(self, directions):
        ghosts = ['inky', 'pinky', 'blinky', 'clyde']
        for ghost, direction in zip(ghosts, directions):
            x, y = self.pos[ghost]
            if direction == None: dx, dy = 0,0
            else: dx, dy = direction.value
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(self.board[0]) and 0 <= ny < len(self.board):
                if self.board[ny][nx] != 0:
                    self.pos[ghost] = (nx, ny)
        if self.scatter_mode : 
            self.scatter_chrono -= 1
            if self.scatter_chrono == 0: 
                self.scatter_mode = False
                self.inky_movement_turns = 15
        else : self.inky_movement_turns -= 1
        for ghost in ['inky', 'pinky', 'blinky', 'clyde']:
            if self.pos['pacman'] == self.pos[ghost]:
                if not self.scatter_mode:
                    self.pacman_lives_number -= 1
                    self.value = float('-inf')
                else:
                    self.pacman_score += 100
                if self.pacman_lives_number == 0:
                    self.value = float('-inf')

    def get_blinky_direction(self, inky = False):
        if inky : return Tree.get_first_direction_a_star(self.pos['inky'],self.pos['pacman'])
        else: return Tree.get_first_direction_a_star(self.pos['blinky'],self.pos['pacman'])

    def get_pinky_direction(self, inky=False):
        x, y = self.pos['pacman']
        dx, dy = self.pacman_direction.value

        for i in range(4, 0, -1):
            target = (x + i*dx, y + i*dy)
            target_x = max(0, min(target[0], len(self.board[0]) - 1))
            target_y = max(0, min(target[1], len(self.board) - 1))
            if self.board[target_y][target_x] != 0:
                if inky: return Tree.get_first_direction_a_star(self.pos['inky'], (target_x, target_y))
                else: return Tree.get_first_direction_a_star(self.pos['pinky'], (target_x, target_y))
        if inky: return Tree.get_first_direction_a_star(self.pos['inky'], self.pos['pacman'])
        else: return Tree.get_first_direction_a_star(self.pos['pinky'], self.pos['pacman'])
        
    def get_clyde_direction(self, inky = False):
        if inky : return [direction for direction in [Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN] 
                        if self.direction_valide(self.pos['inky'], direction)]
        else : return [direction for direction in [Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN] 
                    if self.direction_valide(self.pos['clyde'], direction)]
        
    def get_inky_direction(self):
        if self.inky_last_choice == 'blinky': return [self.get_blinky_direction(inky=True)]
        if self.inky_last_choice == 'pinky': return [self.get_pinky_direction(inky=True)]
        if self.inky_last_choice == 'clyde': return self.get_clyde_direction(inky=True)

    def alpha_beta(self, depth, alpha, beta, doesMaximize): 
        if self.value != None : 
            return self.value
        
        if depth == 0 :
            self.value = Tree.heuristique.evaluate(self, Tree.board) 
            return self.value
   
        if doesMaximize:
            maxEval = float('-inf')
            best_direction = None
            for direction in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:
                # Ignore the opposite direction unless it's the only valid move
                if direction == self.pacman_direction.get_opposite_direction():
                    # Vérifie s'il existe au moins une autre direction valide
                    other_valid = [
                        d for d in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
                        if d != direction and self.direction_valide(self.pos['pacman'], d)
                    ]
                    if other_valid:
                        continue 
                if self.direction_valide(self.pos['pacman'], direction):
                    child = self.clone()
                    child.pacman_direction = direction
                    child.update_pacman_move(direction)
                    evaluation = child.alpha_beta(depth - 1, alpha, beta, False)
                    if evaluation > maxEval:
                        maxEval = evaluation
                        best_direction = direction
                    alpha = max(alpha, evaluation)
                    if beta <= alpha: break
            if depth == Tree.initial_depth:
                return best_direction      
            self.value = maxEval
            return maxEval
        else:
            minEval = float('inf')
            if self.scatter_mode: #comportement deterministe si effrayé
                child = self.clone()
                child.update_ghosts_move([Tree.get_first_direction_a_star(child.pos[ghost], child.initial_pos[ghost]) for ghost in ['inky', 'pinky', 'blinky', 'clyde']])
                evaluation = child.alpha_beta(depth - 1, alpha, beta, True)
                minEval = min(minEval, evaluation)
                beta = min(beta, evaluation)
                self.value = minEval
                return minEval
 
            elif self.inky_movement_turns == 0 or self.inky_last_choice == None:
                blinky_direction = self.get_blinky_direction()
                pinky_direction = self.get_pinky_direction()
                for clyde_direction in self.get_clyde_direction() :
                    for inky_choice in ['pinky', 'blinky', 'clyde'] :   
                        child = self.clone()
                        child.inky_movement_turns = 15
                        child.inky_last_choice = inky_choice
                        for inky_direction in child.get_inky_direction():
                            
                            child.update_ghosts_move([inky_direction, pinky_direction, blinky_direction, clyde_direction])
                            evaluation = child.alpha_beta(depth - 1, alpha, beta, False)
                            minEval = min(minEval, evaluation)
                            beta = min(beta, evaluation)
                            if beta <= alpha: break
                self.value = minEval
                return minEval
            
            else :
                blinky_direction = self.get_blinky_direction()
                pinky_direction = self.get_pinky_direction()
                inky_directions = self.get_inky_direction()
                for clyde_direction in self.get_clyde_direction() :
                    for inky_direction in inky_directions :   
                        child = self.clone()
                        child.update_ghosts_move([inky_direction, pinky_direction, blinky_direction, clyde_direction])
                        evaluation = child.alpha_beta(depth - 1, alpha, beta, False)
                        minEval = min(minEval, evaluation)
                        beta = min(beta, evaluation)
                        if beta <= alpha: break
                self.value = minEval
                return minEval