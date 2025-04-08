import random
import math

class Tree():
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
        self.pacman_pos = pacman_pos
        self.pacman_next_direction = None
        self.inky_pos = inky_pos
        self.pinky_pos = pinky_pos
        self.blinky_pos = blinky_pos
        self.clyde_pos = clyde_pos
        self.value = value
        self.children = children
        self.pacman_lives_number = pacman_lives_number
        self.pacman_direction = pacman_direction
        self.is_packman_invulnerable = is_packman_invulnerable

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
            if is_packman_turn:
                
            else:


    @classmethod
    def get_packman_future_pos(cls, ):


    @classmethod
    def modified_determineDirection_function(cls, board, start, pacman_y, pacman_x, enemy_type, is_enemy_invulnerable):
        if enemy_type == "blinky":
            path = modified_determine_path_function(board, start, pacman_y, pacman_x)
            return modified_path_finding_direction_function(path)
        elif enemy_type == "inky":
            return modified_inky_movement_function(cls, board, start, pacman_y, pacman_x)
        if enemy_type == "pinky":
            
        elif enemy_type == "clyde":
            

    @classmethod
    def modified_determine_path_function(cls, board, start, endpoint_y, endpoint_x, enemy_type, is_enemy_invulnerable):
        if is_enemy_invulnerable:
            return modified_bfs_function(cls, board, start, endpoint_y, endpoint_x)
        else:
            return modified_bfs_function(cls, board, start, Tree.initial_pos[enemy_type][1], Tree.initial_pos[enemy_type][0])[:-1]


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
        choice = modified_random_choice_function(cls, 'inky')
        modified__inky_and_clyde_movement_turns_function(cls)

        if choice <= .33:
            path = modified_determine_path_function(board, start, pacman_y, pacman_x)
            return modified_path_finding_direction_function(path)
        elif choice <= .75:
            
        elif choice <= 1:
            return modified_pinky_movement_function(cls, board, start, pacman_y, pacman_x, pacman_direction, enemy_y, enemy_x, enemy_type, is_enemy_invulnerable)

    @classmethod
    def modified__inky_and_clyde_movement_turns_function(cls, is_inky):
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
        endpoint_y, endpoint_x = modified_pinky_endpoints_function(cls, board, pacman_y, pacman_x, pacman_direction, enemy_y, enemy_x)
        path = modified_determine_path_function(cls, board, start, endpoint_y, endpoint_x, enemy_type, is_enemy_invulnerable)
        return modified_path_finding_direction_function(cls, enemy_y, enemy_x)

    @classmethod
    def modified_pinky_endpoints_function(cls, board, pacman_y, pacman_x, pacman_direction, enemy_y, enemy_x):
        if pacman_direction == 'Left':
            return modified_pinky_ambush_function(cls, board, pacman_y, pacman_x, 0, -1, enemy_y, enemy_x)
        elif pacman_direction == 'Right':
            return modified_pinky_ambush_function(cls, board, pacman_y, pacman_x, 0, 1, enemy_y, enemy_x)
        elif pacman_direction == 'Up':
            return modified_pinky_ambush_function(cls, board, pacman_y, pacman_x, -1, 0, enemy_y, enemy_x)
        elif pacman_direction == 'Down':
            return modified_pinky_ambush_function(cls, board, pacman_y, pacman_x, 1, 0, enemy_y, enemy_x)

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
            if not ( ( 0 <= endpoint_dy <= len(board) - 1 ) and ( 0 <= endpoint_dx <= board.board_width() - 1) ) or \
                type(board[endpoint_y + dy][endpoint_x + dx]) == Wall:
                break
            else:
                endpoint_y += dy
                endpoint_x += dx
        return endpoint_y, endpoint_x
    
    @classmethod

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

