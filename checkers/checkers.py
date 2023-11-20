"""
File: checkers.py
Authors: William Turner
Brief: Implementation of checkers using tkinter GUI
Date: 2023/10/14
"""

# OpenAI's ChatGPT was utilized to assist in the creation of this program

import tkinter as tk
from PIL import Image, ImageTk
import os
import json

# Constants
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 8
SQUARE_SIZE = WIDTH // GRID_SIZE
WHITE = "white"
BLACK = "black"
RED = "red"
GREEN = "#008000"
BEIGE = "#daa06d"
P1 = 1  # Black player
P2 = 2  # White player

# Set directory of game over screen image
cur_path = os.path.dirname(__file__)
crown_img = os.path.join(cur_path, '..', 'img', 'small-crown.png')

# Checkers class
class Checkers:
    def __init__(self, root_window, the_canvas_window, user_data):
        self.root = root_window
        self.root.title("Checkers")
        self.user_data = user_data

        # Initialize canvas
        self.canvas = the_canvas_window

        # Make game window fixed size
        self.root.geometry(f"{WIDTH}x{HEIGHT}")

        self.init_game()
        self.set_player_names()

    def update_checkers_score(self):
        print(f"winner: {self.winner}")

        self.user_data["checkers_wins"] = self.user_data.get("checkers_wins", 0) + 1
        with open("user_data.json", "w") as file:
            json.dump({"users": [self.user_data]}, file, indent=4)

    # Initialize game components and draw the board in the background
    def init_game(self):
        self.board = self.init_board()
        self.selected_piece = None
        self.jump_in_progress = False
        self.current_player = P1
        self.game_over = False
        self.winner = ""

        self.win_img = ImageTk.PhotoImage(Image.open(crown_img)) 
        self.win_box = ImageTk.PhotoImage(Image.new('RGBA', (WIDTH-80, HEIGHT-80), (147, 151, 153, 230))) 
        
        self.canvas.bind("<Button-1>", self.mouse_click)
        
        self.draw_board()

    # Prompt user to input player names via entry boxes 
    def set_player_names(self):
        # Entry boxes
        self.player1_entry = tk.Entry(self.root)
        self.player2_entry = tk.Entry(self.root)
        self.canvas.create_image(WIDTH/2, HEIGHT/2, anchor="center", image=self.win_box) # grey box
        self.canvas.create_text(WIDTH // 2, HEIGHT // 3, text="Player 1:", fill="black", font=('Helvetica 15 bold'))
        self.canvas.create_window(WIDTH // 2, HEIGHT // 3 + 30, window=self.player1_entry)
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2, text="Player 2:", fill="black", font=('Helvetica 15 bold'))
        self.canvas.create_window(WIDTH // 2, HEIGHT // 2 + 30, window=self.player2_entry)

        # Submit button
        self.submit_btn = tk.Button(self.root, text="Start Game", command=self.start_game)
        self.canvas.create_window(WIDTH // 2, HEIGHT * 2 // 3, window=self.submit_btn)

    # Save player names, clear initial screen, and draw board to start game
    def start_game(self):
        # Get player names from the entries
        self.player1 = self.player1_entry.get()
        self.player2 = self.player2_entry.get()

        # Clear the canvas and remove entry fields and submit button
        self.canvas.delete("all")
        self.player1_entry.destroy()
        self.player2_entry.destroy()
        self.submit_btn.destroy()

        self.draw_board()

    # Initialize 2D list for board
    def init_board(self):
        board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        
        # # Place black pieces (player 1)
        for row in range(GRID_SIZE - 3, GRID_SIZE):
            for col in range(GRID_SIZE):
                if (row + col) % 2 == 1:
                    board[row][col] = P1

        # # Place white pieces (player 2)
        # for row in range(3):
        #     for col in range(GRID_SIZE):
        #         if (row + col) % 2 == 1:
        #             board[row][col] = P2

        # test king functionality (comment the above loops to clear other pieces)
        # board[6][1] = P2
        # board[1][4] = P1 

        # test double jump
        board[4][3] = P2
        board[2][5] = P2
        return board
    
    # Draw a single piece 
    def draw_piece(self, col, row, color):
        self.canvas.create_oval(col * SQUARE_SIZE + 5, row * SQUARE_SIZE + 5, (col + 1) * SQUARE_SIZE - 5, (row + 1) * SQUARE_SIZE - 5, fill=color)

    # Handle all graphics - draws board and pieces
    def draw_board(self):
        self.canvas.delete("all")
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                # Board squares
                color = BEIGE if (row + col) % 2 == 0 else GREEN
                self.canvas.create_rectangle(col * SQUARE_SIZE, row * SQUARE_SIZE, (col + 1) * SQUARE_SIZE, (row + 1) * SQUARE_SIZE, fill=color)
                # Red selection outline 
                if self.selected_piece is not None and (row, col) == self.selected_piece:
                    self.canvas.create_rectangle(col * SQUARE_SIZE, row * SQUARE_SIZE, (col + 1) * SQUARE_SIZE, (row + 1) * SQUARE_SIZE, outline=RED, width=4)
                # Black pieces
                if self.board[row][col] == P1:
                    self.draw_piece(col, row, BLACK)
                # White pieces
                elif self.board[row][col] == P2:
                    self.draw_piece(col, row, WHITE)
                # Black king pieces
                elif self.board[row][col] == P1 + 2:
                    self.draw_piece(col, row, BLACK)
                    self.canvas.create_text(col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2, text="K", font=('Helvetica', 14), fill=WHITE)
                # White king pieces
                elif self.board[row][col] == P2 + 2:
                    self.draw_piece(col, row, WHITE)
                    self.canvas.create_text(col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2, text="K", font=('Helvetica', 14), fill=BLACK)

    # Handle user clicking on the board
    def mouse_click(self, event):
        x, y = event.x, event.y
        col = x // SQUARE_SIZE
        row = y // SQUARE_SIZE

        self.select_square(row, col)

    # Handle user selecting a square/piece
    def select_square(self, row, col):
        # Check if a piece is already selected
        if self.selected_piece is None:
            # Select if piece belongs to current player
            if self.board[row][col] == self.current_player or self.board[row][col] - 2 == self.current_player:
                self.selected_piece = (row, col)
                self.draw_board()
        else:
            # Deselect if the same piece is clicked again
            if (row, col) == self.selected_piece: 
                self.selected_piece = None
                self.jump_in_progress = False
            
            # Select new piece if clicked square belongs to current player    
            elif self.board[row][col] == self.current_player: 
                self.selected_piece = (row, col)
            
            # Attempt to move the selected piece to the clicked square
            else:
                if self.move_piece((row, col)):
                    # If a jump was made, check for double jump
                    if self.jump_in_progress and self.can_jump((row, col)):
                        self.selected_piece = (row, col)
                    
                    # If another jump is not possible, end turn
                    else: 
                        self.jump_in_progress = False
                        self.selected_piece = None
                        if self.check_win() == False: #Check for win condition and change player turn
                            self.current_player = P2 if self.current_player == P1 else P1
                        else: # Exit if win
                            self.game_over = True
                            self.update_checkers_score()
                            return

            self.draw_board()

    # Handle movement of pieces
    def move_piece(self, end_pos):
        row, col = end_pos

        # Check for valid move
        move_is_valid, jumped_piece = self.is_valid_move(end_pos)

        if move_is_valid:
            # Move piece to target square
            self.board[row][col] = self.board[self.selected_piece[0]][self.selected_piece[1]]
            self.board[self.selected_piece[0]][self.selected_piece[1]] = 0
            # Remove jumped piece from board
            if jumped_piece != None:
                self.board[jumped_piece[0]][jumped_piece[1]] = 0
                self.jump_in_progress = True
            else:
                self.jump_in_progress = False
        else:
            return False
        
        # Convert regular piece to king if applicable
        self.king_me(end_pos)
        return True
    
    # Handle regular piece to king conversion. Kings are represented by adding 2 to regular piece value
    def king_me(self, pos):
        row, col = pos

        if self.current_player == P1 and row == 0 and self.board[row][col] == P1:
            self.board[row][col] = P1 + 2  # P1 king

        elif self.current_player == P2 and row == GRID_SIZE - 1 and self.board[row][col] == P2:
            self.board[row][col] = P2 + 2  # P2 king

    # Check if selected target position is valid
    def is_valid_move(self, end_pos, start_pos=None, player=None):
        if start_pos is None:
            start_pos = self.selected_piece

        if player is None:
            player = self.current_player

        row_start, col_start = start_pos
        row_end, col_end = end_pos

        # Board boundaries
        if row_end < 0 or row_end >= GRID_SIZE or col_end < 0 or col_end >= GRID_SIZE:
            return False, None

        # Check end position is empty
        if self.board[row_end][col_end] != 0:
            return False, None
        
        # King piece - can move and jump in any direction
        if self.board[row_start][col_start] in [P1+2, P2+2]:
            # Regular move - 1 square, not allowed after a jump
            if self.jump_in_progress == False and abs(row_end - row_start) == 1 and abs(col_end - col_start) == 1:
                return True, None
            
            # Jump move - 2 squares
            if abs(row_end - row_start) == 2 and abs(col_end - col_start) == 2:
                return self.calc_jump(end_pos, start_pos, player)
        
        # Regular piece - can only move and jump "forward"
        elif self.board[row_start][col_start] in [P1, P2]:
            # Set play direction
            move_direction = -1 if player == P1 else 1

            # Regular move - 1 square, not allowed after a jump
            if self.jump_in_progress == False and row_end == row_start + move_direction and abs(col_end - col_start) == 1:
                return True, None

            # Jump move - 2 squares
            if row_end == row_start + 2 * move_direction and abs(col_end - col_start) == 2:
                return self.calc_jump(end_pos, start_pos, player)
        else:
            return False, None
    
    # Calculate the square to jump and check if opponent occupies it
    def calc_jump(self, end_pos, start_pos=None, player=None):
        if start_pos is None:
            start_pos = self.selected_piece

        if player is None:
            player = self.current_player

        row_start, col_start = start_pos
        row_end, col_end = end_pos

        # Calc position of square to jump
        jumped_row = (row_start + row_end) // 2
        jumped_col = (col_start + col_end) // 2

        # Check for opponent piece to jump over
        if self.board[jumped_row][jumped_col] == (3 - player) or self.board[jumped_row][jumped_col] == (5 - player):
            return True, (jumped_row, jumped_col)
        else:
            return False, None

    # Check if any move is possible for a given piece
    def can_move_or_jump(self, start_pos, player=None):
        if player is None:
            player = self.current_player

        row, col = start_pos
        piece = self.board[row][col]

        # Set directions for possible regular moves
        if piece == P1:
            reg_move = [(-1, -1), (-1, 1)]
        elif piece == P2:
            reg_move = [(1, -1), (1, 1)]
        elif piece in [P1 + 2, P2 + 2]:  # If piece is a king
            reg_move = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        # Check for valid moves based on direction
        for row_offset, col_offset in reg_move:
            target_row = row + row_offset
            target_col = col + col_offset
            if self.is_valid_move((target_row, target_col), start_pos=start_pos, player=player)[0]:
                return True
        
        # Check jump moves
        if self.can_jump(start_pos, player):
            return True
            
        return False
    
    # Check if a jump move is possible for a given piece
    def can_jump(self, start_pos=None, player=None):
        if start_pos is None:
            start_pos = self.selected_piece

        if player is None:
            player = self.current_player

        row, col = start_pos
        piece = self.board[row][col]

        # Set directions for possible jump moves
        if piece == P1: 
            jump_moves = [(-2, -2), (-2, 2)]
        elif piece == P2:
            jump_moves = [(2, -2), (2, 2)]
        elif piece in [P1 + 2, P2 + 2]:  # If piece is a king
            jump_moves = [(-2, -2), (-2, 2), (2, -2), (2, 2)]

        # Check for valid jumps based on direction
        for row_offset, col_offset in jump_moves:
            target_row = row + row_offset
            target_col = col + col_offset
            if self.is_valid_move((target_row, target_col), start_pos, player)[0]:
                return True
        return False
    
    # Check for a win condition
    def check_win(self):
        opponent = P2 if self.current_player == P1 else P1

        # Check if the opponent can move any piece
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                piece = self.board[row][col]
                if piece == opponent or piece - 2 == opponent:
                    if self.can_move_or_jump((row, col), opponent):
                        return False # Opponent can still move

        # If no opponent pieces left or they can't move, the current player wins
        self.win()
        return True      
    
    def win(self):
        self.winner = self.player1 if self.current_player == P1 else self.player2

        # Disable clicking on squares
        self.canvas.unbind("<Button-1>")

        # Create exit button
        # quit_button = tk.Button(self.root, text='Exit Checkers', command=self.root.destroy)

        # Display win screen
        self.canvas.create_image(WIDTH/2, HEIGHT/2, anchor="center", image=self.win_box)
        self.canvas.create_text(WIDTH/2, HEIGHT/5, text="GAME OVER", fill="black", font=('Helvetica 15 bold'))
        self.canvas.create_image(WIDTH/2, HEIGHT/2, anchor="center", image=self.win_img)
        self.canvas.create_text(WIDTH/2, HEIGHT/1.33, text=f"{self.winner} wins!", fill="black", font=('Helvetica 15 bold'))
        # self.canvas.create_window(WIDTH // 2, HEIGHT/1.2, window=quit_button)
    
    # Returns the winner's name if it exists
    # def get_winner(self):
    #     if self.game_over:
    #         return self.winner
    #     else:
    #         return "No winner"

    def reset_game(self):
        self.canvas.delete("all")
        self.__init__(self.root, self.canvas, self.user_data)

    # # Run the game
    # def run(self):
    #     self.root.mainloop()

# Uncomment to run outside of main application
# checker_game = Checkers()
# checker_game.run()
# print(f"Winner: {checker_game.get_winner()}")