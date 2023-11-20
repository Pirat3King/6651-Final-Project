"""
File: snake.py
Authors: Trevor Ralston
Brief: Implementation of snake using tkinter GUI
Date: 2023/11/7
OpenAI's ChatGPT was utilized to assist in the creation of this program
"""

import tkinter as tk
import random
import json

# Constants
CANVAS_SIZE = 400
GRID_SIZE = 20
GRID_WIDTH = CANVAS_SIZE // GRID_SIZE
GRID_HEIGHT = CANVAS_SIZE // GRID_SIZE
SNAKE_SPEED = 500  # 150  # Delay in milliseconds


class Snake:

    # main_tkinter is the tkinter window (root) passed in from main
    # the_canvas_window is a canvas widget created in main spefically for the snake game
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

        # Create the canvas
        self.canvas = the_canvas_window

        # Create the score label
        self.score_label = tk.Label(self.canvas, text="Score: 0", fg="white", bg="black")
        self.score_label.place(x=200, y=2)

        # Create the restart button
        # This is in main, but it may be more efficient to implement in this file, commented out for now
        # self.restart_button = tk.Button(main_tkinter, text="Restart", command=self.restart_game)
        # self.restart_button.pack()

        # Bind arrow key events, these are bound to the main tkinter window (root)
        main_tkinter.bind("<Up>", self.on_key_press)
        main_tkinter.bind("<Down>", self.on_key_press)
        main_tkinter.bind("<Left>", self.on_key_press)
        main_tkinter.bind("<Right>", self.on_key_press)

        self.user_data = user_data
        self.username = username

        # Start the game
        self.move_snake()

    def restart_game(self):
        self.snake = [(4, 5), (4, 4), (4, 3)]
        self.direction = (0, 1)
        self.generate_food()
        self.score = 0
        self.game_over = False
        self.score_label.config(text="Score: 0")
        self.move_snake()

    def generate_food(self):
        while self.food in self.snake:
            self.food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def move_snake(self):
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
            else:
                self.snake.insert(0, new_head)

                # Check if the snake eats the food
                if self.snake[0] == self.food:
                    self.score += 1
                    self.generate_food()
                else:
                    self.snake.pop()

            self.canvas.delete("all")
            self.draw_snake()
            self.draw_food()

            # Update the score label
            self.score_label.config(text=f"Score: {self.score}")

            # Schedule the next move
            self.canvas.after(SNAKE_SPEED, self.move_snake)

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
        if event.keysym == "Up" and self.direction != (0, 1):
            self.direction = (0, -1)
        elif event.keysym == "Down" and self.direction != (0, -1):
            self.direction = (0, 1)
        elif event.keysym == "Left" and self.direction != (1, 0):
            self.direction = (-1, 0)
        elif event.keysym == "Right" and self.direction != (-1, 0):
            self.direction = (1, 0)

    def restart_game(self):
        self.update_snake_score()
        self.snake = [(4, 5), (4, 4), (4, 3)]
        self.direction = (0, 1)
        self.generate_food()
        self.score = 0
        self.game_over = False
        self.score_label.config(text="Score: 0")
        self.move_snake()

    def run(self):
        self.move_snake()

    #function to update snake score in the json file
    def update_snake_score(self):
        # if self.user_data["snake_score"]:
        #     self.user_data["snake_score"] = self.score
        #     with open("user_data.json", "w") as file:
        #         json.dump({"users": [self.user_data]}, file, indent=4)

        users = self.user_data.get("users", [])

        for user in users:
            if user["username"] == self.username:
                if user["snake_score"] < self.score:
                    self.user_data["snake_score"] = self.score
                    break

        # Update the data dictionary
        self.user_data["users"] = users

        # Save the updated data to the file
        with open("user_data.json", "w") as file: 
            json.dump(self.user_data, file, indent=4)

        return


# snake_game = Snake()
# snake_game.run()
