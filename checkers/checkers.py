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

cur_path = os.path.dirname(__file__)
crown_img = os.path.join(cur_path, '..', 'img', 'small-crown.png')

# Checkers classs
class Checkers:
    def __init__(self):
        self.board = self.init_board()
        self.selected_piece = None
        self.jump_in_progress = False
        self.current_player = P1
        
        self.root = tk.Tk()
        self.root.title("Checkers")
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT)
        self.canvas.pack()
        self.img = ImageTk.PhotoImage(Image.open(crown_img))
        self.canvas.bind("<Button-1>", self.select_square)
        self.draw_board()

    # Initialize 2D list for board
    def init_board(self):
        board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        
        # Place black pieces (player 1)
        for row in range(GRID_SIZE - 3, GRID_SIZE):
            for col in range(GRID_SIZE):
                if (row + col) % 2 == 1:
                    board[row][col] = P1

        # # Place white pieces (player 2)
        # for row in range(3):
        #     for col in range(GRID_SIZE):
        #         if (row + col) % 2 == 1:
        #             board[row][col] = P2
        # board[1][4] = P1 # test king making
        board[4][3] = P2
        board[2][5] = P2
        return board

    # Handle user selecting a square/piece
    def select_square(self, event):
        x, y = event.x, event.y
        col = x // SQUARE_SIZE
        row = y // SQUARE_SIZE

        print(f"Selected square: {row},{col}")

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

            else:
                # Attempt to move the selected piece to the clicked square
                if self.move_piece((row, col)):
                    print(f"continue jumpimg? {self.jump_in_progress}")
                    if self.jump_in_progress and self.can_jump((row, col)):  # Continue if another jump is possible
                        self.selected_piece = (row, col)
                        print(f"new selected piece: {row},{col}")
                    else:
                        self.jump_in_progress = False
                        self.selected_piece = None
                    
                    self.check_win()
                    self.current_player = P2 if self.current_player == P1 else P1

            self.draw_board()

    # Handle movement of pieces
    def move_piece(self, end_pos):
        row, col = end_pos

        is_valid, jumped_piece = self.is_valid_move(end_pos)

        if is_valid:
            # Move
            self.board[row][col] = self.board[self.selected_piece[0]][self.selected_piece[1]]
            self.board[self.selected_piece[0]][self.selected_piece[1]] = 0
            if jumped_piece != None:
                print("jumped a piece")
                self.board[jumped_piece[0]][jumped_piece[1]] = 0
                self.jump_in_progress = True
            else:
                self.jump_in_progress = False
        else:
            return False
            
        self.king_me(end_pos)
        return True
    
    def king_me(self, pos):
        row, col = pos

        if self.current_player == P1 and row == 0 and self.board[row][col] == P1:
            self.board[row][col] = P1 + 2  # P1 king

        elif self.current_player == P2 and row == GRID_SIZE - 1 and self.board[row][col] == P2:
            self.board[row][col] = P2 + 2  # P2 king

    # Check if selected end position is valid
    def is_valid_move(self, end_pos, start_pos=None, player=None):
        if start_pos is None:
            start_pos = self.selected_piece

        if player is None:
            player = self.current_player

        print(f"checking valid move from {start_pos} to {end_pos} for player {player}")

        row_start, col_start = start_pos
        row_end, col_end = end_pos

        # Board boundaries
        if row_end < 0 or row_end >= GRID_SIZE or col_end < 0 or col_end >= GRID_SIZE:
            print("out of bounds")
            return False, None

        # End position is empty square
        if self.board[row_end][col_end] != 0:
            print("target not empty")
            return False, None
        
        # King piece
        if self.board[row_start][col_start] in [P1+2, P2+2]:
            print("king piece")
            # Regular move
            if abs(row_end - row_start) == 1 and abs(col_end - col_start) == 1:
                print("valid king move")
                return True, None
            
            # Jump move
            if abs(row_end - row_start) == 2 and abs(col_end - col_start) == 2:
                print("potential king jump")
                return self.do_jump(end_pos)
        
        # Regular piece
        elif self.board[row_start][col_start] in [P1, P2]:
            print("regular piece")
            # Set play direction
            move_direction = -1 if player == P1 else 1

            # Regular move
            if row_end == row_start + move_direction and abs(col_end - col_start) == 1:
                print("valid regular move")
                return True, None

            # Jump move
            if row_end == row_start + 2 * move_direction and abs(col_end - col_start) == 2:
                print("potential regular jump")
                return self.do_jump(end_pos)
        else:
            print("other invalid move")   
        return False, None
    
    def do_jump(self, end_pos):
        row_start, col_start = self.selected_piece
        row_end, col_end = end_pos

        # Calc position of square to jump
        jumped_row = (row_start + row_end) // 2
        jumped_col = (col_start + col_end) // 2

        # Check if there's an opponent piece to jump over
        print(f"start: {self.selected_piece}")
        print(f"end: {row_end},{col_end}")
        print(f"jumped place: {jumped_row},{jumped_col}")
        print(f"jumped piece = {self.board[jumped_row][jumped_col]}")
        print(f"player {self.current_player}")
        if self.board[jumped_row][jumped_col] == (3 - self.current_player) or self.board[jumped_row][jumped_col] == (5 - self.current_player):
            print("valid jump")
            return True, (jumped_row, jumped_col)
        else:
            print("no one to jump")
            return False, None
        
    # Check if a move is possible
    def can_jump(self, start_pos):
        print(f"checking can jump from {start_pos}")
        row, col = start_pos
        piece = self.board[row][col]

        # Set directions for possible jump moves
        if piece == P1: 
            jump_moves = [(-2, -2), (-2, 2)]
        elif piece == P2:
            jump_moves = [(2, -2), (2, 2)]
        elif piece in [P1 + 2, P2 + 2]:  # If piece is a king
            jump_moves = [(-2, -2), (-2, 2), (2, -2), (2, 2)]

        # print(f"Piece at {start_pos} (player {piece}) possible moves: {jump_moves}")

        # Check jump moves
        for row_offset, col_offset in jump_moves:
            target_row = row + row_offset
            target_col = col + col_offset
            # print(f"Checking from {start_pos} to target row: {target_row}, target col: {target_col}")
            if self.is_valid_move((target_row, target_col), start_pos=start_pos)[0]:
                print(f"can jump to {target_row},{target_col}")
                return True
        return False

    # Check if any move is possible
    def can_move_or_jump(self, start_pos, player=None):
        if player is None:
            player = self.current_player

        print(f"checking can move from {start_pos}")
        row, col = start_pos
        piece = self.board[row][col]

        # Set directions for possible regular moves
        if piece == P1:
            reg_move = [(-1, -1), (-1, 1)]
        elif piece == P2:
            reg_move = [(1, -1), (1, 1)]
        elif piece in [P1 + 2, P2 + 2]:  # If piece is a king
            reg_move = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        # Check regular moves
        for row_offset, col_offset in reg_move:
            target_row = row + row_offset
            target_col = col + col_offset
            if self.is_valid_move((target_row, target_col), start_pos=start_pos, player=player)[0]:
                return True
        
        # Check regular moves
        self.can_jump(start_pos)
            
        return False
    
    # Draw a single piece 
    def draw_piece(self, col, row, color):
        self.canvas.create_oval(col * SQUARE_SIZE + 5, row * SQUARE_SIZE + 5, (col + 1) * SQUARE_SIZE - 5, (row + 1) * SQUARE_SIZE - 5, fill=color)

    # Handle all graphics - draws board and pieces
    def draw_board(self):
        self.canvas.delete("all")
        print(f"Player {self.current_player}'s turn")
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

    def check_win(self):
        print("checking for winners")
        print("------------------------------------------")
        opponent = P2 if self.current_player == P1 else P1
        print(f"opponent = {opponent}")

        # Check if the opponent can move any piece
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                piece = self.board[row][col]
                if piece == opponent or piece - 2 == opponent:
                    if self.can_move_or_jump((row, col), opponent):
                        print("no winner yet")
                        return False # Opponent can still move

        # If no opponent pieces left or they can't move, the current player wins
        self.win()
        return True      
    
    def win(self):
        self.canvas.unbind("<Button-1>")
        self.canvas.delete("all")
       
        self.canvas.create_text(WIDTH/2, 50, text="GAME OVER", fill="black", font=('Helvetica 15 bold'))
        self.canvas.create_image(WIDTH/2, HEIGHT/2, anchor="center", image=self.img)
        self.canvas.create_text(WIDTH/2, 350, text=f"Player {self.current_player} wins!", fill="black", font=('Helvetica 15 bold'))
        quit_button = tk.Button(self.root,text='QUIT',command=self.root.quit)
        self.canvas.pack()
        quit_button.pack(side="bottom", expand=True)

        #TODO update score

    def run(self):
        self.root.mainloop()

# run game
checker_game = Checkers()
checker_game.run()
