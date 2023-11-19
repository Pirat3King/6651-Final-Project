import tkinter as tk
from tkinter import simpledialog
from checkers.checkers import Checkers
from hangman.hangman_kiren import Hangman, pack_hangman_elements, unpack_hangman_elements
from snake.snake import Snake


game_running = False  # Flag to track whether a game is currently running

# Get the username from the user before starting the game
username = simpledialog.askstring("Phoenix Games", "Welcome to Phoenix Games! Enter your username:")

root = tk.Tk()
root.title("Team Phoenix")
root.geometry("900x700")
root.state('zoomed') # Defaults to maximized view

# Each function will start the selected game and close all other games
def play_hangman():
    pack_hangman_elements()
    checkers_canvas_widget.pack_forget()
    snake_canvas_widget.pack_forget()

def play_snake():
    unpack_hangman_elements()
    checkers_canvas_widget.pack_forget()
    snake_canvas_widget.pack(pady=100)

def play_checkers():
    unpack_hangman_elements()
    checkers_canvas_widget.pack(pady=100)
    snake_canvas_widget.pack_forget()


radio = tk.IntVar()

#Radio buttons to play each game,
game1_radio = tk.Radiobutton(root, text="Play Hangman", variable=radio, value=1, command=play_hangman).place(x=50, y=580)
game2_radio = tk.Radiobutton(root, text="Play Snake", variable=radio, value=2, command=play_snake).place(x=50, y=600)
game3_radio = tk.Radiobutton(root, text="Play Checkers", variable=radio, value=3, command=play_checkers).place(x=50,y=620)

# Create and pack the username display and attempts widgets
username_display_label = tk.Label(root, text=f"Username: {username}")
username_display_label.place(x=50, y=540)

# Entry for the username
"""username_label = tk.Label(root, text="Enter your username:")
username_label.place(x=50, y=540)

username_entry = tk.Entry(root)
username_entry.place(x=200, y=540)"""

checkers_canvas_widget = tk.Canvas(root, width=400, height=400)
checkers_game = Checkers(checkers_canvas_widget)

snake_canvas_widget = tk.Canvas(root, width=400, height=400, bg="black")
snake_game = Snake(root,snake_canvas_widget)

# Used to reset the snake game, we need to
restart_button = tk.Button(root, text="Restart Game", command=snake_game.restart_game).place(x=850,y=800)

# Hangman must be last otherwise it bombs out
Hangman(root)

root.mainloop()
