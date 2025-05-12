from random import random

from tree import Direction


class Heuristique():
    def evaluate(self, tree, board):
        pass

    @staticmethod
    def manhattan_dist(pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    @staticmethod
    def find_closest_object_distance(pos, objects_list):
        if not objects_list:
            return 100
        
        min_dist = float('inf')
        for obj_pos in objects_list:
            dist = Heuristique.manhattan_dist(pos, obj_pos)
            min_dist = min(min_dist, dist)
        
        return min_dist
    
class HeuristiqueNathan(Heuristique):   
    restricted_areas = [(13,11), (13,16), (12,11), (12,12), (12,13), (12,14), (12,15), (12,16),
                    (14,11), (14,12), (14,13), (14,14), (14,15), (14,16),
                    (11,13), (11,14), (15,13), (15,14)]
    
    def evaluate(self, tree, board):
        if tree.pacman_lives_number == 0:
            return float('-inf')
        
        ghost_positions = []
        pacman_pos = tree.pos['pacman']
        boost_pickups = tree.boosts 
        pickups = tree.pellets
        for ghost in ['inky', 'pinky', 'blinky', 'clyde']:
            ghost_positions.append(tree.pos[ghost])    
        
        closest_pickup_dist = Heuristique.find_closest_object_distance(pacman_pos, pickups) if pickups else 100
        
        danger_score = 0
        if tree.scatter_mode:
            for ghost_pos in ghost_positions:
                ghost_dist = abs(pacman_pos[0] - ghost_pos[0]) + abs(pacman_pos[1] - ghost_pos[1])

                if ghost_dist < 2:
                    danger_score -= 1000
                elif ghost_dist < 3:
                    danger_score -= 500
                elif ghost_dist < 5:
                    danger_score -= 200 / ghost_dist
                
                predicted_ghost_pos = HeuristiqueNathan.predict_ghost_movement(ghost_pos, pacman_pos)
                predicted_dist = abs(pacman_pos[0] - predicted_ghost_pos[0]) + abs(pacman_pos[1] - predicted_ghost_pos[1])

                if predicted_dist < 3:
                    danger_score -= 800
                
                if HeuristiqueNathan.is_pacman_trapped(pacman_pos, ghost_positions):
                    danger_score -= 1500
                
                tunnel_escape_value = HeuristiqueNathan.evaluate_tunnel_escape(pacman_pos, ghost_positions)
                danger_score += tunnel_escape_value
        else:
            if Heuristique.find_closest_object_distance(pacman_pos, boost_pickups) < 3: return float('-inf')
            for ghost_pos in ghost_positions:
                ghost_dist = abs(pacman_pos[0] - ghost_pos[0]) + abs(pacman_pos[1] - ghost_pos[1])

                ghost_y, ghost_x = ghost_pos[1], ghost_pos[0]
                if (ghost_y, ghost_x) in HeuristiqueNathan.restricted_areas:
                    continue

                if ghost_dist < 5:
                    danger_score += 400 / (ghost_dist + 0.1)

        closest_boost_dist = Heuristique.find_closest_object_distance(pacman_pos, boost_pickups) if boost_pickups else 100

        score = (
            + 80 * (1.0 / (closest_pickup_dist + 1))
            + danger_score
            + 150 * (1.0 / (closest_boost_dist + 1))
            + 30 * tree.pacman_lives_number
        )

        return score
    
    @staticmethod
    def predict_ghost_movement(ghost_pos, pacman_pos):
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
    
    @staticmethod
    def is_pacman_trapped(pacman_pos, ghost_positions):
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
    
    @staticmethod
    def evaluate_tunnel_escape(pacman_pos, ghost_positions):
        tunnel_positions = [(0, 14), (27, 14)]
        
        if not ghost_positions:
            return 0
        
        min_ghost_dist = float('inf')
        for ghost_pos in ghost_positions:
            ghost_dist = abs(pacman_pos[0] - ghost_pos[0]) + abs(pacman_pos[1] - ghost_pos[1])
            min_ghost_dist = min(min_ghost_dist, ghost_dist)
        
        if min_ghost_dist < 5:
            tunnel_dist = min(abs(pacman_pos[0] - tx) + abs(pacman_pos[1] - ty) for tx, ty in tunnel_positions)        
        return 0
    
class HeuristiqueClement(Heuristique):    
    
    def evaluate(self, tree, board):
        # --- Constants ---
        PENALTY_GHOST_TOUCHING = -10000    # Avant : -5000
        PENALTY_GHOST_IMMINENT = -2000     # Avant : -400
        PENALTY_GHOST_VERY_CLOSE = -1000   # Avant : -200
        PENALTY_GHOST_NEAR = -300          # Avant : -50
        PENALTY_DEAD_END = -1000           # Avant : -300

        BONUS_HUNT_SCARED_GHOST_EAT = 75 
        BONUS_HUNT_SCARED_GHOST_CLOSE = 20 
    
        pacman_pos = tuple(tree.pos['pacman'])

        score = tree.pacman_score * 0.1 + tree.pacman_lives_number * 500

        pickups, boosts = tree.pellets, tree.boosts

        num_pellets = len(pickups)
        pellet_distances = [Heuristique.manhattan_dist(pacman_pos, p) for p in pickups]
        closest_pellet_distance = min(pellet_distances) if pellet_distances else float('inf')
        
        num_boosts = len(boosts)
        boost_distances = [Heuristique.manhattan_dist(pacman_pos, b) for b in boosts]
        closest_boost_distance = min(boost_distances) if boost_distances else float('inf')

        current_ghost_positions = []
        for enemy_type in ['inky', 'pinky', 'blinky', 'clyde']:
            if enemy_type in tree.pos:
                current_ghost_positions.append(tree.pos[enemy_type])

        #FAVORISE DISTANCE AU PELLET LE PLUS PROCHE      
        if num_pellets > 0:
            score -= 2 * num_pellets
            if closest_pellet_distance != float('inf'):
                score += 1000.0 / (closest_pellet_distance + 0.5) 
        else:
            score += 5000
            
        #MODE VULNERABLE             
        if not tree.scatter_mode: 
            free_exits = 0
            directions = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
            for direction in directions:
                dx, dy = direction.value
                next_pos = (pacman_pos[0]+dx, pacman_pos[1]+dy)
                if not any(g == next_pos for g in current_ghost_positions):
                    free_exits += 1
                
            if free_exits <= 1 and ghosts_very_close > 0:
                score += PENALTY_DEAD_END
            
            min_dist_to_ghost = float('inf')
            ghosts_very_close = 0    
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
                    score += PENALTY_GHOST_NEAR
            
            if num_boosts > 0 and closest_boost_distance != float('inf'):
                if ghosts_very_close > 0:
                    score += 200 / (closest_boost_distance + 0.2)
                elif min_dist_to_ghost <= 4:
                    score += 50 / (closest_boost_distance + 0.5)
                else:
                    score += 10 / (closest_boost_distance + 0.5)
                        
        #MODE EFFRAYE
        if tree.scatter_mode:
            for ghost_pos in current_ghost_positions:
                distance = abs(pacman_pos[0] - ghost_pos[0]) + abs(pacman_pos[1] - ghost_pos[1])
                if distance == 0:
                    score += BONUS_HUNT_SCARED_GHOST_EAT
                elif distance < 3:
                    score += BONUS_HUNT_SCARED_GHOST_CLOSE / (distance + 0.1)

            if num_pellets > 0:
                center_zone = [(x, y) for x in range(11, 17) for y in range(11, 17)]
                center_pickups = [p for p in pickups if p in center_zone]
                if center_pickups:
                    for p in center_pickups:
                        dist = abs(pacman_pos[0] - p[0]) + abs(pacman_pos[1] - p[1])
                        score += 200 / (dist + 0.5)
                
            min_dist_to_ghost = float('inf')
            for ghost_pos in current_ghost_positions:
                distance = abs(pacman_pos[0] - ghost_pos[0]) + abs(pacman_pos[1] - ghost_pos[1])
                min_dist_to_ghost = min(min_dist_to_ghost, distance)      
            if num_boosts > 0 and closest_boost_distance <= 4 and min_dist_to_ghost >= 4:
                return float('-inf')
        
        return score

class HeuristiqueSimple(Heuristique):
    def evaluate(self, tree, board):
        pacman_pos = tuple(tree.pos['pacman'])
        pickups = tree.pellets
        ghosts = [tree.pos[g] for g in ['inky', 'pinky', 'blinky', 'clyde'] if g in tree.pos]

        # Score de base : nombre de pellets restants (moins il y en a, mieux c'est)
        score = -10 * len(pickups)

        # Bonus pour la proximité du pellet le plus proche
        if pickups:
            pellet_distances = [Heuristique.manhattan_dist(pacman_pos, p) for p in pickups]
            closest_pellet_distance = min(pellet_distances)
            score += 100 / (closest_pellet_distance + 1)

        # Pénalité pour la proximité des fantômes (plus ils sont proches, plus c'est dangereux)
        for ghost_pos in ghosts:
            dist = Heuristique.manhattan_dist(pacman_pos, ghost_pos)
            if dist == 0:
                score -= 10000  # Fantôme sur Pacman = mort
            elif dist == 1:
                score -= 1000
            elif dist == 2:
                score -= 300
            elif dist <= 4:
                score -= 50

        return score