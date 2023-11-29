
"""
Author: Muhammad Hammad
Date Authored: Nov. 22, 2023
Last Updated: Nov. 26, 2023
Class: CSCI 6651-01
Goal: The code aims to create a Python Tkinter-based graphical interface for playing Hangman, Snake, and Checkers games, with user data management, scoreboard display, and game interactions.
Sources: AI: Blackbox, chatGPT 
"""

import tkinter as tk
from tkinter import simpledialog, messagebox
import json
from checkers.checkers import Checkers
from hangman.hangman import Hangman, pack_hangman_elements, unpack_hangman_elements
from snake.snake import Snake

game_running = False  # Flag to track whether a game is currently running

# Function to handle user data
def get_user_data(username):
    try:
        with open("user_data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        # If the file doesn't exist, create an empty JSON structure
        data = {"users": []}

    users = data.get("users", [])

    for user in users:
        if user["username"] == username:
            return user

    # If the username is not found, create a new user
    new_user = {"username": username, "hangman_wins": 0, "snake_score": 0, "checkers_wins": 0}
    users.append(new_user)

    # Update the data dictionary
    data["users"] = users

    # Save the updated data to the file
    with open("user_data.json", "w") as file:
        json.dump(data, file, indent=4)

    return new_user

# Function to show the scoreboard
def show_scoreboard():
    try:
        with open("user_data.json", "r") as file:
            data = json.load(file)

        users = data.get("users", [])
        scoreboard_text = "\n".join(
            f"{user['username']}: Hangman Wins - {user['hangman_wins']}, Snake Score - {user['snake_score']}, Checkers Wins - {user['checkers_wins']}"
            for user in users)

        # Create a custom Toplevel window
        scoreboard_window = tk.Toplevel(root)
        scoreboard_window.title("Scoreboard")

        # Create a Label to display the scoreboard text
        scoreboard_label = tk.Label(scoreboard_window, text=scoreboard_text, padx=20, pady=20)
        scoreboard_label.pack()

        # Add a button to close the window
        close_button = tk.Button(scoreboard_window, text="Close", command=scoreboard_window.destroy)
        close_button.pack()
    except FileNotFoundError:
        messagebox.showinfo("Scoreboard", "No scores found.")

# Function to terminate the application
def terminate_application():
    root.destroy()

# Get the username from the user before starting the game
username = simpledialog.askstring("Phoenix Games", "Welcome to Phoenix Games! Enter your username:")

def read_data_to_json():
    with open("user_data.json", "r") as file:
        return json.load(file)

name = get_user_data(username)
user_data = read_data_to_json()

root = tk.Tk()
root.title("Team Phoenix")
root.geometry("900x700")
root.state('zoomed') # Defaults to maximized view

# Background Image
background_image = tk.PhotoImage(file="background1.0.png")
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

checkers_canvas_widget = tk.Canvas(root, width=400, height=400)  # Define checkers_canvas_widget here
checkers_game = Checkers(root, checkers_canvas_widget)

snake_canvas_widget = tk.Canvas(root, width=400, height=400, bg="black")
snake_game = Snake(root, snake_canvas_widget, user_data, name)

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

def reset_game():
    if radio.get() == 1:
        pass
    elif radio.get() == 2:
        snake_game.restart_game()
    elif radio.get() == 3:
        checkers_game.reset_game()

radio = tk.IntVar()

# Radio buttons to play each game
game1_radio = tk.Radiobutton(root, text="Play Hangman", variable=radio, value=1, command=play_hangman, font=("Arial", 12), bg="red", fg="white").place(x=80, y=450)
game2_radio = tk.Radiobutton(root, text="Play Snake", variable=radio, value=2, command=play_snake, font=("Arial", 12), bg="#660000", fg="white").place(x=80, y=500)
game3_radio = tk.Radiobutton(root, text="Play Checkers", variable=radio, value=3, command=play_checkers, font=("Arial", 12), bg="#F39C12", fg="white").place(x=80, y=550)

# Create and pack the username display and attempts widgets
username_display_label = tk.Label(root, text=f"Username: {username}", font=("Arial", 14), bg="#BDC3C7")
username_display_label.place(x=50, y=400)

# Button to show scoreboard
scoreboard_button = tk.Button(root, text="Show Scoreboard", command=show_scoreboard, font=("Arial", 12), bg="#008CBA", fg="white")
scoreboard_button.place(relx=.95, rely=.95, anchor=tk.SE)

# Termination button
terminate_button = tk.Button(root, text="Quit", command=terminate_application, font=("Arial", 10), bg="red", fg="white")
terminate_button.place(relx=.95, rely=.05, anchor=tk.NE)

# Hangman must be last otherwise it bombs out
Hangman(root, user_data)

root.mainloop()

# Update snake score after closing the window
snake_game.update_snake_score()
