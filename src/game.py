from ghost import *
from utils import *

class Game:
    def __init__(self):
        self.scatter_mode = False
        self.scatter_chrono = 0
        self.score = 0
        
        self.layout = self.generate_maze()
        self.width = len(self.layout[0])
        self.height = len(self.layout)
        
        self.pacman = Pacman()
        self.blinky = Blinky(Coordinate(12,15))
        self.pinky = Pinky(Coordinate(13,15))
        self.inky = Inky(Coordinate(14,15))
        self.clyde = Clyde(Coordinate(15,15))
        self.ghosts = [self.blinky, self.pinky, self.inky, self.clyde]
        
    def pellets(self):
        return [ Coordinate(y,x) for x,row in enumerate(self.layout) for y,cell in enumerate(row) if cell == 1 ]
    
    def boosts(self):
        return [ Coordinate(y,x) for x,row in enumerate(self.layout) for y,cell in enumerate(row) if cell == 2 ]
    
    # Used to update the scatter mode
    def update(self):
        if self.scatter_mode:
            self.scatter_chrono -= 1
        if self.scatter_chrono == 0:
            self.scatter_mode = False
        
    def eat(self, position):
        if self.layout[position.y][position.x] == 2:
            self.scatter_mode = True
            self.scatter_chrono = 40
            self.score += 500
        if self.layout[position.y][position.x] == 1:
            self.score += 10
        self.layout[position.y][position.x] = 3
        
    def generate_maze(self):
        maze = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
            [0, 2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0],
            [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0], 
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 3, 0, 0, 0, 0, 3, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 3, 3, 3, 3, 3, 3, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 3, 3, 3, 3, 3, 3, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 3, 3, 3, 3, 3, 3, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
            [0, 2, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 2, 0],
            [0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        return maze

    def check_collision(self, position):
        return self.layout[position.y][position.x] == 0

    def display_maze(self):
        for row in self.layout:
            print(''.join(row))
            
    def move_ghost(self):
        for ghost in self.ghosts:
            ghost.move(self)
            
    def get_valid_direction(self, position):
        valid_directions = []

        # Check possible direction (up, down, left, right)
        possible_directions = [
            Direction.UP,
            Direction.DOWN,
            Direction.LEFT,
            Direction.RIGHT
        ]
    
        for direction in possible_directions:
            if not self.check_collision(position+direction.value):
                valid_directions.append(direction)

        return valid_directions
    
    def is_valid_position(self, position):
        return 0 <=  position.x < self.width and 0 <= position.y < self.height and self.layout[position.y][ position.x] != 0
    
    def get_next_maze(self, pacman, inky, pinky, blinky, clyde):
        self.get_valid_direction(pacman.position)
  
    def isWin(self):
        return (
            not any(1 in row for row in self.layout) and 
            all(self.pacman.position != ghost.position for ghost in self.ghosts)
        )

    def isLose(self):
        return any(self.pacman.position == ghost.position for ghost in self.ghosts)

    def isOver(self):
        return self.isLose() or self.isWin()
        