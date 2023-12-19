"""
File: snake.py
Authors: Trevor Ralston
Brief: Implementation of snake using tkinter GUI
Date: 2023/11/7
Last Updated: Dec. 19, 2023 by Kiren
OpenAI's ChatGPT was utilized to assist in the creation of this program

Updates from Kiren: Allows user to select difficulty level for each game
Updates from Trevor: Snake now has a proper start button and game over prompt
                     added accelerator variable to increase snake speed
"""

import tkinter as tk
import random
import json

# Constants
CANVAS_SIZE = 400
GRID_SIZE = 20
GRID_WIDTH = CANVAS_SIZE // GRID_SIZE
GRID_HEIGHT = CANVAS_SIZE // GRID_SIZE
EASY_SPEED = 300
MEDIUM_SPEED = 225
HARD_SPEED = 150
# SNAKE_SPEED = 150  # Delay in milliseconds, increase to make the starting speed slower


class Snake:

    # main_tkinter is the tkinter window (root) passed in from main
    # the_canvas_window is a hangman_canvas widget created in main spefically for the snake game
    def __init__(self, main_tkinter, the_canvas_window, user_data, username):
        # Initial snake position and direction
        self.snake = [(4, 5), (4, 4), (4, 3)]
        self.direction = (0, 1)
        # Initialize food position
        self.food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        # Initialize score
        self.score = 0
        # Initialize game over flag
        self.game_over = False
        # Initialize difficulty to None
        self.difficulty = None

        # Create the hangman_canvas
        self.canvas = the_canvas_window

        # Create the score label
        self.score_label = tk.Label(self.canvas, text="Score: 0", fg="white", bg="black")
        self.score_label.place(x=180, y=2)

        # Create the game over label
        self.game_over_label = tk.Label(self.canvas, text="Game Over\nHit Reset to Play Again", fg="white", bg="red",
                                        width=20)

        # Create Start Button, clicking will begin game
        # self.start_button = tk.Button(self.canvas, text="Start Game", fg="white", bg="blue", command=self.move_snake)
        # self.start_button.place(x=170, y=200)

        # Set difficulty: the more difficult, the faster the snake
        self.set_difficulty()

        # Bind arrow key events, these are bound to the main tkinter window (root)
        main_tkinter.bind("<Up>", self.on_key_press)
        main_tkinter.bind("<Down>", self.on_key_press)
        main_tkinter.bind("<Left>", self.on_key_press)
        main_tkinter.bind("<Right>", self.on_key_press)
        main_tkinter.bind("<w>", self.on_key_press)
        main_tkinter.bind("<s>", self.on_key_press)
        main_tkinter.bind("<a>", self.on_key_press)
        main_tkinter.bind("<d>", self.on_key_press)

        self.user_data = user_data
        self.username = username

        # Increases the speed upon eating food
        self.accelerator = 0

    def place_buttons(self):
        self.difficulty_label.place(relx=0.32, rely=0.3)
        self.easy_button.place(relx=0.45, rely=0.38)
        self.medium_button.place(relx=0.43, rely=0.46)
        self.hard_button.place(relx=0.45, rely=0.54)

    def forget_buttons(self):
        self.difficulty_label.place_forget()
        self.easy_button.place_forget()
        self.medium_button.place_forget()
        self.hard_button.place_forget()

    def set_difficulty(self):
        self.difficulty_label = tk.Label(self.canvas, text="Choose Difficulty Level:", font="Arial, 12", fg="#FFFFFF",
                                         bg="#000000")
        self.easy_button = tk.Button(self.canvas, text="Easy", bg="#FAE070",
                                     command=lambda: self.move_snake('easy'))
        self.medium_button = tk.Button(self.canvas, text="Medium", bg="#F18D32",
                                       command=lambda: self.move_snake('medium'))
        self.hard_button = tk.Button(self.canvas, text="Hard", bg="#DE4923",
                                     command=lambda: self.move_snake('hard'))
        self.place_buttons()

    def generate_food(self):
        while self.food in self.snake:
            self.food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def move_snake(self, difficulty):
        # self.start_button.place_forget()
        self.forget_buttons()

        # Set snake speed based on difficulty level
        if difficulty == 'easy':
            snake_speed = EASY_SPEED
        elif difficulty == 'medium':
            snake_speed = MEDIUM_SPEED
        elif difficulty == 'hard':
            snake_speed = HARD_SPEED
        else:
            raise ValueError("Invalid difficulty level")

        if not self.game_over:
            # Calculate the new head position
            head_x, head_y = self.snake[0]
            new_head = (head_x + self.direction[0], head_y + self.direction[1])

            # Check if the snake hits the wall or itself
            if (
                    new_head[0] < 0
                    or new_head[0] >= GRID_WIDTH
                    or new_head[1] < 0
                    or new_head[1] >= GRID_HEIGHT
                    or new_head in self.snake
            ):
                self.game_over = True
                self.update_snake_score()
                self.game_over_label.place(x=130, y=200)
                self.update_snake_score()
            else:
                self.snake.insert(0, new_head)

                # Check if the snake eats the food
                if self.snake[0] == self.food:
                    self.score += 1
                    self.accelerator += 10
                    self.generate_food()
                else:
                    self.snake.pop()

            self.canvas.delete("all")
            self.draw_snake()
            self.draw_food()

            # Update the score label
            self.score_label.config(text=f"Score: {self.score}")

            # Schedule the next move
            self.canvas.after(snake_speed - self.accelerator, lambda: self.move_snake(difficulty))

    def draw_snake(self):
        for segment in self.snake:
            x, y = segment
            self.canvas.create_rectangle(
                x * GRID_SIZE,
                y * GRID_SIZE,
                (x + 1) * GRID_SIZE,
                (y + 1) * GRID_SIZE,
                fill="green",
            )

    def draw_food(self):
        x, y = self.food
        self.canvas.create_oval(
            x * GRID_SIZE,
            y * GRID_SIZE,
            (x + 1) * GRID_SIZE,
            (y + 1) * GRID_SIZE,
            fill="red",
        )

    def on_key_press(self, event):
        if event.keysym == "Up" or event.keysym == "w" and self.direction != (0, 1):
            self.direction = (0, -1)
        elif event.keysym == "Down" or event.keysym == "s" and self.direction != (0, -1):
            self.direction = (0, 1)
        elif event.keysym == "Left" or event.keysym == "a" and self.direction != (1, 0):
            self.direction = (-1, 0)
        elif event.keysym == "Right" or event.keysym == "d" and self.direction != (-1, 0):
            self.direction = (1, 0)

    def restart_snake_game(self):
        # self.update_snake_score()
        self.game_over_label.place_forget()
        self.accelerator = 0
        self.snake = [(4, 5), (4, 4), (4, 3)]
        self.direction = (0, 1)
        self.generate_food()
        self.score = 0
        self.game_over = False
        self.score_label.config(text="Score: 0")
        # Set the difficulty again to restart the game
        self.set_difficulty()


    # function to update snake score in the json file
    def update_snake_score(self):

        users = self.user_data.get("users", [])

        for user in users:
            if user["username"] == self.username["username"]:
                if user["snake_score"] < self.score:
                    # This doesn't update the api, make sure to access the information from user or username, not user_data
                    # self.user_data["snake_score"] = self.score
                    user["snake_score"] = self.score
                    break

        # Update the data dictionary
        self.user_data["users"] = users

        # Save the updated data to the file
        with open("user_data.json", "w") as file:
            json.dump(self.user_data, file, indent=4)

        return

# snake_game = Snake()
# snake_game.run()
