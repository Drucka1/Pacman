class Heuristique():
    pass
    
def manhattan_distance(pos1, pos2):
        return abs(pos1.x - pos2.x) + abs(pos1.y - pos2.y)    
    
class HeuristiqueSimple():
    def evaluate(self, game):
        ghost_distances = [
            abs(game.pacman.position.x - ghost.position.x) + abs(game.pacman.position.y - ghost.position.y)
            for ghost in game.ghosts
        ]
        min_distance = min(ghost_distances)

        # Pénalité si un fantôme est trop proche
        danger_penalty = -100 if min_distance <= 1 else 0

        # Bonus pour les grosses boules (boosts)
        boost_positions = [
            (y, x) for y, row in enumerate(game.layout) for x, cell in enumerate(row) if cell == 2
        ]
        boost_distances = [
            abs(game.pacman.position.x - boost[1]) + abs(game.pacman.position.y - boost[0])
            for boost in boost_positions
        ]
        closest_boost_distance = min(boost_distances) if boost_distances else float('inf')
        boost_bonus = 50 if closest_boost_distance < 5 else 0

        # Compter les boules restantes
        remaining_pellets = sum(row.count(1) for row in game.layout)

        scatter_bonus = 1000
        pellet_search_bonus = sum(
            max(0, 20 - (abs(game.pacman.position.x - x) + abs(game.pacman.position.y - y)))
            for y, row in enumerate(game.layout)
            for x, cell in enumerate(row) if cell == 1
        )  # Encourage Pacman to explore for pellets, with higher bonus for closer pellets

        # Calculate the barycenter of remaining pellets if there are less than 30
        remaining_pellet_positions = [
            (y, x) for y, row in enumerate(game.layout) for x, cell in enumerate(row) if cell == 1
        ]
        if len(remaining_pellet_positions) < 30 and remaining_pellet_positions:
            barycenter_x = sum(pos[1] for pos in remaining_pellet_positions) / len(remaining_pellet_positions)
            barycenter_y = sum(pos[0] for pos in remaining_pellet_positions) / len(remaining_pellet_positions)
            barycenter_distance = abs(game.pacman.position.x - barycenter_x) + abs(game.pacman.position.y - barycenter_y)
        else:
            barycenter_distance = 0

        # Bonus pour être loin des fantômes en mode scatter
        if game.scatter_mode:
            return (
            game.score
            + scatter_bonus
            + pellet_search_bonus
            + closest_boost_distance
            - 10 * remaining_pellets
            + danger_penalty
            - 5 * barycenter_distance
            )

        # Heuristique combinée
        return (
            game.score
            + boost_bonus
            + 5 * min_distance
            - 10 * remaining_pellets
            + danger_penalty
        )

    
class HeuristiqueLenteMaisOk():        
    def evaluate(self, game):
        # 1. Gérer les états terminaux
        if game.isWin():
            return float('inf')
        if game.isLose():
            return float('-inf') # Défaite = score minimal

        score = game.score # Commencer avec le score actuel du jeu

        pacman_pos = game.pacman.position
        pellets = game.pellets()
        boosts = game.boosts()
        ghosts = game.ghosts

        # 2. Gommes (Pellets)
        num_pellets = len(pellets)
        score -= 15 * num_pellets # Pénalité plus forte pour les gommes restantes

        if num_pellets > 0:
            pellet_distances = [manhattan_distance(pacman_pos, p) for p in pellets]
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
            boost_distances = [manhattan_distance(pacman_pos, b) for b in boosts]
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
            distance = manhattan_distance(pacman_pos, ghost.position)

            if game.scatter_chrono > 5: # Considérer le fantôme comme effrayé (seuil ajustable)
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