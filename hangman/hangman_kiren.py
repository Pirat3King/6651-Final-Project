"""
Author: Kiren Chaudry
Date Authored: Oct. 17, 2023
Last Updated: Nov. 18, 2023
Class: CSCI 6651-01
Goal: This is a program to run a simple game of hangman
"""

import random
import tkinter as tk

# Set up the main window
window = tk.Tk()
window.title("Hangman Game")


# Function to get a random word from wordlist
def choose_random_word():
    with open('wordlist.txt', 'r') as file:
        words = file.read().splitlines()
    return random.choice(words)


# Initialize variables
word_to_guess = choose_random_word()
guessed_letters = []  # List to store guessed letters
attempts = 6  # Number of attempts allowed
current_attempt = 0  # Current attempt

# Create a canvas to draw the hangman figure
canvas = tk.Canvas(window, width=200, height=200)
canvas.pack()

canvas.create_line(10, 180, 90, 180)
canvas.create_line(50, 180, 50, 10)
canvas.create_line(50, 10, 100, 10)
canvas.create_line(100, 10, 100, 30)


# Function to update the hangman figure
def update_hangman():
    global current_attempt
    if current_attempt == 1:    #head
        canvas.create_oval(85, 30, 115, 60)
    elif current_attempt == 2:  #body
        canvas.create_line(100, 60, 100, 120)
    elif current_attempt == 3:  # left arm
        canvas.create_line(100, 80, 80, 60)
    elif current_attempt == 4:  # right arm
        canvas.create_line(100, 80, 120, 60)
    elif current_attempt == 5:  # left leg
        canvas.create_line(100, 120, 80, 140)
    elif current_attempt == 6:  # right leg
        canvas.create_line(100, 120, 120, 140)
        # X's inside the circle for dead eyes
        canvas.create_text(95, 40, text="x")
        canvas.create_text(105, 40, text="x")


# Function to check if the game is won
def is_game_won():
    return all(letter in guessed_letters for letter in word_to_guess)


# Function to handle letter guesses
def guess_letter():
    global current_attempt
    letter = letter_entry.get()
    guessed_letters.append(letter)
    letter_entry.delete(0, tk.END)

    if letter not in word_to_guess:
        current_attempt += 1
        update_hangman()

    word_display.set(" ".join([letter if letter in guessed_letters else "_" for letter in word_to_guess]))

    # Update attempts label
    attempts_left = attempts - current_attempt
    attempts_label.config(text=f"Attempts left: {attempts_left}")

    # Update letters guessed label
    letters_guessed_label.config(text=f"Letters Guessed: {' '.join(guessed_letters)}")

    if is_game_won():
        message_label.config(text="Congratulations! You've won!")
    elif current_attempt == attempts:
        message_label.config(text=f"Game over! The word was '{word_to_guess}'")


# Create and pack the widgets
attempts_label = tk.Label(window, text=f"Attempts left: {attempts - current_attempt}")
attempts_label.pack()

letters_guessed_label = tk.Label(window, text="Letters Guessed: ")
letters_guessed_label.pack()

letter_label = tk.Label(window, text="Guess a letter:")
letter_label.pack()

letter_entry = tk.Entry(window)
letter_entry.pack()

guess_button = tk.Button(window, text="Guess", command=guess_letter)
guess_button.pack()

word_display = tk.StringVar()
word_display.set(" ".join(["_" for _ in word_to_guess]))
word_label = tk.Label(window, textvariable=word_display)
word_label.pack()

message_label = tk.Label(window, text="")
message_label.pack()

# Start the game
update_hangman()

# Run the main loop
window.mainloop()