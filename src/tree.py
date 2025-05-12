from collections import deque
from bitarray import bitarray
from enum import Enum

class Direction(Enum):
    LEFT = (-1,0)
    RIGHT = (1,0)
    UP = (0,-1)
    DOWN = (0,1)

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
        bitarray([0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0]),
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
    
    def bfs_function(start, endpoint):
        queue = deque([[start]])
        seen = set([start])

        while queue:
            path = queue.popleft()
            x, y = path[-1]

            if (x, y) == endpoint:
                return path

            for x2, y2 in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                if (0 <= x2 < len(Tree.board[0]) and 0 <= y2 < len(Tree.board)
                    and Tree.board[y2][x2] != 0 and (x2, y2) not in seen):
                    queue.append(path + [(x2, y2)])
                    seen.add((x2, y2))
                
    def get_first_direction_bfs(start, endpoint):
        path = Tree.bfs_function(start, endpoint)
        if not path or len(path) < 2:
            return None  # Pas de chemin ou déjà sur la case

        x0, y0 = path[0]
        x1, y1 = path[1]
        if x1 == x0 + 1 and y1 == y0:
            return Direction.RIGHT
        elif x1 == x0 - 1 and y1 == y0:
            return Direction.LEFT
        elif x1 == x0 and y1 == y0 + 1:
            return Direction.DOWN
        elif x1 == x0 and y1 == y0 - 1:
            return Direction.UP
        else:
            return None
        
    def direction_valide(self, pacman_pos, direction):
        x, y = pacman_pos
        dx, dy = direction.value
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(self.board[0]) and 0 <= ny < len(self.board):
            return self.board[ny][nx] != 0
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
                print("Pacman bouge vers", nx, ny, "score:", self.pacman_score, "pellets restants:", len(self.pellets))

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
                else:
                    self.pacman_score += 100
                if self.pacman_lives_number == 0:
                    self.value = float('-inf')

    def get_blinky_direction(self, inky = False):
        if inky : return Tree.get_first_direction_bfs(self.pos['inky'],self.pos['pacman'])
        else: return Tree.get_first_direction_bfs(self.pos['blinky'],self.pos['pacman'])

    def get_pinky_direction(self, inky=False):
        x, y = self.pos['pacman']
        dx, dy = self.pacman_direction.value

        for i in range(4, 0, -1):
            target = (x + i*dx, y + i*dy)
            target_x = max(0, min(target[0], len(self.board[0]) - 1))
            target_y = max(0, min(target[1], len(self.board) - 1))
            if self.board[target_y][target_x] != 0:
                if inky: return Tree.get_first_direction_bfs(self.pos['inky'], (target_x, target_y))
                else: return Tree.get_first_direction_bfs(self.pos['pinky'], (target_x, target_y))
        if inky: return Tree.get_first_direction_bfs(self.pos['inky'], self.pos['pacman'])
        else: return Tree.get_first_direction_bfs(self.pos['pinky'], self.pos['pacman'])
        
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
        if self.value != None : return self.value
        
        if depth == 0 :
            res = Tree.heuristique.evaluate(self) 
            if doesMaximize : self.value = res
            else : self.value = -res
            return self.value
   
        if doesMaximize:
            maxEval = float('-inf')
            best_direction = None
            for direction in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:
                if self.direction_valide(self.pos['pacman'], direction):
                    print(direction)
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
            if not self.scatter_mode: #comportement deterministe si effrayé
                child = self.clone()
                child.update_ghosts_move([Tree.get_first_direction_bfs(child.pos[ghost], child.initial_pos[ghost]) for ghost in ['inky', 'pinky', 'blinky', 'clyde']])
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