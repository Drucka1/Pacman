import random

class Tree():
    def __init__(self, value, children):
        self.value = value
        self.children = children

    @classmethod
    def init_tree_randomly(cls, tree, lower_bound, upper_limit):
        tree.value = random.randint(lower_bound, upper_limit)
        for child_tree in tree.children:
            cls.init_tree_randomly(child_tree, lower_bound, upper_limit)
    
    def _init_tree_randomly(self, lower_bound, upper_limit):
        Tree.init_tree_randomly(self, lower_bound, upper_limit)

    def display(self, level=0, prefix="Root: "):
        spaces = "  " * level
        print(f"{spaces}{prefix}{self.value}")
        
        for i, child in enumerate(self.children):
            child.display(level + 1, f"Child {i+1}: ")

if __name__ == "__main__":
    child1 = Tree(0, [])
    child2 = Tree(0, [])
    child3 = Tree(0, [Tree(0, []), Tree(0, [])])
    
    root = Tree(0, [child1, child2, child3])
    
    root._init_tree_randomly(1, 100)
    
    print("Arbre généré aléatoirement:")
    root.display()    
