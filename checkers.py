# TODO 
#   double jumps
#   kings
#   winning
#   make it a class so it can be used in the main program

import tkinter as tk

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

# Initialize the tkinter window
root = tk.Tk()
root.title("Checkers")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
canvas.pack()

selected_piece = None  # To keep track of the selected piece
current_player = P1

# Initialize the game board (represented as a 2D list)
def init_board():
    board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

    # Place black pieces (player 1) on the board
    for row in range(GRID_SIZE - 3, GRID_SIZE):
        for col in range(GRID_SIZE):
            if (row + col) % 2 == 1:
                board[row][col] = P1

    # Place white pieces (player 2) on the board
    for row in range(3):
        for col in range(GRID_SIZE):
            if (row + col) % 2 == 1:
                board[row][col] = P2

    return board

def select_square(event):
    x, y = event.x, event.y
    col = x // SQUARE_SIZE
    row = y // SQUARE_SIZE

    global selected_piece, current_player

    if selected_piece is None:
        # Select a piece if the clicked square is not empty and belongs to the current player
        if board[row][col] == current_player:
            selected_piece = (row, col)
        draw_board()
        
    else:
        if (row, col) == selected_piece:
            # Deselect the piece if it's clicked again
            selected_piece = None
        elif board[row][col] == current_player:
            # Select a new piece if the clicked square belongs to the current player
            selected_piece = (row, col)
        else:
            # Attempt to move the selected piece to the clicked square
            move_piece((row, col))
        draw_board()

def move_piece(end_pos):
    global selected_piece, current_player
    row, col = end_pos

    if is_valid_move(end_pos):
        print("valid move")
        board[row][col] = current_player
        board[selected_piece[0]][selected_piece[1]] = 0  # Remove the piece from the old square
        current_player = P1 if current_player == P2 else P2  # Switch turns
    selected_piece = None

    draw_board()

def is_valid_move(end_pos):
    global selected_piece, current_player

    row_start, col_start = selected_piece
    row_end, col_end = end_pos

    print(f"Start: {selected_piece}")
    print(f"End: {end_pos}")

    # Selected piece belongs to current player
    if board[row_start][col_start] != current_player:
        print("not your piece")
        return False

    # Board boundaries
    if row_end < 0 or row_end >= GRID_SIZE or col_end < 0 or col_end >= GRID_SIZE:
        print("out of bounds")
        return False

    # End position is an empty square
    if board[row_end][col_end] != 0:
        print("occupado")
        return False

    # Set play direction based on the current player
    if current_player == P1:
        move_direction = -1
    else:
        move_direction = 1

    # Regular move (one square diagonally forward)
    if row_end == row_start + move_direction and abs(col_end - col_start) == 1:
        print("regular ol' move")
        return True

    # Jump move (two squares diagonally forward over an opponent's piece)
    if row_end == row_start + 2 * move_direction and abs(col_end - col_start) == 2:
        print("jumpy things")
        # Calculate the position of the jumped piece
        jumped_row = (row_start + row_end) // 2
        jumped_col = (col_start + col_end) // 2

        # Check if there's an opponent's piece to jump over and remove if so.
        if board[jumped_row][jumped_col] == (3 - current_player):
            board[jumped_row][jumped_col] = 0
            return True
        
    print("nuthin")
    return False

def draw_board():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            color = BEIGE if (row + col) % 2 == 0 else GREEN
            canvas.create_rectangle(col * SQUARE_SIZE, row * SQUARE_SIZE, (col + 1) * SQUARE_SIZE, (row + 1) * SQUARE_SIZE, fill=color)

            if selected_piece is not None and (row, col) == selected_piece:
                canvas.create_rectangle(col * SQUARE_SIZE, row * SQUARE_SIZE, (col + 1) * SQUARE_SIZE, (row + 1) * SQUARE_SIZE, outline=RED, width=2)

            if board[row][col] == P1:
                canvas.create_oval(col * SQUARE_SIZE + 5, row * SQUARE_SIZE + 5, (col + 1) * SQUARE_SIZE - 5, (row + 1) * SQUARE_SIZE - 5, fill=BLACK)

            elif board[row][col] == P2:
                canvas.create_oval(col * SQUARE_SIZE + 5, row * SQUARE_SIZE + 5, (col + 1) * SQUARE_SIZE - 5, (row + 1) * SQUARE_SIZE - 5, fill=WHITE)

board = init_board()

canvas.bind("<Button-1>", select_square)
draw_board()

root.mainloop()
