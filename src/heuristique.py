class Heuristique():
    def evaluate(self, tree, board):
        pass
    
    @classmethod
    def _find_closest_object_distance(self, pos, objects_list):
        if not objects_list:
            return 100
        
        min_dist = float('inf')
        for obj_pos in objects_list:
            dist = abs(pos[0] - obj_pos[0]) + abs(pos[1] - obj_pos[1])
            min_dist = min(min_dist, dist)
        
        return min_dist
    
class HeuristiqueNathan(Heuristique):  
    def evaluate(self, tree, board):
        if tree.pacman_lives_number == 0:
            return float('-inf')
        
        pickups = []
        ghosts = []
        boost_pickups = []
        pacman_pos = tuple(tree.pos['pacman'])

        for game_obj in board.game_objects:
            obj_pos = (game_obj.x, game_obj.y)
            if type(game_obj).__name__ == 'Pickup':
                if game_obj.boost:
                    boost_pickups.append(obj_pos)
                else:
                    pickups.append(obj_pos)
            elif type(game_obj).__name__ == 'Enemy':
                ghosts.append(obj_pos)
        
        closest_pickup_dist = self._find_closest_object_distance(pacman_pos, pickups) if pickups else 100

        ghost_positions = []

        restricted_areas = [(13,11), (13,16), (12,11), (12,12), (12,13), (12,14), (12,15), (12,16),
                        (14,11), (14,12), (14,13), (14,14), (14,15), (14,16),
                        (11,13), (11,14), (15,13), (15,14)]
        
        for enemy_type in ['inky', 'pinky', 'blinky', 'clyde']:
            if enemy_type in tree.pos:
                ghost_pos = tuple(tree.pos[enemy_type])
                ghost_positions.append(ghost_pos)
        
        danger_score = 0
        if tree.is_enemy_invulnerable:
            for ghost_pos in ghost_positions:
                ghost_dist = abs(pacman_pos[0] - ghost_pos[0]) + abs(pacman_pos[1] - ghost_pos[1])

                if ghost_dist < 2:
                    danger_score -= 1000
                elif ghost_dist < 3:
                    danger_score -= 500
                elif ghost_dist < 5:
                    danger_score -= 200 / ghost_dist
                
                predicted_ghost_pos = self._predict_ghost_movement(ghost_pos, pacman_pos)
                predicted_dist = abs(pacman_pos[0] - predicted_ghost_pos[0]) + abs(pacman_pos[1] - predicted_ghost_pos[1])

                if predicted_dist < 3:
                    danger_score -= 800
                
                if self._is_pacman_trapped(pacman_pos, ghost_positions):
                    danger_score -= 1500
                
                tunnel_escape_value = self._evaluate_tunnel_escape(pacman_pos, ghost_positions)
                danger_score += tunnel_escape_value
        else:
            if self._find_closest_object_distance(pacman_pos, boost_pickups) < 3: return float('-inf')
            for ghost_pos in ghost_positions:
                ghost_dist = abs(pacman_pos[0] - ghost_pos[0]) + abs(pacman_pos[1] - ghost_pos[1])

                ghost_y, ghost_x = ghost_pos[1], ghost_pos[0]
                if (ghost_y, ghost_x) in restricted_areas:
                    continue

                if ghost_dist < 5:
                    danger_score += 400 / (ghost_dist + 0.1)

        closest_boost_dist = self._find_closest_object_distance(pacman_pos, boost_pickups) if boost_pickups else 100

        score = (
            + 80 * (1.0 / (closest_pickup_dist + 1))
            + danger_score
            + 150 * (1.0 / (closest_boost_dist + 1))
            + 30 * tree.pacman_lives_number
        )

        return score
    
    @classmethod
    def _predict_ghost_movement(self, ghost_pos, pacman_pos):
        ghost_x, ghost_y = ghost_pos
        pacman_x, pacman_y = pacman_pos

        dx, dy = 0, 0

        if ghost_x < pacman_x:
            dx = 1
        elif ghost_x > pacman_x:
            dx = -1
        
        if ghost_y < pacman_y:
            dy = 1
        elif ghost_y > pacman_y:
            dy = -1
        
        if abs(ghost_x - pacman_x) > abs(ghost_y - pacman_y):
            return (ghost_x + dx, ghost_y)
        else:
            return (ghost_x, ghost_y + dy)
    
    @classmethod
    def _is_pacman_trapped(self, pacman_pos, ghost_positions):
        if not ghost_positions:
            return False
        
        directions_blocked = 0
        px, py = pacman_pos

        for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dx, dy = direction
            check_pos = (px + dx, py + dy)

            for ghost_pos in ghost_positions:
                gx, gy = ghost_pos
                ghost_dist = abs(check_pos[0] - gx) + abs(check_pos[1] - gy)
                if ghost_dist < 3:
                    directions_blocked += 1
                    break
        
        return directions_blocked > 1
    
    @classmethod
    def _evaluate_tunnel_escape(self, pacman_pos, ghost_positions):
        tunnel_positions = [(0, 14), (27, 14)]
        
        if not ghost_positions:
            return 0
        
        min_ghost_dist = float('inf')
        for ghost_pos in ghost_positions:
            ghost_dist = abs(pacman_pos[0] - ghost_pos[0]) + abs(pacman_pos[1] - ghost_pos[1])
            min_ghost_dist = min(min_ghost_dist, ghost_dist)
        
        if min_ghost_dist < 5:
            tunnel_dist = min(abs(pacman_pos[0] - tx) + abs(pacman_pos[1] - ty) for tx, ty in tunnel_positions)

            tunnel_value = 300 / (tunnel_dist + 1) if tunnel_dist < 10 else 0
        
        return 0
    
class HeuristiqueClement(Heuristique):
    def evaluate(self, tree, game):
        # --- Constants ---
        PENALTY_GHOST_TOUCHING = -5000
        PENALTY_GHOST_IMMINENT = -1000
        PENALTY_GHOST_VERY_CLOSE = -500
        PENALTY_GHOST_NEAR = -100
        PENALTY_DEAD_END = -1500
        PENALTY_STUCK = -100

        BONUS_HUNT_SCARED_GHOST_EAT = 500
        BONUS_HUNT_SCARED_GHOST_CLOSE = 100
    
        pacman_pos = tuple(tree.pos['pacman'])
        prev_pos = getattr(tree, "prev_pacman_pos", None)  # Si dispo

        if tree.pacman_lives_number == 0:
            return float('-inf')

        score = 0

        # --- Collecte des objets ---
        pickups, boosts = [], []
        for game_obj in game.game_objects:
            obj_pos = (game_obj.x, game_obj.y)
            if type(game_obj).__name__ == 'Pickup':
                if game_obj.boost:
                    boosts.append(obj_pos)
                else:
                    pickups.append(obj_pos)

        num_pellets = len(pickups)
        pellet_distances = [abs(pacman_pos[0] - p[0]) + abs(pacman_pos[1] - p[1]) for p in pickups]
        closest_pellet_distance = min(pellet_distances) if pellet_distances else float('inf')
        num_boosts = len(boosts)
        boost_distances = [abs(pacman_pos[0] - b[0]) + abs(pacman_pos[1] - b[1]) for b in boosts]
        closest_boost_distance = min(boost_distances) if boost_distances else float('inf')
        
     
        # --- Fantômes ---
        current_ghost_positions = []
        for enemy_type in ['inky', 'pinky', 'blinky', 'clyde']:
            if enemy_type in tree.pos:
                current_ghost_positions.append(tuple(tree.pos[enemy_type]))

        # --- Danger Fantômes ---
        min_dist_to_ghost = float('inf')
        ghosts_very_close = 0
        directions = [(0,1),(1,0),(0,-1),(-1,0)]
        free_exits = 0

        for dx, dy in directions:
            next_pos = (pacman_pos[0]+dx, pacman_pos[1]+dy)
            if not any(g == next_pos for g in current_ghost_positions):
                free_exits += 1

        if tree.is_enemy_invulnerable: 
            for ghost_pos in current_ghost_positions:
                distance = abs(pacman_pos[0] - ghost_pos[0]) + abs(pacman_pos[1] - ghost_pos[1])
                min_dist_to_ghost = min(min_dist_to_ghost, distance)
                if distance == 0:
                    score += PENALTY_GHOST_TOUCHING
                elif distance == 1:
                    score += PENALTY_GHOST_IMMINENT
                    ghosts_very_close += 1
                elif distance == 2:
                    score += PENALTY_GHOST_VERY_CLOSE
                    ghosts_very_close += 1
                elif distance <= 4:
                    score += PENALTY_GHOST_NEAR / (distance + 1)

        # Dead-end panic
        if free_exits <= 1 and ghosts_very_close > 0:
            score += PENALTY_DEAD_END

        # --- Favorise la mobilité ---
        if free_exits >= 3:
            score += 50  # Encourage les positions avec plusieurs sorties
        elif free_exits == 2:
            score += 10

        # --- Pénalise la proximité de plusieurs fantômes ---
        ghosts_close = sum(1 for g in current_ghost_positions if abs(pacman_pos[0] - g[0]) + abs(pacman_pos[1] - g[1]) <= 2)
        if ghosts_close > 1:
            score += PENALTY_GHOST_VERY_CLOSE * ghosts_close

        # --- Pickups ---
        if num_pellets > 0:
            score -= 8 * num_pellets
            if closest_pellet_distance != float('inf'):
                score += 100.0 / (closest_pellet_distance + 0.5)
        else:
            score += 2000

        # --- Boosts ---
        if num_boosts > 0 and closest_boost_distance != float('inf'):
            if ghosts_very_close > 0:
                score += 200 / (closest_boost_distance + 0.2)
            elif min_dist_to_ghost <= 4:
                score += 50 / (closest_boost_distance + 0.5)
            else:
                score += 10 / (closest_boost_distance + 0.5)

        # --- Fantômes vulnérables ---
        if not tree.is_enemy_invulnerable:
            for ghost_pos in current_ghost_positions:
                distance = abs(pacman_pos[0] - ghost_pos[0]) + abs(pacman_pos[1] - ghost_pos[1])
                if distance == 0:
                    score += BONUS_HUNT_SCARED_GHOST_EAT
                elif distance < 3:
                    score += BONUS_HUNT_SCARED_GHOST_CLOSE / (distance + 0.1)
            # Évite de gaspiller un boost
            if num_boosts > 0 and closest_boost_distance < 3:
                score -= 100
                
        # --- Mangé au centre si invulnérable et pickups au centres ---
        if not tree.is_enemy_invulnerable and num_pellets > 0:
            center_zone = [(x, y) for x in range(11, 17) for y in range(11, 17)]
            center_pickups = [p for p in pickups if p in center_zone]
            if center_pickups:
                # Bonus proportionnel à la proximité du centre
                for p in center_pickups:
                    dist = abs(pacman_pos[0] - p[0]) + abs(pacman_pos[1] - p[1])
                    score += 200 / (dist + 0.5)        

        # --- Pénalise l'immobilisme ---
        if prev_pos is not None and prev_pos == pacman_pos:
            score += PENALTY_STUCK

        return score