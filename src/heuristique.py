from pacman import Pacman
from enemy import Enemy
from pickup import Pickup
import math

def heuristique(game_state):
    # Évalue l'etat des fantomes et le nombre restant de boule sur la map
    score = 0 

    for row in game_state:
        for cell in row:
            if type(cell) == Pickup:
                score -= 50 if cell.boostUp else 10
            if type(cell) == Enemy:
                score += -100 if cell.invulnerable else 500
            
    return score

def heuristique_distance(game_state):
    # Ajout de la distance entre pacman et les fantomes
    score = 0
    pacman_position = None
    enemies_positions = []

    for y, row in enumerate(game_state):
        for x, cell in enumerate(row):
            if type(cell) == Pacman:
                pacman_position = (x, y)
            elif type(cell) == Enemy:
                enemies_positions.append((x, y))
            elif type(cell) == Pickup:
                score -= 50 if cell.boostUp else 10
            elif type(cell) == Enemy:
                score += -100 if cell.invulnerable else 500

    if pacman_position:
        for enemy_position in enemies_positions:
            distance = math.sqrt((pacman_position[0] - enemy_position[0])**2 + 
                                 (pacman_position[1] - enemy_position[1])**2)
            score += distance * 10  

    return score