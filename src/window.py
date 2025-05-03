import tkinter as tk
import math
from board import Board
from gameImage import GameImage
from pacman import Pacman
from enemy import Enemy
from pickup import Pickup
from wall import Wall
from tree import Tree
import heuristique

class Window():

    def __init__(self, master):
        '''
        Initializes a Window Object that is the GUI for Pacman. The Window updates
        the GUI accordingly to the progression of the game, by the use of the Board
        object attribute initialized here. '''
        self._master = master

        screen_width = self._master.winfo_screenwidth()
        screen_height = self._master.winfo_screenheight()

        self._width = min(1000, int(screen_width * 0.8))
        self._height = min(850, int(screen_height * 0.8))

        self._images = GameImage()      # All images used for the game are stored as a GameImage() object

        self._ai_mode = False
        self.heuristique = None

        self._ai_button = tk.Button(self._master, text="Toggle AI", command=self._toggle_ai)
        self._ai_button.grid(row=2, column=0, sticky=tk.W)

        # All Tkinter Settings Initialized #
        self._canvas = tk.Canvas(self._master, width = self._width, height = self._height, background="black")
        self._canvas.grid(row=0,column=0, sticky=tk.N)
        
        self._score_label = tk.Label(self._master, text = '0', font = ('Arial', 20))
        self._level_label = tk.Label(self._master, text = '0', font = ('Arial', 20))
        self._lives_label = tk.Label(self._master, text = '0', font = ('Arial', 20))
        
        self._score_label.grid(row=1,column=0,sticky=tk.W)
        self._level_label.grid(row=1,column=0,sticky=tk.N)
        self._lives_label.grid(row=1,column=0,sticky=tk.E)
        
        self._master.resizable(width=False, height=False)
        self._master.title('Pacman')

        # Arrow Keys Binded #
        self._bindings_enabled( True )
        self._pause = False

        # Pacman Board Initialized #
        self.board = Board(self._width, self._height, self._images)
        self.board.new_level()          # Initializes a new level for Pacman

        self._master.resizable(width=True, height=True)

        x = (screen_width - self._width) // 2
        y = (screen_height - self._height) // 2
        self._master.geometry(f"{self._width}x{self._height}+{x}+{y}")

    # Drawing Functions #
    def _draw_board(self) -> None:
        ''' Draws the board given the game_objs in the board's set. '''
        total_height = self.board.square_height() # Approximately ~24
        total_width = self.board.square_width()   # Approximately ~36
        
        for game_obj in self.board.game_objects:
            if type(game_obj) == Wall:
                self._canvas.create_rectangle(game_obj.x * total_width,
                                              game_obj.y * total_height,
                                              (game_obj.x * total_width / total_width + 1) * total_width,
                                              (game_obj.y * total_height / total_height + 1) * total_height,
                                              fill = 'blue', width = 0)
        
            elif type(game_obj) == Pickup or type(game_obj) == Pacman or type(game_obj) == Enemy:
                self._canvas.create_image( game_obj.x * total_width + (total_width / 2),
                                           game_obj.y * total_height + (total_height / 2), image = game_obj._image)


    def _draw_stats(self) -> None:
        ''' Draws the statistics of Pacman for the player to see. '''
        self._score_label['text'] = self.board.pacman.display_score()
        self._level_label['text'] = self.board.pacman.display_level()
        self._lives_label['text'] = self.board.pacman.display_lives()

    def _adjust_board(self) -> None:
        ''' Deletes the board and then redraws to prevent animation overlapping. '''
        self._canvas.delete(tk.ALL)
        self._draw_board()
        self._draw_stats()

    # Level Completion / Transitioning Functions #
    def _check_for_completion(self) -> None:
        ''' Checks for completion of the level. If so, then displayCompleted is called
            to assist in the transition of the level change and loading screen. If not,
            then update the game as normal. '''
        # Completed Level GUI #
        if self.board.level_complete():
            self.display_completed()
            self._canvas.after(5000, self.run)

        # Gameover -> Stops Updating / Transitions to Gameover Screen #
        elif self.board.game_over:
            self._gameover_transition()

        elif self.board.pacman.is_respawning:
            self.board.pacman.is_respawning = False
            self._draw_board()
            self._master.after(550, self._respawn_transition())
            
        # Game Progress #
        else:
            self._canvas.after(125, self.update)
    
    def display_completed(self) -> None:
        ''' This functions is to add a proper transition between the completed
            level and the loading screen. Mainly for visual purposes to appear nicer. '''
        self.board.pacman.direction = None
        self._bindings_enabled(False)       # bindings are disabled during loading screen
        self._canvas.after(750, self.loading_screen)

    def loading_screen(self) -> None:
        ''' Adds a loading screen transition in between levels. '''
        self._canvas.delete(tk.ALL)
        self._canvas.create_image( self._width / 2, self._height / 2,
                                   image = self._images.return_image('loading_screen') )
        
        self._master.after(3500, self.level_advancement)

    def level_advancement(self) -> None:
        ''' Board loads up a new level once the previous level is completed. '''
        self.board.new_level()
        self._bindings_enabled(True)

    def gameover_screen(self) -> None:
        ''' Creates an image to display to the User when it is Game Over. '''
        self._canvas.create_image( self._width / 2, self._height / 2,
                                   image = self._images.return_image('over') )

    def _gameover_transition(self) -> None:
        self._bindings_enabled(False)       # bindings are disabled when game is over
        self.board.pacman._image = None     # pacman is no longer on the board, so no image required
        self.gameover_screen()

        
    def _respawn_transition(self) -> None:
        ''' Allows a transition to be in between respawning so that the game does not
            continue too quickly. '''
        self._adjust_board()
        self.delay_beginning()
        
        self._master.after(2100, self.update)
        
    def delay_beginning(self) -> None:
        ''' Delays the game by a short amount of time with GUI to
            inform the player when the game is going to start. This is
            in order to prevent the game starting immediately and affecting
            gameplay. '''
        def three():
            self._canvas.create_image(self._width / 2, self._height / 2,
                                                  image = self._images.return_image('three') )

        def two():
            self._adjust_board()
            self._canvas.create_image(self._width / 2, self._height / 2,
                                                  image = self._images.return_image('two') )

        def one():
            self._adjust_board()
            self._canvas.create_image(self._width / 2, self._height / 2,
                                                  image = self._images.return_image('one') )
        
        self._adjust_board()
        self._master.after(100, three)
        self._master.after(700, two)
        self._master.after(1300, one)
        
    # (Player) Binding Functions #
    def pacmans_direction(self, event: tk.Event) -> None:
        ''' Function that allows the player to move Pacman. Directions have
            to be validated in order to avoid stopped movement. nextDirection
            and lastDirection allow smoother control of Pacman. '''
        try:
            self.board.pacman.change_direction(event.keysym)

            if not self.board.validate_path( event.keysym ):
                self.board.pacman.next_direction = event.keysym
                self.board.pacman.direction = self.board.pacman.last_direction

            else:
                self.board.pacman.direction_image( self._images )
                self.board.pacman.next_direction = None

        except AttributeError:
            pass

    def check_pause(self) -> None:
        ''' Check_pause constantly calls itself to check when the player
            no longer wants the game to be paused. If so, then calls the
            update() function which will continue the game. '''
        if self._pause:
            self._master.after(1, self.check_pause)
        else:
            self.update()
    
    def _pause_game(self, event: tk.Event) -> None:
        ''' Pauses or unpauses the game by pressing the esc key. '''
        self._pause = not self._pause

    def _bindings_enabled(self, enabled: bool) -> None:
        ''' The boolean argument is what decides if the bindings are enabled or
            disabled. The bindings are enabled during play, but disabled in betwene
            level transition, specifically during the loading screen. '''
        if enabled:
            self._master.bind('<Left>', self.pacmans_direction)
            self._master.bind('<Right>', self.pacmans_direction)
            self._master.bind('<Up>', self.pacmans_direction)
            self._master.bind('<Down>', self.pacmans_direction)
            self._master.bind('<Escape>', self._pause_game)

        else:
            self._master.unbind('<Left>')
            self._master.unbind('<Right>')
            self._master.unbind('<Up>')
            self._master.unbind('<Down>')
            self._master.unbind('<Escape>')
    
    def _toggle_ai(self, which_heuristique):
        self._ai_mode = not self._ai_mode
        if self._ai_mode:
            self._ai_button.config(text="AI: ON")
            if which_heuristique == '1' : self.heuristique = heuristique.HeuristiqueSimple()
            elif which_heuristique == '2' : self.heuristique = heuristique.HeuristiqueLenteMaisOk()
            else : self.heuristique = heuristique.HeuristiqueNathan()
        else:
            self._ai_button.config(text="AI: OFF")
            self.heuristique = None

    # Main Functions #
    def update(self) -> None:
        '''
        Updates the game consistently throughout the game. Also, updates the
        directions of the player, and the objects that are on the board as objects
        are removed from the board by the player.
        '''

        if not self._pause:
            if self._ai_mode and not self.board.game_over:
                self._compute_ai_move()
            
            self.board.update_directions()
            self.board.update_board()
            self._check_for_completion()

            if not self.board.game_over:
                self._adjust_board()
            
        else:
            self._canvas.create_image(self._width / 2, self._height / 2,
                                      image = self._images.return_image('game_paused') )
            self.check_pause()
    
    def _compute_ai_move(self):
        import time

        if not hasattr(self, 'last_positions'):
            self.last_positions = []
        
        current_pos = (self.board.pacman.x, self.board.pacman.y)

        is_in_danger = self._is_pacman_in_danger()
        search_depth = 4 if is_in_danger else 3

        root_tree = Tree(0, [])
        root_tree.pos['pacman'] = [self.board.pacman.x, self.board.pacman.y]

        root_tree.is_enemy_invulnerable = not self.board.pacman.invulnerable

        for enemy in self.board.enemies:
            root_tree.pos[enemy.enemy_type] = [enemy.x, enemy.y]
        
        Tree.build_pacman_tree(root_tree, self.board, search_depth, True, self.heuristique)

        Tree.alpha_beta_calculus(root_tree, search_depth, -math.inf, math.inf, True)

        direction_values = {}
        current_direction = self.board.pacman.direction

        direction_bonus = {'Left': 0, 'Right': 0, 'Up': 0, 'Down': 0}
        direction_bonus[current_direction] = 8

        opposite_dir = {'Left': 'Right', 'Right': 'Left', 'Up': 'Down', 'Down': 'Up'}

        self.last_positions.append(current_pos)
        if len(self.last_positions) > 8:
            self.last_positions.pop(0)
        
        for child in root_tree.children:
            if hasattr(child, 'pacman_direction'):
                direction = child.pacman_direction
                if self.board.validate_path(direction):
                    dir_value = child.value + direction_bonus.get(direction, 0)

                    tunnel_bonus = self._evaluate_tunnel_strategic_value(direction)
                    dir_value += tunnel_bonus

                    next_pos = self._predict_next_position(current_pos, direction)
                    if next_pos in self.last_positions:
                        dir_value -= 50
                    
                    next_pos_board = (next_pos[1], next_pos[0])

                    if self._is_near_restricted_area(next_pos_board) and self._vulnerable_ghost_in_restricted_area():
                        dir_value = -200
                    
                    if direction == opposite_dir.get(current_direction):
                        enemy_close_behind = False
                        for enemy in self.board.enemies:
                            if self._is_enemy_close_behind(enemy, current_direction):
                                enemy_close_behind = True
                                break

                        if not enemy_close_behind and not self._is_escape_needed():
                            dir_value -= 80
                    
                    direction_values[direction] = dir_value
        
        if not direction_values:
            return
        
        best_direction = max(direction_values, key=direction_values.get)

        self.board.pacman.change_direction(best_direction)
        self.board.pacman.direction_image(self._images)
    
    def _is_near_restricted_area(self, pos):
        restricted_areas = [(13,11), (13,16), (12,11), (12,12), (12,13), (12,14), (12,15), (12,16),
                        (14,11), (14,12), (14,13), (14,14), (14,15), (14,16),
                        (11,13), (11,14), (15,13), (15,14)]
        
        x, y = pos
        for ry, rx in restricted_areas:
            if abs(y - ry) + abs (x - rx) <= 2:
                return True
        return False
    
    def _vulnerable_ghost_in_restricted_area(self):
        if not self.board.pacman.invulnerable:
            return False
        
        restricted_areas = [(13,11), (13,16), (12,11), (12,12), (12,13), (12,14), (12,15), (12,16),
                        (14,11), (14,12), (14,13), (14,14), (14,15), (14,16),
                        (11,13), (11,14), (15,13), (15,14)]
        
        for enemy in self.board.enemies:
            if (enemy.y, enemy.x) in restricted_areas:
                return True
        return False
    
    def _is_pacman_in_danger(self):
        pacman_pos = (self.board.pacman.x, self.board.pacman.y)
        danger_threshold = 3
        danger_count = 0

        if self.board.pacman.invulnerable:
            return False
        
        for enemy in self.board.enemies:
            if not self.board.pacman.invulnerable:
                dist = abs(pacman_pos[0] - enemy.x) + abs(pacman_pos[1] - enemy.y)
                if dist < danger_threshold:
                    danger_count += 1
        
        return danger_count > 1
    
    def _evaluate_tunnel_strategic_value(self, direction):
        pacman_pos = (self.board.pacman.x, self.board.pacman.y)

        tunnel_entries = [(0, 14), (27, 14)]

        next_pos = self._predict_next_position(pacman_pos, direction)

        for tx, ty in tunnel_entries:
            if abs(pacman_pos[0] - tx) + abs(pacman_pos[1] - ty) <= 2:
                if self._is_escape_needed():
                    return 200
        
        if self._is_escape_needed():
            current_tunnel_dist = min(abs(pacman_pos[0] - tx) + abs(pacman_pos[1] - ty) for tx, ty in tunnel_entries)
            next_tunnel_dist = min(abs(next_pos[0] - tx) + abs(next_pos[1] - ty) for tx, ty in tunnel_entries)

            if next_tunnel_dist < current_tunnel_dist:
                return 50
        
        return 0
    
    def _is_escape_needed(self):
        if self.board.pacman.invulnerable:
            return False
        
        pacman_pos = (self.board.pacman.x, self.board.pacman.y)

        approaching_ghosts = 0
        for enemy in self.board.enemies:
            dist = abs(pacman_pos[0] - enemy.x) + abs(pacman_pos[1] - enemy.y)
            if dist < 5:
                approaching_ghosts += 1
        
        return approaching_ghosts >= 2

    
    def _predict_next_position(self, current_pos, direction):
        x, y = current_pos

        if y == 14 and x == 0 and direction == 'Left':
            return (27, 14)
        elif y == 14 and x == 27 and direction == 'Right':
            return (0, 14)
        
        if direction == 'Left':
            return (x-1, y)
        elif direction == 'Right':
            return (x+1, y)
        elif direction == 'Up':
            return (x, y-1)
        elif direction == 'Down':
            return (x, y+1)
        return current_pos
    
    def _is_enemy_close_behind(self, enemy, pacman_direction):
        dx = abs(self.board.pacman.x - enemy.x)
        dy = abs(self.board.pacman.y - enemy.y)

        if dx + dy <= 2:
            if pacman_direction == 'Left' and enemy.x > self.board.pacman.x:
                return True
            elif pacman_direction == 'Right' and enemy.x < self.board.pacman.x:
                return True
            elif pacman_direction == 'Up' and enemy.y > self.board.pacman.y:
                return True
            elif pacman_direction == 'Down' and enemy.y < self.board.pacman.y:
                return True
        return False

    def run(self) -> None:
        self.delay_beginning()
        self._master.after(2000, self.update) # put again here to allow mainloop() to still occur and also call gameloop
        self._master.mainloop()
