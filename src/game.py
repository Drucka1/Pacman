from ghost import *
from utils import *

class Game:
    def __init__(self):
        self.scatter_mode = False
        self.scatter_chrono = 0
        self.score = 0
        self.width,self.height,self.layout = self.generate_maze()
        
        self.pacman = Pacman()
        self.blinky = Blinky(Coordinate(12,15))
        self.pinky = Pinky(Coordinate(13,15))
        self.inky = Inky(Coordinate(14,15))
        self.clyde = Clyde(Coordinate(15,15))
        self.ghosts = [self.blinky, self.pinky, self.inky, self.clyde]
        
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
        return len(maze[0]), len(maze), maze

    def check_collision(self, position):
        return self.layout[position.y][position.x] == 0

    def display_maze(self):
        for row in self.layout:
            print(''.join(row))
            
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
  
    def is_game_over(self):
        return (
            self.pacman.position == self.blinky.position or
            self.pacman.position == self.pinky.position or
            self.pacman.position == self.inky.position or
            self.pacman.position == self.clyde.position or
            not any(1 in row for row in self.layout)
        )
        
    def evaluate(self):
        ghost_distances = [
            abs(self.pacman.position.x - ghost.position.x) + abs(self.pacman.position.y - ghost.position.y)
            for ghost in self.ghosts
        ]
        min_distance = min(ghost_distances)

        # Pénalité si un fantôme est trop proche
        danger_penalty = -100 if min_distance <= 1 else 0

        # Bonus pour les grosses boules (boosts)
        boost_positions = [
            (y, x) for y, row in enumerate(self.layout) for x, cell in enumerate(row) if cell == 2
        ]
        boost_distances = [
            abs(self.pacman.position.x - boost[1]) + abs(self.pacman.position.y - boost[0])
            for boost in boost_positions
        ]
        closest_boost_distance = min(boost_distances) if boost_distances else float('inf')
        boost_bonus = 50 if closest_boost_distance < 5 else 0

        # Compter les boules restantes
        remaining_pellets = sum(row.count(1) for row in self.layout)

        scatter_bonus = 1000
        pellet_search_bonus = sum(
            max(0, 20 - (abs(self.pacman.position.x - x) + abs(self.pacman.position.y - y)))
            for y, row in enumerate(self.layout)
            for x, cell in enumerate(row) if cell == 1
        )  # Encourage Pacman to explore for pellets, with higher bonus for closer pellets

        # Calculate the barycenter of remaining pellets if there are less than 30
        remaining_pellet_positions = [
            (y, x) for y, row in enumerate(self.layout) for x, cell in enumerate(row) if cell == 1
        ]
        if len(remaining_pellet_positions) < 30 and remaining_pellet_positions:
            barycenter_x = sum(pos[1] for pos in remaining_pellet_positions) / len(remaining_pellet_positions)
            barycenter_y = sum(pos[0] for pos in remaining_pellet_positions) / len(remaining_pellet_positions)
            barycenter_distance = abs(self.pacman.position.x - barycenter_x) + abs(self.pacman.position.y - barycenter_y)
        else:
            barycenter_distance = 0

        # Bonus pour être loin des fantômes en mode scatter
        if self.scatter_mode:
            return (
            self.score
            + scatter_bonus
            + pellet_search_bonus
            + closest_boost_distance
            - 10 * remaining_pellets
            + danger_penalty
            - 5 * barycenter_distance
            )

        # Heuristique combinée
        return (
            self.score
            + boost_bonus
            + 5 * min_distance
            - 10 * remaining_pellets
            + danger_penalty
        )