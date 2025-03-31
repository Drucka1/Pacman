from collections import deque
from pickup import Pickup
from enemy import Enemy
from wall import Wall

class PacmanAI:
    def __init__(self, board):
        self.board = board
        self.look_ahead_depth = 8
        self.ghost_danger_radius = 5
        self.boost_value_multiplier = 5
        self.ghost_value_when_vulnerable = 200
    
    def choose_direction(self):
        pacman = self.board.pacman
        possible_directions = ['Left', 'Right', 'Up', 'Down']
        valid_directions = []
        direction_scores = {}

        for direction in possible_directions:
            if self._is_valid_direction(direction):
                valid_directions.append(direction)
        
        if not valid_directions and self._is_valid_direction(pacman.direction):
            return pacman.direction
        elif not valid_directions:
            return 'Left'
        
        for direction in valid_directions:
            direction_scores[direction] = self._evaluate_direction(direction)
        
        best_direction = max(direction_scores, key=direction_scores.get)
        return best_direction
    
    def _is_valid_direction(self, direction):
        return self.board.validate_path(direction)
    
    def _evaluate_direction(self, direction):
        pacman = self.board.pacman

        original_pos = (pacman.y, pacman.x)
        original_dir = pacman.direction

        pacman.direction = direction

        next_y, next_x = self._get_next_position(pacman.y, pacman.x, direction)

        score = self._calculate_square_value(next_y, next_x)

        path_value = self._calculate_path_value(next_y, next_x)
        score += path_value

        ghost_danger = self._calculate_ghost_danger(next_y, next_x)
        score -= ghost_danger

        escape_value = self._calculate_escape_routes(next_y, next_x)
        score += escape_value

        if self._is_power_pellet(next_y, next_x):
            power_strategy_value = self._evaluate_power_pellet_strategy(next_y, next_x)
            score += power_strategy_value
        
        pacman.direction = original_dir

        return score
    
    def _get_next_position(self, y, x, direction):
        if direction == 'Left':
            return y, x - 1
        elif direction == 'Right':
            return y, x + 1
        elif direction == 'Up':
            return y - 1, x
        elif direction == 'Down':
            return y + 1, x
        return y, x
    
    def _calculate_square_value(self, y, x):
        if y < 0 or y >= len(self.board) or x < 0 or x >= self.board.board_width():
            return -1000
        
        square_content = self.board[y][x]

        if square_content is None:
            return 0
        elif type(square_content) == Pickup:
            if square_content.boost:
                return 50 * self.boost_value_multiplier
            return 10
        elif type(square_content) == Enemy:
            if not square_content.invulnerable and self.board.pacman.invulnerable:
                return self.ghost_value_when_vulnerable
            return -500
        elif type(square_content) == Wall:
            return -1000
        
        return 0
    
    def _calculate_path_value(self, start_y, start_x):
        visited = set([(start_y, start_x)])
        queue = deque([(start_y, start_x, 0)])
        total_value = 0

        while queue:
            y, x, depth = queue.popleft()

            if depth > self.look_ahead_depth:
                continue

            weight = 1.0 - (depth / (self.look_ahead_depth * 1.5))
            if weight < 0:
                weight = 0
            
            square_content = self.board[y][x]
            if type(square_content) == Pickup:
                if square_content.boost:
                    total_value += 50 * weight * self.boost_value_multiplier
                else:
                    total_value += 10 * weight
            
            for next_y, next_x in [(y+1, x), (y-1, x), (y, x+1), (y, x-1)]:
                if (next_y, next_x) in visited:
                    continue

                if (0 <= next_y < len(self.board) and
                    0 <= next_x < self.board.board_width() and
                    type(self.board[next_y][next_x]) != Wall):
                    visited.add((next_y, next_x))
                    queue.append((next_y, next_x, depth + 1))
        
        return total_value
    
    def _calculate_ghost_danger(self, y, x):
        danger = 0
        pacman_invulnerable = self.board.pacman.invulnerable

        for enemy in self.board.enemies:
            if not enemy.invulnerable and pacman_invulnerable:
                continue

            ghost_distance = abs(enemy.y - y) + abs(enemy.x - x)

            if ghost_distance <= self.ghost_danger_radius:
                distance_factor = (self.ghost_danger_radius - ghost_distance + 1) / self.ghost_danger_radius
                danger += 300 * distance_factor
        
        return danger
    
    def _calculate_escape_routes(self, y, x):
        routes = 0

        for next_y, next_x in [(y+1, x), (y-1, x), (y, x+1), (y, x-1)]:
            if (0 <= next_y < len(self.board) and
                0 <= next_x < self.board.board_width() and
                type(self.board[next_y][next_x]) != Wall):
                routes += 1
        
        return routes * 20
    
    def _is_power_pellet(self, y, x):
        return (type(self.board[y][x]) == Pickup and self.board[y][x].boost)
    
    def _evaluate_power_pellet_strategy(self, y, x):
        nearby_ghosts = 0

        for enemy in self.board.enemies:
            if enemy.invulnerable:
                ghost_distance = abs(enemy.y - y) + abs(enemy.x - x)
                if ghost_distance < 10:
                    nearby_ghosts += 1
        
        return nearby_ghosts * 100