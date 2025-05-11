from collections import deque
import copy
import math
import random
import tkinter as tk

from board import Board
from gameImage import GameImage
from wall import Wall
import bitarray
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
    board = bitarray([   
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
    ])
    heuristique = None
    initial_depth = None

    def __init__(self,initial_depth, heuristique, pacman_score, pacman_lives_number, pacman_direction, scatter_mode,
                       scatter_chrono, inky_movement_turns, inky_last_choice, pos, pellets, boosts):
        Tree.initial_depth = initial_depth
        Tree.heuristique = heuristique
        self.value = None
        self.children = []
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
        res = copy.deepcopy(self)
        res.children = []
        res.value = None
        return res 
    
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
                    self.boosts.remove((nx, ny))
                if not self.boosts and not self.pellets:
                    self.value = float('inf')

    def update_ghosts_move(self, directions):
        ghosts = ['inky', 'pinky', 'blinky', 'clyde']
        for ghost, direction in zip(ghosts, directions):
            x, y = self.pos[ghost]
            dx, dy = direction.value
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(self.board[0]) and 0 <= ny < len(self.board):
                if self.board[ny][nx] != 0:
                    self.pos[ghost] = (nx, ny)
        if self.scatter_mode : 
            self.scatter_chrono -= 1
            if self.scatter_chrono == 0: 
                self.scatter_mode = False
                self.clyde_and_inky_movement_turns = 15
        else : self.clyde_and_inky_movement_turns -= 1
        for ghost in ['inky', 'pinky', 'blinky', 'clyde']:
            if self.pos['pacman'] == self.pos[ghost]:
                if self.is_enemy_invulnerable:
                    self.pacman_lives_number -= 1
                else:
                    self.pacman_score += 100
                if self.pacman_lives_number == 0:
                    self.value = float('-inf')

    def get_blinky_direction(self):
        return self.get_first_direction_bfs(
            self.pos['blinky'],
            self.pos['pacman']
        )

    def get_pinky_direction(self):
        x, y = self.pos['pacman']
        dx, dy = self.pacman_direction.value
        
        target = (x + 4*dx, y + 4*dy)
        
        target_x = max(0, min(target[0], len(self.board[0]) - 1))
        target_y = max(0, min(target[1], len(self.board) - 1))
        return self.get_first_direction_bfs(
            self.pos['pinky'],
            (target_x, target_y)
        )
        
    def get_clyde_direction(self):
        return [direction for direction in [Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN] 
                if self.direction_valide(self.pos['clyde'], direction)]
        
    def get_inky_direction(self):
        if self.inky_last_choice == 'blinky': return [self.get_blinky_direction()]
        if self.inky_last_choice == 'pinky': return [self.get_pinky_direction()]
        if self.inky_last_choice == 'clyde': return self.get_clyde_direction()

    def alpha_beta(self, depth, alpha, beta, doesMaximize): 
        if self.value != None : return self.value
        
        if depth == 0 :
            if doesMaximize : self.value = Tree.heuristique.evaluate(self) 
            else : self.value = -Tree.heuristique.evaluate(self) 
            return self.value
   
        if doesMaximize:
            maxEval = float('-inf')
            best_direction = None
            for direction in [Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN]:
                if self.direction_valide(self.pos['pacman'], direction):
                    child = self.clone()
                    child.update_pacman_move(direction)
                    evaluation = self.alpha_beta(child, depth - 1, alpha, beta, False)
                    if evaluation > maxEval:
                        maxEval = evaluation
                        best_direction = direction
                    alpha = max(alpha, evaluation)
                    if beta <= alpha:
                        break
            if depth == Tree.initial_depth:
                return best_direction      
            self.value = maxEval
            return maxEval
        else:
            minEval = float('inf')
            if not self.scatter_mode: #comportement deterministe si effrayé
                child = self.clone()
                child.update_ghosts_move([self.get_first_direction_bfs(self.pos[ghost], self.initial_pos[ghost]) for ghost in ['inky', 'pinky', 'blinky', 'clyde']])
                evaluation = self.alpha_beta(child, depth - 1, alpha, beta, True)
                minEval = min(minEval, evaluation)
                beta = min(beta, evaluation)
                self.value = minEval
                return minEval
 
            elif self.inky_movement_turns == 0:
                blinky_direction = self.get_blinky_direction()
                pinky_direction = self.get_pinky_direction()
                for clyde_direction in self.get_clyde_direction() :
                    for inky_choice in ['pinky', 'blinky', 'clyde'] :   
                        for inky_direction in self.get_inky_direction():
                            child = self.clone()
                            child.inky_movement_turns = 15
                            child.inky_last_choice = inky_choice
                            child.update_ghosts_move([inky_direction, pinky_direction, blinky_direction, clyde_direction])
                            evaluation = self.alpha_beta(child, depth - 1, alpha, beta, False)
                            minEval = min(minEval, evaluation)
                            beta = min(beta, evaluation)
                            if beta <= alpha:
                                break
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
                        evaluation = self.alpha_beta(child, depth - 1, alpha, beta, False)
                        minEval = min(minEval, evaluation)
                        beta = min(beta, evaluation)
                        if beta <= alpha:
                            break
                self.value = minEval
                return minEval