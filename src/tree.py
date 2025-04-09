from collections import deque
import random
import math

from board import Board
from wall import Wall

class Tree():
    initial_pos = {}
    initial_pos['pacman'] = (14,23)
    initial_pos['blinky'] = (13, 15)
    initial_pos['inky'] = (12, 15)
    initial_pos['pinky'] = (14, 15)
    initial_pos['clyde'] = (15, 15)
    inky_movement_turns = 15
    inky_last_choice = None
    clyde_movement_turns = 15
    clyde_last_choice = None

    def __init__(self, value, children, pacman_pos, inky_pos, pinky_pos, blinky_pos, clyde_pos, pacman_lives_number, pacman_direction, is_pacman_invulnerable):
        self.pos['pacman'] = pacman_pos
        self.pos['inky'] = inky_pos
        self.pos['pinky'] = pinky_pos
        self.pos['blinky'] = blinky_pos
        self.pos['clyde'] = clyde_pos
        self.value = value
        self.children = children
        self.pacman_lives_number = pacman_lives_number
        self.pacman_direction = pacman_direction
        self.is_packman_invulnerable = is_pacman_invulnerable

    @classmethod
    def get_initial_tree_attributes(cls, tree, initial_board):
        pacman_lives_number = 3
        pacman_direction = 'Left'
        is_pacman_invulnerable = False
        pacman_pos = Tree.initial_pos['pacman']
        blinky_pos = Tree.initial_pos['blinky']
        inky_pos = Tree.initial_pos['inky']
        pinky_pos = Tree.initial_pos['pinky']
        clyde_pos = Tree.initial_pos['clyde']

        tree.__init__(0, [], pacman_pos, inky_pos, pinky_pos, blinky_pos, clyde_pos, pacman_lives_number, pacman_direction, is_pacman_invulnerable)

    @classmethod
    def build_pacman_tree(cls, tree, initial_board, depth, is_packman_turn, heuristique):
        if depth == 0:
            tree.value = heuristique(tree)
            return
        elif tree.pacman_lives_number == 0:
            tree.value = - math.inf
            return
        else:
            if ((tree.pacman_pos[1] == tree.pos['inky'][1]) and (tree.pacman_pos[0] == tree.pos['inky'][0])) or \
                ((tree.pacman_pos[1] == tree.pos['pinky'][1]) and (tree.pacman_pos[1] == tree.pos['pinky'][0])) or \
                ((tree.pacman_pos[1] == tree.pos['blinky'][1]) and (tree.pacman_pos[1] == tree.pos['blinky'][0])) or \
                ((tree.pacman_pos[1] == tree.pos['clyde'][1]) and (tree.pacman_pos[1] == tree.pos['clyde'][0])):
                tree.pacman_lives_number -= 1
                child = Tree(0, [], Tree.initial_pos['pacman'], Tree.initial_pos['inky'], Tree.initial_pos['pinky'], Tree.initial_pos['blinky'], Tree.initial_pos['clyde'], tree.pacman_lives_number - 1, 'Left', False)
                tree.children.append(child)
                Tree.build_pacman_tree(child, initial_board, depth - 1, not(is_packman_turn), heuristique)
            else:
                if is_packman_turn:
                    direction_options = []
                    for direction in ['Left', 'Right', 'Up', 'Down']:
                        if Tree.modified_validate_path_function(initial_board, tree.pos['pacman'][1], tree.pos['pacman'][0], direction):
                            direction_options.append(direction)
                    
                    for selected_direction in direction_options:
                        child = Tree(0, [], tree.pos['pacman'], tree.pos['inky'], tree.pos['pinky'], tree.pos['blinky'], tree.pos['clyde'], tree.pacman_lives_number, selected_direction, False)
                        Tree.modified__validate_movement_function(tree, tree.pos['pacman'][1], tree.pos['pacman'][0], selected_direction)
                        Tree.modified_movement_function(child, 'pacman', selected_direction)
                        tree.children.append(child)
                        Tree.build_pacman_tree(child, initial_board, depth - 1, not(is_packman_turn), heuristique)
                else:
                    inky_direction = Tree.modified_inky_movement_function(initial_board, tree.pos['inky'], tree.pacman_pos[1], tree.pacman_pos[0], tree.pacman_direction, tree.pos['inky'][1], tree.pos['inky'][0], 'inky', False)
                    pinky_direction = Tree.modified_inky_movement_function(initial_board, tree.pos['pinky'], tree.pacman_pos[1], tree.pacman_pos[0], tree.pacman_direction, tree.pos['pinky'][1], tree.pos['pinky'][0], 'pinky', False)
                    blinky_direction = Tree.modified_inky_movement_function(initial_board, tree.pos['blinky'], tree.pacman_pos[1], tree.pacman_pos[0], tree.pacman_direction, tree.pos['blinky'][1], tree.pos['blinky'][0], 'blinky', False)
                    clyde_direction = Tree.modified_inky_movement_function(initial_board, tree.pos['clyde'], tree.pacman_pos[1], tree.pacman_pos[0], tree.pacman_direction, tree.pos['clyde'][1], tree.pos['clyde'][0], 'clyde', False)

                    child = Tree(0, [], tree.pos['pacman'], tree.pos['inky'], tree.pos['pinky'], tree.pos['blinky'], tree.pos['clyde'], tree.pacman_lives_number, tree.pacman_direction, False)

                    Tree.modified_movement_function(child, 'inky', inky_direction)
                    Tree.modified_movement_function(child, 'pinky', pinky_direction)
                    Tree.modified_movement_function(child, 'blinky', blinky_direction)
                    Tree.modified_movement_function(child, 'clyde', clyde_direction)

                    tree.children.append(child)
                    Tree.build_pacman_tree(child, initial_board, depth - 1, not(is_packman_turn), heuristique)

    @classmethod
    def modified_determineDirection_function(cls, board, start, pacman_y, pacman_x, pacman_direction, enemy_y, enemy_x, enemy_type, is_enemy_invulnerable):
        if enemy_type == "blinky":
            path = Tree.modified_determine_path_function(board, start, pacman_y, pacman_x)
            return Tree.modified_path_finding_direction_function(path)
        elif enemy_type == "inky":
            return Tree.modified_inky_movement_function(board, start, pacman_y, pacman_x, pacman_direction, enemy_y, enemy_x, enemy_type, is_enemy_invulnerable)
        if enemy_type == "pinky":
            return Tree.modified_pinky_movement_function(board, start, pacman_y, pacman_x, pacman_direction, enemy_y, enemy_x, enemy_type, is_enemy_invulnerable)
        elif enemy_type == "clyde":
            return Tree.modified_clyde_movement_function(board, enemy_y, enemy_x, is_enemy_invulnerable)

    @classmethod
    def modified_determine_path_function(cls, board, start, endpoint_y, endpoint_x, enemy_type, is_enemy_invulnerable):
        if is_enemy_invulnerable:
            return Tree.modified_bfs_function(board, start, endpoint_y, endpoint_x)
        else:
            return Tree.modified_bfs_function(board, start, Tree.initial_pos[enemy_type][1], Tree.initial_pos[enemy_type][0])[:-1]


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
                if (0 <= x < board.board_width() and 0 <= y < len(board) and type(gamestate[y][x]) != Wall and (x, y) not in seen):
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
    def modified_random_choice_function(cls, enemy_type):
        if enemy_type == 'inky':
            if Tree.inky_movement_turns == 15 or Tree.inky_last_choice == None:
                Tree.inky_last_choice = random()
            return Tree.inky_last_choice
        elif enemy_type == 'clyde':
            if Tree.clyde_movement_turns == 15 or Tree.clyde_last_choice == None:
                Tree.clyde_last_choice = random()
            return Tree.clyde_last_choice

    @classmethod
    def modified_inky_movement_function(cls, board, start, pacman_y, pacman_x, pacman_direction, enemy_y, enemy_x, enemy_type, is_enemy_invulnerable):
        choice = Tree.modified_random_choice_function('inky')
        Tree.modified__inky_and_clyde_movement_turns_function()

        if choice <= .33:
            path = Tree.modified_determine_path_function(board, start, pacman_y, pacman_x)
            return Tree.modified_path_finding_direction_function(path)
        elif choice <= .75:
            return Tree.modified_clyde_movement_function(board, enemy_y, enemy_x, is_enemy_invulnerable)
        elif choice <= 1:
            return Tree.modified_pinky_movement_function(board, start, pacman_y, pacman_x, pacman_direction, enemy_y, enemy_x, enemy_type, is_enemy_invulnerable)

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
    def modified_pinky_movement_function(cls, board, start, pacman_y, pacman_x, pacman_direction, enemy_y, enemy_x, enemy_type, is_enemy_invulnerable):
        endpoint_y, endpoint_x = Tree.modified_pinky_endpoints_function(board, pacman_y, pacman_x, pacman_direction, enemy_y, enemy_x)
        path = Tree.modified_determine_path_function(board, start, endpoint_y, endpoint_x, enemy_type, is_enemy_invulnerable)
        return Tree.modified_path_finding_direction_function(enemy_y, enemy_x)

    @classmethod
    def modified_pinky_endpoints_function(cls, board, pacman_y, pacman_x, pacman_direction, enemy_y, enemy_x):
        if pacman_direction == 'Left':
            return Tree.modified_pinky_ambush_function(board, pacman_y, pacman_x, 0, -1, enemy_y, enemy_x)
        elif pacman_direction == 'Right':
            return Tree.modified_pinky_ambush_function(board, pacman_y, pacman_x, 0, 1, enemy_y, enemy_x)
        elif pacman_direction == 'Up':
            return Tree.modified_pinky_ambush_function(board, pacman_y, pacman_x, -1, 0, enemy_y, enemy_x)
        elif pacman_direction == 'Down':
            return Tree.modified_pinky_ambush_function(board, pacman_y, pacman_x, 1, 0, enemy_y, enemy_x)

    @classmethod
    def modified_pinky_ambush_function(cls, board, pacman_y, pacman_x, dy, dx, enemy_y, enemy_x):
        ambush_limit = 7
        endpoint_y, endpoint_x = pacman_y, pacman_x
        
        if abs(enemy_y - endpoint_y) < ambush_limit and abs(enemy_x - endpoint_x) < ambush_limit:
            return endpoint_y, endpoint_x
        else:
            return Tree.modified_ambush_loop_function(cls, board, dy, dx, endpoint_y, endpoint_x, ambush_limit)
    
    @classmethod
    def modified_ambush_loop_function(cls, board, dy, dx, endpoint_y, endpoint_x, ambush_limit):
        for i in range(1, ambush_limit):
            if not ( ( 0 <= endpoint_y + dy <= len(board) - 1 ) and ( 0 <= endpoint_x + dx <= board.board_width() - 1) ) or \
                type(board[endpoint_y + dy][endpoint_x + dx]) == Wall:
                break
            else:
                endpoint_y += dy
                endpoint_x += dx
        return endpoint_y, endpoint_x
    
    @classmethod
    def modified_clyde_movement_function(cls, board, enemy_y, enemy_x, is_enemy_invulnerable):
        choice = Tree.modified_random_choice_function('clyde')
        Tree.modified__inky_and_clyde_movement_turns_function()
        random_direction = Tree.modified_random_direction_function(choice)
        
        if Tree.modified_valid_direction_function(board, enemy_y, enemy_x, random_direction):
            if is_enemy_invulnerable:
                return random_direction
        else:
            Tree.clyde_movement_turns = 0
            Tree.clyde_last_choice = None

    @classmethod
    def modified_random_direction_function(cls, choice):
        if choice <= .25:
            return 'Left'
        elif choice <= .50:
            return 'Right'
        elif choice <= .75:
            return 'Down'
        elif choice <= 1:
            return 'Up'

    @classmethod
    def modified_valid_direction_function(cls, board, enemy_y, enemy_x, enemy_direction):
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
    def modified_movement_function(cls, tree, character_type, direction):
        if direction == 'Up':
            tree.pos[character_type][1] -= 1
        elif direction == 'Right':
            tree.pos[character_type][0] += 1
        elif direction == 'Down':
            tree.pos[character_type][1] += 1
        elif direction == 'Left':
            tree.pos[character_type][1] -= 1

    @classmethod
    def modified__validate_movement_function(cls, tree, pacman_y, pacman_x, pacman_direction):
        if pacman_y == 14 and (pacman_x == 0 or pacman_x == 27):
            if pacman_direction == 'Left':
                tree.pos['pacman'] = (27,14)
            else:
                tree.pos['pacman'] = (0,14)

    @classmethod
    def modified_validate_path_function(cls, board, pacman_y, pacman_x, direction):
        if direction == 'Left':
            return type(board[pacman_y][pacman_x - 1]) != Wall

        elif direction == 'Right':
            return type(board[pacman_y][pacman_x + 1]) != Wall

        elif direction == 'Down':
            return type(board[pacman_y + 1][pacman_x]) != Wall and (pacman_y + 1, pacman_x) not in Board.restricted_area

        elif direction == 'Up':
            return type(board[pacman_y - 1][pacman_x]) != Wall

    ##########################################################################################""""

    @classmethod
    def init_tree_randomly(cls, tree, lower_bound, upper_limit):
        if (len(tree.children) == 0):
            tree.value = random.randint(lower_bound, upper_limit)
        for child_tree in tree.children:
            cls.init_tree_randomly(child_tree, lower_bound, upper_limit)
    
    def _init_tree_randomly(self, lower_bound, upper_limit):
        Tree.init_tree_randomly(self, lower_bound, upper_limit)

    @classmethod
    def alpha_beta_calculus(cls, node, depth, alpha, beta, doesMaximize): # inspired from: https://www.youtube.com/watch?v=l-hh51ncgDI
        """if ((depth == 0) or (game over in position)):
            return eval of position"""
        if (depth == 0):
            return node.value

        if doesMaximize:
            maxEval = - math.inf
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
            minEval = math.inf
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
        return Tree.alpha_beta_calculus(self, depth, alpha, beta, doesMaximize)

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
        Tree.get_node_list(self, self.value, L)
        return L

    def display(self, level=0, prefix="Root: "):
        spaces = "  " * level
        print(f"{spaces}{prefix}{self.value}")
        
        for i, child in enumerate(self.children):
            child.display(level + 1, f"Child {i+1}: ")

if __name__ == "__main__":
    child1 = Tree(0, [Tree(0, []), Tree(0, []), Tree(0, [])])
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
        print(str(path[i]) + ", ")

