import pygame
from game import Game
from ghost import *
from utils import *

class PacmanGame:
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Pacman")
        self.clock = pygame.time.Clock()

        self.game = Game()  # Adjust based on your tile size

        self.tile_size = min(self.width // self.game.width, self.height // self.game.height)
        self.running = True

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.game.pacman.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.game.pacman.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.game.pacman.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.game.pacman.direction = Direction.DOWN

    def update(self):
        # Update Pac-Man's position
        new_position = self.game.pacman.position + self.game.pacman.direction.value
        
        self.game.update()

        if not self.game.check_collision(new_position):
            self.game.pacman.position = new_position
            self.game.eat(self.game.pacman.position)

        self.game.inky.move(self.game)
        self.game.pinky.move(self.game)
        self.game.blinky.move(self.game)
        self.game.clyde.move(self.game)
        
        if self.game.is_game_over():
            if not any(1 in row for row in self.game.layout): print("Gagné")
            else : print("Perdu")
            self.running = False
            

    def render(self):
        self.screen.fill((0, 0, 0))  # Black background

        # Draw the game
        for y, row in enumerate(self.game.layout):
            for x, cell in enumerate(row):
                rect = pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                if cell == 0:
                    pygame.draw.rect(self.screen, (0, 0, 255), rect)  # Blue walls
                elif cell == 1:
                    # Draw small pellet
                    pygame.draw.circle(self.screen, (255, 255, 255), rect.center, self.tile_size // 8)
                elif cell == 2:
                    # Draw large pellet
                    pygame.draw.circle(self.screen, (255, 255, 255), rect.center, self.tile_size // 4)

        # Draw Pac-Man
        pacman_rect = pygame.Rect(self.game.pacman.position.x * self.tile_size, self.game.pacman.position.y * self.tile_size, self.tile_size, self.tile_size)
        pygame.draw.ellipse(self.screen, (255, 255, 0), pacman_rect)  # Yellow Pac-Man

        # Draw ghosts
        for ghost in self.game.ghosts:
            ghost_rect = pygame.Rect(ghost.position.x * self.tile_size, ghost.position.y * self.tile_size, self.tile_size, self.tile_size)
            pygame.draw.rect(self.screen, ghost.color, ghost_rect)

        pygame.display.flip()

    def run(self):
        heur = Simple_Heuristique()
        a_b = Alpha_Beta(heur)
        
        while self.running:
            self.handle_input()
            # Call alpha_beta with the correct parameters
            self.render()
            
            # Profondeur max 3
            _,direction = a_b.run(Alpha_Beta_Leaf(self.game), 3, -float("inf"), float("inf"), True)
            self.game.pacman.direction = direction
            
            #self.handle_input()
            self.update()
            self.clock.tick(10)  # Limit frame rate to 10 FPS
        pygame.quit()

if __name__ == "__main__":
    game = PacmanGame(560, 620)
    game.run()