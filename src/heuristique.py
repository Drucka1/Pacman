class Heuristique():
    def evaluate(self, tree, game):
        pass
    
class HeuristiqueSimple(Heuristique):
    def evaluate(self, tree, game):
        ghost_distances = [
            abs(game.pacman.x - ghost.x) + abs(game.pacman.y - ghost.y)
            for ghost in game.enemies
        ]
        min_distance = min(ghost_distances)

        # Pénalité si un fantôme est trop proche
        danger_penalty = -100 if min_distance <= 1 else 0

        # Bonus pour les grosses boules (boosts)
        boost_positions = [
            (y, x) for y, row in enumerate(game.Gamestate) for x, cell in enumerate(row) if cell == 2
        ]
        boost_distances = [
            abs(game.pacman.x - boost[1]) + abs(game.pacman.y - boost[0])
            for boost in boost_positions
        ]
        closest_boost_distance = min(boost_distances) if boost_distances else float('inf')
        boost_bonus = 50 if closest_boost_distance < 5 else 0

        # Compter les boules restantes
        remaining_pellets = sum(row.count(1) for row in game.Gamestate)

        scatter_bonus = 1000
        pellet_search_bonus = sum(
            max(0, 20 - (abs(game.pacman.x - x) + abs(game.pacman.y - y)))
            for y, row in enumerate(game.Gamestate)
            for x, cell in enumerate(row) if cell == 1
        )  # Encourage Pacman to explore for pellets, with higher bonus for closer pellets

        # Calculate the barycenter of remaining pellets if there are less than 30
        remaining_pellet_positions = [
            (y, x) for y, row in enumerate(game.Gamestate) for x, cell in enumerate(row) if cell == 1
        ]
        if len(remaining_pellet_positions) < 30 and remaining_pellet_positions:
            barycenter_x = sum(pos[1] for pos in remaining_pellet_positions) / len(remaining_pellet_positions)
            barycenter_y = sum(pos[0] for pos in remaining_pellet_positions) / len(remaining_pellet_positions)
            barycenter_distance = abs(game.pacman.x - barycenter_x) + abs(game.pacman.y - barycenter_y)
        else:
            barycenter_distance = 0
            
        score = game.numberOfEatenPickup()*10 + game.numberOfEatenBoost()*500

        # Bonus pour être loin des fantômes en mode scatter
        """if game.scatter_mode:
            return (
            score
            + scatter_bonus
            + pellet_search_bonus
            + closest_boost_distance
            - 10 * remaining_pellets
            + danger_penalty
            - 5 * barycenter_distance
            )"""

        # Heuristique combinée
        return (
            score
            + boost_bonus
            + 5 * min_distance
            - 10 * remaining_pellets
            + danger_penalty
        )

    
class HeuristiqueLenteMaisOk(Heuristique):        
    def evaluate(self, tree, game):
        # 1. Gérer les états terminaux
        if game.isWin():
            return float('inf')
        if game.isLose():
            return float('-inf') # Défaite = score minimal

        # Commencer avec le score actuel du jeu
        score = game.numberOfEatenPickup()*5 + game.numberOfEatenBoost()*500

        pacman = game.pacman
        pellets = game.pellets()
        boosts = game.boosts()
        ghosts = game.enemies

        # 2. Gommes (Pellets)
        num_pellets = len(pellets)
        score -= 15 * num_pellets # Pénalité plus forte pour les gommes restantes

        if num_pellets > 0:
            pellet_distances = [abs(pacman.x - p[0]) + abs(pacman.y - p[1]) for p in pellets]
            closest_pellet_distance = min(pellet_distances)
            # Bonus pour être proche de la gomme la plus proche (plus fort quand très proche)
            score += 10.0 / (closest_pellet_distance + 1)
        else:
            # Si aucune gomme, très bon état (presque gagné)
            score += 500

        # 3. Boosts (Super-Pastilles)
        num_boosts = len(boosts)
        score -= 20 * num_boosts # Légère pénalité pour les boosts non consommés

        if num_boosts > 0:
            boost_distances = [abs(pacman.x - b[0]) + abs(pacman.y - b[1]) for b in boosts]
            closest_boost_distance = min(boost_distances)
            # Bonus pour être proche d'un boost, surtout si des fantômes menaçants sont là (voir section fantômes)
            score += 5.0 / (closest_boost_distance + 1)
        else:
            closest_boost_distance = float('inf') # Pas de boost restant

        # 4. Fantômes
        min_dist_normal_ghost = float('inf')
        bonus_scared_ghost = 0
        PENALTY_CLOSE_GHOST = -200  # Forte pénalité si un fantôme normal est TRES proche
        PENALTY_NEAR_GHOST = -50    # Pénalité moindre si un fantôme normal est proche
        BONUS_CHASE_GHOST = 150     # Bonus de base pour chasser un fantôme effrayé
        FACTOR_SCARED_TIMER = 2     # Bonus supplémentaire basé sur le temps restant

        # Pour rendre le bonus de proximité au boost dépendant des fantômes:
        is_normal_ghost_near = False

        for ghost in ghosts:
            distance = abs(pacman.x - ghost.x) + abs(pacman.y - ghost.y)

            if False :#game.scatter_chrono > 5:#  Considérer le fantôme comme effrayé (seuil ajustable)
                # Bonus pour être proche d'un fantôme effrayé
                # Le bonus augmente avec le temps restant et diminue avec la distance
                bonus_scared_ghost += (BONUS_CHASE_GHOST + game.scatter_chrono * FACTOR_SCARED_TIMER) / (distance + 1)
            
            else: # Fantôme normal ou presque plus effrayé = menace
                min_dist_normal_ghost = min(min_dist_normal_ghost, distance)
                if distance < 5: # Seuil pour considérer un fantôme comme "proche"
                    is_normal_ghost_near = True

        # Appliquer les pénalités pour les fantômes normaux
        if min_dist_normal_ghost <= 2:
            score += PENALTY_CLOSE_GHOST * 5 # Danger immédiat ! Très forte pénalité.
        elif min_dist_normal_ghost <= 5:
            score += PENALTY_CLOSE_GHOST
        elif min_dist_normal_ghost <= 7:
            score += PENALTY_NEAR_GHOST
        # Pas de bonus direct pour être loin, la pénalité pour être proche suffit généralement

        score += bonus_scared_ghost # Ajouter le bonus total pour la chasse aux fantômes effrayés

        # Bonus supplémentaire pour être près d'un boost SI un fantôme normal est proche
        if is_normal_ghost_near and num_boosts > 0:
            score += 20.0 / (closest_boost_distance + 1) # Encouragement plus fort à prendre le boost

        return score
    
class HeuristiqueNathan(Heuristique):  
    def evaluate(self, tree, board):
        if tree.pacman_lives_number == 0:
            return -10000
        
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
        ghost_in_restricted = False

        restricted_areas = [(13,11), (13,16), (12,11), (12,12), (12,13), (12,14), (12,15), (12,16),
                        (14,11), (14,12), (14,13), (14,14), (14,15), (14,16),
                        (11,13), (11,14), (15,13), (15,14)]
        
        for enemy_type in ['inky', 'pinky', 'blinky', 'clyde']:
            if enemy_type in tree.pos:
                ghost_pos = tuple(tree.pos[enemy_type])
                ghost_positions.append(ghost_pos)

                if (ghost_pos[1], ghost_pos[0]) in restricted_areas:
                    ghost_in_restricted = True
        
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

    
    @classmethod
    def _find_closest_object_distance(self, pos, objects_list):
        if not objects_list:
            return 100
        
        min_dist = float('inf')
        for obj_pos in objects_list:
            dist = abs(pos[0] - obj_pos[0]) + abs(pos[1] - obj_pos[1])
            min_dist = min(min_dist, dist)
        
        return min_dist
