from collections import deque
from pickup import Pickup
from enemy import Enemy
from wall import Wall

class PacmanAI:
    def __init__(self, board):
        self.board = board
        self.look_ahead_depth = 10
        self.ghost_danger_radius = 8
        self.boost_value_multiplier = 7
        self.ghost_value_when_vulnerable = 300
        self.previous_direction = None
        self.direction_history = []
        self.history_max_length = 10
        self.max_tunnel_x = 27
        
    def choose_direction(self):
        pacman = self.board.pacman
        possible_directions = ['Left', 'Right', 'Up', 'Down']
        valid_directions = []
        direction_scores = {}
        
        if pacman.direction:
            self.previous_direction = pacman.direction
            self.direction_history.append(pacman.direction)
            if len(self.direction_history) > self.history_max_length:
                self.direction_history.pop(0)
        
        for direction in possible_directions:
            if self._is_valid_direction(direction):
                valid_directions.append(direction)
        
        if not valid_directions:
            return self.previous_direction if self.previous_direction else 'Left'
            
        for direction in valid_directions:
            direction_scores[direction] = self._evaluate_direction(direction)

            if self._is_reversal(direction) and len(self.direction_history) >= 2:
                direction_scores[direction] -= 100
            
            if self._is_repetitive_pattern(direction):
                direction_scores[direction] -= 50
        
        best_direction = max(direction_scores, key=direction_scores.get)
        return best_direction
    
    def _is_valid_direction(self, direction):
        pacman = self.board.pacman
        y, x = pacman.y, pacman.x

        if self.board.edge_crossing(y, x):
            if direction == 'Left' and x == 0:
                return True
            elif direction == 'Right' and x == self.max_tunnel_x:
                return True
        
        try:
            return self.board.validate_path(direction)
        except IndexError:
            return False
    
    def _is_reversal(self, new_direction):
        if not self.previous_direction:
            return False
        
        opposite_directions = {
            'Left': 'Right',
            'Right': 'Left',
            'Up': 'Down',
            'Down': 'Up'
        }

        return new_direction == opposite_directions.get(self.previous_direction)
    
    def _is_repetitive_pattern(self, new_direction):
        if len(self.direction_history) < 4:
            return False
        
        last_four = ''.join(d[0] for d in self.direction_history[-4:])
        if last_four in ('LRLR', 'RLRL', 'UDUD', 'DUDU'):
            return True
        
        return False
        
    def _evaluate_direction(self, direction):
        pacman = self.board.pacman
        
        original_dir = pacman.direction
        
        pacman.direction = direction
        
        next_y, next_x = self._get_next_position(pacman.y, pacman.x, direction)

        if self.board.edge_crossing(pacman.y, pacman.x):
            if direction == 'Left' and pacman.x == 0:
                next_y, next_x = 14, self.max_tunnel_x
            elif direction == 'Right' and pacman.x == self.max_tunnel_x:
                next_y, next_x = 14, 0
        
        if not self._is_valid_position(next_y, next_x):
            pacman.direction = original_dir
            return -1000
        
        square_value = self._calculate_square_value(next_y, next_x)
        path_value = self._calculate_path_value(next_y, next_x)
        ghost_danger = self._calculate_ghost_danger(next_y, next_x, direction)
        escape_value = self._calculate_escape_routes(next_y, next_x)
        power_strategy_value = 0
        
        if self._is_power_pellet(next_y, next_x):
            power_strategy_value = self._evaluate_power_pellet_strategy(next_y, next_x)
        
        if pacman.invulnerable:
            ghost_danger *= 0.3
            path_value *= 0.7
        elif self._is_cornered(pacman.y, pacman.x):
            escape_value *= 3
            ghost_danger *= 1.5
        elif self._pellets_remaining() < 30:
            ghost_danger *= 1.2
        
        pacman.direction = original_dir

        total_score = square_value + path_value - ghost_danger + escape_value + power_strategy_value

        return total_score
    
    def _is_valid_position(self, y, x):
        return (0 <= y < len(self.board) and
                0 <= x < self.board.board_width() and
                type(self.board[y][x] != Wall))
    
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
        if not (0 <= y < len(self.board) and 0 <= x < self.board.board_width()):
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
                
            weight = 1.0 - (depth / (self.look_ahead_depth * 1.2))
            if weight < 0:
                weight = 0.1
                
            if 0 <= y < len(self.board) and 0 <= x < self.board.board_width():
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
    
    def _calculate_ghost_danger(self, y, x, direction):
        danger = 0
        pacman_invulnerable = self.board.pacman.invulnerable
        
        for enemy in self.board.enemies:
            if not enemy.invulnerable and pacman_invulnerable:
                continue
            
            ghost_distance = abs(enemy.y - y) + abs(enemy.x - x)
            
            if ghost_distance <= self.ghost_danger_radius:
                distance_factor = (self.ghost_danger_radius - ghost_distance + 1) / self.ghost_danger_radius
                base_danger = 400 * (distance_factor ** 2)

                if self._is_ghost_approaching(enemy, y, x, direction):
                    base_danger *= 1.5
                
                danger += base_danger
        
        return danger
    
    def _is_ghost_approaching(self, ghost, pacman_y, pacman_x, pacman_direction):
        if ghost.direction == 'Left' and ghost.x > pacman_x:
            return True
        elif ghost.direction == 'Right' and ghost.x < pacman_x:
            return True
        elif ghost.direction == 'Up' and ghost.y > pacman_y:
            return True
        elif ghost.direction == 'Down' and ghost.y < pacman_y:
            return True
        return False
    
    def _calculate_escape_routes(self, y, x):
        routes = 0
        open_squares = 0
        
        visited = set([(y, x)])
        queue = deque([(y, x, 0)])

        while queue:
            cy, cx, depth = queue.popleft()

            if depth > 3:
                continue

            open_squares += 1

            if depth == 1:
                routes += 1
            
            for next_y, next_x in [(cy+1, cx), (cy-1, cx), (cy, cx+1), (cy, cx-1)]:
                if (next_y, next_x) in visited:
                    continue

                if (0 <= next_y < len(self.board) and
                    0 <= next_x < self.board.board_width() and
                    type(self.board[next_y][next_x]) != Wall):
                    visited.add((next_y, next_x))
                    queue.append((next_y, next_x, depth + 1))
            
        return (routes * 30) + (open_squares * 10)
    
    def _is_cornered(self, y, x):
        walls_around = 0
        for ny, nx in [(y+1, x), (y-1, x), (y, x+1), (y, x-1)]:
            if not (0 <= ny < len(self.board) and 0 <= nx < self.board.board_width()):
                walls_around += 1
            elif type(self.board[ny][nx]) == Wall:
                walls_around += 1
        
        if walls_around >= 3:
            return True
        elif walls_around == 2:
            for enemy in self.board.enemies:
                ghost_distance = abs(enemy.y - y) + abs(enemy.x - x)
                if ghost_distance <= 5:
                    return True
        
        return False
    
    def _is_power_pellet(self, y, x):
        if not (0 <= y < len(self.board) and 0 <= x < self.board.board_width()):
            return False
        return (type(self.board[y][x]) == Pickup and self.board[y][x].boost)
    
    def _evaluate_power_pellet_strategy(self, y, x):
        nearby_ghosts = 0
        
        for enemy in self.board.enemies:
            if enemy.invulnerable:
                ghost_distance = abs(enemy.y - y) + abs(enemy.x - x)
                if ghost_distance < 10:
                    nearby_ghosts += 1
        
        if nearby_ghosts >= 3:
            return 350
        elif nearby_ghosts == 2:
            return 250
        elif nearby_ghosts == 1:
            return 150
        else:
            return 50
        
    def _pellets_remaining(self):
        count = 0
        for obj in self.board.game_objects:
            if type(obj) == Pickup:
                count += 1
        return count