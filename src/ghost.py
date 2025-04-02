import random
from utils import *
from collections import deque

MOVEMENT_TURN = 20

class Ghost:
    def __init__(self, start_position, color):
        self.position = start_position
        self.original_position = start_position
        self.color = color

    def reset_position(self):
        self.position = self.original_position
        
    def get_direction(self, target, maze):
        # Directions to explore (UP, DOWN, LEFT, RIGHT)
        directions = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
        visited = set()  # Keep track of visited positions
        queue = deque([(self.position, None)])  # Queue for BFS: (current_position, first_direction)

        while queue:
            current_position, first_direction = queue.popleft()

            # If we reach the target, return the first direction
            if current_position == target:
                return first_direction if first_direction else Direction.STOP

            # Mark the current position as visited
            visited.add((current_position.x, current_position.y))

            # Explore neighbors
            for direction in directions:
                new_position = current_position + direction.value

                # Check if the new position is valid and not visited
                if (new_position.x, new_position.y) not in visited and not maze.check_collision(new_position):
                    queue.append((new_position, first_direction or direction))

        # If no path is found, return STOP
        return Direction.STOP
        
class Blinky(Ghost):
    def __init__(self, start_position):
        super().__init__(start_position, "red")

    # Chase Pacman
    def move(self, maze):
        if maze.scatter_mode :
            self.position += self.get_direction(self.original_position,maze).value
        else :
            self.position += self.get_direction(maze.pacman.position,maze).value
            
class Pinky(Ghost):
    def __init__(self, start_position):
        super().__init__(start_position, "pink")

    # Ambush Pacman
    def move(self, maze):
        # Pinky targets 5 spaces ahead of Pac-Man
        if maze.scatter_mode :  
            self.position += self.get_direction(self.original_position,maze).value
            return
        target = maze.pacman.position+5*maze.pacman.direction.value
        if not maze.is_valid_position(target) or maze.pacman.position.distance(self.position) < 7:
            self.position += self.get_direction(maze.pacman.position, maze).value
        else :
            self.position += self.get_direction(target, maze).value

class Inky(Ghost):
    def __init__(self, start_position):
        super().__init__(start_position, "cyan")
        self.counter = 0
        self.behavior = None

    def move(self, maze):
        if maze.scatter_mode :  
            self.position += self.get_direction(self.original_position,maze).value
            return
        # Change behavior every 20 turns
        if self.counter % MOVEMENT_TURN == 0:
            self.counter = 0
            self.behavior = random.choice(["pinky", "blinky", "clyde"])
        self.counter += 1

        if maze.scatter_mode:
            self.position += self.get_direction(self.original_position, maze).value
        else:
            if self.behavior == "pinky":
                # Pinky-like behavior: target 4 spaces ahead of Pac-Man
                target_position = maze.pacman.position + 4 * maze.pacman.direction.value
            elif self.behavior == "blinky":
                # Blinky-like behavior: target Pac-Man's position
                target_position = maze.pacman.position
            elif self.behavior == "clyde":
                # Clyde-like behavior: target a random tile far from Inky
                if self.counter % 20 == 1:  # Recalculate target at the start of behavior
                    self.target = self.random_target(maze)
                target_position = self.target
            else:
                target_position = maze.pacman.position  # Default to Pac-Man's position

            self.position += self.get_direction(target_position, maze).value

    def random_target(self, maze):
        while True:
            # Choose a random tile in the maze
            random_target = Coordinate(
                random.randint(1, maze.width - 2),
                random.randint(1, maze.height - 2)
            )
            # Check if the Manhattan distance is greater than 15 and if the tile is not a wall
            if not maze.check_collision(random_target) and abs(random_target.x - self.position.x) + abs(random_target.y - self.position.y) >= 15:
                return random_target

class Clyde(Ghost):
    def __init__(self, start_position):
        super().__init__(start_position, "orange")
        self.counter = 0
        self.target = None
        
    # Choose a tile each 15 loops and go to it
    def move(self, maze):
        if maze.scatter_mode :  
            self.position += self.get_direction(self.original_position,maze).value
            return
        if self.counter % MOVEMENT_TURN == 0:
            self.counter = 0
            self.target = self.random_target(maze)
        self.counter += 1
        # Move towards the random target
        self.position += self.get_direction(self.target, maze).value
    
    def random_target(self, maze):
        while True:
            # Choose a random tile in the maze
            random_target = Coordinate(
                random.randint(1, maze.width - 2),
                random.randint(1, maze.height - 2)
            )
            # Check if the Manhattan distance is greater than 15 and if the tile is not a wall
            if not maze.check_collision(random_target) and abs(random_target.x - self.position.x) + abs(random_target.y - self.position.y) >= 15:
                return random_target