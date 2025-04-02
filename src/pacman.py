import pygame
from maze import Maze
from ghost import *
from utils import *

class Pacman:
    def __init__(self):
        self.position = Coordinate(14,23)  # Starting position
        self.direction = Direction.STOP

class PacmanGame:
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Pacman")
        self.clock = pygame.time.Clock()

        self.maze = Maze()  # Adjust based on your tile size
        self.pacman = Pacman()
        self.blinky = Blinky(Coordinate(12,15), self.maze.width)
        self.pinky = Pinky(Coordinate(13,15), self.maze.height, self.maze.width)
        self.inky = Inky(Coordinate(14,15))  # Pass blinky instance
        self.clyde = Clyde(Coordinate(15,15), self.maze.height)
        self.ghosts = [self.blinky, self.pinky, self.inky, self.clyde]

        self.tile_size = min(self.width // self.maze.width, self.height // self.maze.height)
        self.running = True

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.pacman.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.pacman.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.pacman.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.pacman.direction = Direction.DOWN

    def update(self):
        # Update Pac-Man's position
        new_position = self.pacman.position + self.pacman.direction.value
        
        self.maze.update()

        if not self.maze.check_collision(new_position):
            self.pacman.position = new_position
            self.maze.eat(self.pacman.position)

        self.inky.move(self.pacman.position, self.pacman.direction, self.maze)
        self.pinky.move(self.pacman.position, self.pacman.direction, self.maze)
        self.blinky.move(self.pacman.position, self.maze)
        self.clyde.move(self.maze)

    def render(self):
        self.screen.fill((0, 0, 0))  # Black background

        # Draw the maze
        for y, row in enumerate(self.maze.layout):
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
        pacman_rect = pygame.Rect(self.pacman.position.x * self.tile_size, self.pacman.position.y * self.tile_size, self.tile_size, self.tile_size)
        pygame.draw.ellipse(self.screen, (255, 255, 0), pacman_rect)  # Yellow Pac-Man

        # Draw ghosts
        for ghost in self.ghosts:
            ghost_rect = pygame.Rect(ghost.position.x * self.tile_size, ghost.position.y * self.tile_size, self.tile_size, self.tile_size)
            pygame.draw.rect(self.screen, ghost.color, ghost_rect)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_input()
            self.update()
            self.render()
            self.clock.tick(8)  # Limit frame rate to 10 FPS
        pygame.quit()

if __name__ == "__main__":
    game = PacmanGame(560, 620)
    game.run()
    
