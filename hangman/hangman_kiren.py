"""
Author: Kiren Chaudry
Date Authored: Oct. 17, 2023
Last Updated: Nov. 18, 2023
Class: CSCI 6651-01
Goal: This is a program to run a simple game of hangman
"""

import random
import tkinter as tk

class Hangman:

    def __init__(self, main_tkinter):
        global canvas, attempts_label, letters_guessed_label, letter_label, letter_entry, guess_button, word_label
        global word_display, message_label, restart_button, exit_button
        self.window = main_tkinter

        # Initialize variables
        self.word_to_guess = self.choose_random_word()
        self.guessed_letters = []
        self.attempts = 6
        self.current_attempt = 0

        # Create a canvas to draw the hangman figure
        canvas = tk.Canvas(self.window, width=200, height=200)

        canvas.create_line(10, 180, 90, 180)
        canvas.create_line(50, 180, 50, 10)
        canvas.create_line(50, 10, 100, 10)
        canvas.create_line(100, 10, 100, 30)

        # Create and pack the widgets
        attempts_label = tk.Label(self.window, text=f"Attempts left: {self.attempts - self.current_attempt}")

        letters_guessed_label = tk.Label(self.window, text="Letters Guessed: ")

        letter_label = tk.Label(self.window, text="Guess a letter:")

        letter_entry = tk.Entry(self.window)

        guess_button = tk.Button(self.window, text="Guess", command=self.guess_letter)

        word_display = tk.StringVar()
        word_display.set(" ".join(["_" for _ in self.word_to_guess]))
        word_label = tk.Label(self.window, textvariable=word_display)

        message_label = tk.Label(self.window, text="")

        restart_button = tk.Button(self.window, text="Restart", command=self.play_again)

        exit_button = tk.Button(self.window, text="Exit", command=self.exit_game)

        # Start the game
        self.update_hangman()

    # Function to get a random word from wordlist
    def choose_random_word(self):
        with open('wordlist.txt', 'r') as file:
            words = file.read().splitlines()
        return random.choice(words)

    # Function to update the hangman figure
    def update_hangman(self):
        if self.current_attempt == 1:    #head
            canvas.create_oval(85, 30, 115, 60)
        elif self.current_attempt == 2:  #body
            canvas.create_line(100, 60, 100, 120)
        elif self.current_attempt == 3:  # left arm
            canvas.create_line(100, 80, 80, 60)
        elif self.current_attempt == 4:  # right arm
            canvas.create_line(100, 80, 120, 60)
        elif self.current_attempt == 5:  # left leg
            canvas.create_line(100, 120, 80, 140)
        elif self.current_attempt == 6:  # right leg
            canvas.create_line(100, 120, 120, 140)
            # X's inside the circle for dead eyes
            canvas.create_text(95, 40, text="x")
            canvas.create_text(105, 40, text="x")

    # Function to check if the game is won
    def is_game_won(self):
        return all(letter in self.guessed_letters for letter in self.word_to_guess)

    # Function to handle letter guesses
    def guess_letter(self):
        letter = letter_entry.get().lower()
        self.guessed_letters.append(letter)
        letter_entry.delete(0, tk.END)

        if letter not in self.word_to_guess:
            self.current_attempt += 1
            self.update_hangman()

        word_display.set(" ".join([char if char in self.guessed_letters else "_" for char in self.word_to_guess]))

        # Update attempts label
        attempts_left = self.attempts - self.current_attempt
        attempts_label.config(text=f"Attempts left: {attempts_left}")

        # Update letters guessed label
        letters_guessed_label.config(text=f"Letters Guessed: {' '.join(self.guessed_letters)}")

        if self.is_game_won():
            message_label.config(text="Congratulations! You've won!")
        elif self.current_attempt == self.attempts:
            message_label.config(text=f"Game over! The word was '{self.word_to_guess}'")

    # Function to play again
    def play_again(self):
        self.reset_game()
        unpack_hangman_elements()
        hangman_game = Hangman(self.window)
        pack_hangman_elements()

    # Function to exit the game
    def exit_game(self):
        self.window.destroy()

    # Function to reset the game state
    def reset_game(self):
        self.word_to_guess = self.choose_random_word()
        self.guessed_letters = []
        self.attempts = 6
        self.current_attempt = 0
        self.update_hangman()
        word_display.set(" ".join(["_" for _ in self.word_to_guess]))
        attempts_label.config(text=f"Attempts left: {self.attempts}")
        letters_guessed_label.config(text="Letters Guessed: ")
        message_label.config(text="")

    # Run the main loop
    def run(self):
        self.window.mainloop()

# Call the Hangman class to start the game
#hangman_game = Hangman()
#hangman_game.run()

def pack_hangman_elements():
    canvas.pack()
    attempts_label.pack()
    letters_guessed_label.pack()
    letter_label.pack()
    letter_entry.pack()
    guess_button.pack()
    word_label.pack()
    message_label.pack()
    restart_button.place(relx=0.48, rely=0.56, anchor=tk.CENTER)
    exit_button.place(relx=0.52, rely=0.56, anchor=tk.CENTER)

def unpack_hangman_elements():
    canvas.pack_forget()
    attempts_label.pack_forget()
    letters_guessed_label.pack_forget()
    letter_label.pack_forget()
    letter_entry.pack_forget()
    guess_button.pack_forget()
    word_label.pack_forget()
    message_label.pack_forget()
    restart_button.place_forget()
    exit_button.place_forget()


