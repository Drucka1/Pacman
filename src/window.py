import tkinter as tk
import math
from board import Board
from gameImage import GameImage
from pacman import Pacman
from enemy import Enemy
from pickup import Pickup
from wall import Wall
from tree import Tree
from heuristique import HeuristiqueClement, HeuristiqueNathan

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
        self.ai_next_positions = []
        self.ai_tree = None
        self.ai_current_tree = None
        self.ai_no_remaining_moves = True
        self.ai_next_move_index = 0

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
            if which_heuristique == '1' : self.heuristique = HeuristiqueNathan()
            else : self.heuristique = HeuristiqueClement()
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
            if self._ai_mode and self.ai_no_remaining_moves and not self.board.game_over:
                self._compute_ai_move()
                self.ai_no_remaining_moves = False
            
            if not(self._ai_mode):
                print(self.board.pacman.return_location(), end="")
                print({enemy.enemy_type : (enemy.x, enemy.y) for enemy in self.board.enemies})
                self.board.update_directions()
                self.board.update_board()
            else:
                print(self.ai_current_tree.pos)
                self.board.pacman.change_direction(self.ai_current_tree.pacman_direction)
                self.board.pacman.direction_image(self._images)
                self.board.update_directions()
                
                self.ai_current_tree = self.ai_current_tree.children[self.ai_next_positions[self.ai_next_move_index]]
                self.ai_next_move_index += 1
                
                
                self.board.game_objects = { objs for rows in self.board.Gamestate for objs in rows if objs is not None }
                self.board.pacman = self.board.pacman_location()
                y, x = self.board.pacman.return_location()
                self.board._validate_movement(y, x)       
                for enemy in self.board.enemies:
                    enemy.last_location = enemy.return_location()
                    if enemy.enemy_type == Enemy.blinky:
                        enemy.x = self.ai_current_tree.pos['blinky'][0]
                        enemy.y = self.ai_current_tree.pos['blinky'][1]
                    elif enemy.enemy_type == Enemy.inky:
                        enemy.x = self.ai_current_tree.pos['inky'][0]
                        enemy.y = self.ai_current_tree.pos['inky'][1]
                    elif enemy.enemy_type == Enemy.pinky:
                        enemy.x = self.ai_current_tree.pos['pinky'][0]
                        enemy.y = self.ai_current_tree.pos['pinky'][1]
                    else:
                        enemy.x = self.ai_current_tree.pos['clyde'][0]
                        enemy.y = self.ai_current_tree.pos['clyde'][1]
                
                    if (enemy.y, enemy.x) == (y, x):
                        self.board._validate_enemy_death_or_kill(enemy)
                    else:
                        self.board._update_enemy_movement(enemy)
                self.board._game_continuation(y,x)
                
                if self.ai_next_move_index == len(self.ai_next_positions):
                    self.ai_no_remaining_moves = True
                else:
                    self.ai_current_tree = self.ai_current_tree.children[self.ai_next_positions[self.ai_next_move_index]]
                    self.ai_next_move_index += 1
            self._check_for_completion()

            if not self.board.game_over:
                self._adjust_board()
            
        else:
            self._canvas.create_image(self._width / 2, self._height / 2,
                                      image = self._images.return_image('game_paused') )
            self.check_pause()
        
    
    def add_pos_indices(self, tree):
        children = tree.children
        children_length = len(children)
        
        if children_length > 0:
            tree_value = tree.value
            
            for i in range(children_length):
                child = children[i]
                if child.value == tree_value:
                    self.ai_next_positions.append(i)
                    self.add_pos_indices(child)
                    return
    
    def _compute_ai_move(self):
        board = self.board
        pellets = [
            (x, y)
            for y, row in enumerate(board.Gamestate)
            for x, obj in enumerate(row)
            if isinstance(obj, Pickup) and obj.pickup_type == Pickup.pickup
        ]
        boosts = [
            (x, y)
            for y, row in enumerate(board.Gamestate)
            for x, obj in enumerate(row)
            if isinstance(obj, Pickup) and obj.pickup_type == Pickup.boostUp
        ]
        pos = {enemy.enemy_type : (enemy.x, enemy.y) for enemy in board.enemies}
        pos['pacman'] = (board.pacman.x, board.pacman.y)
        initial_depth = 8
        tree, = Tree(
            initial_depth,
            board.pacman.score,
            board.pacman.lives,
            board.pacman.direction,
            not board.pacman.invulnerable,
            board.pacman.invulnerable_ticks,
            board.enemies['inky'].last_choice,
            board.enemies['inky'].movement_turns,
            pellets,
            boosts
        )     
        result = tree.alpha_beta(initial_depth, float('+inf'), float('-inf'), True)
        

    @classmethod
    def display_pacman_tree_aux(cls, tree, i):
        for _ in range(i):
            print("    ", end="")
        print(tree.pos)
        for child in tree.children:            
            Window.display_pacman_tree_aux(child, i+1)

    def run(self) -> None:
        self.delay_beginning()
        self._master.after(2000, self.update) # put again here to allow mainloop() to still occur and also call gameloop
        self._master.mainloop()
