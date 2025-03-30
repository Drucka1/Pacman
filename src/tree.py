import random
import math

class Tree():
    def __init__(self, value, children):
        self.position = None
        self.value = value
        self.children = children

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

