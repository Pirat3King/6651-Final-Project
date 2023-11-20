import tkinter as tk
from checkers.checkers import Checkers
from hangman.hangman import Hangman, call_pack,call_unpack
from snake.snake import Snake
import json
import socket
import os

def gen_json_format(username, hm_score, s_score, ch_score):
    json_format = {
        username: [
            {
                "hangman_score": hm_score,
                "snake_score": s_score,
                "checkers_score": ch_score
            }
        ]
    }
    return json_format

username = socket.gethostname()
user_scores = "my_high_scores.json"
json_hangman_score = 0
json_snake_score = 0
json_checkers_score = 0

game_running = False  # Flag to track whether a game is currently running

if not os.path.exists(user_scores):
    with open(user_scores, 'w') as json_file:
        json.dump(gen_json_format(username, json_hangman_score, json_snake_score, json_checkers_score), json_file, indent=4)
else:
    with open(user_scores, 'r') as json_file:
        data = json.load(json_file)
        for user in data[username]:
            json_hangman_score = user['hangman_score']
            json_snake_score = user['snake_score']
            json_checkers_score = user['checkers_score']


root = tk.Tk()
root.title("Team Pheonix")
root.geometry("900x700")
root.state('zoomed') # Defaults to maximized view


# Each function will start the selected game and close all other games
def play_hangman():
    call_pack()
    checkers_canvas_widget.pack_forget()
    snake_canvas_widget.pack_forget()

def play_snake():
    call_unpack()
    checkers_canvas_widget.pack_forget()
    snake_canvas_widget.pack(pady=100)

def play_checkers():
    call_unpack()
    checkers_canvas_widget.pack(pady=100)
    snake_canvas_widget.pack_forget()

def reset_game():
    if radio.get() == 1:
        pass
    elif radio.get() == 2:
        snake_game.restart_game()
    elif radio.get() == 3:
        checkers_game.reset_game()

def save_high_scores():
    global json_snake_score
    if snake_game.score > json_snake_score:
        json_snake_score = snake_game.score
    with open(user_scores, 'w') as json_file:
        json.dump(gen_json_format(username, json_hangman_score, json_snake_score, json_checkers_score), json_file, indent=4)


# def test_func():
#     print(snake_game.score)
#     print(json_snake_score)

radio = tk.IntVar()

#Radio buttons to play each game, 
game1_radio = tk.Radiobutton(root, text="Play Hangman", variable=radio, value=1, command=play_hangman).place(x=650, y=800)
game2_radio = tk.Radiobutton(root, text="Play Snake", variable=radio, value=2, command=play_snake).place(x=650, y=820)
game3_radio = tk.Radiobutton(root, text="Play Checkers", variable=radio, value=3, command=play_checkers).place(x=650,y=840)


checkers_canvas_widget = tk.Canvas(root, width=400, height=400)
checkers_game = Checkers(root, checkers_canvas_widget)

snake_canvas_widget = tk.Canvas(root, width=400, height=400, bg="black")
snake_game = Snake(root,snake_canvas_widget)

# Used to reset snake or checkers, issues with checkers
restart_button = tk.Button(root, text="Restart Game", command=reset_game).place(x=850,y=800)
save_button = tk.Button(root, text="Save High Scores", command=save_high_scores).place(x=850,y=830)
# test_button = tk.Button(root, text="Test Button", command=test_func).place(x=850,y=830)


# Hangman must be last otherwise it bombs out
Hangman(root)

root.mainloop()