from collections import deque
import copy
import math
import random
import tkinter as tk

from board import Board
from gameImage import GameImage
from wall import Wall

class Tree():
    initial_pos = {}
    initial_pos['pacman'] = [14, 23]
    initial_pos['inky'] = [12, 15]
    initial_pos['pinky'] = [14, 15]
    initial_pos['blinky'] = [13, 15]
    initial_pos['clyde'] = [15, 15]
    inky_movement_turns = 15
    inky_last_choice = None
    clyde_movement_turns = 15
    clyde_last_choice = None

    def __init__(self, value, children):
        Tree.get_initial_tree_attributes(self)
        self.value = value
        self.children = children

    def get_initial_tree_attributes(self):
        self.pacman_lives_number = 3
        self.pacman_direction = 'Left'
        self.is_enemy_invulnerable = True
        self.pos = {}
        self.pos['pacman'] = self.initial_pos['pacman']
        self.pos['blinky'] = self.initial_pos['blinky']
        self.pos['inky'] = self.initial_pos['inky']
        self.pos['pinky'] = self.initial_pos['pinky']
        self.pos['clyde'] = self.initial_pos['clyde']

    def set_tree_attributes(self, value, children, pacman_pos, inky_pos, pinky_pos, blinky_pos, clyde_pos, pacman_lives_number, pacman_direction, is_enemy_invulnerable):
        self.value = value
        self.children = children
        self.pos['pacman'] = pacman_pos
        self.pos['inky'] = inky_pos
        self.pos['pinky'] = pinky_pos
        self.pos['blinky'] = blinky_pos
        self.pos['clyde'] = clyde_pos
        self.pacman_lives_number = pacman_lives_number
        self.pacman_direction = pacman_direction
        self.is_enemy_invulnerable = is_enemy_invulnerable     
           
    def clone(self):
        res = Tree(self.value, self.children)
        res.set_tree_attributes(self.value, self.children, copy.deepcopy(self.pos['pacman']), copy.deepcopy(self.pos['inky']), copy.deepcopy(self.pos['pinky']), copy.deepcopy(self.pos['blinky']), copy.deepcopy(self.pos['clyde']), self.pacman_lives_number, self.pacman_direction, self.is_enemy_invulnerable)
        return res

    @classmethod
    def build_pacman_tree(self, tree, initial_board, depth, is_packman_turn, heuristique):
        #print(depth, tree.pos['pacman'], is_packman_turn)
        if depth == 0:
            tree.value = heuristique.evaluate(tree, initial_board) if heuristique else depth
            return
        elif tree.pacman_lives_number == 0:
            tree.value = float('-inf')
            return
        elif ((tree.pos['pacman'][1] == tree.pos['inky'][1]) and (tree.pos['pacman'][0] == tree.pos['inky'][0])) or \
            ((tree.pos['pacman'][1] == tree.pos['pinky'][1]) and (tree.pos['pacman'][1] == tree.pos['pinky'][0])) or \
            ((tree.pos['pacman'][1] == tree.pos['blinky'][1]) and (tree.pos['pacman'][1] == tree.pos['blinky'][0])) or \
            ((tree.pos['pacman'][1] == tree.pos['clyde'][1]) and (tree.pos['pacman'][1] == tree.pos['clyde'][0])):
            if tree.is_enemy_invulnerable:
                tree.pacman_lives_number -= 1
            
            child = Tree(0, [])
            child.pacman_lives_number = tree.pacman_lives_number
            child.is_enemy_invulnerable = tree.is_enemy_invulnerable
            tree.children.append(child)
            self.build_pacman_tree(child, initial_board, depth - 1, not(is_packman_turn), heuristique)
        elif is_packman_turn:
            direction_options = []
            for direction in ['Left', 'Right', 'Up', 'Down']:
                if self.modified_validate_path_function(initial_board, tree.pos['pacman'][1], tree.pos['pacman'][0], direction):
                    direction_options.append(direction)
                    
            for selected_direction in direction_options:
                child = tree.clone()
                child.children = []
                child.pacman_direction = selected_direction
                child.is_enemy_invulnerable = tree.is_enemy_invulnerable
                self.modified__validate_movement_function(child, child.pos['pacman'][1], child.pos['pacman'][0], selected_direction)
                self.modified_movement_function(child, 'pacman', selected_direction)
                #print(selected_direction, child.pos['pacman'])
                tree.children.append(child)
            
            for child in tree.children:
                self.build_pacman_tree(child, initial_board, depth - 1, not(is_packman_turn), heuristique)
        else:
            inky_direction = self.modified_determineDirection_function(initial_board, tree.pos['inky'], tree.pos['pacman'][1], tree.pos['pacman'][0], tree.pacman_direction, tree.pos['inky'][1], tree.pos['inky'][0], 'inky', tree.is_enemy_invulnerable)
            pinky_direction = self.modified_determineDirection_function(initial_board, tree.pos['pinky'], tree.pos['pacman'][1], tree.pos['pacman'][0], tree.pacman_direction, tree.pos['pinky'][1], tree.pos['pinky'][0], 'pinky', tree.is_enemy_invulnerable)
            blinky_direction = self.modified_determineDirection_function(initial_board, tree.pos['blinky'], tree.pos['pacman'][1], tree.pos['pacman'][0], tree.pacman_direction, tree.pos['blinky'][1], tree.pos['blinky'][0], 'blinky', tree.is_enemy_invulnerable)
            clyde_direction = self.modified_determineDirection_function(initial_board, tree.pos['clyde'], tree.pos['pacman'][1], tree.pos['pacman'][0], tree.pacman_direction, tree.pos['clyde'][1], tree.pos['clyde'][0], 'clyde', tree.is_enemy_invulnerable)

            child = tree.clone()
            child.children = []
            child.is_enemy_invulnerable = tree.is_enemy_invulnerable

            self.modified_movement_function(child, 'inky', inky_direction)
            self.modified_movement_function(child, 'pinky', pinky_direction)
            self.modified_movement_function(child, 'blinky', blinky_direction)
            if clyde_direction is not None:
                self.modified_movement_function(child, 'clyde', clyde_direction)

            tree.children.append(child) 
            self.build_pacman_tree(tree.children[-1], initial_board, depth - 1, not(is_packman_turn), heuristique)

    @classmethod
    def modified_determineDirection_function(self, board, start, pacman_y, pacman_x, pacman_direction, enemy_y, enemy_x, enemy_type, is_enemy_invulnerable):
        if enemy_type == "blinky":
            return self.modified_blinky_movement_function(board, start, pacman_y, pacman_x, enemy_y, enemy_x, enemy_type, is_enemy_invulnerable)
        elif enemy_type == "inky":
            return self.modified_inky_movement_function(board, start, pacman_y, pacman_x, pacman_direction, enemy_y, enemy_x, enemy_type, is_enemy_invulnerable)
        if enemy_type == "pinky":
            return self.modified_pinky_movement_function(board, start, pacman_y, pacman_x, pacman_direction, enemy_y, enemy_x, enemy_type, is_enemy_invulnerable)
        elif enemy_type == "clyde":
            return self.modified_clyde_movement_function(board, enemy_y, enemy_x, is_enemy_invulnerable)

    @classmethod
    def modified_determine_path_function(self, board, start, endpoint_y, endpoint_x, enemy_type, is_enemy_invulnerable):
        start = start[0], start[1]
        if is_enemy_invulnerable:
            return self.modified_bfs_function(board, start, endpoint_y, endpoint_x)
        else:
            return self.modified_bfs_function(board, start, self.initial_pos[enemy_type][1], self.initial_pos[enemy_type][0])[:-1]


    @classmethod
    def modified_bfs_function(cls, board, start, endpoint_y, endpoint_x):
        queue = deque([[start]])
        seen = set([start])
        gamestate = board.Gamestate

        while queue:
            path = queue.popleft()
            x, y = path[-1]

            if (y, x) == (endpoint_y, endpoint_x):
                return path

            for x2, y2 in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):        
                if (0 <= x < board.board_width() and 0 <= y < len(board) and type(gamestate[y][x]) != Wall and (x2, y2) not in seen):
                    queue.append(path + [(x2, y2)])
                    seen.add((x2, y2))
        
    def modified_path_finding_direction_function(path, enemy_y, enemy_x):
        if path is not None and path != []:
            distance = int(len(path) > 1)

            if enemy_y < path[distance][1]:
                return 'Down'
            elif enemy_y > path[distance][1]:
                return 'Up'
            elif enemy_x < path[distance][0]:
                return 'Right'
            elif enemy_x > path[distance][0]:
                return 'Left'

    @classmethod
    def modified_random_choice_function(self, enemy_type):
        if enemy_type == 'inky':
            if self.inky_movement_turns == 15 or self.inky_last_choice == None:
                self.inky_last_choice = random.random()
            return self.inky_last_choice
        elif enemy_type == 'clyde':
            if self.clyde_movement_turns == 15 or self.clyde_last_choice == None:
                self.clyde_last_choice = random.random()
            return self.clyde_last_choice

    @classmethod
    def modified_blinky_movement_function(self, board, start, pacman_y, pacman_x, enemy_y, enemy_x, enemy_type, is_enemy_invulnerable):
        path = self.modified_determine_path_function(board, start, pacman_y, pacman_x, enemy_type, is_enemy_invulnerable)
        return self.modified_path_finding_direction_function(path, enemy_y, enemy_x)

    @classmethod
    def modified_inky_movement_function(self, board, start, pacman_y, pacman_x, pacman_direction, enemy_y, enemy_x, enemy_type, is_enemy_invulnerable):
        choice = self.modified_random_choice_function('inky')
        self.modified__inky_and_clyde_movement_turns_function()

        if choice <= .33:
            return self.modified_blinky_movement_function(board, start, pacman_y, pacman_x, enemy_y, enemy_x, enemy_type, is_enemy_invulnerable)    
        elif choice <= .75:
            return self.modified_clyde_movement_function(board, enemy_y, enemy_x, is_enemy_invulnerable)
        elif choice <= 1:
            return self.modified_pinky_movement_function(board, start, pacman_y, pacman_x, pacman_direction, enemy_y, enemy_x, enemy_type, is_enemy_invulnerable)

    @classmethod
    def modified__inky_and_clyde_movement_turns_function(is_inky):
        if is_inky:
            Tree.inky_movement_turns -= 1

            if Tree.inky_movement_turns == 0:
                Tree.inky_movement_turns = 15
                Tree.inky_last_choice = None
        else:
            Tree.clyde_movement_turns -= 1

            if Tree.clyde_movement_turns == 0:
                Tree.clyde_movement_turns = 15
                Tree.clyde_last_choice = None

    @classmethod
    def modified_pinky_movement_function(self, board, start, pacman_y, pacman_x, pacman_direction, enemy_y, enemy_x, enemy_type, is_enemy_invulnerable):
        endpoint_y, endpoint_x = self.modified_pinky_endpoints_function(board, pacman_y, pacman_x, pacman_direction, enemy_y, enemy_x)
        path = self.modified_determine_path_function(board, start, endpoint_y, endpoint_x, enemy_type, is_enemy_invulnerable)
        return self.modified_path_finding_direction_function(path, enemy_y, enemy_x)

    @classmethod
    def modified_pinky_endpoints_function(self, board, pacman_y, pacman_x, pacman_direction, enemy_y, enemy_x):
        if pacman_direction == 'Left':
            return self.modified_pinky_ambush_function(board, pacman_y, pacman_x, 0, -1, enemy_y, enemy_x)
        elif pacman_direction == 'Right':
            return self.modified_pinky_ambush_function(board, pacman_y, pacman_x, 0, 1, enemy_y, enemy_x)
        elif pacman_direction == 'Up':
            return self.modified_pinky_ambush_function(board, pacman_y, pacman_x, -1, 0, enemy_y, enemy_x)
        elif pacman_direction == 'Down':
            return self.modified_pinky_ambush_function(board, pacman_y, pacman_x, 1, 0, enemy_y, enemy_x)

    @classmethod
    def modified_pinky_ambush_function(self, board, pacman_y, pacman_x, dy, dx, enemy_y, enemy_x):
        ambush_limit = 7
        endpoint_y, endpoint_x = pacman_y, pacman_x
        
        if abs(enemy_y - endpoint_y) < ambush_limit and abs(enemy_x - endpoint_x) < ambush_limit:
            return endpoint_y, endpoint_x
        else:
            return self.modified_ambush_loop_function(board, dy, dx, endpoint_y, endpoint_x, ambush_limit)
    
    @classmethod
    def modified_ambush_loop_function(self, board, dy, dx, endpoint_y, endpoint_x, ambush_limit):
        for i in range(1, ambush_limit):
            if not ( ( 0 <= endpoint_y + dy <= len(board) - 1 ) and ( 0 <= endpoint_x + dx <= board.board_width() - 1) ) or \
                type(board[endpoint_y + dy][endpoint_x + dx]) == Wall:
                break
            else:
                endpoint_y += dy
                endpoint_x += dx
        return endpoint_y, endpoint_x
    
    @classmethod
    def modified_clyde_movement_function(self, board, enemy_y, enemy_x, is_enemy_invulnerable):
        choice = self.modified_random_choice_function('clyde')
        self.modified__inky_and_clyde_movement_turns_function()
        random_direction = self.modified_random_direction_function(choice)
        
        if self.modified_valid_direction_function(board, enemy_y, enemy_x, random_direction):
            if is_enemy_invulnerable:
                return random_direction
        else:
            self.clyde_movement_turns = 0
            self.clyde_last_choice = None

    @classmethod
    def modified_random_direction_function(self, choice):
        if choice <= .25:
            return 'Left'
        elif choice <= .50:
            return 'Right'
        elif choice <= .75:
            return 'Down'
        elif choice <= 1:
            return 'Up'

    @classmethod
    def modified_valid_direction_function(self, board, enemy_y, enemy_x, enemy_direction):
        y, x = enemy_y, enemy_x
        
        if enemy_direction == 'Left':
            return type(board[y][x - 1]) != Wall
        elif enemy_direction == 'Right': 
            return type(board[y][x + 1]) != Wall
        elif enemy_direction == 'Down':
            return type(board[y + 1][x]) != Wall
        elif enemy_direction == 'Up':
            return type(board[y - 1][x]) != Wall

    @classmethod
    def modified_movement_function(self, tree, character_type, direction):
        if direction == 'Up':
            tree.pos[character_type][1] -= 1
        elif direction == 'Right':
            tree.pos[character_type][0] += 1
        elif direction == 'Down':
            tree.pos[character_type][1] += 1
        elif direction == 'Left':
            tree.pos[character_type][0] -= 1

    @classmethod
    def modified__validate_movement_function(self, tree, pacman_y, pacman_x, pacman_direction):
        if pacman_y == 14 and (pacman_x == 0 or pacman_x == 27):
            if pacman_direction == 'Left':
                tree.pos['pacman'] = [27,14]
            else:
                tree.pos['pacman'] = [0,14]

    @classmethod
    def modified_validate_path_function(self, board, pacman_y, pacman_x, direction):
        if direction == 'Left':
            return type(board.Gamestate[pacman_y][pacman_x - 1]) != Wall

        elif direction == 'Right':
            return type(board.Gamestate[pacman_y][pacman_x + 1]) != Wall

        elif direction == 'Down':
            return type(board.Gamestate[pacman_y + 1][pacman_x]) != Wall and (pacman_y + 1, pacman_x) not in Board.restricted_area

        elif direction == 'Up':
            return type(board.Gamestate[pacman_y - 1][pacman_x]) != Wall

    @classmethod
    def init_tree_randomly(cls, tree, lower_bound, upper_limit):
        if (len(tree.children) == 0):
            tree.value = random.randint(lower_bound, upper_limit)
        for child_tree in tree.children:
            cls.init_tree_randomly(child_tree, lower_bound, upper_limit)
    
    def _init_tree_randomly(self, lower_bound, upper_limit):
        self.init_tree_randomly(self, lower_bound, upper_limit)

    @classmethod
    def alpha_beta_calculus(cls, node, depth, alpha, beta, doesMaximize): # inspired from: https://www.youtube.com/watch?v=l-hh51ncgDI
        """if ((depth == 0) or (game over in position)):
            return eval of position"""
        if (depth == 0):
            return node.value

        if doesMaximize:
            maxEval = float('-inf')
            for child in node.children:
                evaluation = cls.alpha_beta_calculus(child, depth - 1, alpha, beta, False)
                maxEval = max(maxEval, evaluation)
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    node.value = maxEval
                    return maxEval
            node.value = maxEval
            return maxEval
        else:
            minEval = float('inf')
            for child in node.children:
                evaluation = cls.alpha_beta_calculus(child, depth - 1, alpha, beta, True)
                minEval = min(minEval, evaluation)
                beta = min(beta, evaluation)
                if beta <= alpha:
                    node.value = minEval
                    return minEval
            node.value = minEval
            return minEval

    def _alpha_beta_calculus(self, depth, alpha, beta, doesMaximize):
        return self.alpha_beta_calculus(self, depth, alpha, beta, doesMaximize)

    @classmethod
    def get_node_list(cls, node, value, target_list):
        for i in range(len(node.children)):
            child = node.children[i]
            if (child.value == value):
                target_list.append(i)
                cls.get_node_list(child, value, target_list)
                break

    def _get_node_list(self):
        L = [0]
        self.get_node_list(self, self.value, L)
        return L

    def display(self, level=0, prefix="Root: "):
        spaces = "  " * level
        print(f"{spaces}{prefix}{self.value}")
        
        for i, child in enumerate(self.children):
            child.display(level + 1, f"Child {i+1}: ")
    
    @classmethod
    def display_pacman_tree_aux(cls, tree, i):
        for _ in range(i):
            print("    ", end="")
        print(tree.pos)
        for child in tree.children:            
            Tree.display_pacman_tree_aux(child, i+1)

if __name__ == "__main__":
    """child1 = Tree(0, [Tree(0, []), Tree(0, []), Tree(0, [])])
    child2 = Tree(0, [Tree(0, []), Tree(0, []), Tree(0, []), Tree(0, [])])
    child3 = Tree(0, [Tree(0, []), Tree(0, [])])
    
    root = Tree(0, [child1, child2, child3])
    
    root._init_tree_randomly(-10, 10)
    root._alpha_beta_calculus(2, - math.inf, math.inf, True)
    path = root._get_node_list()

    print("Arbre généré aléatoirement:")
    root.display()    
    print("Trajectoire")
    for i in range(len(path)):
        print(str(path[i]) + ", ")"""
    
    root = tk.Tk()
    board = Board(1000, 850, GameImage())
    board.new_level()
    test_tree = Tree(0, [])
    print(test_tree.pos['pacman'])

    Tree.build_pacman_tree(test_tree, board, 3, True, None)
    Tree.alpha_beta_calculus(test_tree, 3, -math.inf, math.inf, True)
    Tree.display_pacman_tree_aux(test_tree, 0)

    

